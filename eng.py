import os, requests, pickle, random, sqlite3

class WhoGoHost:
    def __init__(self, headers={}):
        self.session = requests.Session()
        self.signup_url= "https://api.go54.com/api/v1/auth/register"
        self.login_url = "https://api.go54.com/api/v1/auth/login"
        self.bvn_url = "https://api.go54.com/api/v1/user/account/validate-bvn"
        self.phone_url = "https://api.go54.com/api/v1/user/account/phone-verification"
        self.ticket_url = "https://api.go54.com/api/v1/public/support/email"
        self.headers = headers
        self.session.headers.update(self.headers)
        if not os.path.exists('localdb/wgh_spam_accounts.db'):
            open('localdb/wgh_spam_accounts.db', 'w').close()
        self.conn = sqlite3.connect('localdb/wgh_spam_accounts.db')
        self.cursor = self.conn.cursor()
        self.create_database()

    def create_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone_number TEXT,
                is_verified BOOLEAN,
                uid TEXT,
                updated_at TEXT,
                created_at TEXT,
                user_id INTEGER,
                whmcs_id INTEGER,
                full_name TEXT
            )
        ''')
        self.conn.commit()

    def save_user_to_db(self, user_data):
        if user_data is None:
            return
        self.cursor.execute('''
            INSERT INTO users (
                first_name, last_name, email, phone_number, is_verified, uid, 
                updated_at, created_at, user_id, whmcs_id, full_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['first_name'], user_data['last_name'], user_data['email'],
            user_data['phone_number'], user_data['is_verified'], user_data['uid'],
            user_data['updated_at'], user_data['created_at'], user_data['id'],
            user_data['whmcs_id'], user_data['full_name']
        ))
        self.conn.commit()

    def signup(self, payload):
        response = self.session.post(self.signup_url, data=payload)
        if response.status_code != 200:
            print(response.text)
            return None
        response = response.json()
        if not response['message'] == 'Registration successful':
            print(response)
            return None
        user_data = response.get('data', None).get('user', None)
        token = response.get('data', None).get('token', None)
        self.headers = { "Authorization": f"Bearer {token}"}
        message = response.get('message', None)
        if message == "Registration successful":
            self.save_user_to_db(user_data)
            return message
        return None

    def login(self, payload):
        response = self.session.post(self.login_url, data=payload)
        if response.status_code != 200:
            print(response.text)
            return None
        response = response.json()
        if not response['message'] == 'Login successful':
            print(response)
            return None
        token = response.get('data', None).get('token', None)
        self.headers = { "Authorization": f"Bearer {token}"}
        return token

    def create_ticket(self, ticket):
        # self.session.headers.update(self.headers) # not required
        response = self.session.post(self.ticket_url, data=ticket)
        if not response.status_code == 200:
            print(response.text)
            return None
        response = response.json()
        message = response.get('message', None)
        if message == "Message received, we will get back soon!":
            # self.save_user_to_db(user_data) no need to save anything here jhoor
            return message
        return None
    
    def verify_phone(self, phone):
        payload = {"phonenumber": phone}
        self.session.headers.update(self.headers)
        response = self.session.post(self.phone_url, data=payload)
        if not response.status_code == 200:
            print(response.text)
            return None
        response = response.json()
        if response.get('message', None) == 'OTP sent to user phone number':
            return response
        print(response)
        return None

    def verify_bvn(self):
        self.session.headers.update(self.headers)
        bvn = lambda: ''.join([str(random.randint(0, 9)) for _ in range(11)])
        payload = {"bvn": bvn()}
        response = self.session.post(self.bvn_url, data=payload)
        if not response.status_code == 200:
            print(response.text)
            return None
        return response.json()

    def __del__(self):
        self.conn.close()

class Spam:
    def __init__(self):
        pass
    
    def get_subject(self, sentence, min_words=3, max_words=5):
        words = sentence.split()
        word_count = len(words)
        num_words_to_pick = random.randint(min_words, min(max_words, word_count))
        selected_words = words[:num_words_to_pick]
        result_sentence = ' '.join(selected_words)
        return result_sentence

    def signup_single(self, email, username, phone):
        whogohost = WhoGoHost()
        password = username+"theGudBadGuys1$"
        payload = {
            "email": email,
            "lastname": username,
            "password": password,
            "firstname": username,
            "phonenumber": phone
            }
        response = whogohost.signup(payload)
        if response is not None:
            print(f"{username}: {response}")
        
    def signup_all(self, new_accounts, new_phone_numbers):
        if new_accounts is None or new_phone_numbers is None:
            print("New Accounts and New Phone numbers are required for Singup all")
            return
        successes = 0
        togo = len(new_accounts)
        for index, username, email in new_accounts:
            random_vowel = lambda: random.choice('aeiou')
            phone = new_phone_numbers[index]
            password = username+"theGudBadGuys1$"
            payload = {
                    "email": email,
                    "lastname": username,
                    "password": password,
                    "firstname": username,
                    "phonenumber": phone
                }
            whogohost = WhoGoHost()
            response = whogohost.signup(payload)
            if response is not None:
                successes +=1
                print(f"user: {username} {response}===goes: {index}, successes: {successes}, togo: {togo}")
            if index >= len(new_phone_numbers):
                print("Out of Phone numbers")
                break

    def ticket_single(self, tickets, username, email):
        if tickets is None:
            print("Ticket, Username, and Email are required for Ticket single")
            return
        successes = 0
        togo = len(tickets)
        password = username+"theGudBadGuys1$"
        user = {"email": email, "password": password}
        whogohost = WhoGoHost()
        # login = whogohost.login(user)
        # if login is None:
        #     return
        for index, issue in tickets:
            ticket = {
                "email": email,
                "name": username,
                "password": password,
                "department": "Technical Support",
                "issue": "Abuse and Compliance",
                "subject": issue,
                "message": issue
            }
            response = whogohost.create_ticket(ticket)
            if response is not None:
                successes +=1
                print(f"ticket_single: {response}===goes: {index}, successes: {successes}, togo: {togo}")

    def ticket_all(self, tickets, wgh_spam_accounts):
        if tickets is None:
            print("Ticket and Verified Accounts required for Ticket all")
            return
        successes = 0
        togo = len(wgh_spam_accounts)
        for index, username, email, phone_number in wgh_spam_accounts:
            password = username+"theGudBadGuys1$"
            user = {"email": email, "password": password}
            id, ticket = tickets[index]
            subject = self.get_subject(ticket, 5, 10)
            ticket = {
                    "email": email,
                    "name": username,
                    "password": password,
                    "department": "Technical Support",
                    "issue": "Abuse and Compliance",
                    "subject": subject,
                    "message": ticket
                }
            whogohost = WhoGoHost()
            login = whogohost.login(user)
            if login is None:
                break
            response = whogohost.create_ticket(ticket)
            if response is not None:
                successes +=1
                print(f"ticket_all: {response}===goes: {index}, successes: {successes}, togo: {togo}")
            if index >= len(tickets):
                break

    def sms_bulk(self, phone_numbers, email, username):
        if phone_numbers is None:
            print("Phone Numbers and one verified account are required for SMS all")
            return
        successes = 0
        togo = len(phone_numbers)
        for index, phone in phone_numbers:
            password = username+"theGudBadGuys1$"
            user = {"email": email, "password": password}
            whogohost = WhoGoHost()
            login = whogohost.login(user)
            if login is None:
                break
            response = whogohost.verify_phone(phone)
            if response is not None:
                successes +=1
                print(f"sms_all: {response}===goes: {index}, successes: {successes}, togo: {togo}")

    def sms_all(self, phone_numbers, wgh_spam_accounts):
        if phone_numbers is None:
            print("Phone Numbers and Verified Accounts are required for SMS all")
            return
        successes = 0
        togo = len(wgh_spam_accounts)
        for index, username, email, phone_number in wgh_spam_accounts:
            password = username+"theGudBadGuys1$"
            user = {"email": email, "password": password}
            whogohost = WhoGoHost()
            login = whogohost.login(user)
            if login is None:
                break
            response = whogohost.verify_phone(phone_number)
            if response is not None:
                successes +=1
                print(f"sms_all: {response}===goes: {index}, successes: {successes}, togo: {togo}")
    
    def bvn_all(self, wgh_spam_accounts):
        if not wgh_spam_accounts:
            print("Verified Accounts is required for bvn all")
            return
        successes = 0
        togo = len(wgh_spam_accounts)
        for index, username, email, phone_number in wgh_spam_accounts:
            password = username+"theGudBadGuys1$"
            user = {"email": email, "password": password}
            whogohost = WhoGoHost()
            login = whogohost.login(user)
            if login is None:
                break
            response = whogohost.verify_bvn()
            if response is not None:
                successes +=1
                print(f"bvn_all: {response}===goes: {index}, successes: {successes}, togo: (togo)")
    
    def __del__(self):
        print("Done...")


class DataHandler:
    def __init__(self, db_path):
        if not os.path.exists(db_path):
            open(db_path, 'w').close()
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def load_account(self, table_name):
        self.cursor.execute(f"SELECT id, first_name, email, phone_number FROM {table_name}")
        rows = self.cursor.fetchall()
        return rows

    def load_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        return rows

    def save_data(self, table_name, data):
        if not data:
            return
        if len(data) >=1 and all(isinstance(item, tuple) for item in data):
            placeholders = ', '.join('?' * len(data[0]))
            columns = ', '.join([f"name{i+1}" for i in range(len(data[0]))])
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})")
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.executemany(query, data)
        else:
            columns = "name1"
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})")
            query = f"INSERT INTO {table_name} ({columns}) VALUES (?)"
            self.cursor.executemany(query, [(item,) for item in data])

        self.conn.commit()

    @staticmethod
    def get_old(wgh_spam_accounts, all_accounts):
        if not wgh_spam_accounts or not all_accounts:
            print("wgh spam accounts and all accounts are required to get old accounts")
            return
        wgh_spam_accounts = [(t[1], t[2]) for t in wgh_spam_accounts]
        all_accounts = [(t[1], t[2]) for t in all_accounts]
        set1 = set(wgh_spam_accounts)
        set2 = set(all_accounts)
        wgh_accounts = list(set2.symmetric_difference(set1))
        return wgh_accounts

    def merge_duplicates(self, table_name):
        columns = [col[1] for col in self.cursor.execute(f"PRAGMA table_info({table_name})").fetchall() if col[1] != "id"]
        column_names = ', '.join(columns)
        all_data = self.cursor.execute(f"SELECT {column_names} FROM {table_name}").fetchall()
        unique_data = list(set(all_data))
        self.cursor.execute(f"ALTER TABLE {table_name} RENAME TO {table_name}_old")
        placeholders = ', '.join('?' * len(columns))
        self.cursor.execute(f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {column_names})")
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        self.cursor.executemany(query, unique_data)
        self.cursor.execute(f"DROP TABLE {table_name}_old")
        self.conn.commit()

    def clear_db(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        for table in tables:
            self.cursor.execute(f"DELETE FROM {table[0]}")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

