import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def browser(request):
    driver = webdriver.Remote(options=webdriver.ChromeOptions())
    request.cls.driver = driver
    yield
    # Stop test
    driver.quit()
  