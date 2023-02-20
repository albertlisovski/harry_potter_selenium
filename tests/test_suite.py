import csv
import allure
import pytest
from pages import Helper, SiteLocators

@allure.feature('Transactions module')
@pytest.mark.usefixtures("browser")
class TestSuite():
    def setup_method(self):
        self.main_page = Helper(self.driver)
    
    def tx_splitted(self):
        return []

    @allure.story('Test balance')
    def test_balance(self):
        # Input and submit deposit
        self.main_page.make_transaction(SiteLocators.LOCATOR_DEPOSIT_BUTTON, SiteLocators.LOCATOR_DEPOSIT_AMOUNT_FIELD, SiteLocators.LOCATOR_DEPOSIT_SUBMIT_BUTTON, self.main_page.amount)
        # Input and submit withdraw
        balance = self.main_page.make_transaction(SiteLocators.LOCATOR_WITHDRAWL_BUTTON, SiteLocators.LOCATOR_WITHDRAWL_AMOUNT_FIELD, SiteLocators.LOCATOR_WITHDRAWL_SUBMIT_BUTTON, self.main_page.amount)
        # Check balance
        assert balance == "0"
        print('Balance is 0')

    
    @allure.story('Test number of transactions')
    def test_transactions_number(self):
        # Check transactions
        transactions = self.main_page.get_transactions()
        setattr(TestSuite, 'tx_splitted', property(TestSuite.tx_splitted))
        TestSuite.tx_splitted = [tx.text.split() for tx in transactions]
        TestSuite.tx_splitted.pop(0) # Remove headers
        assert len(TestSuite.tx_splitted) == 2
        print('There are 2 transactions')
    
    @staticmethod
    def assert_transaction(transaction_list, amount, type):
        assert transaction_list[5] == amount
        assert transaction_list[6] == type

    @allure.story('Test content of transactions')
    def test_transactions(self):
        TestSuite.assert_transaction(TestSuite.tx_splitted[0], str(self.main_page.amount), "Credit")
        TestSuite.assert_transaction(TestSuite.tx_splitted[1], str(self.main_page.amount), "Debit")

    @staticmethod
    def test_create_report():
        # Format data for CSV
        for tx in TestSuite.tx_splitted:
            tx[0] = f"{tx[1][:-1]} {tx[0]} {tx[2]} {tx[3]}{tx[4]}"
            tx[1] = tx[5]
            tx[2] = tx[6]
            del tx[-4:]

        TestSuite.tx_splitted.insert(0, ['Дата-времяТранзакции', 'Сумма', 'ТипТранзакции'])

        # Write CSV file
        f_name = "out.csv"
        with open(f_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(TestSuite.tx_splitted)
        allure.attach.file(f_name, attachment_type=allure.attachment_type.CSV)
