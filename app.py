from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_episode_url(anime_url, browser_choice):
    if browser_choice == "chrome":
        driver = webdriver.Chrome()
    elif browser_choice == "firefox":
        driver = webdriver.Firefox()
    elif browser_choice == "edge":
        driver = webdriver.Edge()  # Use Edge WebDriver
    else:
        print("Unsupported browser choice")
        return None

    driver.get(anime_url)

    try:
        # Wait for the iframe to be visible
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe[src^="https://ok.ru/videoembed/"], iframe[src^="https://www.animeiat.xyz/player/"]'))
        )

        # Find the iframe element after it's visible
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[src^="https://ok.ru/videoembed/"], iframe[src^="https://www.animeiat.xyz/player/"]')

        # Get the value of the src attribute
        episode_url = iframe.get_attribute('src')

        return episode_url

    finally:
        driver.quit()

def main():
    anime_url = input("Enter the anime episode URL: ")
    browser_choice = input("Enter your browser choice (chrome/firefox/edge): ").lower()

    episode_url = get_episode_url(anime_url, browser_choice)

    if episode_url:
        print("Episode URL 🎉 :", episode_url)
    else:
        print("Episode URL extraction failed.")

if __name__ == "__main__":
    main()

input("Press ENTER to Exit ...")
