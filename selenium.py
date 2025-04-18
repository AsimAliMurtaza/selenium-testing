import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

BASE_URL = "http://localhost:3000"  # Adjust this to your actual URL

# Read credentials from CSV
def read_credentials():
    credentials = []
    with open('credentials.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            credentials.append({
                "name": row["name"],
                "email": row["email"],
                "password": row["password"]
            })
    return credentials

# --- SIGNUP TEST ---
def test_signup(user):
    driver.get(f"{BASE_URL}/signup")

    wait.until(EC.presence_of_element_located((By.NAME, "name")))
    driver.find_element(By.NAME, "name").send_keys(user["name"])
    driver.find_element(By.NAME, "email").send_keys(user["email"])
    driver.find_element(By.NAME, "password").send_keys(user["password"])

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(2)
    assert "dashboard" in driver.current_url or "success" in driver.page_source.lower()
    print(f"✅ Signup test passed for {user['email']}")

# --- LOGIN TEST ---
def test_login(user):
    driver.get(f"{BASE_URL}/login")

    wait.until(EC.presence_of_element_located((By.NAME, "email")))
    driver.find_element(By.NAME, "email").send_keys(user["email"])
    driver.find_element(By.NAME, "password").send_keys(user["password"])

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(2)
    assert "dashboard" in driver.current_url or "welcome" in driver.page_source.lower()
    print(f"✅ Login test passed for {user['email']}")

# Run tests using each user in CSV
try:
    users = read_credentials()
    for user in users:
        test_signup(user)
        test_login(user)
finally:
    driver.quit()
