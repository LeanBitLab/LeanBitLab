import os
import re
import json
import urllib.request

def get_repos_info():
    url = "https://api.github.com/users/LeanBitLab/repos?per_page=100"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    token = os.getenv("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    
    with urllib.request.urlopen(req) as response:
        repos = json.loads(response.read().decode())
        return [
            {
                "name": repo["name"],
                "stars": repo.get("stargazers_count", 0)
            }
            for repo in repos
            if not repo.get("fork", False)
        ]

def get_repo_downloads(repo_name):
    total = 0
    token = os.getenv("GITHUB_TOKEN")
    page = 1
    while True:
        try:
            url = f"https://api.github.com/repos/LeanBitLab/{repo_name}/releases?per_page=100&page={page}"
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
            print(f"Error fetching downloads for {repo_name} (page {page}): {e}")
            break
    return total

def format_number(num):
    if num >= 1000:
        return f"{num / 1000:.1f}k"
    return str(num)

def main():
    repos = get_repos_info()
    print(f"Found repos: {[r['name'] for r in repos]}")
    
    repo_stars = {}
    repo_downloads = {}
    total_downloads = 0
    
    for repo in repos:
        name = repo["name"]
        stars = repo["stars"]
        downloads = get_repo_downloads(name)
        
        repo_stars[name.lower()] = stars
        repo_downloads[name.lower()] = downloads
        total_downloads += downloads
        print(f"Repo {name}: {stars} stars, {downloads} downloads")
        
    print(f"Total downloads: {total_downloads}")
    
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        readme_path = "../../README.md"  # if run from script folder
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Update Total Downloads badge
    # Regex to find: Total%20Downloads-value-7C4DFF
    total_formatted = format_number(total_downloads)
    total_pattern = r'Total%20Downloads-[^-\s)]+-7C4DFF'
    total_replacement = f'Total%20Downloads-{total_formatted}-7C4DFF'
    content, total_count = re.subn(total_pattern, total_replacement, content)
    print(f"Total Downloads badge updated: {total_count > 0}")
    
    # Update Stars badges in the table
    # Pattern looks for: [![Stars](https://img.shields.io/badge/Stars-<value>-7C4DFF?style=flat-square)](https://github.com/LeanBitLab/<repo_name>/stargazers)
    def replace_stars(match):
        repo_name = match.group(2)
        stars = repo_stars.get(repo_name.lower(), 0)
        stars_formatted = format_number(stars)
        return f'[![Stars](https://img.shields.io/badge/Stars-{stars_formatted}-7C4DFF?style=flat-square)](https://github.com/LeanBitLab/{repo_name}/stargazers)'
        
    stars_pattern = r'\[!\[Stars\]\(https://img\.shields\.io/badge/Stars-([^-\s?)]+)-7C4DFF\?style=flat-square\)\]\(https://github\.com/LeanBitLab/([a-zA-Z0-9_-]+)/stargazers\)'
    content, stars_count = re.subn(stars_pattern, replace_stars, content)
    print(f"Repo Star badges updated: {stars_count}")
    
    # Update Downloads badges in the table
    # Pattern looks for: [![Downloads](https://img.shields.io/badge/Downloads-<value>-7C4DFF?style=flat-square)](https://github.com/LeanBitLab/<repo_name>/releases/latest)
    def replace_downloads(match):
        repo_name = match.group(2)
        downloads = repo_downloads.get(repo_name.lower(), 0)
        downloads_formatted = format_number(downloads)
        return f'[![Downloads](https://img.shields.io/badge/Downloads-{downloads_formatted}-7C4DFF?style=flat-square)](https://github.com/LeanBitLab/{repo_name}/releases/latest)'
        
    downloads_pattern = r'\[!\[Downloads\]\(https://img\.shields\.io/badge/Downloads-([^-\s?)]+)-7C4DFF\?style=flat-square\)\]\(https://github\.com/LeanBitLab/([a-zA-Z0-9_-]+)/releases/latest\)'
    content, downloads_count = re.subn(downloads_pattern, replace_downloads, content)
    print(f"Repo Download badges updated: {downloads_count}")
    
    if total_count > 0 or stars_count > 0 or downloads_count > 0:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("README.md updated successfully!")
    else:
        print("No badges updated in README.md")

if __name__ == "__main__":
    main()
