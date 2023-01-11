import unittest
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from app import models, utilities
"""
Set-up
https://selenium-python.readthedocs.io/getting-started.html

Screenshots
https://pythonbasics.org/selenium-screenshot/

Locating elements
https://selenium-python.readthedocs.io/locating-elements.html

Notes
The driver renders the webpage.
The driver object can be queried to find elements on the webpage.
Once a component of the webpage is found it can also be queried.
Input elements can also use the sendKeys() method to have data sent to them.
"""


class UiTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path='/home/jake/Leeds/SEP/cinema/tests/geckodriver')
        self.homepage = "http://0.0.0.0:5000/"
        self.login = self.homepage + "login"
        self.basket = self.homepage + "basket"
        self.account = self.homepage + "account"
        self.bookings = self.homepage + "bookings"
        self.register = self.homepage + "register"

    def tearDown(self):
        self.driver.close()

    # --------------- NAVBAR ----------------
    def check_logo_exists(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            logo = driver.find_element_by_id('navbar-title')
            return True
        except NoSuchElementException:
            return False

    def check_basket_exists(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            logo = driver.find_element_by_id('navbar-basket')
            return True
        except NoSuchElementException:
            return False

    def check_colour_dropdown_light_exists(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            logo = driver.find_element_by_id('navbar-colour-dropdown-light')
            return True
        except NoSuchElementException:
            return False

    def check_colour_dropdown_dark_exists(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            logo = driver.find_element_by_id('navbar-colour-dropdown-dark')
            return True
        except NoSuchElementException:
            return False

    def check_colour_dropdown_high_contrast_exists(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            logo = driver.find_element_by_id('navbar-colour-dropdown-high-contrast')
            return True
        except NoSuchElementException:
            return False

    def check_colour_dropdown_exists(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            logo = driver.find_element_by_id('navbar-colour-dropdown')
            light = self.check_colour_dropdown_light_exists()
            dark = self.check_colour_dropdown_dark_exists()
            high = self.check_colour_dropdown_high_contrast_exists()
            if light and dark and high:
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def check_account_exists(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            account = driver.find_element_by_id('navbar-account')
            return True
        except NoSuchElementException:
            return False

    def check_bookings_exists(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            account = driver.find_element_by_id('navbar-bookings')
            return True
        except NoSuchElementException:
            return False

    def check_login_button_exists(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            account = driver.find_element_by_id('navbar-login')
            return True
        except NoSuchElementException:
            return False

    def login_with_form(self):
        driver = self.driver
        driver.get(self.login)
        email_to_use = "sc19jcrk@leeds.ac.uk"
        password_to_use = "JJpeter"
        email = driver.find_element_by_id("email")
        password = driver.find_element_by_id("password")
        login = driver.find_element_by_id("submit")
        email.send_keys(email_to_use)
        password.send_keys(password_to_use)
        login.click()
        if driver.title == "Home - Dadpad Cinema":
            return True
        else:
            return False

    def navbar_logo_link(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            if driver.find_element_by_id("navbar-title").get_attribute('href') == self.homepage:
                return True
            return False
        except NoSuchElementException:
            return False

    def navbar_basket_link(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            if driver.find_element_by_id("navbar-basket").get_attribute('href') == self.basket:
                return True
            return False
        except NoSuchElementException:
            return False

    def navbar_login_link(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            if driver.find_element_by_id("navbar-login").get_attribute('href') == self.login:
                return True
            return False
        except NoSuchElementException:
            return False

    def navbar_bookings_link(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            if driver.find_element_by_id("navbar-bookings").get_attribute('href') == self.bookings:
                return True
            return False
        except NoSuchElementException:
            return False

    def navbar_account_link(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            if driver.find_element_by_id("navbar-account").get_attribute('href') == self.account:
                return True
            return False
        except NoSuchElementException:
            return False

    def check_light_mode(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            colour_dropdown = driver.find_element_by_id('navbar-colour-dropdown')
            colour_dropdown.click()
            light = driver.find_element_by_id("navbar-colour-dropdown-light")
            light.click()
            navbar_light = driver.find_element_by_css_selector('nav.navbar-light')
            bg_light = driver.find_element_by_css_selector('nav.bg-light')
            text_dark = driver.find_element_by_css_selector('nav.text-dark')
            body_bg_light = driver.find_element_by_css_selector('body.bg-light')
            body_text_black = driver.find_element_by_css_selector('body.text-black')
            return True
        except NoSuchElementException:
            return False

    def check_dark_mode(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            colour_dropdown = driver.find_element_by_id('navbar-colour-dropdown')
            colour_dropdown.click()
            dark = driver.find_element_by_id("navbar-colour-dropdown-dark")
            dark.click()
            navbar_dark = driver.find_element_by_css_selector('nav.navbar-dark')
            bg_dark = driver.find_element_by_css_selector('nav.bg-dark')
            text_light = driver.find_element_by_css_selector('nav.text-light')
            body_bg_dark = driver.find_element_by_css_selector('body.bg-dark')
            body_text_white = driver.find_element_by_css_selector('body.text-white')
            return True
        except NoSuchElementException:
            return False

    def check_high_contrast_mode(self):
        driver = self.driver
        driver.get(self.homepage)
        try:
            colour_dropdown = driver.find_element_by_id('navbar-colour-dropdown')
            colour_dropdown.click()
            high_contrast = driver.find_element_by_id("navbar-colour-dropdown-high-contrast")
            high_contrast.click()
            navbar_primary = driver.find_element_by_css_selector('nav.navbar-primary')
            bg_primary = driver.find_element_by_css_selector('nav.bg-primary')
            text_warning = driver.find_element_by_css_selector('nav.text-warning')
            body_bg_primary = driver.find_element_by_css_selector('body.bg-primary')
            body_text_warning = driver.find_element_by_css_selector('body.text-warning')
            return True
        except NoSuchElementException:
            return False

    # def test_check_navbar_logged_out(self):
    #     logo = self.check_logo_exists()
    #     basket = self.check_basket_exists()
    #     colour_dropdown = self.check_colour_dropdown_exists()
    #     account = self.check_account_exists()
    #     bookings = self.check_bookings_exists()
    #     login = self.check_login_button_exists()
    #     self.assertTrue(logo and basket and colour_dropdown and not account and not bookings and login)
    #
    # def test_check_navbar_logged_in(self):
    #     login = self.login_with_form()
    #     login_button = self.check_login_button_exists()
    #     logo = self.check_logo_exists()
    #     basket = self.check_basket_exists()
    #     colour_dropdown = self.check_colour_dropdown_exists()
    #     account = self.check_account_exists()
    #     bookings = self.check_bookings_exists()
    #
    #     self.assertTrue(login and not login_button and logo and basket and colour_dropdown and account and bookings)
    #
    # def test_navbar_links(self):
    #     logo = self.navbar_logo_link()
    #     basket = self.navbar_basket_link()
    #     login = self.navbar_basket_link()
    #     login_attempt = self.login_with_form()
    #     bookings = self.navbar_bookings_link()
    #     account = self.navbar_account_link()
    #     self.assertTrue(logo and basket and login and bookings and account)
    #
    # def test_theming(self):
    #     light = self.check_light_mode()
    #     dark = self.check_dark_mode()
    #     high_contrast = self.check_high_contrast_mode()
    #     self.assertTrue(light and dark and high_contrast)
    #
    # # -------------------- HOMEPAGE ------------------
    # def test_home_all_movies_display(self):
    #     driver = self.driver
    #     driver.get(self.homepage)
    #     movies = models.Movie.get_all_active()
    #     for movie in movies:
    #         try:
    #             movie_poster = driver.find_element_by_id('movie-col-' + str(movie.id))
    #         except NoSuchElementException:
    #             self.assertFalse(True)
    #
    #     self.assertTrue(True)
    #
    # def test_home_carousel(self):
    #     driver = self.driver
    #     driver.get(self.homepage)
    #     # get the movies rendered on the carousel
    #     carousel_movies = utilities.get_carousel_movies()
    #     # check each one is rendered
    #     try:
    #         next = driver.find_element_by_id('carousel-next')
    #         prev = driver.find_element_by_id('carousel-prev')
    #         # go forwards through the carousel, checking that the correct movie is active when next is clicked
    #         for i in range(len(carousel_movies)):
    #             # check the element rendered correctly
    #             carousel_movie = driver.find_element_by_id('carousel-' + str(carousel_movies[i].id))
    #             # check if the element is active
    #             if carousel_movie.get_attribute("class") != "carousel-item active":
    #                 self.assertFalse(True)
    #             # click the next button
    #             if i != len(carousel_movies) - 1:
    #                 next.click()
    #             # wait so the transition can complete
    #             time.sleep(0.5)
    #         # now go backwards, checking the correct movie is active when prev is clicked
    #         for i in range(len(carousel_movies)-1, -1, -1):
    #             # check the element rendered correctly
    #             carousel_movie = driver.find_element_by_id('carousel-' + str(carousel_movies[i].id))
    #             # check if the element is active
    #             if carousel_movie.get_attribute("class") != "carousel-item active":
    #                 self.assertFalse(True)
    #             # click the next button
    #             prev.click()
    #             # wait so the transition can complete
    #             time.sleep(0.5)
    #     except NoSuchElementException:
    #         print("Couldn't find the element")
    #         self.assertFalse(True)
    #     self.assertTrue(True)

    def test_home_search(self):
        driver = self.driver
        driver.get(self.homepage)
        movies = models.Movie.get_all_active()
        try:
            search = driver.find_element_by_id('movie-search')
            i=0
            for movie in movies:
                title = ""
                for char in movie.title:
                    title += char
                    search.send_keys(title)
                    movie_poster = driver.find_element_by_id('movie-col-' + str(movie.id))
                    print("isDisplayed:"+str(movie_poster.is_displayed()))
                    print("poster:"+str(movie_poster))
                    if not movie_poster.is_displayed():
                        self.assertFalse(True)
                search.clear()

                if i < 3:
                    for keyword in movie.keywords:
                        term = ""
                        for char in keyword.name:
                            term += char
                            search.send_keys(term)
                            movie_poster = driver.find_element_by_id('movie-col-' + str(movie.id))
                            if not movie_poster.is_displayed():
                                self.assertFalse(True)
                            search.clear()
                        search.clear()
                i+=1
        except NoSuchElementException:
            self.assertFalse(True)

        self.assertTrue(True)


if __name__=="__main__":
    unittest.main()
