import os
import sys
import re
import json
import urllib.request
import datetime

from badges import safe_name, write_repo_badges

def get_repos_info():
    urls = [
        "https://api.github.com/users/LeanBitLab/repos?per_page=100",
        "https://api.github.com/orgs/leanbitlab-org/repos?per_page=100"
    ]
    token = os.getenv("GITHUB_TOKEN")
    repos = []
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            if token:
                req.add_header("Authorization", f"token {token}")
            with urllib.request.urlopen(req) as response:
                items = json.loads(response.read().decode())
                if isinstance(items, list):
                    for repo in items:
                        if not repo.get("fork", False):
                            repos.append({
                                "name": repo["name"],
                                "full_name": repo["full_name"],
                                "owner": repo["owner"]["login"],
                                "stars": repo.get("stargazers_count", 0)
                            })
        except Exception as e:
            print(f"Error fetching repos from {url}: {e}")
            
    return repos

def get_repo_downloads(full_name):
    total = 0
    token = os.getenv("GITHUB_TOKEN")
    page = 1
    while True:
        try:
            url = f"https://api.github.com/repos/{full_name}/releases?per_page=100&page={page}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            if token:
                req.add_header("Authorization", f"token {token}")
            with urllib.request.urlopen(req) as response:
                releases = json.loads(response.read().decode())
                if not releases:
                    break
                for r in releases:
                    for asset in r.get("assets", []):
                        total += asset.get("download_count", 0)
                if len(releases) < 100:
                    break
                page += 1
        except Exception as e:
            print(f"Error fetching downloads for {full_name} (page {page}): {e}")
            break
    return total

def get_repo_commits(full_name):
    token = os.getenv("GITHUB_TOKEN")
    try:
        url = f"https://api.github.com/repos/{full_name}/commits?per_page=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        if token:
            req.add_header("Authorization", f"token {token}")
        with urllib.request.urlopen(req) as response:
            link = response.headers.get("Link", "")
            if link:
                m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
                if m:
                    return int(m.group(1))
            content = json.loads(response.read().decode())
            if isinstance(content, list) and len(content) > 0:
                return 1
            return 0
    except Exception as e:
        print(f"Error fetching commits for {full_name}: {e}")
        return 0

def get_repo_latest_release(full_name):
    token = os.getenv("GITHUB_TOKEN")
    try:
        url = f"https://api.github.com/repos/{full_name}/releases/latest"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        if token:
            req.add_header("Authorization", f"token {token}")
        with urllib.request.urlopen(req) as response:
            rel = json.loads(response.read().decode())
            return rel.get("tag_name"), rel.get("html_url")
    except Exception as e:
        return None, None

def format_number(num):
    if num >= 1000:
        return f"{num / 1000:.1f}k"
    return str(num)

STATS_PALETTE = {
    "light": {"bg": "#ffffff", "border": "#d0d7de", "title": "#1f2328", "muted": "#6e7781", "value": "#1f2328"},
    "dark": {"bg": "#0d1117", "border": "#30363d", "title": "#f0f6fc", "muted": "#8b949e", "value": "#f0f6fc"},
}


def generate_stats_card(total_stars, total_downloads, repo_count, total_commits, output_path="stats.svg"):
    """Writes stats-light.svg and stats-dark.svg next to output_path (GitHub picks one per viewer theme)."""
    stars_fmt = format_number(total_stars)
    downloads_fmt = format_number(total_downloads)
    commits_fmt = f"{format_number(total_commits)}+" if total_commits > 0 else "2.2k+"
    base, ext = os.path.splitext(output_path)

    for theme, c in STATS_PALETTE.items():
        style = f"""<style>
    .bg {{ fill: {c['bg']}; stroke: {c['border']}; stroke-width: 1px; }}
    .title {{ font: 600 14px 'Segoe UI', Ubuntu, Roboto, sans-serif; fill: {c['title']}; }}
    .sub {{ font: 400 12px 'Segoe UI', Ubuntu, Roboto, sans-serif; fill: {c['muted']}; }}
    .value {{ font: 700 28px 'Segoe UI', Ubuntu, Roboto, sans-serif; fill: {c['value']}; }}
    .label {{ font: 400 12px 'Segoe UI', Ubuntu, Roboto, sans-serif; fill: {c['muted']}; }}
    .rule {{ stroke: {c['border']}; stroke-width: 1px; }}
    .accent {{ fill: {c['title']}; }}
  </style>"""
        svg = f'''<svg width="495" height="160" viewBox="0 0 495 160" fill="none" xmlns="http://www.w3.org/2000/svg">
{style}

  <rect class="bg" width="494" height="159" x="0.5" y="0.5" rx="14"/>

  <!-- Header -->
  <g transform="translate(28, 24)">
    <path class="accent" d="M8 0C3.58 0 0 3.58 0 8C0 11.54 2.29 14.53 5.47 15.59C5.87 15.66 6.02 15.42 6.02 15.21C6.02 15.02 6.01 14.39 6.01 13.72C4 14.09 3.48 13.23 3.32 12.78C3.23 12.55 2.84 11.84 2.5 11.65C2.22 11.5 1.82 11.13 2.49 11.12C3.12 11.11 3.57 11.7 3.72 11.94C4.44 13.15 5.59 12.81 6.05 12.6C6.12 12.08 6.33 11.73 6.56 11.53C4.78 11.33 2.92 10.64 2.92 7.58C2.92 6.71 3.23 5.99 3.74 5.43C3.66 5.23 3.38 4.41 3.82 3.31C3.82 3.31 4.49 3.1 6.02 4.13C6.66 3.95 7.34 3.86 8.02 3.86C8.7 3.86 9.38 3.95 10.02 4.13C11.55 3.09 12.22 3.31 12.22 3.31C12.66 4.41 12.38 5.23 12.3 5.43C12.81 5.99 13.12 6.7 13.12 7.58C13.12 10.65 11.25 11.33 9.47 11.53C9.76 11.78 10.01 12.26 10.01 13.01C10.01 14.08 10 14.94 10 15.21C10 15.42 10.15 15.67 10.55 15.59C13.71 14.53 16 11.53 16 8C16 3.58 12.42 0 8 0Z"/>
    <text x="24" y="13" class="title">LeanBitLab</text>
    <text x="112" y="13" class="sub">GitHub stats across all repos</text>
  </g>
  <line class="rule" x1="28" y1="58" x2="466" y2="58"/>

  <!-- Stats row -->
  <g transform="translate(28, 100)">
    <text x="0" y="0" class="value">{stars_fmt}</text>
    <text x="0" y="24" class="label">Total Stars</text>
  </g>
  <g transform="translate(145, 100)">
    <text x="0" y="0" class="value">{downloads_fmt}</text>
    <text x="0" y="24" class="label">Total Downloads</text>
  </g>
  <g transform="translate(278, 100)">
    <text x="0" y="0" class="value">{repo_count}</text>
    <text x="0" y="24" class="label">Public Repos</text>
  </g>
  <g transform="translate(378, 100)">
    <text x="0" y="0" class="value">{commits_fmt}</text>
    <text x="0" y="24" class="label">Total Commits</text>
  </g>
</svg>'''
        with open(f"{base}-{theme}{ext}", "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"Generated {base}-light{ext} and {base}-dark{ext} successfully!")


def mask_private_name(name: str) -> str:
    """Masks private sponsor name showing first and last letter (e.g. a****c)."""
    if not name:
        return "a****c"
    clean = name.strip().replace("*", "")
    if not clean:
        return "a****c"
    if len(clean) == 1:
        return f"{clean}****"
    return f"{clean[0]}****{clean[-1]}"


# Lowest dollar amount of each sub-tier (fallback total for sponsors missing from the private ledger).
TIER_FLOOR = {
    "Diamond": 250, "Gold II": 100, "Gold I": 50, "Silver II": 25, "Silver I": 10,
    "Bronze": 5, "Supporter II": 2, "Supporter I": 1,
}
LEDGER_PATH = os.getenv("SPONSOR_LEDGER_PATH", "sponsor-ledger/ledger.json")


def round_amount(amount: float) -> int:
    """Coarse rounding so the public bubble size does not reveal exact dollars (step grows with the amount)."""
    step = 2 if amount < 10 else 5 if amount < 50 else 25 if amount < 250 else 50
    return max(step, int(round(amount / step)) * step)


def public_ratio(amount: float, divisor: float) -> float:
    """Public bubble size share from a coarsely rounded amount (exact amounts stay in the private ledger)."""
    return round(round_amount(amount) / divisor, 4)


def load_ledger(path: str):
    """Private running totals {key: {"total": dollars, "counted": "YYYY-MM"}}, or None when unavailable."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except Exception as e:
        print(f"Notice: Could not read sponsor ledger: {e}")
        return None


def get_tier_info(amount: float) -> dict:
    """Computes tier and subTier based on dollar amount."""
    if amount >= 250:
        return {"tier": "diamond", "subTier": "Diamond"}
    if amount >= 100:
        return {"tier": "gold", "subTier": "Gold II"}
    if amount >= 50:
        return {"tier": "gold", "subTier": "Gold I"}
    if amount >= 25:
        return {"tier": "silver", "subTier": "Silver II"}
    if amount >= 10:
        return {"tier": "silver", "subTier": "Silver I"}
    if amount >= 5:
        return {"tier": "bronze", "subTier": "Bronze"}
    if amount >= 2:
        return {"tier": "supporter", "subTier": "Supporter II"}
    return {"tier": "supporter", "subTier": "Supporter I"}


OC_SLUG = "leanbitlab-org"
OC_JSON_PATH = "opencollective-data.json"


def get_opencollective_backers(slug: str):
    """Fetches public Open Collective backers; returns (all_time, this_month) lists, or None on failure.

    Only name, tier, ratio and an optional public profile URL are kept (the API also lists emails).
    The members API repeats a backer once per tier, so records are deduplicated by profile URL.
    """
    try:
        req = urllib.request.Request(
            f"https://opencollective.com/{slug}/members/all.json",
            headers={"User-Agent": "leanbitlab-site-stats"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            members = json.load(resp)
    except Exception as e:
        print(f"Notice: Could not fetch Open Collective members: {e}")
        return None
    if not isinstance(members, list):
        return None

    now = datetime.datetime.now(datetime.timezone.utc)
    by_profile = {}
    for m in members:
        if m.get("role") != "BACKER" or m.get("type") != "USER":
            continue
        total = m.get("totalAmountDonated") or 0
        profile = m.get("profile") or ""
        if total <= 0 or not profile:
            continue
        prev = by_profile.get(profile)
        if prev is None or (m.get("lastTransactionAt") or "") > (prev.get("lastTransactionAt") or ""):
            by_profile[profile] = {**m, "totalAmountDonated": max(total, (prev or {}).get("totalAmountDonated") or 0)}

    all_time, this_month = [], []
    for profile, m in by_profile.items():
        is_guest = "/guest-" in profile
        name = (m.get("name") or "").strip() or "Guest"
        url = None if is_guest or not profile.startswith("https://opencollective.com/") else profile

        total = m["totalAmountDonated"]
        info = get_tier_info(total)
        all_time.append({"name": name, "url": url, **info, "ratio": public_ratio(total, 1000.0)})

        last = m.get("lastTransactionAmount") or 0
        try:
            last_at = datetime.datetime.fromisoformat(m["lastTransactionAt"].replace("Z", "+00:00"))
            if last_at.tzinfo is None:
                last_at = last_at.replace(tzinfo=datetime.timezone.utc)
        except Exception:
            continue
        if last > 0 and (now - last_at).days < 30:
            info = get_tier_info(last)
            this_month.append({"name": name, "url": url, **info, "ratio": public_ratio(last, 700.0)})

    for lst in (all_time, this_month):
        lst.sort(key=lambda s: (-s["ratio"], s["name"].lower()))
    return all_time, this_month


def update_opencollective_json(path: str) -> bool:
    """Writes opencollective-data.json only when its content changed (no timestamp, so no daily noise)."""
    result = get_opencollective_backers(OC_SLUG)
    if result is None:
        return False
    text = json.dumps({"allTime": result[0], "thisMonth": result[1]}, indent=2, ensure_ascii=False) + "\n"
    if os.path.exists(path) and open(path, encoding="utf-8").read() == text:
        print("Open Collective data is already up to date.")
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Open Collective data updated: {len(result[0])} all time, {len(result[1])} this month.")
    return True


def get_github_sponsors(token: str):
    """Fetches public and private sponsors for LeanBitLab via GitHub GraphQL API."""
    if not token:
        print("Notice: No SPONSORS_TOKEN or GITHUB_TOKEN provided for sponsors sync.")
        return None

    query = """
    query {
      user(login: "LeanBitLab") {
        publicSponsors: sponsorshipsAsMaintainer(first: 100, activeOnly: false, includePrivate: false) {
          nodes {
            sponsorEntity {
              ... on User { login name }
              ... on Organization { login name }
            }
          }
        }
        allSponsors: sponsorshipsAsMaintainer(first: 100, activeOnly: false, includePrivate: true) {
          nodes {
            sponsorEntity {
              ... on User { login name }
              ... on Organization { login name }
            }
            tier {
              monthlyPriceInDollars
              isOneTime
            }
          }
        }
        activeSponsors: sponsorshipsAsMaintainer(first: 100, activeOnly: true, includePrivate: true) {
          nodes {
            sponsorEntity {
              ... on User { login name }
              ... on Organization { login name }
            }
            tier {
              monthlyPriceInDollars
              isOneTime
            }
          }
        }
      }
    }
    """
    try:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query}).encode("utf-8"),
            headers={
                "Authorization": f"bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "LeanBitLab-Sync"
            }
        )
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            if "errors" in res:
                print(f"Notice: GraphQL errors while fetching sponsors: {res['errors']}")
                return None
            user_data = res.get("data", {}).get("user")
            return user_data
    except Exception as e:
        print(f"Notice: Could not fetch sponsors from GitHub GraphQL API: {e}")
        return None


def update_sponsors_section(content: str, user_data: dict) -> tuple[str, bool]:
    """Updates the GitHub Sponsors section in README while preserving order and privacy."""
    if not user_data:
        return content, False

    pub_nodes = user_data.get("publicSponsors", {}).get("nodes", [])
    all_nodes = user_data.get("allSponsors", {}).get("nodes", [])

    pub_logins = {
        n["sponsorEntity"]["login"].lower()
        for n in pub_nodes
        if n.get("sponsorEntity") and n["sponsorEntity"].get("login")
    }

    # Locate existing sponsors block
    match = re.search(r'<!-- SPONSORS_LIST:START -->(.*?)<!-- SPONSORS_LIST:END -->', content, re.DOTALL)
    existing_html = ""
    has_markers = False
    if match:
        has_markers = True
        existing_html = match.group(1)
    else:
        # Fallback: look for <p align="center"> under ### 💖 GitHub Sponsors
        p_match = re.search(
            r'### 💖 GitHub Sponsors\s*\n\s*Thank you to our amazing sponsors!\s*\n\s*(<p align="center">.*?</p>)',
            content,
            re.DOTALL
        )
        if p_match:
            existing_html = p_match.group(1)

    seen = set()
    formatted_items = []

    # Parse existing items to preserve their exact order and any manual entries
    if existing_html:
        item_pattern = re.compile(
            r'<strong>(?:<a href="https://github\.com/([^"/]+)">([^<]+)</a>|([^<]+))</strong>'
        )
        for m in item_pattern.finditer(existing_html):
            gh_user = m.group(1)
            plain_text = m.group(3)

            if gh_user:
                seen.add(gh_user.lower())
                formatted_items.append(f'<strong><a href="https://github.com/{gh_user}">{gh_user}</a></strong>')
            elif plain_text:
                pt = plain_text.strip()
                if '*' in pt or pt.lower().startswith('qu'):
                    seen.add('quiet-tangent')
                    formatted_items.append(f'<strong>{mask_private_name(pt)}</strong>')
                else:
                    seen.add(pt.lower())
                    formatted_items.append(f'<strong>{pt}</strong>')

    # Append any new sponsors from GitHub API
    new_sponsors_added = 0
    for n in all_nodes:
        entity = n.get("sponsorEntity") or {}
        login = entity.get("login")
        if not login:
            continue
        login_lower = login.lower()
        if login_lower in seen:
            continue
        seen.add(login_lower)
        new_sponsors_added += 1
        if login_lower in pub_logins:
            formatted_items.append(f'<strong><a href="https://github.com/{login}">{login}</a></strong>')
        else:
            formatted_items.append(f'<strong>{mask_private_name(login)}</strong>')

    if not formatted_items:
        return content, False

    lines = []
    for i, item in enumerate(formatted_items):
        if i < len(formatted_items) - 1:
            lines.append(f"  {item} &nbsp;&bull;&nbsp;")
        else:
            lines.append(f"  {item}")

    sponsors_block = '<p align="center">\n' + "\n".join(lines) + "\n</p>"

    if has_markers:
        new_content = re.sub(
            r'(<!-- SPONSORS_LIST:START -->)(.*?)(<!-- SPONSORS_LIST:END -->)',
            f'\\1\n{sponsors_block}\n\\3',
            content,
            flags=re.DOTALL
        )
    else:
        pattern = r'(### 💖 GitHub Sponsors\s*\n\s*Thank you to our amazing sponsors!\s*\n\s*)<p align="center">.*?</p>'
        new_content = re.sub(
            pattern,
            f'\\1<!-- SPONSORS_LIST:START -->\n{sponsors_block}\n<!-- SPONSORS_LIST:END -->',
            content,
            flags=re.DOTALL
        )

    updated = (new_content != content)
    if new_sponsors_added > 0:
        print(f"Added {new_sponsors_added} new sponsor(s) to README!")
    elif updated:
        print("Sponsors list in README updated successfully!")
    else:
        print("Sponsors list in README is already up to date.")
    return new_content, updated


def current_month() -> str:
    """Calendar month as YYYY-MM (a function so tests can patch it)."""
    return datetime.date.today().strftime("%Y-%m")


def months_between(earlier: str, later: str) -> int:
    """Whole months from 'YYYY-MM' earlier to later (0 when equal)."""
    ey, em = map(int, earlier.split("-"))
    ly, lm = map(int, later.split("-"))
    return (ly - ey) * 12 + (lm - em)


def update_sponsor_data_js(sponsor_data_path: str, user_data: dict, ledger_path: str = LEDGER_PATH) -> bool:
    """Directly updates sponsor-data.js: keeps historical in allTime and actively prunes cancelled from thisMonth."""
    if not user_data or not os.path.exists(sponsor_data_path):
        return False

    pub_nodes = user_data.get("publicSponsors", {}).get("nodes", [])
    all_nodes = user_data.get("allSponsors", {}).get("nodes", [])
    active_nodes = user_data.get("activeSponsors", {}).get("nodes", [])

    pub_logins = {
        n["sponsorEntity"]["login"].lower()
        for n in pub_nodes
        if n.get("sponsorEntity") and n["sponsorEntity"].get("login")
    }

    try:
        with open(sponsor_data_path, "r", encoding="utf-8") as f:
            text = f.read()

        m = re.search(r'const\s+sponsorData\s*=\s*(\{.*?\});?\s*$', text, re.DOTALL)
        if not m:
            print("Notice: Could not parse sponsorData object in sponsor-data.js")
            return False

        json_str = re.sub(r'(\ballTime|\bthisMonth)\s*:', r'"\1":', m.group(1))
        data = json.loads(json_str)

        all_time = data.get("allTime", [])
        original_this_month = data.get("thisMonth", [])
        changed = False

        # 1. Normalize existing private masks (e.g. qu***t*** -> q****t) in all_time
        for s in all_time:
            name = s.get("name", "")
            if "*" in name or name.startswith("qu"):
                masked = mask_private_name(name)
                if s.get("name") != masked or s.get("github") is not None:
                    s["name"] = masked
                    s["github"] = None
                    changed = True

        # 1b. Real dollar amounts never go into the public file. All Time keeps a running total per sponsor
        # (`total`) and the last month counted (`counted`) in a private ledger; the public file only gets
        # name, tier and a coarsely rounded bubble size. Without a ledger, All Time is left as it is.
        month_now = current_month()
        ledger = load_ledger(ledger_path)
        if ledger is None:
            print("Notice: sponsor ledger not found; All Time totals are not updated.")
        ledger_before = json.dumps(ledger, sort_keys=True)
        before_all_time = json.dumps(all_time, sort_keys=True)

        def ledger_key(entry):
            return (entry.get("github") or entry.get("name") or "").lower()

        if ledger is not None:
            for s in all_time:
                known = ledger.get(ledger_key(s))
                if known:
                    s["total"], s["counted"] = known["total"], known["counted"]
                else:
                    s["total"], s["counted"] = TIER_FLOOR.get(s.get("subTier"), 1), month_now

        # 2. Existing sponsor keys in all_time
        existing_keys = set()
        for s in all_time:
            if s.get("github"):
                existing_keys.add(s["github"].lower())
            if s.get("name"):
                existing_keys.add(s["name"].lower())

        # 3. Add new historical sponsors to all_time (past sponsors are never removed)
        new_added = 0
        for n in all_nodes:
            entity = n.get("sponsorEntity") or {}
            login = entity.get("login")
            if not login:
                continue

            login_lower = login.lower()
            is_pub = login_lower in pub_logins
            masked = mask_private_name(login)

            if login_lower in existing_keys or masked.lower() in existing_keys:
                continue

            existing_keys.add(login_lower)
            if not is_pub:
                existing_keys.add(masked.lower())

            tier_obj = n.get("tier") or {}
            amount = tier_obj.get("monthlyPriceInDollars") or 5
            tier_info = get_tier_info(amount)
            all_time_ratio = public_ratio(amount, 1000.0)

            display_name = login if is_pub else masked
            github_handle = login if is_pub else None

            all_time.append({
                "name": display_name,
                "github": github_handle,
                "tier": tier_info["tier"],
                "subTier": tier_info["subTier"],
                "ratio": all_time_ratio,
                "total": amount,
                "counted": month_now
            })
            new_added += 1
            changed = True

        # 3b. Recurring sponsors add their current monthly price once per calendar month (a downgrade only
        # affects later months; cancelled sponsors simply stop growing). One-time sponsors never repeat.
        by_key = {}
        for s in (all_time if ledger is not None else []):
            if s.get("github"):
                by_key[s["github"].lower()] = s
            if s.get("name"):
                by_key.setdefault(s["name"].lower(), s)
        for n in active_nodes:
            login = (n.get("sponsorEntity") or {}).get("login")
            tier_obj = n.get("tier") or {}
            if not login or tier_obj.get("isOneTime"):
                continue
            entry = by_key.get(login.lower()) or by_key.get(mask_private_name(login).lower())
            if entry is None:
                continue
            owed = months_between(entry.get("counted") or month_now, month_now)
            if owed > 0:
                entry["total"] += (tier_obj.get("monthlyPriceInDollars") or 5) * owed
                entry["counted"] = month_now

        # Tier and bubble size follow the running total (size uses the coarsely rounded total)
        if ledger is not None:
            for s in all_time:
                info = get_tier_info(s["total"])
                s["tier"], s["subTier"] = info["tier"], info["subTier"]
                s["ratio"] = public_ratio(s["total"], 1000.0)
        public_all_time = [
            {k: v for k, v in s.items() if k not in ("total", "counted")} for s in all_time
        ]
        if json.dumps(public_all_time, sort_keys=True) != before_all_time:
            changed = True
        if ledger is not None:
            new_ledger = {ledger_key(s): {"total": s["total"], "counted": s["counted"]} for s in all_time}
            if json.dumps(new_ledger, sort_keys=True) != ledger_before:
                os.makedirs(os.path.dirname(ledger_path) or ".", exist_ok=True)
                with open(ledger_path, "w", encoding="utf-8") as f:
                    json.dump(new_ledger, f, indent=2, sort_keys=True)
                    f.write("\n")
                print("Sponsor ledger updated.")

        # 4. Dynamically rebuild thisMonth strictly from activeSponsors (pruning cancelled sponsors)
        new_this_month = []
        active_seen = set()
        for n in active_nodes:
            entity = n.get("sponsorEntity") or {}
            login = entity.get("login")
            if not login:
                continue

            login_lower = login.lower()
            if login_lower in active_seen:
                continue
            active_seen.add(login_lower)

            is_pub = login_lower in pub_logins
            masked = mask_private_name(login)

            tier_obj = n.get("tier") or {}
            amount = tier_obj.get("monthlyPriceInDollars") or 5
            tier_info = get_tier_info(amount)
            month_ratio = public_ratio(amount, 700.0)

            display_name = login if is_pub else masked
            github_handle = login if is_pub else None

            new_this_month.append({
                "name": display_name,
                "github": github_handle,
                "tier": tier_info["tier"],
                "subTier": tier_info["subTier"],
                "ratio": month_ratio
            })

        # Preserve any manual non-GitHub sponsors in thisMonth if present in original
        for s in original_this_month:
            if s.get("github") is None and not ("*" in s.get("name", "") or s.get("name", "").startswith("qu")):
                if not any(item["name"] == s["name"] for item in new_this_month):
                    new_this_month.append(s)

        # Sort both lists descending by ratio
        public_all_time.sort(key=lambda s: s.get("ratio", 0), reverse=True)
        new_this_month.sort(key=lambda s: s.get("ratio", 0), reverse=True)

        if new_this_month != original_this_month:
            changed = True

        if not changed:
            print("Site sponsor-data.js is already up to date.")
            return False

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        output = f"""// Auto-generated by .github/scripts/update_downloads.py - do not edit manually
// Generated: {now_iso}
const sponsorData = {{
  allTime: {json.dumps(public_all_time, indent=4)},
  thisMonth: {json.dumps(new_this_month, indent=4)}
}};
"""
        with open(sponsor_data_path, "w", encoding="utf-8") as f:
            f.write(output)

        if new_added > 0:
            print(f"Added {new_added} new sponsor(s) to site sponsor-data.js!")
        else:
            print("Site sponsor-data.js updated successfully with active sponsors!")
        return True

    except Exception as e:
        print(f"Notice: Could not update sponsor-data.js: {e}")
        return False


def sync_local_sponsors_json(sponsors_json_path: str, user_data: dict) -> bool:
    """Updates local sponsors.json if it exists (kept strictly gitignored)."""
    if not user_data or not os.path.exists(sponsors_json_path):
        return False

    pub_nodes = user_data.get("publicSponsors", {}).get("nodes", [])
    all_nodes = user_data.get("allSponsors", {}).get("nodes", [])

    pub_logins = {
        n["sponsorEntity"]["login"].lower()
        for n in pub_nodes
        if n.get("sponsorEntity") and n["sponsorEntity"].get("login")
    }

    try:
        with open(sponsors_json_path, "r", encoding="utf-8") as f:
            sponsors = json.load(f)

        changed = False
        existing_keys = set()
        for s in sponsors:
            gh = s.get("github")
            name = s.get("name", "")
            if gh:
                existing_keys.add(gh.lower())
            if name:
                existing_keys.add(name.lower())
                if "*" in name or name.startswith("qu"):
                    masked = mask_private_name(name)
                    if s["name"] != masked:
                        s["name"] = masked
                        s["github"] = None
                        changed = True

        today = datetime.date.today().isoformat()
        for n in all_nodes:
            entity = n.get("sponsorEntity") or {}
            login = entity.get("login")
            if not login:
                continue

            login_lower = login.lower()
            masked = mask_private_name(login)
            is_pub = login_lower in pub_logins

            if login_lower in existing_keys or masked.lower() in existing_keys:
                continue

            existing_keys.add(login_lower)
            tier_obj = n.get("tier") or {}
            amount = tier_obj.get("monthlyPriceInDollars") or 5
            is_one_time = tier_obj.get("isOneTime", False)
            c_type = "one-time" if is_one_time else "monthly"

            sponsors.append({
                "name": login if is_pub else masked,
                "github": login if is_pub else None,
                "contributions": [
                    {"type": c_type, "amount": amount, "date": today}
                ]
            })
            changed = True

        if changed:
            with open(sponsors_json_path, "w", encoding="utf-8") as f:
                json.dump(sponsors, f, indent=2)
            print("Local Pdoc/sponsors/sponsors.json updated.")
            return True
        return False
    except Exception as e:
        print(f"Notice: Could not sync local sponsors.json: {e}")
        return False


def main():
    repos = get_repos_info()
    if not repos:
        print("No repositories found.")
        return

    json_path = "stats.json"
    if not os.path.exists(json_path) and os.path.exists("../../stats.json"):
        json_path = "../../stats.json"

    existing_stats = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                existing_stats = json.load(f)
        except Exception:
            existing_stats = {}

    total_downloads = 0
    total_stars = 0
    total_commits = 0
    repo_data = {}
    
    for r in repos:
        name = r["name"]
        full_name = r["full_name"]
        owner = r["owner"]
        stars = r["stars"]
        downloads = get_repo_downloads(full_name)
        commits = get_repo_commits(full_name)
        version, release_url = get_repo_latest_release(full_name)
        
        existing_repo = existing_stats.get(name.lower(), {})
        if downloads == 0 and existing_repo.get("downloads", 0) > 0:
            downloads = existing_repo["downloads"]
        if not version and existing_repo.get("version"):
            version = existing_repo["version"]
            release_url = existing_repo.get("release_url")
        if commits == 0 and existing_repo.get("commits", 0) > 0:
            commits = existing_repo.get("commits", 0)

        repo_data[name.lower()] = {
            "name": name,
            "owner": owner,
            "stars": stars,
            "downloads": downloads,
            "commits": commits,
            "version": version,
            "release_url": release_url
        }
        total_downloads += downloads
        total_stars += stars
        total_commits += commits
        print(f"Repo {full_name}: {stars} stars, {downloads} downloads, {commits} commits, version {version}")
        
    print(f"Total stars: {total_stars}")
    print(f"Total downloads: {total_downloads}")
    print(f"Total commits: {total_commits}")
    
    active_repos = [r for r in repos if not r["name"].startswith(".")]
    generate_stats_card(total_stars, total_downloads, len(active_repos), total_commits, "stats.svg")
    
    # Export stats.json for website
    json_path = "stats.json"
    if not os.path.exists(json_path) and os.path.exists("../../stats.json"):
        json_path = "../../stats.json"
        
    stats_export = {}
    for repo_key, data in repo_data.items():
        stats_export[repo_key] = {
            "name": data["name"],
            "owner": data["owner"],
            "stars": data["stars"],
            "downloads": data["downloads"],
            "downloads_formatted": format_number(data["downloads"]),
            "version": data["version"],
            "release_url": data["release_url"]
        }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(stats_export, f, indent=2)
    print("Exported stats.json successfully!")
        
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        readme_path = "../../README.md"  # if run from script folder
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Regenerate the local SVG stats badge of every repo the README references (no shields.io)
    badges_dir = os.path.join(os.path.dirname(os.path.abspath(readme_path)), "badges")
    os.makedirs(badges_dir, exist_ok=True)
    badges_count = 0
    for data in repo_data.values():
        fname = safe_name(data["name"])
        if f"./badges/{fname}-light.svg" not in content:
            continue
        write_repo_badges(
            badges_dir, fname,
            data.get("version") or None,
            format_number(data["stars"]),
            format_number(data["downloads"]) if data["downloads"] > 0 else None,
        )
        badges_count += 1
    print(f"Repo badges generated: {badges_count}")

    # Update Sponsors in README & site sponsor-data.js
    sponsors_token = os.getenv("SPONSORS_TOKEN") or os.getenv("GITHUB_TOKEN")
    user_data = get_github_sponsors(sponsors_token)

    readme_sponsors_updated = False
    if user_data:
        content, readme_sponsors_updated = update_sponsors_section(content, user_data)
        
        sponsor_data_path = "sponsor-data.js"
        if not os.path.exists(sponsor_data_path) and os.path.exists("../../sponsor-data.js"):
            sponsor_data_path = "../../sponsor-data.js"
        update_sponsor_data_js(sponsor_data_path, user_data)

        # Local-only ledger sync if Pdoc exists (kept strictly gitignored)
        local_sponsors_json = "Pdoc/sponsors/sponsors.json"
        if not os.path.exists(local_sponsors_json) and os.path.exists("../../Pdoc/sponsors/sponsors.json"):
            local_sponsors_json = "../../Pdoc/sponsors/sponsors.json"
        if os.path.exists(local_sponsors_json):
            sync_local_sponsors_json(local_sponsors_json, user_data)

    oc_path = OC_JSON_PATH
    if not os.path.exists(oc_path) and os.path.exists("../../" + OC_JSON_PATH):
        oc_path = "../../" + OC_JSON_PATH
    update_opencollective_json(oc_path)

    if readme_sponsors_updated:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("README.md updated successfully!")
    else:
        print("No sponsor changes in README.md")

if __name__ == "__main__":
    main()
