import pytest
from pages.login_page import LoginPage

@pytest.fixture
def login_page(page):
    # This creates the login page object for ANY test that asks for it
    return LoginPage(page)
