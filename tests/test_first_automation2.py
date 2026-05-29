import re
from playwright.sync_api import Page, expect

def test_login_and_inventory(page: Page):
    # 1. Go to a site that doesn't block bots
    page.goto("https://saucedemo.com")
    
    # 2. Fill in the login details
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    # 3. Assert we are on the products page
    # This site is stable and won't throw a CAPTCHA at you!
    expect(page).to_have_title(re.compile("Swag Labs"))
    
    # 4. Check if the 'Products' header is visible
    header = page.locator(".title")
    expect(header).to_have_text("Products")

        # 5. Add the first item to the cart
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    
    # 6. Verify the cart badge shows '1'
    badge = page.locator(".shopping_cart_badge")
    expect(badge).to_have_text("1")

    
    print("Test Passed on SauceDemo!")
