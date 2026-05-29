from playwright.sync_api import Page, expect

# Ensure this is your Classic token with 'delete_repo' scope
GITHUB_TOKEN = "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"
USERNAME = "alexecorreo-ctrl"  # Your GitHub username

def test_bulk_delete_test_repos(page: Page):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Playwright-Cleanup-Script"
    }

    # 1. LIST all repositories owned by you
    # GET /user/repos returns repositories you have access to
    list_response = page.request.get("https://api.github.com/users/alexecorreo-ctrl/repos", headers=headers)
    assert list_response.status == 200
    
    repos = list_response.json()
    # Filter for repos that start with 'test-repo-'
    repos_to_delete = [repo['name'] for repo in repos if repo['name'].startswith("test-repo-")]
    
    print(f"\nFound {len(repos_to_delete)} test repositories to delete.")

    # 2. DELETE each matching repository
    for repo_name in repos_to_delete:
        delete_url = f"https://api.github.com/repos/{USERNAME}/{repo_name}"
        delete_response = page.request.delete(delete_url, headers=headers)
        
        # 204 means successful deletion
        if delete_response.status == 204:
            print(f"Successfully deleted: {repo_name}")
        else:
            print(f"Failed to delete {repo_name}: {delete_response.status} - {delete_response.text()}")

    # Final check: no repos with that prefix should remain
    assert all(not r['name'].startswith("test-repo-") for r in page.request.get("https://api.github.com/users/alexecorreo-ctrl/repos", headers=headers).json())
