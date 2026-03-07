import json
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import JOBS_DB_FILE, RESUME_DATA

def load_jobs():
    try:
        with open(JOBS_DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def auto_apply():
    jobs = load_jobs()
    jobs.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    if not jobs:
        print("No jobs found to apply to.")
        return

    print(f"Found {len(jobs)} jobs. Starting Edge automation...")

    # Configure Edge Options
    edge_options = EdgeOptions()
    # edge_options.add_argument("--headless") # Uncomment if you want it to run in background
    
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)

    for job in jobs[:10]: # Check top 10
        print(f"Opening: {job['company']} - {job['title']}")
        driver.get(job['url'])
        
        try:
            # Platform detection
            if "greenhouse.io" in driver.current_url:
                fill_greenhouse(driver)
            elif "lever.co" in driver.current_url:
                fill_lever(driver)
            else:
                print("Unknown platform. Please fill manually. Waiting for you...")
            
            # Instead of closing, we wait for you to check and press Enter in the terminal
            print("===> Check the browser. If it looks good, press Enter here to move to the next job.")
            input("Press Enter...")
            
        except Exception as e:
            print(f"Automation assist failed for this link: {e}")
            
    driver.quit()

def fill_greenhouse(driver):
    try:
        # Wait for form
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "first_name")))
        driver.find_element(By.ID, "first_name").send_keys(RESUME_DATA["first_name"])
        driver.find_element(By.ID, "last_name").send_keys(RESUME_DATA["last_name"])
        driver.find_element(By.ID, "email").send_keys(RESUME_DATA["email"])
        driver.find_element(By.ID, "phone").send_keys(RESUME_DATA["phone"])
        
        # Resume
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(RESUME_DATA["resume_path"])
        print("Filled Greenhouse basics.")
    except:
        pass

def fill_lever(driver):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "name")))
        driver.find_element(By.NAME, "name").send_keys(f"{RESUME_DATA['first_name']} {RESUME_DATA['last_name']}")
        driver.find_element(By.NAME, "email").send_keys(RESUME_DATA["email"])
        driver.find_element(By.NAME, "phone").send_keys(RESUME_DATA["phone"])
        
        # Resume
        file_input = driver.find_element(By.ID, "resume-upload-input")
        file_input.send_keys(RESUME_DATA["resume_path"])
        print("Filled Lever basics.")
    except:
        pass

if __name__ == "__main__":
    auto_apply()
