import csv
import time
import allure
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

@pytest.fixture(scope="class")
def driver_init(request):
    driver = webdriver.Remote(options=webdriver.ChromeOptions())
    # Calculate amount
    def fib(num):
        a = 0
        b = 1
        for _i in range(0, num):
            yield a
            a, b = b, a + b

    amount = list(fib(datetime.today().day + 1))[-1]
    # Open start page
    driver.get('https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login')
    time.sleep(1)
    # Log in
    driver.find_element(By.XPATH, "//button[@ng-click='customer()']").click()
    time.sleep(1)
    user_name_element = Select(driver.find_element(By.ID, "userSelect"))
    user_name_element.select_by_visible_text('Harry Potter')
    driver.find_element(By.XPATH, "//button[@class='btn btn-default']").click()
    time.sleep(1)
    request.cls.driver = driver
    request.cls.amount = amount
    yield
    # Stop test
    driver.quit()
    

@allure.feature('Transactions module')
@pytest.mark.usefixtures("driver_init")
class TestTransactions():
    def make_transaction(self, operation_button_xpath, amount_field_xpath, submit_button_xpath):
        self.driver.find_element(By.XPATH, operation_button_xpath).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, amount_field_xpath).send_keys(self.amount)
        self.driver.find_element(By.XPATH, submit_button_xpath).click()

    @allure.story('Test balance')
    def test_balance(self):
        # Input and submit deposit
        self.make_transaction("//button[@ng-click='deposit()']", "//input[@ng-model='amount']", "//button[@type='submit']")
        # Input and submit withdraw
        self.make_transaction("//button[@ng-click='withdrawl()']", '//form[@ng-submit="withdrawl()"]/div/input', '//form[@ng-submit="withdrawl()"]/button') 
        # Check balance
        balance = self.driver.find_element(By.XPATH, '//div[@ng-hide="noAccount"]/strong[2]').text
        assert balance == "0"
        print('Balance is 0')
        time.sleep(1)
    
    def tx_splitted(self):
        return []
    
    @allure.story('Test number of transactions')
    def test_transactions_number(self):
        # Check transactions
        self.driver.find_element(By.XPATH, "//button[@ng-click='transactions()']").click()
        time.sleep(1)
        transactions = self.driver.find_elements(By.CSS_SELECTOR, 'tr')
        setattr(TestTransactions, 'tx_splitted', property(TestTransactions.tx_splitted))
        TestTransactions.tx_splitted = [tx.text.split() for tx in transactions]
        TestTransactions.tx_splitted.pop(0) # Remove headers
        assert len(TestTransactions.tx_splitted) == 2
        print('There are 2 transactions')
    
    @staticmethod
    def assert_transaction(transaction_list, amount, type):
        assert transaction_list[5] == amount
        assert transaction_list[6] == type

    @allure.story('Test content of transactions')
    def test_transactions(self):
        TestTransactions.assert_transaction(TestTransactions.tx_splitted[0], str(self.amount), "Credit")
        TestTransactions.assert_transaction(TestTransactions.tx_splitted[1], str(self.amount), "Debit")
    
    @staticmethod
    def test_create_report():
        # Format data for CSV
        for tx in TestTransactions.tx_splitted:
            tx[0] = f"{tx[1][:-1]} {tx[0]} {tx[2]} {tx[3]}{tx[4]}"
            tx[1] = tx[5]
            tx[2] = tx[6]
            del tx[-4:]

        TestTransactions.tx_splitted.insert(0, ['Дата-времяТранзакции', 'Сумма', 'ТипТранзакции'])

        # Write CSV file
        f_name = "out.csv"
        with open(f_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(TestTransactions.tx_splitted)
        allure.attach.file(f_name, attachment_type=allure.attachment_type.CSV)
