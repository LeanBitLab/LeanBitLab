import os
import re
import json
import urllib.request

def get_repos():
    url = "https://api.github.com/users/LeanBitLab/repos?per_page=100"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    token = os.getenv("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    
    with urllib.request.urlopen(req) as response:
        repos = json.loads(response.read().decode())
        return [repo["name"] for repo in repos if not repo.get("fork", False)]

def get_total_downloads(repos):
    total = 0
    token = os.getenv("GITHUB_TOKEN")
    for repo in repos:
        try:
            url = f"https://api.github.com/repos/LeanBitLab/{repo}/releases"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            if token:
                req.add_header("Authorization", f"token {token}")
            with urllib.request.urlopen(req) as response:
                releases = json.loads(response.read().decode())
                for r in releases:
                    for asset in r.get("assets", []):
                        total += asset.get("download_count", 0)
        except Exception as e:
            print(f"Error fetching downloads for {repo}: {e}")
    return total

def main():
    repos = get_repos()
    print(f"Found repos: {repos}")
    total = get_total_downloads(repos)
    print(f"Total downloads: {total}")
    
    # Format total
    if total >= 1000:
        formatted = f"{total / 1000:.1f}k"
    else:
        formatted = str(total)
        
    print(f"Formatted total: {formatted}")
    
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        readme_path = "../../README.md"  # if run from script folder
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Regex to find: Total%20Downloads-value-7C4DFF
    pattern = r'Total%20Downloads-[^-\s)]+-7C4DFF'
    replacement = f'Total%20Downloads-{formatted}-7C4DFF'
    
    new_content, count = re.subn(pattern, replacement, content)
    if count > 0:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md updated successfully!")
    else:
        print("Total Downloads badge pattern not found in README.md")

if __name__ == "__main__":
    main()
