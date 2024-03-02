from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
from selenium.webdriver.edge.options import Options as EdgeOptions

options = EdgeOptions()
options.browser_version = 'latest'
options.platform_name = 'Windows 11'
sauce_options = {}
sauce_options['username'] = 'oauth-bradevansqa-ac17e'
sauce_options['accessKey'] = 'b5524a83-4ece-429a-9724-f8978f951e5a'
sauce_options['build'] = '<your build id>'
sauce_options['name'] = '<your test name>'
options.set_capability('sauce:options', sauce_options)

url = "https://oauth-bradevansqa-ac17e:b5524a83-4ece-429a-9724-f8978f951e5a@ondemand.us-west-1.saucelabs.com:443/wd/hub"
driver = webdriver.Remote(command_executor=url, options=options)



# Set options for not prompting DevTools information
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

print("testing started")
driver = webdriver.Chrome(options=options)

driver.get("https://www.saucedemo.com/")
sleep(3)

# Find element using element's id attribute
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

# Wait for the products to load
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "title")))

text = driver.find_element(By.CLASS_NAME, "title").text

# Check if login was successful
assert "products" in text.lower()
print("TEST PASSED : LOGIN SUCCESSFUL")

# Find and click on Add to Cart buttons
add_to_cart_btns = driver.find_elements(By.CLASS_NAME, "btn_inventory")
for btns in add_to_cart_btns[:3]:
    btns.click()

# Wait for the cart badge to update
WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "3"))

cart_value = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
assert "3" in cart_value.text
print("TEST PASSED : ADD TO CART", "\n")

# Remove items from cart
remove_btns = driver.find_elements(By.CLASS_NAME, "btn_inventory")
for btns in remove_btns[:2]:
    btns.click()

# Wait for the cart badge to update
WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1"))

assert "1" in cart_value.text
print("TEST PASSED : REMOVE FROM CART", "\n")

# Close the driver
driver.quit()


