# -*- coding: utf-8 -*-
"""
pip install bs4
pip install cloudscraper
"""
import cloudscraper
from bs4 import BeautifulSoup


def re_active_user(name):
    scraper = cloudscraper.create_scraper(browser='chrome')
    resp = scraper.get("https://3ups.xyz/reActiveUser?username=%s" % name)
    if resp.status_code == 200:
        print("get web page successfully.")
    soup = BeautifulSoup(resp.text, "html.parser")
    token = soup.find(attrs={"name": "_token"})["value"]

    resp = scraper.post("https://3ups.xyz/reActiveUser", data={"username": name, "_token": token})
    soup = BeautifulSoup(resp.text, "html.parser")
    result = soup.find(name="div", attrs={"class": "alert"}).find_next().text
    print("result: %s" % result)


if __name__ == "__main__":
    re_active_user("1562024895@qq.com")
