import re
from playwright.sync_api import Page, expect

# We just add 'login_page' as an argument, and pytest "injects" it for us!
def test_login_with_fixture(login_page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    
    expect(login_page.page).to_have_title(re.compile("Swag Labs"))
