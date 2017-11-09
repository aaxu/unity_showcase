from flask import Flask, render_template, Markup
from random import randint
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

app = Flask(__name__)


@app.route("/")
def index():
    return "Index!"

@app.route("/random")
def random():
    """
    Can be accessed via localhost:5000/random. Displays a random game from
    https://unity3d.com/showcase/gallery/ and does not repeat until all games
    have been displayed once.
    """
    initial = time.time()
    driver = webdriver.PhantomJS(service_args=['--load-images=no'])
    driver.get("https://unity3d.com/showcase/gallery/")
    elem = driver.find_element_by_xpath('//*[@id="main-wrapper"]/div[5]/div/div')
    try:
        while elem:
            elem.click()
            time.sleep(0.1)
    except:
        pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    games = list(set(soup.select("li.game")))
    print "Number of games found:", len(games)
    xpath_beginning = '//*[@id="main-wrapper"]/div[4]/ul/li['
    game_number = randint(1, len(games))
    xpath_end = ']'
    xpath = xpath_beginning + str(game_number) + xpath_end
    driver.find_element_by_xpath(xpath).click()
    inner = driver.find_element_by_css_selector(".expanded").get_attribute('innerHTML')
    print "Time to load page:", time.time() - initial
    return render_template('template.html', html_body=Markup(inner))

if __name__ == "__main__":
    app.run(host='0.0.0.0')