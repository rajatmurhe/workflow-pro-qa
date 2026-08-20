import pytest
from playwright.sync_api import expect
import uuid

@pytest.fixture
def test_project(api_client):
    project_payload = {
        "name": f"QA_Proj_{uuid.uuid4().hex[:8]}",
        "description": "Tenant isolation validation",
        "team_members": ["admin@company1.com"]
    }
    response = api_client.post("/api/v1/projects", json=project_payload)
    project_data = response.json()
    yield project_data
    api_client.delete(f"/api/v1/projects/{project_data['id']}")

def test_project_creation_flow(test_project, desktop_page, mobile_page, alt_tenant_page):
    project_name = test_project["name"]
    
    # 1. Desktop UI
    desktop_page.goto("/projects") 
    expect(desktop_page.locator(f".project-card:has-text('{project_name}')")).to_be_visible(timeout=15000)
    
    # 2. Mobile Accessibility
    mobile_page.goto("/projects")
    menu_btn = mobile_page.locator("#mobile-menu-toggle")
    if menu_btn.is_visible():
        menu_btn.click()
        mobile_page.locator("text=Projects").click()
    expect(mobile_page.locator(f".project-card:has-text('{project_name}')")).to_be_visible()
    
    # 3. Security (Tenant Isolation)
    alt_tenant_page.goto("/projects")
    expect(alt_tenant_page.locator(".projects-header")).to_be_visible()
    expect(alt_tenant_page.locator(f".project-card:has-text('{project_name}')")).to_have_count(0)
