# Test task for UI automation testing by selenium and pytest

Used technologies:

- PyTest
- Selenium WebDriver
- Selenium Grid
- Allure

## Requirements
- install Python 3.8 or above
- install PIP
> pip install webdriver-manager
pip install selenium
pip install allure-pytest
pip install pytest-html
pip install allure-python-commons
## Run autotests
> pytest -v --alluredir=./reports
## Generate reports
> allure serve ./reports