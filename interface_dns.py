from colorama import Fore, Back, Style
from time import gmtime, strftime

class Interface:
    def __init__(self, silent):
        self.silent = silent
        self.ErrorBox = " [" + Fore.RED + "Error" + Style.RESET_ALL + "] "
        self.WarningBox = " [" + Fore.YELLOW + "Warning" + Style.RESET_ALL + "] "
        self.LogBox = " [" + Fore.GREEN + "Info" + Style.RESET_ALL + "] "

    def Banner(self):
        banner = '''
         _____  _   _  _____ ______                      
        |  __ \| \ | |/ ____|  ____|                     
        | |  | |  \| | (___ | |__ _   _ ___________ _ __ 
        | |  | | . ` |\___ \|  __| | | |_  /_  / _ \ '__|
        | |__| | |\  |____) | |  | |_| |/ / / /  __/ |   
        |_____/|_| \_|_____/|_|   \__,_/___/___\___|_|   

                        mahdi0x6b
        '''
        print(banner)

    def error(self, Text):
        LogTime = "[" + Fore.BLUE + strftime("%H:%M:%S", gmtime()) + Style.RESET_ALL + "]"
        print(LogTime + self.ErrorBox + Text)
    
    def warning(self, Text):
        LogTime = "[" + Fore.BLUE + strftime("%H:%M:%S", gmtime()) + Style.RESET_ALL + "]"
        print(LogTime + self.WarningBox + Text)
    
    def info(self, Text):
        if not(self.silent):
            LogTime = "[" + Fore.BLUE + strftime("%H:%M:%S", gmtime()) + Style.RESET_ALL + "]"
            print(LogTime + self.LogBox + Text)
