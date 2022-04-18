from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from colorama import Style, Fore

#cria um chrome webdriver com opções personalizadas
def create_webdriver(profile = "Profile 1", headless = False, show_inspect = False, dont_load_images = True, mute = True):
        chrome_driver_options = Options()
        chrome_driver_options.binary_location = r"portable-chrome/App/Chrome-bin/chrome.exe"
        chrome_driver_options.add_argument(f"user-data-dir={r'chrome-profiles'}")
        chrome_driver_options.add_argument(f"--profile-directory={profile}")
        chrome_driver_options.add_argument("--log-level=3")
        chrome_driver_options.add_argument("--remote-debugging-port=9222")
        chrome_driver_options.add_argument("--disable-extensions")
        # user_agent_1 = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
        # user_agent_2 = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
        # user_agent_3 = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
        # chrome_driver_options.add_argument(f"user-agent={user_agent_2}")
        # chrome_driver_options.add_argument("--disable-gpu")
        # chrome_driver_options.add_argument("--disable-dev-shm-usage")
        # chrome_driver_options.add_argument("start-maximized")
        # chrome_driver_options.add_argument("--ignore-certificate-errors")
        # chrome_driver_options.add_argument("--disable-popup-blocking")
        # chrome_driver_options.add_argument("--incognito")
        # chrome_driver_options.add_argument("--no-sandbox")
        # chrome_driver_options.add_argument("--disable-infobars")
        if headless == True:
            chrome_driver_options.add_argument("--headless")
        if mute == True:
            chrome_driver_options.add_argument("--mute-audio")
        if dont_load_images == True:
            chrome_driver_options.add_argument("--blink-settings=imagesEnabled=false")
        if show_inspect == True and headless == False:
            chrome_driver_options.add_argument("--window-size=1300,820")
            chrome_driver_options.add_argument("--auto-open-devtools-for-tabs")
        elif headless == False:
            chrome_driver_options.add_argument("--window-size=300,820")
        # chrome_driver_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_driver_options.add_experimental_option("useAutomationExtension", False)
        chrome_driver_options.add_experimental_option("mobileEmulation", {"deviceName":"Nexus 5"})
        chrome_driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = chrome_driver_options)




#usado para mostrar traceback completo do erro com cores personalizadas
#error_details(str(traceback.format_exc()), str(e))
def error_details(error_details, aditional_info = ""):
    print(f"{Fore.RED}{Style.BRIGHT}XXXXX{Fore.WHITE}{Style.NORMAL}")
    print(f"{Fore.RED}{Style.BRIGHT}{error_details}{Fore.WHITE}{Style.NORMAL}")
    print(f"{Fore.RED}{Style.BRIGHT}ADITIONAL INFO: '{aditional_info}'{Fore.WHITE}{Style.NORMAL}")
    print(f"{Fore.RED}{Style.BRIGHT}XXXXX{Fore.WHITE}{Style.NORMAL}")