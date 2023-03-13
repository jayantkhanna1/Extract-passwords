# This file does nothing but gets user os adn calls necessary os file

def get_os():
    import platform
    operating_system = platform.system()
    if operating_system == "Windows":
        from windows import Windows
        win = Windows()

if __name__ == "__main__":
    get_os()