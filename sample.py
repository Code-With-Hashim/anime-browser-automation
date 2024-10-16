from seleniumbase import SB
from selenium.webdriver.common.by import By
import re
import requests
import time

# Constants
SCRAPOPS_API_KEY = "fd2d0dcd-c9d7-47ff-ba7c-1be8a63f5df4"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"


def verify_success(sb):
    """Check for successful verification."""
    sb.assert_element('img[alt="Logo Assembly"]', timeout=4)
    sb.sleep(3)


# Define the main function using SeleniumBase
def main(link, search, eps):
    with SB(uc=True) as sb:
        sb.open(link)

        # Retrieve all anime cards
        anime_cards = sb.find_elements(By.CLASS_NAME, "herald-post-thumbnail")

        for anime_card in anime_cards:
            title = anime_card.find_element(By.TAG_NAME, "a").get_attribute("title")
            link = anime_card.find_element(By.TAG_NAME, "a").get_attribute("href")
            print(title)

            if search in title:
                anchor_tag = anime_card.find_element(By.TAG_NAME, "a")
                anchor_tag.click()
                # sb.click(anime_card.find_element(By.TAG_NAME, "a"))
                print('open-link')

                # Wait for the content to load on the new page
                sb.wait_for_element("body", timeout=10)

                # Find the element by ID
                link_html = sb.find_element(By.ID, "pryc-wp-acctp-original-content")
                p_lists = link_html.find_elements(By.TAG_NAME, "p")

                # Iterate over paragraphs to find the right episode
                for p_index, p_tag in enumerate(p_lists):
                    try:
                        title = p_tag.find_element(By.TAG_NAME,"strong").text
                        link = p_lists[p_index + 2].find_element(By.TAG_NAME,"a")
                        link_part = link.get_attribute("innerHTML")
                        print(title, eps, link_part)

                        title_words = title.split(" ")
                        if any(word.isdigit() and int(word) == eps for word in title_words) and link_part == 'Mir':
                            print("GOES IN")
                            # sb.click(link)
                # First click the link
                            link.click()

                            # Start the loop to check and repeat if necessary
                            while True:
                                try:
                                    # Find the button and get the link attribute
                                    link_btn = sb.find_element("css selector", ".btn-success")
                                    click_link = link_btn.get_attribute('href')

                                    # If the click link contains "https://publicearn.com", go back and retry
                                    if "https://modijiurl.com" not in click_link:
                                        print("Found publicearn.com, going back and retrying...")

                                        # Go back to the previous page
                                        sb.go_back()

                                        # Wait for the previous page to load (use a specific element to ensure the page has loaded)
                                        sb.wait_for_element(By.TAG_NAME, "body", timeout=10)

                                        # Click the link again to retry
                                        link.click()

                                    else:
                                        print(click_link)
                                        if "https://modijiurl.com" in click_link:
                                            print('found modi url')
                                            break
                                        else:
                                            print("Non-publicearn link found and modiji url is not found, proceeding...")
                                    
                                except Exception as e:
                                    print("Error occurred while processing the link:", str(e))
                                    break  # Exit the loop on error
                                


                            if "https://modijiurl.com" in click_link:
                                print("goes in")
                                # link_btn.click()
                                # print("clicked")


                                # sb.wait_for_element(By.TAG_NAME, "body", timeout=10)

                                # sb.switch_to_newest_window()

                                # print(f"Current URL after switching: {sb.get_current_url()}")
                                # sb.wait_for_element(By.TAG_NAME, "body", timeout=10)


                                # time.sleep(10)
                                sb.uc_open_with_reconnect(click_link, 3)
                                print('connect')

                                # try:
                                #     verify_success(sb)
                                # except Exception:
                                #     if sb.is_element_visible('input[value*="Verify"]'):
                                #         sb.uc_click('input[value*="Verify"]')
                                #     else:
                                #         sb.uc_gui_click_captcha()
                                #     try:
                                #         verify_success(sb)
                                #     except Exception as er:
                                #         print("is any error" , er)
                                #         # raise Exception("Detected!")
                                
                                # print("verification successfull")
                                sb.wait_for_element(By.TAG_NAME, "body", timeout=10)
                                print(sb.get_page_source())
                                sb.save_screenshot("datacamp.png")


                                # Wait for the new window/tab and switch to it
                                # print('window switch')

                               

                                # print('wait completed')
                                # url_pattern = re.compile(r'window\.location\.href\s*=\s*"(https?://.*?)"')
                                # print('url pattern')

                                # print(sb.get_page_source())
                                # match = re.search(url_pattern, sb.get_page_source())
                                # print('is match')

                                # if match:
                                #     redirect_url = match.group(1)
                                #     print(f"Found redirect URL: {redirect_url}")

                                # sb.open(redirect_url)
                                 # Write the page source to the file
                                time.sleep(5)
                                # sb.wait_for_element(By.ID, "verifybtn", timeout=30)

                                with open("page_source.html", "w", encoding='utf-8') as file:
                                    file.write(sb.get_page_source())
                                publicEarnFormByPass(sb, 'verifybtn')
                                publicEarnFormByPass(sb, 'rtg-snp2')
                                publicEarnFormByPass(sb, 'rtg-snp2')
                                publicEarnFormByPass(sb, 'rtg-snp2')

                                time.sleep(10)
                                # sb.wait_for_element(By.TAG_NAME, "body", timeout=10)
                                # Using Selenium Base
                                continue_btn = sb.find_element(By.CSS_SELECTOR, 'a:has(button.secondary.larger)')
                                link = continue_btn.get_attribute('href')

                                sb.open(link)
                                print('open-link')
                                # sb.click("xpath=//a[normalize-space(text())='Click to view the file links']")

                                time.sleep(10)
                                rows = sb.find_elements(By.TAG_NAME , "tr")

                                print(rows , len(rows))

                                # List to store the links and their titles
                                link_list = []

                                # Iterate through each row to extract data
                                for row in rows:
                                    # Find the link in the second column
                                    try:
                                        link_element = row.find_element(By.CSS_SELECTOR,  "td[data-label='File Link'] a")

                                        # Get the href attribute of the link
                                        link = link_element.get_attribute("href")

                                        # Get the link provider title from the first column
                                        provider_title = row.find_element(By.CSS_SELECTOR, "td[data-label='Host'] img").get_attribute("alt")

                                        # Append the data to the list
                                        link_list.append((provider_title, link))
                                    except Exception as e:
                                        print(e)
                                

                                # Print the extracted links and titles
                                for provider_title, link in link_list:
                                    print(f"Provider: {provider_title}, Link: {link}")
                                


                                    # sb.uc_open_with_reconnect(sb.get_current_url(), 3)

                                    
                                # else:
                                #     print("NOT PUBLIC", link)

                    except Exception as e:
                        print("NO tag found")
        sb.input("Press Enter to close the browser...")
        sb.quit()


def publicEarnFormByPass(sb, id):
    """Bypass the form on the publicEarn site."""
    try:
        try:
            sb.execute_script(f"document.getElementById('SoumyaHelp-Ads').remove();")
            print('Ads remove successfully')
            sb.execute_script(f"document.getElementById('BR-Footer-Ads').remove();")
            print('Ads remove successfully')

        except Exception as eror:
            print(eror)
        sb.execute_script(f"document.getElementById('{id}').style.display = 'block';")
        continue_click = sb.find_element(By.ID , id)
        print('findit', continue_click.get_attribute('outerHTML'))
        try:

            continue_click.click()
        except Exception as er:
            print('eror', er)
        sb.wait_for_element("body", timeout=10)
        print(sb.get_current_url())
    except Exception as e:
        print('form is not found', id)


def test_proxy():
    """Check if the request was successful."""
    response = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': SCRAPOPS_API_KEY,
        },
    )
    if response.status_code == 200:
        proxy_data = response.json()
        print(proxy_data)  # This will print the list of proxies you can use
    else:
        print(f"Failed to retrieve proxies: {response.status_code}, {response.text}")


# Example usage
if __name__ == "__main__":
    main(link='https://tpxsub.com/', search="Demon Lord 2099", eps=1)
