from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://books.toscrape.com/")
print("Title:", driver.title)
driver.quit()
