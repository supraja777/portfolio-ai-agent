import requests
import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "supraja777"
REPO = "my-new-repo"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def commit_file(FILE_PATH: str):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_sha = response.json()["sha"]
        print("File exists. SHA:", file_sha)
    else:
        file_sha = None
        print("File does not exist. Ready to create new file.")

    import base64

    # Read file
    with open(FILE_PATH, "rb") as f:
        content = f.read()

    encoded_content = base64.b64encode(content).decode("utf-8")

    payload = {
        "message": "Add or update {FILE_PATH}",
        "content": encoded_content,
        "branch": "main"
    }

    # If file exists, include sha
    if file_sha:
        payload["sha"] = file_sha

    # PUT request
    response = requests.put(url, headers=headers, json=payload)

    print("GITHUB RESPONSE - ", response)

    print("COMMITTED ", {FILE_PATH})
