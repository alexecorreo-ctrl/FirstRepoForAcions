import pytest
from playwright.sync_api import APIRequestContext

def test_create_post(api_request_context: APIRequestContext):
    # Added '/posts' to the end of the URL
    response = api_request_context.post(
        "https://jsonplaceholder.typicode.com/posts", 
        data={
            "title": "My New Playwright Post",
            "body": "This was created via API!",
            "userId": 1,
        }
    )

    # Now this will be True (201 Created)
    assert response.ok
    assert response.status == 201
    
    print(f"\n[API Response] {response.json()}")
