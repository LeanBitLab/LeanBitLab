import os
import re
import json
import urllib.request

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

def format_number(num):
    if num >= 1000:
        return f"{num / 1000:.1f}k"
    return str(num)

def generate_stats_card(total_stars, total_downloads, repo_count, output_path="stats.svg"):
    stars_fmt = format_number(total_stars)
    downloads_fmt = format_number(total_downloads)
    
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
      <text x="126" y="13" class="stat-value">2.2k+</text>
    </g>
  </g>
</svg>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path} successfully!")

def main():
    repos = get_repos_info()
    print(f"Found repos: {[r['full_name'] for r in repos]}")
    
    repo_data = {}
    total_downloads = 0
    total_stars = 0
    
    for repo in repos:
        name = repo["name"]
        full_name = repo["full_name"]
        owner = repo["owner"]
        stars = repo["stars"]
        downloads = get_repo_downloads(full_name)
        
        repo_data[name.lower()] = {
            "name": name,
            "owner": owner,
            "stars": stars,
            "downloads": downloads
        }
        total_downloads += downloads
        total_stars += stars
        print(f"Repo {full_name}: {stars} stars, {downloads} downloads")
        
    print(f"Total stars: {total_stars}")
    print(f"Total downloads: {total_downloads}")
    
    active_repos = [r for r in repos if not r["name"].startswith(".")]
    generate_stats_card(total_stars, total_downloads, len(active_repos), "stats.svg")
    
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
        owner = match.group(2)
        repo_name = match.group(3)
        data = repo_data.get(repo_name.lower())
        if data:
            stars_formatted = format_number(data["stars"])
            return f'[![Stars](https://img.shields.io/badge/Stars-{stars_formatted}-7C4DFF?style=flat-square)](https://github.com/{data["owner"]}/{data["name"]}/stargazers)'
        return match.group(0)
        
    stars_pattern = r'\[!\[Stars\]\(https://img\.shields\.io/badge/Stars-([^-\s?)]+)-7C4DFF\?style=flat-square\)\]\(https://github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)/stargazers\)'
    content, stars_count = re.subn(stars_pattern, replace_stars, content)
    print(f"Repo Star badges updated: {stars_count}")
    
    # Update Downloads badges in the table
    def replace_downloads(match):
        owner = match.group(2)
        repo_name = match.group(3)
        data = repo_data.get(repo_name.lower())
        if data:
            downloads_formatted = format_number(data["downloads"])
            return f'[![Downloads](https://img.shields.io/badge/Downloads-{downloads_formatted}-7C4DFF?style=flat-square)](https://github.com/{data["owner"]}/{data["name"]}/releases/latest)'
        return match.group(0)
        
    downloads_pattern = r'\[!\[Downloads\]\(https://img\.shields\.io/badge/Downloads-([^-\s?)]+)-7C4DFF\?style=flat-square\)\]\(https://github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)/releases/latest\)'
    content, downloads_count = re.subn(downloads_pattern, replace_downloads, content)
    print(f"Repo Download badges updated: {downloads_count}")
    
    if total_count > 0 or total_stars_count > 0 or stars_count > 0 or downloads_count > 0:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("README.md updated successfully!")
    else:
        print("No badges updated in README.md")

if __name__ == "__main__":
    main()
