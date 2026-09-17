import os
import re
import json
import urllib.request
import datetime

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

def format_number(num):
    if num >= 1000:
        return f"{num / 1000:.1f}k"
    return str(num)

def generate_stats_card(total_stars, total_downloads, repo_count, total_commits, output_path="stats.svg"):
    stars_fmt = format_number(total_stars)
    downloads_fmt = format_number(total_downloads)
    commits_fmt = f"{format_number(total_commits)}+" if total_commits > 0 else "2.2k+"
    
    svg = f'''<svg width="495" height="160" viewBox="0 0 495 160" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg {{ fill: #ffffff; stroke: #e1e4e8; stroke-width: 1px; rx: 10px; }}
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Roboto, sans-serif; fill: #7C4DFF; }}
    .stat-label {{ font: 400 14px 'Segoe UI', Ubuntu, Roboto, sans-serif; fill: #57606a; }}
    .stat-value {{ font: 600 14px 'Segoe UI', Ubuntu, Roboto, sans-serif; fill: #1f2328; }}
    .accent {{ fill: #7C4DFF; }}

    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #0d0f17; stroke: #2a2a3c; }}
      .stat-label {{ fill: #9e9e9e; }}
      .stat-value {{ fill: #ffffff; }}
      .header {{ fill: #7C4DFF; }}
      .accent {{ fill: #7C4DFF; }}
    }}
  </style>

  <rect class="bg" width="494" height="159" x="0.5" y="0.5" rx="10"/>
  
  <!-- Centered Title -->
  <g transform="translate(247.5, 35)">
    <path class="accent" transform="translate(-130, -13)" d="M8 0C3.58 0 0 3.58 0 8C0 11.54 2.29 14.53 5.47 15.59C5.87 15.66 6.02 15.42 6.02 15.21C6.02 15.02 6.01 14.39 6.01 13.72C4 14.09 3.48 13.23 3.32 12.78C3.23 12.55 2.84 11.84 2.5 11.65C2.22 11.5 1.82 11.13 2.49 11.12C3.12 11.11 3.57 11.7 3.72 11.94C4.44 13.15 5.59 12.81 6.05 12.6C6.12 12.08 6.33 11.73 6.56 11.53C4.78 11.33 2.92 10.64 2.92 7.58C2.92 6.71 3.23 5.99 3.74 5.43C3.66 5.23 3.38 4.41 3.82 3.31C3.82 3.31 4.49 3.1 6.02 4.13C6.66 3.95 7.34 3.86 8.02 3.86C8.7 3.86 9.38 3.95 10.02 4.13C11.55 3.09 12.22 3.31 12.22 3.31C12.66 4.41 12.38 5.23 12.3 5.43C12.81 5.99 13.12 6.7 13.12 7.58C13.12 10.65 11.25 11.33 9.47 11.53C9.76 11.78 10.01 12.26 10.01 13.01C10.01 14.08 10 14.94 10 15.21C10 15.42 10.15 15.67 10.55 15.59C13.71 14.53 16 11.53 16 8C16 3.58 12.42 0 8 0Z"/>
    <text x="10" y="0" text-anchor="middle" class="header">LeanBitLab's GitHub Stats</text>
  </g>

  <!-- Stat Items (2-Column Grid) -->
  <!-- Column 1 (Left) -->
  <g transform="translate(35, 75)">
    <!-- Total Stars -->
    <g transform="translate(0, 0)">
      <path class="accent" d="M8 0L10.472 5.008L16 5.816L12 9.712L12.944 15.216L8 12.616L3.056 15.216L4 9.712L0 5.816L5.528 5.008L8 0Z"/>
      <text x="24" y="13" class="stat-label">Total Stars:</text>
      <text x="104" y="13" class="stat-value">{stars_fmt}</text>
    </g>
    
    <!-- Public Repositories -->
    <g transform="translate(0, 36)">
      <path class="accent" d="M4 1.75C4 .783 4.783 0 5.75 0h4.5c.967 0 1.75.783 1.75 1.75v1.5c0 .967-.783 1.75-1.75 1.75h-4.5A1.75 1.75 0 0 1 4 3.25zm1.75-.25a.25.25 0 0 0-.25.25v1.5c0 .138.112.25.25.25h4.5a.25.25 0 0 0 .25-.25v-1.5a.25.25 0 0 0-.25-.25zM1.75 6C.783 6 0 6.783 0 7.75v6.5C0 15.217.783 16 1.75 16h12.5A1.75 1.75 0 0 0 16 14.25v-6.5A1.75 1.75 0 0 0 14.25 6zM1.5 7.75a.25.25 0 0 1 .25-.25h12.5a.25.25 0 0 1 .25.25v6.5a.25.25 0 0 1-.25.25H1.75a.25.25 0 0 1-.25-.25z"/>
      <text x="24" y="13" class="stat-label">Public Repos:</text>
      <text x="116" y="13" class="stat-value">{repo_count}</text>
    </g>
  </g>

  <!-- Column 2 (Right) -->
  <g transform="translate(255, 75)">
    <!-- Total Downloads -->
    <g transform="translate(0, 0)">
      <path class="accent" d="M8 12L3 7H6V0H10V7H13L8 12ZM0 14H16V16H0V14Z"/>
      <text x="24" y="13" class="stat-label">Total Downloads:</text>
      <text x="142" y="13" class="stat-value">{downloads_fmt}</text>
    </g>

    <!-- Total Commits -->
    <g transform="translate(0, 36)">
      <path class="accent" d="M11.93 8.5a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 0 1 0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 0 1 0 1.5h-3.32zM8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/>
      <text x="24" y="13" class="stat-label">Total Commits:</text>
      <text x="126" y="13" class="stat-value">{commits_fmt}</text>
    </g>
  </g>
</svg>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path} successfully!")

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


def update_sponsor_data_js(sponsor_data_path: str, user_data: dict) -> bool:
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
            all_time_ratio = round(amount / 1000.0, 4)

            display_name = login if is_pub else masked
            github_handle = login if is_pub else None

            all_time.append({
                "name": display_name,
                "github": github_handle,
                "tier": tier_info["tier"],
                "subTier": tier_info["subTier"],
                "ratio": all_time_ratio
            })
            new_added += 1
            changed = True

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
            month_ratio = round(amount / 700.0, 4)

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
        all_time.sort(key=lambda s: s.get("ratio", 0), reverse=True)
        new_this_month.sort(key=lambda s: s.get("ratio", 0), reverse=True)

        if new_this_month != original_this_month:
            changed = True

        if not changed:
            print("Site sponsor-data.js is already up to date.")
            return False

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        output = f"""// Auto-generated by .github/scripts/update_downloads.py — do not edit manually
// Generated: {now_iso}
const sponsorData = {{
  allTime: {json.dumps(all_time, indent=4)},
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
        
        repo_data[name.lower()] = {
            "name": name,
            "owner": owner,
            "stars": stars,
            "downloads": downloads,
            "commits": commits
        }
        total_downloads += downloads
        total_stars += stars
        total_commits += commits
        print(f"Repo {full_name}: {stars} stars, {downloads} downloads, {commits} commits")
        
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
            "downloads_formatted": format_number(data["downloads"])
        }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(stats_export, f, indent=2)
    print("Exported stats.json successfully!")
        
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        readme_path = "../../README.md"  # if run from script folder
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Update Total Downloads badge
    total_formatted = format_number(total_downloads)
    total_pattern = r'Total%20Downloads-[^-\s)]+-7C4DFF'
    total_replacement = f'Total%20Downloads-{total_formatted}-7C4DFF'
    content, total_count = re.subn(total_pattern, total_replacement, content)
    print(f"Total Downloads badge updated: {total_count > 0}")

    # Update Total Stars badge if present
    total_stars_formatted = format_number(total_stars)
    total_stars_pattern = r'Total%20Stars-[^-\s)]+-7C4DFF'
    total_stars_replacement = f'Total%20Stars-{total_stars_formatted}-7C4DFF'
    content, total_stars_count = re.subn(total_stars_pattern, total_stars_replacement, content)
    print(f"Total Stars badge updated: {total_stars_count > 0}")
    
    # Update Stars badges in the table
    def replace_stars(match):
        repo_name = match.group(2)
        data = repo_data.get(repo_name.lower())
        if data:
            stars_formatted = format_number(data["stars"])
            return f'<a href="https://github.com/{data["owner"]}/{data["name"]}/stargazers"><img src="https://img.shields.io/badge/Stars-{stars_formatted}-7C4DFF?style=flat-square&amp;labelColor=161b22" alt="Stars"></a>'
        return match.group(0)
        
    stars_pattern = r'<a href="https://github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)/stargazers"><img src="https://img\.shields\.io/badge/Stars-([^-\s?]+)-7C4DFF[^"]*" alt="Stars"></a>'
    content, stars_count = re.subn(stars_pattern, replace_stars, content)
    print(f"Repo Star badges updated: {stars_count}")
    
    # Update Downloads badges in the table
    def replace_downloads(match):
        repo_name = match.group(2)
        data = repo_data.get(repo_name.lower())
        if data:
            downloads_formatted = format_number(data["downloads"])
            return f'<a href="https://github.com/{data["owner"]}/{data["name"]}/releases/latest"><img src="https://img.shields.io/badge/Downloads-{downloads_formatted}-7C4DFF?style=flat-square&amp;labelColor=161b22" alt="Downloads"></a>'
        return match.group(0)
        
    downloads_pattern = r'<a href="https://github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)/releases/latest"><img src="https://img\.shields\.io/badge/Downloads-([^-\s?]+)-7C4DFF[^"]*" alt="Downloads"></a>'
    content, downloads_count = re.subn(downloads_pattern, replace_downloads, content)
    print(f"Repo Download badges updated: {downloads_count}")
    
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

    if total_count > 0 or total_stars_count > 0 or stars_count > 0 or downloads_count > 0 or readme_sponsors_updated:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("README.md updated successfully!")
    else:
        print("No badges or sponsors updated in README.md")

if __name__ == "__main__":
    main()
