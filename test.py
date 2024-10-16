from seleniumbase import SB
import time

def verify_success(sb):
    """Verify the success of the page load by checking for a specific element."""
    sb.assert_element('img[alt="Logo Assembly"]', timeout=4)
    time.sleep(3)  # Wait for a bit longer if necessary

def handle_captcha(sb):
    """Attempt to handle CAPTCHA if it appears."""
    if sb.is_element_visible('input[value*="Verify"]'):
        sb.uc_click('input[value*="Verify"]')
    else:
        sb.uc_gui_click_captcha()  # Use GUI click for the CAPTCHA

def main():
    with SB(uc=True) as sb:
        # Open the URL with a reconnect attempt
        sb.uc_open_with_reconnect("https://modijiurl.com/fBUFTv", 3)
        
        # Try to verify success
        try:
            verify_success(sb)
        except Exception as e:
            print("Initial verification failed. Attempting to handle CAPTCHA.")
            handle_captcha(sb)
            try:
                verify_success(sb)
            except Exception:
                print("Failed after CAPTCHA handling, detected!")
                raise  # Raise the exception to indicate a failure

if __name__ == "__main__":
    main()
