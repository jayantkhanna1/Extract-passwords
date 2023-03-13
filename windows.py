from brave import Brave

class Windows:
    def __init__(self):
        users = self.get_users()
        for x in users:
            if x != "All Users" and x != "desktop.ini":
                Brave("C://Users/"+x, "\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data")
            # print(x)
    
    def get_users(self):
        import os
        users = []
        for x in os.listdir("C://Users"):
            users.append(x)
        return users