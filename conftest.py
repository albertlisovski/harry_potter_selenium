import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Remote(options=webdriver.ChromeOptions())
    yield driver
    # Stop test
    driver.quit()
  