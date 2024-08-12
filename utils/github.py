import requests
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_github_stars():
    repo_url = "https://api.github.com/repos/nitdraig/roger"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 200:
        repo_data = response.json()
        stars = repo_data.get("stargazers_count", 0)
        return stars
    else:
        return 0
