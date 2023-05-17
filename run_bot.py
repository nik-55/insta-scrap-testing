"""
This file invokes a method that in turn call itself after a certain interval (default 30 minutes).
"""

import requests
from time import sleep
from bot.insta_bot.scrape_posts import ScrapePost

# Intialize the bot
bot = ScrapePost()


def run_bot_periodically(time_interval):
    # GET request that returns the iitr club basic information (containing instagram username as well).
    usernames = requests.get("http://localhost:5000/all_clubs")
    usernames = usernames.json()
    usernames = usernames["clubs"]
    # Scrape the latest post if any from instagram
    info = bot.getInfo(usernames=usernames)
    # Make a POST request with the latest post in the body
    requests.post("http://localhost:5000/all_clubs_update", json={"clubs_info": info})
    # Pause the function for 30 minutes
    sleep(time_interval)
    # Again call the same function
    run_bot_periodically(time_interval)


if __name__ == "__main__":
    # Time interval: 30 minutes
    run_bot_periodically(30 * 60)
