from flask import Flask, flash, redirect, render_template, request, session, abort, Markup
from random import randint
from selenium import webdriver

app = Flask(__name__)


@app.route("/")
def index():
    return "Index!"

@app.route("/random")
def random():
    driver = webdriver.PhantomJS()
    driver.get("https://unity3d.com/showcase/gallery/")
    xpath_beginning = '//*[@id="main-wrapper"]/div[4]/ul/li['

    # Should set 20 to some dynamic value that depends on the number of
    # actual games in the gallery. Can click button by finding xpath
    # '//*[@id="main-wrapper"]/div[5]/div/div' until it doesn't show up.
    game_number = randint(1, 20)
    xpath_end = ']'
    xpath = xpath_beginning + str(game_number) + xpath_end
    driver.find_element_by_xpath(xpath).click()
    inner = driver.find_element_by_css_selector(".expanded").get_attribute('innerHTML')
    return render_template('template.html', html_body=Markup(inner))


    # randomNumber = randint(0, len(quotes) - 1)
    # quote = quotes[randomNumber]
    # return render_template("template.html", **locals())
    # return "RANDOM"

# @app.route("/members/<string:name>/")
# def getMember(name):
#     return render_template('template.html', name=name)


if __name__ == "__main__":
    app.run(host='0.0.0.0')