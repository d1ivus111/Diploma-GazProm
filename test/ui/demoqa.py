import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
driver.get('https://demoqa.com/automation-practice-form')
driver.maximize_window()


driver.find_element(By.ID, value='firstName').send_keys('qerliu')
driver.find_element(By.ID, value='lastName').send_keys('afuauhi')
driver.find_element(By.ID, value='userEmail').send_keys('test@test.com')
driver.find_element(By.ID, value='userNumber').send_keys('1828592830')
driver.find_element(By.ID, value='currentAddress').send_keys('ajwgaug')

driver.find_element(By.XPATH, value='(//*[@name="gender"])[1]').click()

dob_input = driver.find_element(By.ID, 'dateOfBirthInput')
dob_input.send_keys("04 May 2026")
dob_input.send_keys(Keys.ENTER)

dob_input = driver.find_element(By.ID, 'subjectsInput')
dob_input.send_keys("maths")
dob_input.send_keys(Keys.ENTER)

driver.find_element(By.ID, value='react-select-3-input').send_keys("NCR", Keys.ENTER)
driver.find_element(By.ID, value='react-select-4-input').send_keys("Noida", Keys.ENTER)
time.sleep(5)

driver.find_element(By.ID, 'submit').click()
time.sleep(5)

table_text = driver.find_element(By.CLASS_NAME, "modal-body").text

assert "qerliu afuauhi" in table_text
assert "test@test.com" in table_text
assert "1828592830" in table_text
assert "ajwgaug" in table_text
assert "NCR Noida" in table_text
assert "04 May,2026" in table_text
assert "Male" in table_text
assert "Male" in table_text
assert "Maths" in table_text


print("данные указаны верно.")

driver.quit()
