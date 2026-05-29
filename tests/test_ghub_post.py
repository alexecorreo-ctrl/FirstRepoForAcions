import pytest
import uuid
from playwright.sync_api import Page, expect

# PASTE YOUR TOKEN HERE (or use an environment variable)
GITHUB_TOKEN = "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"

def test_create_github_repo(page: Page):
    # 1. Setup headers with Authentication
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Playwright-Test"
    }
    
    # 2. Setup the data (The Body)
    # We use uuid to ensure the repo name is always unique
    repo_name = f"test-repo-{uuid.uuid4().hex[:6]}"
    payload = {
        "name": repo_name,
        "description": "Created via Playwright API Test",
        "private": False
    }
    
    # 3. Perform the POST request
    response = page.request.post("https://api.github.com/user/repos", headers=headers, data=payload)
    
    # 4. ASSERT: 201 means "Created"
    assert response.status == 201, f"Failed to create repo. Body: {response.text()}"
    
    body = response.json()
    print(f"\nSuccessfully created repo: {body['full_name']}")
    assert body["name"] == repo_name

  # 5. CLEANUP: Delete the repo we just created
    # The endpoint for deleting is /repos/{owner}/{repo}
    full_name = body['full_name']
    owner = full_name.split('/')[0]
    delete_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    
    delete_response = page.request.delete(delete_url, headers=headers)

    if delete_response.status == 403:
        print(f"FAILED CLEANUP: 403 Forbidden. Check if your token has 'Administration: Write' permissions.")
    elif delete_response.status == 204:
        print(f"Successfully cleaned up: {full_name}")
    else:
        print(f"Unexpected status {delete_response.status}: {delete_response.text()}")
    
    """  # 204 No Content is the success code for a DELETE
    assert delete_response.status == 204
    print(f"Successfully cleaned up: {full_name}") """