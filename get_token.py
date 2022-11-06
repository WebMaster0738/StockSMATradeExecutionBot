from tda import auth, client
import json
import config

try:
    c = auth.client_from_token_file('C:/Users/admin/PycharmProjects/pythonProject5/token.pickle', 'AARYPZGHY9QGXQ3RBIEHFRG6XL5LETH4')
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path='C:/Users/admin/PycharmProjects/pythonProject5/chromedriver.exe') as driver:
        c = auth.client_from_login_flow(
            driver, 'AARYPZGHY9QGXQ3RBIEHFRG6XL5LETH4', 'http://localhost/test', 'C:/Users/admin/PycharmProjects/pythonProject5/token.pickle')
