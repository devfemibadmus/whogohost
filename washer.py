from eng import DataHandler, Spam

wgh_spam_accounts_handler = DataHandler('localdb/wgh_spam_accounts.db')
wgh_spam_accounts = wgh_spam_accounts_handler.load_account("users")

generated_accounts_handler = DataHandler('localdb/generated_accounts.db')
generated_accounts = generated_accounts_handler.load_data("accounts")

wgh_old_accounts = DataHandler.get_old(wgh_spam_accounts, generated_accounts)

wgh_old_acounts_handler = DataHandler('serverdb/wgh_old_acounts.db')
wgh_old_acounts_handler.save_data("users", wgh_old_accounts)

wgh_new_acounts_handler = DataHandler('serverdb/wgh_new_acounts.db')
wgh_spam_accounts = [(t[1], t[2], t[3]) for t in wgh_spam_accounts]
wgh_new_acounts_handler.save_data("users", wgh_spam_accounts)

wgh_old_acounts_handler.merge_duplicates("users")
wgh_new_acounts_handler.merge_duplicates("users")

generated_accounts_handler.clear_db()
wgh_spam_accounts_handler.clear_db()

print("Done...")
