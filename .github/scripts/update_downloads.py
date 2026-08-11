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
