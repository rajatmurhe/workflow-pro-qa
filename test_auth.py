import re
from playwright.sync_api import Page, expect

def test_user_login(page: Page):
    # 1. Go to a public test site (using a real demo site for this example)
    page.goto("https://demo.applitools.com/")
    
    # 2. Fill in the login form
    page.locator("#username").fill("admin")
    page.locator("#password").fill("password123")
    page.locator("#log-in").click()
    
    # 3. Verify successful login by checking if the app logo is visible
    expect(page.locator(".logo-w")).to_be_visible(timeout=10000)
