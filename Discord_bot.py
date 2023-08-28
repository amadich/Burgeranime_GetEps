import discord
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!geturl'):
        await message.channel.send("Please enter the anime episode URL:")

        def check(m):
            return m.channel == message.channel and m.author == message.author

        try:
            response = await client.wait_for('message', timeout=30.0, check=check)
            anime_url = response.content.strip()

            # Now use the anime_url with your Selenium function
            browser_choice = "chrome"  # You can set the default browser here
            episode_url = get_episode_url(anime_url, browser_choice)

            if episode_url:
                await message.channel.send(f"Episode URL 🎉 : {episode_url}")
            else:
                await message.channel.send("Episode URL extraction failed.")

        except asyncio.TimeoutError:
            await message.channel.send("Time limit exceeded. Please try again.")

bot_token = 'TOKEN'
client.run(bot_token)
