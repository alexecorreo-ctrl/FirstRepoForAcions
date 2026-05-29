import pytest
from playwright.sync_api import Page, expect

def test_get_user_success(page: Page):
    # This endpoint is truly open and returns valid JSON
    response = page.request.get("https://typicode.com")
    
    # 1. Check if the request actually worked (200 OK)
    expect(response).to_be_ok()
    
    # 2. Parse the JSON
    body = response.json()
    
    # 3. Assertions
    # Since we used /users/1, body is a dictionary (no index [0] needed)
    print(f"\nSuccessfully fetched user: {body['name']}")
    assert body["name"] == "Leanne Graham"
    assert body["email"] == "Sincere@april.biz"
