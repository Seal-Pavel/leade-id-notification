# import time
# from config.config import (
#     BROWSER_LOGIN,
#     NOVNC_PASSWORD,
#     BROWSER_HOST,
#     BROWSER_PORT
# )
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# remote_url = f'http://{BROWSER_LOGIN}:{NOVNC_PASSWORD}@{BROWSER_HOST}:{BROWSER_PORT}/wd/hub'
#
# options = webdriver.ChromeOptions()
# options.set_capability('pageLoadStrategy', 'eager')
# options.add_argument('--disable-gpu')
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--no-sandbox")
# options.add_argument("--headless")
#
# templates = {
#     1: 'Отбивка несовершеннолетнему',
#     2: 'Неверная дата рождения',
# }
#
#
# class Usedesk:
#     def __init__(self, employee_name, email, password):
#         self.driver = webdriver.Remote(command_executor=remote_url, options=options)
#         self.name = employee_name
#         self.email = email
#         self.password = password
#         self._authorization()
#
#     def _focus_on_element(self, search_by, value):
#         wait = WebDriverWait(self.driver, 10)
#         retries = 5
#         while True:
#             try:
#                 time.sleep(1)
#                 element = wait.until(EC.presence_of_element_located((search_by, value)))
#                 time.sleep(1)
#                 self.driver.execute_script("arguments[0].scrollIntoView();", element)
#                 time.sleep(1)
#                 element = wait.until(EC.element_to_be_clickable((search_by, value)))
#                 time.sleep(1)
#                 return element
#             except Exception as exc:
#                 if retries == 0:
#                     raise exc
#                 retries -= 1
#                 time.sleep(5)
#
#     def _authorization(self):
#         print(f'[*] Usedesk authorization START for {self.name} {self.email} {self.password[:4]}...')
#         self.driver.get("https://secure.usedesk.ru/login")
#         login_el = self._focus_on_element(By.NAME, "login")
#         login_el.send_keys(self.email)
#         password_el = self._focus_on_element(By.NAME, "password")
#         password_el.send_keys(self.password)
#         enter_button_el = self._focus_on_element(By.TAG_NAME, "button")
#         enter_button_el.click()
#         time.sleep(5)
#         print('[+] Usedesk authorization END')
#
#     def send_answer_by_template(self, ticket_id, template_num):
#         try:
#             print(f'[*] Ticket: https://secure.usedesk.ru/tickets/{ticket_id}')
#             self.driver.get(f'https://secure.usedesk.ru/tickets/{ticket_id}')
#             time.sleep(1)
#
#             template_selection = self._focus_on_element(By.XPATH, '//*[@id="redactor-toolbar-0"]/li[18]/a/i')
#             template_selection.click()
#             print('[+] template_selection.click')
#
#             template = self._focus_on_element(By.XPATH, f'//*[@id="macros-autocomplete"]/ul[1]/li[{template_num}]')
#             assert templates[template_num] == template.text
#             template.click()
#             print('[+] template.click')
#
#             send_button = self._focus_on_element(By.NAME, 'send_as_public')
#             send_button.click()
#             print('[+] send_button.click')
#
#             time.sleep(5)
#             self.driver.quit()
#             print('[+] Send answer by template')
#
#         except Exception as e:
#             self.driver.quit()
#             raise e
