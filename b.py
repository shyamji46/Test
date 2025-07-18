from playwright.sync_api import sync_playwright
import time

def trigger_rummycircle_otp_call(phone):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 360, 'height': 640})
        page.goto("https://www.rummycircle.com/")

        # Fill phone number
        page.fill('input[placeholder="Enter Mobile Number"]', phone)

        # Click Get Started
        page.click('text=GET STARTED')

        # Wait for OTP input to appear
        page.wait_for_selector('input[placeholder="Enter 6 digit OTP"]')

        print("📲 OTP sent to", phone)
        time.sleep(31)

        # Loop: keep clicking "Get OTP on call" every 31 seconds
        while True:
            try:
                page.click('text=Get OTP on call')
                print("📞 Get OTP on Call clicked again")
            except Exception as e:
                print("❌ Error clicking OTP on call:", e)
            time.sleep(31)

        browser.close()

# Example
trigger_rummycircle_otp_call("9369660538")
