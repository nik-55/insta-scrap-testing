"""
This file invokes a method that in turn call itself after a certain interval (default 30 minutes).
"""

import requests
from time import sleep
from bot.insta_bot.scrape_posts import ScrapePost

# Intialize the bot
bot = ScrapePost()


def run_bot_periodically(time_interval):
    usernames = requests.get("http://localhost:5000/all_clubs")
    usernames = usernames.json()
    usernames = usernames["clubs"]
    info = bot.getInfo(usernames=usernames)
    print(info)
    requests.post("http://localhost:5000/all_clubs_update", data=info)
    sleep(time_interval)
    run_bot_periodically(time_interval)


if __name__ == "__main__":
    # Time interval: 30 minutes
    run_bot_periodically(30 * 60)
