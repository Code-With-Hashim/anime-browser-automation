from seleniumbase import SB

with SB(uc=True, xvfb=True) as sb:
    url = "https://gitlab.com/login"
    sb.uc_open_with_reconnect(url, 4)
    sb.uc_gui_click_captcha()
    print(sb.get_page_title())