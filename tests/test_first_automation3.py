import re
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage # Import your blueprint

def test_login_with_pom(page: Page):
    # Initialize the page object
    login_page = LoginPage(page)
    
    # Use the methods from the class
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    
    # Assertions stay in the test file
    expect(page).to_have_title(re.compile("Swag Labs"))
    expect(page.locator(".title")).to_have_text("Products")
