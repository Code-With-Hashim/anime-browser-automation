from seleniumbase import SB
import time

def verify_tab_open(sb):
    """Verify that the current tab is still open and accessible."""
    try:
        current_url = sb.get_current_url()
        print("Current URL:", current_url)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    chrome_args = [
        "--disable-extensions",  # Disable Chrome extensions
        "--no-sandbox",  # Needed for running in EC2
        "--disable-infobars",  # Disable infobars
        "--disable-gpu",  # Disable GPU acceleration
        # "--headless",  # Uncomment if running in headless mode
    ]
    
    with SB(uc=True, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36", ad_block=True, incognito=True, is_mobile=True, undetectable=True, chromium_arg=chrome_args) as sb:
        # Open the URL with a reconnect attempt
        sb.uc_open_with_reconnect("https://modijiurl.com/fBUFTv", 3)

        # Switch to the correct tab if a new one opens
        current_tabs = sb.driver.window_handles  # Get list of open tabs
        for tab in current_tabs:
            sb.switch_to_window(tab)
            if "modijiurl.com" in sb.get_current_url():  # Check if it's the correct tab
                break
        
        if sb.is_element_visible('input[value*="Verify"]'):
            sb.uc_click('input[value*="Verify"]')
            print("clickable")

        # Verify the current URL and tab status
        if verify_tab_open(sb):
            time.sleep(10)  # Wait to make sure page is loaded
            print("Final URL:", sb.get_current_url())
        else:
            print("The browser window was closed or not accessible.")

if __name__ == "__main__":
    main()
