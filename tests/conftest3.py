import pytest
import os
from pages.login_page import LoginPage

@pytest.fixture
def login_page(page):
    # --- EVERYTHING BEFORE 'YIELD' IS "SETUP" ---
    print("\n[SETUP] Creating the Login Page object...")
    lp = LoginPage(page)
    
    yield lp  # <--- This "hands" the object to the test and PAUSES here.

    # --- EVERYTHING AFTER 'YIELD' IS "TEARDOWN" ---
    print("\n[TEARDOWN] Clearing cookies and closing up...")
    page.context.clear_cookies()
    # Note: We don't need to close the page or browser here, Playwright's pytest plugin handles that automatically.