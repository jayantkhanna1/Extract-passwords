class Database:
    def __init__(self):
        pass

    def insert_passwords(main_url,login_url,user_name,decrypted_password,date_of_creation,last_usuage):
        print(f"Main URL: {main_url}")
        print(f"Login URL: {login_url}")
        print(f"User name: {user_name}")
        print(f"Creation date: {date_of_creation}")
        print(f"Last Used: {last_usuage}")
        print(f"Decrypted Password: {decrypted_password}")