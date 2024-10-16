from seleniumbase import SB

def verify_success(sb):
    sb.assert_element('img[alt="Logo Assembly"]', timeout=4)
    sb.sleep(3)

with SB(uc=True, driver_version="129.0.6668.100") as sb:
    sb.uc_open_with_reconnect("https://modijiurl.com/fBUFTv", 3)

    driver_version = sb.driver.capabilities['chrome']['chromedriverVersion']  # For Chrome
        # For Firefox, use:
        # driver_version = self.driver.capabilities['moz:geckodriverVersion']
        
    print("Driver Version:", driver_version)
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