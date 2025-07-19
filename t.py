from playwright.sync_api import sync_playwright
import time

def trigger_rummycircle_otp_call(phone):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 360, 'height': 640})
        page.goto("https://www.playrummy.com/")
        
        page.click('text=Login/Register')

        # Fill phone number
        page.fill('input[placeholder="Enter Email/Mobile No. *"]', phone)
        time.sleep(31)
        
        # Click Get Started
        page.click('text=Resend OTP')

        print("📲 OTP sent to", phone)
        time.sleep(31)

        while True:
            try:
                page.click('text=Resend OTP')
                print("📞 Get OTP on Call clicked again")
            except Exception as e:
                print("❌ Error clicking OTP on call:", e)
            time.sleep(31)

        # This will never be reached in infinite loop
        browser.close()

# Example
trigger_rummycircle_otp_call("7309369669")
