from seleniumbase import SB
import time

def verify_success(sb):
    sb.assert_element('img[alt="Logo Assembly"]', timeout=4)
    sb.sleep(3)

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
with SB(uc=True, headed=True, disable_features="UserAgentClientHint", agent=ua) as sb:
    sb.uc_open_with_reconnect("https://modijiurl.com/fBUFTv", 3)

    print(sb.get_current_url())
    # driver_version = sb.driver.capabilities['chrome']['chromedriverVersion']  # For Chrome
        # For Firefox, use:
        # driver_version = self.driver.capabilities['moz:geckodriverVersion']
        
    try:
        verify_success(sb)
    except Exception:
        if sb.is_element_visible('input[value*="Verify"]'):
            sb.uc_click('input[value*="Verify"]')
        else:
            sb.uc_gui_click_captcha()
        try:
            verify_success(sb)
        except Exception:
            print("error")
            pass
    time.slee(10)
    print(sb.get_current_url())
