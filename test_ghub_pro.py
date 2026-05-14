import os
import uuid
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
from jsonschema import validate

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
USER = os.getenv("GITHUB_USER")

REPO_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
    },
    "required": ["id", "name"]
}

@pytest.mark.parametrize("description", ["Simple test", "Special chars !@#"])
def test_repo_lifecycle(page: Page, description):
    headers = {
        "Authorization": f"Bearer {TOKEN}", 
        "Accept": "application/vnd.github+json", 
        "User-Agent": "Pytest"
    }
    
    # 1. SETUP: Create
    repo_name = f"test-repo-{uuid.uuid4().hex[:6]}"
    # IMPORTANT: Ensure 'api.' is at the start
    url_create = "https://api.github.com/user/repos"
    
    response_create = page.request.post(url_create, headers=headers, data={"name": repo_name, "description": description})
    
    # Added () to .text() to see the actual error if it fails
    assert response_create.status == 201, f"Create failed: {response_create.text()}"

    # 2. VALIDATE
    url_get = f"https://api.github.com/repos/{USER}/{repo_name}"
    response_get = page.request.get(url_get, headers=headers)
    expect(response_get).to_be_ok()
    
    body = response_get.json()
    validate(instance=body, schema=REPO_SCHEMA)
    assert body["description"] == description

    # 3. TEARDOWN: Delete
    url_delete = f"https://api.github.com/repos/{USER}/{repo_name}"
    response_delete = page.request.delete(url_delete, headers=headers)
    
    assert response_delete.status == 204
    print(f"\nSuccessfully handled: {repo_name}")
