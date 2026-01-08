import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"] 

# 2️⃣ GitHub API URL for creating a repo
url = "https://api.github.com/user/repos"

# 3️⃣ Repo data
payload = {
    "name": "my-new-repo",        # Repo name
    "description": "Created via REST API in Python",
    "private": False             # True for private repo
}

# 4️⃣ Headers
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}

# 5️⃣ Make the POST request
response = requests.post(url, headers=headers, json=payload)

# 6️⃣ Output response
print("Status Code:", response.status_code)
print("Response Body:", response.json())
