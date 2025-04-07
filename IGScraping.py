from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import json

import time

#Need to log into instagram :(
def log_in():
    # Go to Instagram login page
    driver.get("https://www.instagram.com/accounts/login/")

    #Wait for the page to load
    time.sleep(3)

    # Log in to Instagram (replace with your credentials)
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    #Hey! That's my username and password!
    username.send_keys("dhurg4")
    password.send_keys("blue-snake63")
    password.send_keys(Keys.RETURN)

    # Wait for login to complete
    time.sleep(5)



def get_post_data(tags):

    #List to store all caption data
    all_data = []
    
    for tag in tags:
        # Now you can navigate to any profile or hashtag page.
        driver.get('https://www.instagram.com/explore/tags/'+tag)

        # Give the page some time to load
        time.sleep(5)

        # Scroll down to load more posts
        for _ in range(3):  # Adjust range to control the number of scrolls
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(3)

        # Wait for the posts to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x9f619.xjbqb8w.x1lliihq.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1"))
        )

        # Scrape post content, basically the caption
        posts = driver.find_elements(By.CSS_SELECTOR, ".x9f619.xjbqb8w.x1lliihq.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1")

        i = 1
        for post in posts:
        
            try:
                # Click on each post to get more details
                post.click()
                time.sleep(2)

                # Wait for the caption to be visible
                caption_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "._ap3a._aaco._aacu._aacx._aad7._aade"))
                )
                
                caption = caption_element.text
                #print(f"Caption {i}, {caption}")
                all_data.append({
                    'number': i,
                    'caption': caption,
                })
                
                i = i + 1

            except StaleElementReferenceException:
                print("A post became stale, skipping...")

            except Exception as e:
                print(f"Error retrieving post caption: {e}")

            finally:
                # Close the post modal (click the "X" to close the post view)
                try:
                    close_button = driver.find_element(By.CSS_SELECTOR, ".x1lliihq.x1n2onr6.x9bdzbf")
                    close_button.click()
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Err or closing post modal: {e}")

        return all_data


def export_to_json(all_data, filename = "/Users/dhurgadharani/Fashion/data/IG_captions.json"):
    # Open the JSON file in write mode
    with open(filename, mode='w') as file:
        json.dump(all_data, file, indent=4, ensure_ascii=False)  # Write the data to the file


options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")  # Run headless for non-GUI environments
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

service = Service()

# Set up WebDriver
driver = webdriver.Chrome(service=service, options=options)

log_in()

#These are the tags we search, I'll add to it later!!!!
all_tags = ["fashiontrends", "2025fashion", "fashionweek", "pinterest", "moodboard"]

all_data = get_post_data(all_tags)

export_to_json(all_data)

print("Done!")



# Close the WebDriver
driver.quit()
