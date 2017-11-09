from flask import Flask, render_template, Markup
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random

app = Flask(__name__)
games_found = 0
driver = webdriver.PhantomJS(service_args=['--load-images=no'])
visited = set()
cached_html = {}

@app.route("/")
def index():
    return "Index!"

@app.route("/random")
def random_game():
    """
    Can be accessed via localhost:5000/random. Displays a random game from
    https://unity3d.com/showcase/gallery/ and does not repeat until all games
    have been displayed once.
    """

    initial = time.time()
    global driver
    global games_found
    global cached_html
    # Cache games and reload the page if we found less than 77 games.
    if games_found < 77:
        driver.get("https://unity3d.com/showcase/gallery/")
        elem = driver.find_element_by_xpath('//*[@id="main-wrapper"]/div[5]/div/div')
        try:
            while elem:
                elem.click()
                time.sleep(0.1)
        except:
            pass
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        games_found = len(soup.select("li.game"))
        print "Number of games found:", games_found
    games_to_visit = set(range(1, games_found + 1))
    random_game_number = get_random_game(games_to_visit)
    if random_game_number in cached_html:
        inner = cached_html[random_game_number]
    else:
        xpath = get_game_xpath(random_game_number)
        driver.find_element_by_xpath(xpath).click()
        inner = Markup(driver.find_element_by_css_selector(".expanded").get_attribute('innerHTML'))
        cached_html[random_game_number] = inner
    print "Time to load page:", time.time() - initial
    return render_template('template.html', html_body=inner)

def get_random_game(possible_game_numbers):
    """
    Given the possible game numbers, return one that has not yet been visited.
    If we have visited all possible game numbers, reset the visited set.

    Args:
        possible_game_numbers (int): A set containing all possible game numbers.

    Returns:
        A random game number that has not yet been visited
    """
    global visited
    not_visited = tuple((possible_game_numbers - visited))
    if not not_visited:
        visited = set()
        not_visited = tuple((possible_game_numbers - visited))
    random_game_number = random.choice(not_visited)
    visited.add(random_game_number)
    return random_game_number

def get_game_xpath(game_number):
    """
    Given a game number, return the corresponding xpath string found on the
    Unity website.

    Args:
        game_number (int): The game number that you want the xpath of.

    Returns:
        A string representing the xpath of the game element.
    """
    xpath_beginning = '//*[@id="main-wrapper"]/div[4]/ul/li['
    xpath_end = ']'
    return xpath_beginning + str(game_number) + xpath_end

if __name__ == "__main__":
    app.run(host='0.0.0.0')