from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time

PATH = "C:/Users/Jan/PycharmProjects/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

regions = {"euw1": "https://www.leagueofgraphs.com/pl/rankings/summoners/euw/page-",
           "na1": "https://www.leagueofgraphs.com/pl/rankings/summoners/na/page-",
           "kr": "https://www.leagueofgraphs.com/pl/rankings/summoners/kr/page-",
           "br1": "https://www.leagueofgraphs.com/pl/rankings/summoners/br/page-",
           "eun1": "https://www.leagueofgraphs.com/pl/rankings/summoners/eune/page-",
           "jp1": "https://www.leagueofgraphs.com/pl/rankings/summoners/jp/page-",
           "la1": "https://www.leagueofgraphs.com/pl/rankings/summoners/lan/page-",
           "la2": "https://www.leagueofgraphs.com/pl/rankings/summoners/las/page-",
           "oce1": "https://www.leagueofgraphs.com/pl/rankings/summoners/oce/page-",
           "ru": "https://www.leagueofgraphs.com/pl/rankings/summoners/ru/page-",
           "tr1": "https://www.leagueofgraphs.com/pl/rankings/summoners/tr/page-"
           }


def scrape_reviews_from_single_site(url, page):
    driver.get(url + str(page))
    names = []

    try:
        names = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "name"))
        )
    except:
        pass

    return [name.text for name in names]


def insert_player_into_db(player):
    conn = sqlite3.connect('lol.db')
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO PLAYERS
                    VALUES (?, ?)
                    """, player)

    conn.commit()
    conn.close()


def job():
    for page in range(1, 50):
        time.sleep(10)
        for region, url in regions.items():
            time.sleep(1)
            names = scrape_reviews_from_single_site(url, page)
            for name in names:
                insert_player_into_db((name, region))


job()
