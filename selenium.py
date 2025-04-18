from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

# Launch the driver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

BASE_URL = "http://localhost:3000"  # Change to your actual URL if deployed

# --- SIGNUP TEST ---
def test_signup():
    driver.get(f"{BASE_URL}/signup")

    wait.until(EC.presence_of_element_located((By.NAME, "name")))
    name_input = driver.find_element(By.NAME, "name")
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    
    name_input.send_keys("Chakra Test User")
    email_input.send_keys("chakratestuser@example.com")
    password_input.send_keys("SecurePassword123")

    # Find Chakra UI styled submit button (assumes it's still a <button type="submit">)
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    # Wait for navigation or success
    time.sleep(2)
    assert "dashboard" in driver.current_url or "success" in driver.page_source.lower()
    print("✅ Signup test passed!")

# --- LOGIN TEST ---
def test_login():
    driver.get(f"{BASE_URL}/login")

    wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")

    email_input.send_keys("chakratestuser@example.com")
    password_input.send_keys("SecurePassword123")

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    time.sleep(2)
    assert "dashboard" in driver.current_url or "welcome" in driver.page_source.lower()
    print("✅ Login test passed!")

# Run tests
try:
    test_signup()
    test_login()
finally:
    driver.quit()
