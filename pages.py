from datetime import datetime
from baseapp import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class SiteLocators:
    LOCATOR_LOGIN_TYPE_BUTTON = (By.XPATH, "//button[@ng-click='customer()']")
    LOCATOR_USER_NAME_ELEMENT = (By.ID, "userSelect")
    LOCATOR_LOGIN_BUTTON = (By.XPATH, "//button[@class='btn btn-default']")
    LOCATOR_DEPOSIT_BUTTON = (By.XPATH, "//button[@ng-click='deposit()']")
    LOCATOR_DEPOSIT_AMOUNT_FIELD = (By.XPATH, "//input[@ng-model='amount']")
    LOCATOR_DEPOSIT_SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    LOCATOR_WITHDRAWL_BUTTON = (By.XPATH, "//button[@ng-click='withdrawl()']")
    LOCATOR_WITHDRAWL_AMOUNT_FIELD = (By.XPATH, '//form[@ng-submit="withdrawl()"]/div/input')
    LOCATOR_WITHDRAWL_SUBMIT_BUTTON = (By.XPATH, '//form[@ng-submit="withdrawl()"]/button')
    LOCATOR_BALANCE_VALUE = (By.XPATH, '//div[@ng-hide="noAccount"]/strong[2]')
    LOCATOR_TRANSACTIONS_BUTTON = (By.XPATH, "//button[@ng-click='transactions()']")
    LOCATOR_TRANSACTIONS_ROWS = (By.CSS_SELECTOR, 'tr')

class Helper(BasePage):
    @staticmethod
    def fib(num):
        a = 0
        b = 1
        for _i in range(0, num):
            yield a
            a, b = b, a + b

    def __init__(self, driver):
        super().__init__(driver)
        # Open start page
        self.go_to_site()    
        # Calculate amount        
        self.amount = list(Helper.fib(datetime.today().day + 1))[-1]
        # Login as Harry Potter
        self.login('Harry Potter')        

    def login(self, login):
        login_type_button = self.find_element(SiteLocators.LOCATOR_LOGIN_TYPE_BUTTON)
        login_type_button.click()
        user_name_element = Select(self.find_element(SiteLocators.LOCATOR_USER_NAME_ELEMENT))
        user_name_element.select_by_visible_text(login)
        login_button = self.find_element(SiteLocators.LOCATOR_LOGIN_BUTTON)
        login_button.click()

    def make_transaction(self, operation_button_locator, amount_field_locator, submit_button_locator, amount):
        operation_button = self.find_element(operation_button_locator)
        operation_button.click()
        amount_field = self.find_element(amount_field_locator)
        amount_field.send_keys(amount)
        submit_button = self.find_element(submit_button_locator)
        submit_button.click()
        return self.find_element(SiteLocators.LOCATOR_BALANCE_VALUE).text
    
    def get_transactions(self):
        transaction_button = self.find_element(SiteLocators.LOCATOR_TRANSACTIONS_BUTTON)
        transaction_button.click()
        return self.find_elements(SiteLocators.LOCATOR_TRANSACTIONS_ROWS)
    