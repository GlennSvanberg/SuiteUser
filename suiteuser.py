import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import io
import requests


class User:
    def __init__(self, mgn, name, password):
        self.name = name
        self.mgn = mgn
        self.password = password


# Read Users
df = pd.read_csv('users.csv')
userStrings = list(df)
users = []
for u in userStrings:
    data = u.split(",")
    mgn = data[0]
    name = data[1]
    password = data[2]
    users.append(User(mgn, name, password))

ids = []


# Driver
driver = webdriver.Chrome("chromedriver.exe")
wait = WebDriverWait(driver, 10)

# Open Suite
url = 'https://suite.telefonihuset.se'
#url = 'http://localhost/suite'
driver.get(url)
driver.maximize_window()

# ssl
driver.find_element_by_id('details-button').click()
driver.find_element_by_id('proceed-link').click()

# Login
driver.find_element_by_id('user_name').send_keys("admin")
driver.find_element_by_id('user_password').send_keys("password")
driver.find_element_by_id('login_button').click()

# Admin page
men_menu = driver.find_element_by_id("globalLinks")
actions = ActionChains(driver)
actions.move_to_element(men_menu).perform()
wait.until(EC.visibility_of_element_located(
    (By.ID, "admin_link"))).click()

# Användarhantering
driver.find_element_by_id('user_management').click()
driver.find_element_by_id('create_link').click()

for user in users:
    # Fill fields
    driver.find_element_by_id('user_name').send_keys(user.mgn)
    driver.find_element_by_id('first_name').send_keys(user.mgn)
    driver.find_element_by_id('last_name').send_keys(user.name + ' (S)')
    driver.find_element_by_id('description').send_keys(
        user.mgn + " " + user.name + ' (S)')

    # Lösenord
    driver.find_element_by_id('tab2').click()
    driver.find_element_by_id('new_password').send_keys(user.password)
    driver.find_element_by_id('confirm_pwd').send_keys(user.password)
    driver.find_element_by_id('SAVE_FOOTER').click()

    # ID
    currentURL = driver.current_url
    id = currentURL.split("record=")[-1]
    id = id.split("&")[0]
    ids.append(id)

    # Säkerhetsgrupp
    driver.find_element_by_id('show_link_securitygroups').click()
    driver.find_element_by_id('securitygroups_users_select_button').click()
    driver.switch_to_window(driver.window_handles[1])
    driver.find_element_by_xpath("//a[text()='Abonnemang']").click()

    # Roller
    driver.switch_to_window(driver.window_handles[0])
    driver.find_element_by_xpath(
        "//form[@id='formacl_roles_users']/following-sibling::span").click()
    driver.find_element_by_id('acl_roles_users_select_button').click()
    driver.switch_to_window(driver.window_handles[1])
    driver.find_element_by_xpath("//a[text()='Säljare begränsad']").click()
    driver.switch_to_window(driver.window_handles[0])

    # Säkerhetsgrupp2
    driver.find_element_by_id('show_link_securitygroups').click()
    driver.find_element_by_id('securitygroups_users_select_button').click()
    driver.switch_to_window(driver.window_handles[1])
    driver.find_element_by_xpath("//a[text()='begränsad säljare']").click()
    driver.switch_to_window(driver.window_handles[0])

    # Admin page
    men_menu = driver.find_element_by_id("globalLinks")
    actions = ActionChains(driver)
    actions.move_to_element(men_menu).perform()
    wait = WebDriverWait(driver, 50)
    wait.until(EC.visibility_of_element_located(
        (By.ID, "admin_link"))).click()

    # Användarhantering
    driver.find_element_by_id('user_management').click()
    driver.find_element_by_id('create_link').click()

# Log out
men_menu = driver.find_element_by_id("globalLinks")
actions = ActionChains(driver)
actions.move_to_element(men_menu).perform()
wait = WebDriverWait(driver, 50)
wait.until(EC.visibility_of_element_located(
    (By.ID, "logout_link"))).click()

for user in users:
    # Login
    driver.find_element_by_id('user_name').send_keys(user.mgn)
    driver.find_element_by_id('user_password').send_keys(user.password)
    driver.find_element_by_id('login_button').click()

    driver.find_element_by_id('next_tab_personalinfo').click()
    driver.find_element_by_id('next_tab_locale').click()
    driver.find_element_by_xpath(
        "//select[@name='timezone']/option[text()='Europa/Stockholm (GMT+1:00)']").click()
    driver.find_element_by_id('next_tab_finish').click()
    driver.find_element_by_name('save').click()

    # Module menu filter
    driver.find_element_by_id('globalLinks').click()
    driver.find_element_by_id('tab4').click()
    driver.find_element_by_id('use_group_tabs').click()
    driver.find_element_by_xpath(
        "//select[@id='display_tabs']/option[text()='Produkter']").click()
    driver.find_element_by_id('chooser_display_tabs_left_to_right').click()
    driver.find_element_by_xpath(
        "//select[@id='display_tabs']/option[text()='Rapporter']").click()
    driver.find_element_by_id('chooser_display_tabs_left_to_right').click()
    driver.find_element_by_xpath(
        "//select[@id='display_tabs']/option[text()='Butiker']").click()
    driver.find_element_by_id('chooser_display_tabs_left_to_right').click()
    driver.find_element_by_xpath(
        "//select[@id='display_tabs']/option[text()='Operatörer']").click()
    driver.find_element_by_id('chooser_display_tabs_left_to_right').click()
    driver.find_element_by_xpath(
        "//select[@id='display_tabs']/option[text()='Lager']").click()
    driver.find_element_by_id('chooser_display_tabs_left_to_right').click()
    driver.find_element_by_id('SAVE_FOOTER').click()

    # Log out
    men_menu = driver.find_element_by_id("globalLinks")
    actions = ActionChains(driver)
    actions.move_to_element(men_menu).perform()
    wait.until(EC.visibility_of_element_located(
        (By.ID, "logout_link"))).click()

# SQL
for id in ids:
    print("ID: " + id)
content = "'YToyOntzOjg6ImRhc2hsZXRzIjthOjU6e3M6MzY6IjNlY2NmNTZhLTU4OGMtOTc2Ni0yYjMzLTVlMmU4MTExMTQ0OCI7YTo0OntzOjk6ImNsYXNzTmFtZSI7czoxNzoiQU9SUmVwb3J0c0Rhc2hsZXQiO3M6NjoibW9kdWxlIjtzOjExOiJBT1JfUmVwb3J0cyI7czo3OiJvcHRpb25zIjthOjI6e3M6MTI6ImRhc2hsZXRUaXRsZSI7czoxOToiRGFnZW5zIFRvcHBsaXN0YSBUQiI7czoxMzoiYW9yX3JlcG9ydF9pZCI7czozNjoiMjdkMTkyODYtZTI1NC1kNmE5LTk5MDEtNTlmMWY3MDlhM2Q0Ijt9czoxMjoiZmlsZUxvY2F0aW9uIjtzOjY4OiJtb2R1bGVzL0FPUl9SZXBvcnRzL0Rhc2hsZXRzL0FPUlJlcG9ydHNEYXNobGV0L0FPUlJlcG9ydHNEYXNobGV0LnBocCI7fXM6MzY6IjNiZTU1ZjkyLWQyODEtNGRmZi1hMDZhLTVlMmU4MWYzMzA2YiI7YTo0OntzOjk6ImNsYXNzTmFtZSI7czoxNzoiQU9SUmVwb3J0c0Rhc2hsZXQiO3M6NjoibW9kdWxlIjtzOjExOiJBT1JfUmVwb3J0cyI7czo3OiJvcHRpb25zIjthOjI6e3M6MTI6ImRhc2hsZXRUaXRsZSI7czoyMjoiTcOlbmFkZW5zIFRvcHBsaXN0YSBUQiI7czoxMzoiYW9yX3JlcG9ydF9pZCI7czozNjoiOWRmN2E0Y2ItZGZmNS1iOTg1LWJkZjgtNWE5YzRhNWVhN2QxIjt9czoxMjoiZmlsZUxvY2F0aW9uIjtzOjY4OiJtb2R1bGVzL0FPUl9SZXBvcnRzL0Rhc2hsZXRzL0FPUlJlcG9ydHNEYXNobGV0L0FPUlJlcG9ydHNEYXNobGV0LnBocCI7fXM6MzY6IjI4YWI5ZDUwLTAyMmYtOGE2Yy0zMjhjLTVlMmU4MTBiZWY1NyI7YTo0OntzOjk6ImNsYXNzTmFtZSI7czoxNzoiQU9SUmVwb3J0c0Rhc2hsZXQiO3M6NjoibW9kdWxlIjtzOjExOiJBT1JfUmVwb3J0cyI7czo3OiJvcHRpb25zIjthOjI6e3M6MTI6ImRhc2hsZXRUaXRsZSI7czoyNzoiTcOlbmFkc2Zha3R1cmVyaW5nIEFsbCBUaW1lIjtzOjEzOiJhb3JfcmVwb3J0X2lkIjtzOjM2OiI4MGQ4NTlhZi0xOTQ1LWYyMjQtMmJiZC01ZTFmNmJiZjRhMDQiO31zOjEyOiJmaWxlTG9jYXRpb24iO3M6Njg6Im1vZHVsZXMvQU9SX1JlcG9ydHMvRGFzaGxldHMvQU9SUmVwb3J0c0Rhc2hsZXQvQU9SUmVwb3J0c0Rhc2hsZXQucGhwIjt9czozNjoiMmQ4NmIyYjQtOGIwNC04ODdkLWVkOTEtNWUyZTgxNzQ4MTg1IjthOjQ6e3M6OToiY2xhc3NOYW1lIjtzOjEzOiJpRnJhbWVEYXNobGV0IjtzOjY6Im1vZHVsZSI7czo0OiJIb21lIjtzOjc6Im9wdGlvbnMiO2E6NDp7czo1OiJ0aXRsZSI7czo2OiJQb2RpdW0iO3M6MzoidXJsIjtzOjQ4OiJodHRwczovL3N1aXRlLnRlbGVmb25paHVzZXQuc2UvcG9kaXVtL3BvZGl1bS5waHAiO3M6NjoiaGVpZ2h0IjtpOjQwMDtzOjExOiJhdXRvUmVmcmVzaCI7czoyOiItMSI7fXM6MTI6ImZpbGVMb2NhdGlvbiI7czo1MzoibW9kdWxlcy9Ib21lL0Rhc2hsZXRzL2lGcmFtZURhc2hsZXQvaUZyYW1lRGFzaGxldC5waHAiO31zOjM2OiJiNDZkN2FmNi1jYjE0LWViZWEtMjlmMS01ZTJlODE3NmY1MzIiO2E6NDp7czo5OiJjbGFzc05hbWUiO3M6MTM6ImlGcmFtZURhc2hsZXQiO3M6NjoibW9kdWxlIjtzOjQ6IkhvbWUiO3M6Nzoib3B0aW9ucyI7YTo0OntzOjU6InRpdGxlIjtzOjM5OiJNw6Vsc8OkdHRuaW5nIDEuMDAwLjAwMGtyIGkgZmFrdHVyZXJpbmciO3M6MzoidXJsIjtzOjUyOiJodHRwczovL3N1aXRlLnRlbGVmb25paHVzZXQuc2UvcG9kaXVtL2J1ZGdldC9iYXIucGhwIjtzOjY6ImhlaWdodCI7aTozMTU7czoxMToiYXV0b1JlZnJlc2giO3M6MjoiLTEiO31zOjEyOiJmaWxlTG9jYXRpb24iO3M6NTM6Im1vZHVsZXMvSG9tZS9EYXNobGV0cy9pRnJhbWVEYXNobGV0L2lGcmFtZURhc2hsZXQucGhwIjt9fXM6NToicGFnZXMiO2E6MTp7aTowO2E6Mzp7czo3OiJjb2x1bW5zIjthOjI6e2k6MDthOjI6e3M6NToid2lkdGgiO3M6MzoiNjAlIjtzOjg6ImRhc2hsZXRzIjthOjI6e2k6MDtzOjM2OiIyZDg2YjJiNC04YjA0LTg4N2QtZWQ5MS01ZTJlODE3NDgxODUiO2k6MTtzOjM2OiIyOGFiOWQ1MC0wMjJmLThhNmMtMzI4Yy01ZTJlODEwYmVmNTciO319aToxO2E6Mjp7czo1OiJ3aWR0aCI7czozOiI0MCUiO3M6ODoiZGFzaGxldHMiO2E6Mzp7aTowO3M6MzY6ImI0NmQ3YWY2LWNiMTQtZWJlYS0yOWYxLTVlMmU4MTc2ZjUzMiI7aToxO3M6MzY6IjNlY2NmNTZhLTU4OGMtOTc2Ni0yYjMzLTVlMmU4MTExMTQ0OCI7aToyO3M6MzY6IjNiZTU1ZjkyLWQyODEtNGRmZi1hMDZhLTVlMmU4MWYzMzA2YiI7fX19czoxMDoibnVtQ29sdW1ucyI7czoxOiIzIjtzOjE0OiJwYWdlVGl0bGVMYWJlbCI7czoyMDoiTEJMX0hPTUVfUEFHRV8xX05BTUUiO319fQ=='"

idString = ""
count = 0
for id in ids:
    idString = idString + "'" + id + "', "
    count = count + 1
    if (count == len(ids)):
        idString = idString[:-2]
db = "`mobilegroup_se_suitecrm`"
sql = "UPDATE " + db + ".`user_preferences` SET `contents` = " + \
    content + " WHERE `user_preferences`.`assigned_user_id` IN (" + \
    idString + ") AND `user_preferences`.`category` = 'Home';"
print(sql)


# User 0
# driver.find_element_by_link_text(users[0]).click()

# Copy User
# driver.find_element_by_class_name('subnav').click()
# driver.find_element_by_id('duplicate_button').click()
# driver.find_element_by_id('admin_link').click()
