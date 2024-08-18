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
any_phone_numbers = []
new_phone_numbers = []
id, username, email, phone_number = wgh_new_acounts[0]


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
# 

emails = ['godwinajibola@yahoo.com', 'codemyhobby9@gmail.com', 'deji@dejinova.com', 'broketechsis0@gmail.com', 'godwinajibola@yahoo.com', 'udishoots@gmail.com', 'ValorReviews@gmail.com', 'tiktok@oscarmini.com', 'izzitechng@gmail.com', 'tayllor@tayllorlloyd.com', 'adebimpeayorinde@gmail.com', 'hello@gomycode.com', 'ayomideadeduro@gmail.com', 'stellaajulor01@gmail.com', 'info@knewkeed.com', 'abbytech77@gmail.com', 'shotbykagan@gmail.com', 'sharonenoabasi17@gmail.com']
for index, (email) in enumerate(emails):
    username = re.match(r'^[^@]+', email).group()
    new_phone_number = f"+2347{index}1321{index}08{index}"
    trimmed_phone_number = new_phone_number[:14]
    # spam.signup_single(email, username, trimmed_phone_number)
    spam.ticket_single(short_tickets, "Make a TikTtok Video about this 😂😂😂", email)

"""
spam.signup_single('godwinajibola@yahoo.com', 'godwinajibola', '+2347021010101')
spam.ticket_single(short_tickets, 'godwinajibola', 'godwinajibola@yahoo.com')
spam.ticket_single(long_tickets, 'godwinajibola', 'godwinajibola@yahoo.com')


phone_numbers = [(index, f"+234{str(i)}") for index, i in enumerate(range(7080000000, 7089999999))] # 10 million.
spam.sms_bulk(phone_numbers, 'sharonenoabasi17@gmail.com', 'sharonenoabasi17')
"""

