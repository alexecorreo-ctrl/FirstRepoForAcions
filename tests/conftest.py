import pytest
import os
from pages.login_page import LoginPage

@pytest.fixture
def login_page(page, request):
    # Setup
    lp = LoginPage(page)
    
    yield lp 

    # Teardown: This part runs AFTER the test
    # Check if the test failed
    # 'request.node' represents the test itself
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        # Create a 'failures' folder if it doesn't exist
        if not os.path.exists("failures"):
            os.makedirs("failures")
        
        # Take a screenshot with the name of the test
        screenshot_path = f"failures/{request.node.name}.png"
        page.screenshot(path=screenshot_path)
        print(f"\n[TEARDOWN] Test failed! Screenshot saved to {screenshot_path}")

# This magic bit of code allows the fixture to see if the test failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    #--------------------------

import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def api_request_context(playwright):
    # Setup: Create the API context
    request_context = playwright.request.new_context(
        base_url="https://typicode.com"
    )
    yield request_context
    # Teardown: Close it after the tests are done
    request_context.dispose()

