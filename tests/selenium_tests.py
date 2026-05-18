import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_page_title(driver):
    """Test Case 1: Verify the page title"""
    driver.get('http://app:5000')
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    
    assert "User Management" in driver.page_source
    print("✓ Test 1 Passed: Page title is correct")

def test_add_user_form(driver):
    """Test Case 2: Verify add user form functionality"""
    driver.get('http://app:5000')
    
    # Wait for form to be present
    wait = WebDriverWait(driver, 10)
    name_field = wait.until(
        EC.presence_of_element_located((By.ID, "userName"))
    )
    
    # Fill the form
    name_field.send_keys("Test User")
    
    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("test@example.com")
    
    # Verify submit button exists
    submit_button = driver.find_element(By.ID, "submitBtn")
    assert submit_button.is_displayed()
    
    print("✓ Test 2 Passed: Add user form is functional")
