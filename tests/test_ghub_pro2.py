import os
import uuid
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
from jsonschema import validate # <--- New import

load_dotenv() # Loads the variables from .env
TOKEN = os.getenv("GITHUB_TOKEN")
USER = os.getenv("GITHUB_USER")

# The Blueprint: What a GitHub Repo object MUST look like
REPO_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "full_name": {"type": "string"},
        "private": {"type": "boolean"},
        "owner": {
            "type": "object",
            "properties": {
                "login": {"type": "string"}
            },
            "required": ["login"]
        }
    },
    "required": ["id", "name", "full_name", "private", "owner"]
}


@pytest.fixture
def repo_context(page: Page):
    # --- SETUP ---
    repo_name = f"test-repo-{uuid.uuid4().hex[:6]}"
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json", "User-Agent": "Pytest"}
    
    # Create the repo
    page.request.post("https://api.github.com/user/repos", headers=headers, data={"name": repo_name})
    
    # Give the test the name of the repo
    yield repo_name 

    # --- TEARDOWN (Runs after the test is done) ---
    page.request.delete(f"https://api.github.com/repos/{USER}/{repo_name}", headers=headers)
    print(f"\n[Cleanup] Deleted {repo_name}")

def test_repo_exists_after_creation(page: Page, repo_context):
    # 'repo_context' now contains the name of the repo we created
    headers = {"Authorization": f"Bearer {TOKEN}", "User-Agent": "Pytest"}
    response = page.request.get(f"https://api.github.com/repos/{USER}/{repo_context}", headers=headers)
    
    expect(response).to_be_ok()
    assert response.json()["name"] == repo_context

  # --- UPGRADE #2: Schema Validation ---
    # If the JSON doesn't match REPO_SCHEMA, this will throw a clear error
    validate(instance=body, schema=REPO_SCHEMA)
    print("\nSchema validation passed!")

    # Standard value assertions
    assert body["name"] == repo_context
    assert body["owner"]["login"] == USER