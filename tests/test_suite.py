import csv
from datetime import datetime
import allure
from pages import Helper, SiteLocators

@allure.feature('Test deposit and withdraw.')
@allure.story('An user should be able to deposit some value then withdraw it. A balance should be\
             equal zero. Finally an user checks transactions, found his two transactions.')
def test_suite(browser):
    main_page = Helper(browser)
    tx_splitted = []

    def fib(num):
        a = 0
        b = 1
        for _i in range(0, num):
            yield a
            a, b = b, a + b
    
    # Calculate amount
    amount = list(fib(datetime.today().day + 1))[-1]

    @allure.step('Check Balance')
    def check_balance():
        # Input and submit deposit
        nonlocal amount
        main_page.make_transaction(SiteLocators.LOCATOR_DEPOSIT_BUTTON,
                                        SiteLocators.LOCATOR_DEPOSIT_AMOUNT_FIELD,
                                        SiteLocators.LOCATOR_DEPOSIT_SUBMIT_BUTTON, amount)
        # Input and submit withdraw
        balance = main_page.make_transaction(SiteLocators.LOCATOR_WITHDRAWL_BUTTON,
                                                    SiteLocators.LOCATOR_WITHDRAWL_AMOUNT_FIELD,
                                                    SiteLocators.LOCATOR_WITHDRAWL_SUBMIT_BUTTON,
                                                    amount)
        assert balance == "0"
    
    @allure.step('Check Transactions')
    def check_transactions():
        transactions = main_page.get_transactions()
        nonlocal tx_splitted
        tx_splitted = [tx.text.split() for tx in transactions]
        tx_splitted.pop(0) # Remove headers
        assert len(tx_splitted) == 2

        def assert_transaction(transaction_list, amount, type):
            assert transaction_list[5] == amount
            assert transaction_list[6] == type

        assert_transaction(tx_splitted[0], str(amount), "Credit")
        assert_transaction(tx_splitted[1], str(amount), "Debit")

    @allure.step('Create Report')
    def create_report():
        nonlocal tx_splitted
        for tx in tx_splitted:
            tx[0] = f"{tx[1][:-1]} {tx[0]} {tx[2]} {tx[3]}{tx[4]}"
            tx[1] = tx[5]
            tx[2] = tx[6]
            del tx[-4:]
        tx_splitted.insert(0, ['Дата-времяТранзакции', 'Сумма', 'ТипТранзакции'])
        # Write CSV file
        f_name = "out.csv"
        with open(f_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(tx_splitted)
        allure.attach.file(f_name, attachment_type=allure.attachment_type.CSV)

    check_balance()
    check_transactions()
    create_report()
