import os
from seleniumbase import SB
import time
import pyautogui
import random
# from pyvirtualdisplay.display import Display
# disp = Display(visible=True, size=(1366, 768), backend="xvfb", use_xauth=True)
# disp.start()

# os.environ['DISPLAY'] = ':99'

# print(os.environ['DISPLAY'], 'after')
# import Xlib.display
# pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])

def verify_success(sb):
    sb.assert_element('img[alt="Logo Assembly"]', timeout=4)
    sb.sleep(3)

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
with SB(uc=True, headed=True, disable_features="UserAgentClientHint", agent=ua, incognito=True, xvfb=True) as sb:
    sb.uc_open_with_reconnect("https://modijiurl.com/fBUFTv", 3)
    tab_handles = sb.get_window_handles()
    print(len(tab_handles))
    print(sb.get_current_url())
    # driver_version = sb.driver.capabilities['chrome']['chromedriverVersion']  # For Chrome
        # For Firefox, use:
        # driver_version = self.driver.capabilities['moz:geckodriverVersion']
        
    if sb.is_element_visible("iframe"):
        sb.switch_to_frame("iframe")
        sb.execute_script('document.querySelector("input").focus()')
        sb.disconnect()
        print('Click..')
        pyautogui.press(" ")
        sb.driver.reconnect(10)

    # sb.uc_gui_click_x_y(x, y, timeframe=0.25)

    sb.uc_gui_click_captcha(frame="iframe", retry=False, blind=False)
    # driver.uc_gui_click_cf(frame="iframe", retry=False, blind=False)
    # driver.uc_gui_click_rc(frame="iframe", retry=False, blind=False)

    sb.uc_gui_handle_captcha(frame="iframe")
    sb.uc_gui_click_captcha()
    print("connect")
    random_number = random.randint(1000, 9999)
    filename = f"screenshot_{random_number}.png"
    sb.save_screenshot(filename)
    print('End.')

    time.sleep(10)
    print(sb.get_current_url())
    sb.sb.uc_gui_click_captcha()
    time.sleep(10)
    print(sb.get_current_url())


