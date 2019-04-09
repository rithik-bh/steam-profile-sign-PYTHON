from selenium import webdriver
from time import sleep
from datetime import date
import os

has_steam_authenticator = 1


def login(account_name, password, steam_auth_code, has_steam_authenticator):
    driver.get("https://store.steampowered.com/login/")
    sleep(1.5)

    driver.find_element_by_css_selector("#input_username").click()
    driver.find_element_by_css_selector("#input_username").clear()
    driver.find_element_by_css_selector(
        "#input_username").send_keys(account_name)

    driver.find_element_by_css_selector("#input_password").click()
    driver.find_element_by_css_selector("#input_password").clear()
    driver.find_element_by_css_selector("#input_password").send_keys(password)

    driver.find_element_by_xpath("//button[@type='submit']").click()
    sleep(3.25)

    if has_steam_authenticator:
        driver.find_element_by_xpath(
            "//input[@id='twofactorcode_entry']").click()
        driver.find_element_by_xpath(
            "//input[@id='twofactorcode_entry']").send_keys(steam_auth_code)
        driver.find_element_by_xpath("//div[@type='submit']").click()
        sleep(5.5)


def get_signing_id():

    signing_id = []
    print(
        "\nEnter ID's or Links To Sign Profiles(Maximum 10) .. [Enter -1 to exit] :")

    for x in range(0, 10):
        id = input(
            f"{x+1}. Enter Profile Link For Account {x+1} [-1 to stop] : ")
        if id == "-1":
            break

        signing_id.append(id)

    return signing_id


def sign_id(signing_id, comment, f):
    successful_signs = 0
    name = ""
    for x in range(0, len(signing_id)):
        driver.get(signing_id[x])
        sleep(2)

        name = driver.find_element_by_xpath(
            "//span[@class='actual_persona_name']").text

        sleep(1)

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)
        try:
            driver.find_element_by_xpath(
                "//textarea[@placeholder='Add a comment']").click()
            driver.find_element_by_xpath(
                "//textarea[@placeholder='Add a comment']").send_keys(comment)
            sleep(0.75)
            driver.find_element_by_xpath(
                "//span[@class='btn_green_white_innerfade btn_small']").click()
            sleep(1)
            print(
                f"{x+1}. Successfully Signed Profile Named : '{name}'")
            f.write(
                f"{x+1}. Successfully Signed Profile Named : '{name}' [{signing_id[x]}]\n")
            successful_signs = successful_signs+1
        except:
            print(
                f"{x+1}. Error Occured While Signing Profile Named : '{name}'")
            f.write(
                f"{x+1}. Error Occured While Signing Profile Named : '{name}' [{signing_id[x]}]\n")

    return successful_signs


account_name = input("Enter Account Name [ID] : ")
password = input("Enter Password : ")
comment = input("Enter Comment : ")

steam_auth_code = ""

signing_id = get_signing_id()

temp_char = input(
    "\nDo You Have Steam Mobile Authenticator enabled ? (Y / N) : ")

if temp_char.lower() == 'n':
    has_steam_authenticator = 0

if has_steam_authenticator:
    print(
        "\nWAIT FOR THE STEAM AUTHENTICATOR CODE TO REFRESH AND THEN ENTER THE CODE !")
    steam_auth_code = input("Enter Steam Mobile Authenticator Code : ")

driver = webdriver.Chrome("chromedriver.exe")

login(account_name, password, steam_auth_code, has_steam_authenticator)

sleep(2)

today = date.today()
date = today.strftime("%d %B %Y")

f = open(f"C:\\Users\\{os.getlogin()}\\Desktop\\Steam Profile Sign.txt", "a")

f.write("============================================\n")
f.write(f"           DATE :  {date}                  \n")
f.write("============================================\n\n")

print(
    f"\nStarting signing {len(signing_id)} Profile(s) Now ... \n\nSTATUS HERE : \n")
f.write(
    f'Starting signing {len(signing_id)} Profile(s) Now ... \n\nCommenting : "{comment}"\n\nSTATUS HERE : \n\n')

successful_signs = sign_id(signing_id, comment, f)
print(
    f"\nProfiles Successfully Signed : {successful_signs}\nProfiles Failed To Sign : {len(signing_id)-successful_signs}\n\n")

f.write(
    f"\n\nProfiles Successfully Signed : {successful_signs}\nProfiles Failed To Sign : {len(signing_id)-successful_signs}\n\n")

print("\n\n================================================================")
print(f"Check FILE NAMED : 'Steam Profile Sign' on Desktop for Status !")
print("================================================================")
driver.close()
