import re
from eng import DataHandler, Spam


wgh_new_acounts_handler = DataHandler('serverdb/wgh_new_acounts.db')
wgh_new_acounts = wgh_new_acounts_handler.load_data("users")

generated_accounts_handler = DataHandler('localdb/generated_accounts.db')
generated_accounts = generated_accounts_handler.load_data("accounts")

data_handler = DataHandler('localdb/wgh_tickets_message.db')
long_tickets = data_handler.load_data("Long_issues")
short_tickets = data_handler.load_data("Short_issues")

spam = Spam()

# ALL RUN

# spam.bvn_all(wgh_new_acounts)
# spam.sms_all(wgh_new_acounts)
# spam.signup_all(generated_accounts, new_phone_numbers)
# spam.ticket_all(short_tickets, wgh_new_acounts)


# SINGLE RUN

# spam.signup_single('email', 'username', 'phone')
# spam.sms_bulk(any_phone_numbers, email, username)
# spam.ticket_single(short_tickets, username, email)


# THIS IS JUST RUNNING SINGLE TICKET TO CUSTOM EMAILS

phone_numbers = [(index, f"+234{str(i)}") for index, i in enumerate(range(7010000000, 7019999999))] # 10 million.
spam.sms_bulk(phone_numbers, 'sharonenoabasi17@gmail.com', 'sharonenoabasi17')


