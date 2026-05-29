from playwright.sync_api import Page, expect

def test_github_get_user(page: Page):
    headers = {
        "User-Agent": "Playwright-Test",
        "Accept": "application/vnd.github+json"
    }
    
    response = page.request.get("https://api.github.com/users/octocat", headers=headers)
    body = response.json()

    # DEBUG: Print keys to see what is actually inside 'body'
    print(f"\nResponse Keys: {list(body.keys())}")
    
    # Check if we got an error message instead of a user
    if "message" in body:
        print(f"GitHub Error: {body['message']}")
        assert False, f"API returned an error message: {body['message']}"

    # Now it's safe to assert the login
    assert body["login"] == "octocat"
    print(f"Success! Found user: {body['login']}")
