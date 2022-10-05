from time import sleep
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import sqlite3

username = os.getenv("SPOTIFY_USERNAME")
password = os.getenv("SPOTIFY_PASSWORD")

# connect to our sqlite db
connection = sqlite3.connect(r"C:\Users\frank\Desktop\Programming\Playlist Bot\song_db.db")
# get cursor to execute sql statements
cursor = connection.cursor()


class LoginPage:
    def __init__(self, browser):
        self.browser = browser

    def login(self, username, password):
        # enter email in the email box
        enter_email = self.browser.find_element("id", "login-username")
        enter_email.send_keys(username)
        sleep(2)
        # enter password
        enter_pass = self.browser.find_element("id", "login-password")
        enter_pass.send_keys(password)
        sleep(1)
        # click login button
        login_bnt = self.browser.find_element("class name", "Button-qlcn5g-0.frUdWl")
        login_bnt.click()
        sleep(5)
        return Spotify(self.browser)


# Landing page object classes
class HomePage:
    def __init__(self, browser):
        self.browser = browser

    def open_spotify(self):
        # open spotify
        self.browser.get("https://open.spotify.com/")
        sleep(2)
        # click 'Login button'
        login_btn = self.browser.find_element("class name", "Button-qlcn5g-0.gPMZVP")
        login_btn.click()
        return LoginPage(self.browser)


class Spotify:
    def __init__(self, browser):
        self.browser = browser

    def open_search(self):
        # click on search button
        search_btn = browser.find_element(
            "xpath", "/html/body/div[4]/div/div[2]/nav/div[1]/ul/li[2]/a"
        )
        search_btn.click()
        sleep(1)

    def add_songs(self, song):
        self.browser.refresh()
        search_field = browser.find_element(
            "class name", "Type__TypeElement-goli3j-0.cPwEdQ.QO9loc33XC50mMRUCIvf"
        )
        search_field.click()
        search_field.send_keys(song)
        search_field.send_keys(Keys.RETURN)
        sleep(2)
        # select song under songs
        song_option_menu = self.browser.find_element(
            "xpath",
            "/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/section[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/button[2]",
        )
        song_option_menu.click()
        a = ActionChains(self.browser)
        # identify element
        m = self.browser.find_element(By.XPATH, "/html/body/div[16]/div/ul/li[6]/button")
        # hover over element
        a.move_to_element(m).perform()
        # identify sub menu element
        n = self.browser.find_element(
            "xpath", "/html/body/div[16]/div/ul/li[6]/div/ul/div/li[3]"
        )
        # hover over element and click
        a.move_to_element(n).click().perform()
        search_field.clear()
        sleep(1)


browser = webdriver.Firefox()
browser.implicitly_wait(5)

home_page = HomePage(browser)
home_page.open_spotify()
login_page = LoginPage(browser)
login_page.login(username, password)
spotify = Spotify(browser)
spotify.open_search()


#Retrieve all songs in the db
sql = "SELECT Name, Flag FROM Song"
cursor.execute(sql)

songs = cursor.fetchall()

for song in songs:
    #add song on if the {Flag} is 0 ( 0 indicates song is not in playlist yet)
    if (song[1] == 0):
        spotify.add_songs(song[0])
        #update the {Flag} to indicate song has been added to playlist
        cursor.execute("UPDATE Song SET Flag = 1 WHERE Name = (?)", (song[0],))
        connection.commit()  
sleep(3)
browser.close()
