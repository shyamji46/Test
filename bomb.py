import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def trigger_rummycircle_otp_call(phone):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=360,640")  # Mobile view

    driver = uc.Chrome(options=options)

    try:
        driver.get("https://www.rummycircle.com/registernow.html")

        wait = WebDriverWait(driver, 15)

        # Step 1: Fill phone number
        phone_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Mobile Number']"))
        )
        phone_input.send_keys(phone)

        # Step 2: Click GET STARTED
        get_started_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'GET STARTED')]"))
        )
        get_started_button.click()
        print("📲 OTP Sent to:", phone)

        # Step 3: Wait for OTP screen to load
        otp_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter 6 digit OTP']"))
        )
        print("⌛ Waiting 31 seconds before triggering OTP call...")

        time.sleep(31)

        # Step 4: Click "Get OTP on call"
        otp_call_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Get OTP on call')]")
        otp_call_btn.click()

        print("📞 'Get OTP on call' triggered successfully!")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        driver.quit()

# Example call
trigger_rummycircle_otp_call("9369660538")
