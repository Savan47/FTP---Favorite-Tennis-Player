from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time

def get_tomorrow_matches():
    """Vraća listu sirovih podataka o mečevima za sutra."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    tomorrow = datetime.now() + timedelta(days=1)
    url = f"https://www.tennisexplorer.com/matches/?type=all&year={tomorrow.year}&month={tomorrow.month:02d}&day={tomorrow.day:02d}"
    
    scraped_data = []

    try:
        driver.get(url)
        time.sleep(5)
        
        name_elements = driver.find_elements(By.CLASS_NAME, "t-name")
        time_elements = driver.find_elements(By.CLASS_NAME, "time")

        for i in range(len(time_elements)):
            try:
                m_time = time_elements[i].text.strip()
                p1 = name_elements[i*2].text.strip()
                p2 = name_elements[i*2 + 1].text.strip()
                scraped_data.append({"p1": p1, "p2": p2, "time": m_time})
            except IndexError:
                continue
    finally:
        driver.quit()
    
    return scraped_data







































'''my_players = ["djokovic", "wawrinka"]
sent_notifications = set()

while True:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        tomorrow = datetime.now() + timedelta(days=1)
        url = f"https://www.tennisexplorer.com/matches/?type=all&year={tomorrow.year}&month={tomorrow.month:02d}&day={tomorrow.day:02d}"

        driver.get(url)
        time.sleep(5)

        # 2. Pronađi sve ćelije koje sadrže imena igrača
        name_elements = driver.find_elements(By.CLASS_NAME, "t-name")
        # 3. Pronađi sve ćelije koje sadrže vreme
        time_elements = driver.find_elements(By.CLASS_NAME, "time")

        
        for i in range(len(time_elements)):
            timeplaying = time_elements[i].text
           
            player1 = name_elements[i*2].text 
           
            player2 = name_elements[i*2 + 1].text
            
            print(f"Meč u {timeplaying}: {player1} vs {player2}")
            
            
            for my_favorite in my_players:
                if my_favorite.lower() in player1.lower() or my_favorite.lower() in player2.lower():
                    print(f"!!! THERE IS FAVORITE: {my_favorite} plays tomorrow at {timeplaying} !!!")
    
    except Exception as e:
        print(f"There is an Error: {e}")


    driver.quit()
        
    
    sleep_timer = random.randrange(6000,10800)
    time.sleep(sleep_timer)
try:
        driver.get(url)
        elements = driver.find_element(By.CSS_SELECTOR, "td.first.time")
        for el in elements:
            name_from_site = el.text.lower()
            if name_from_site in sent_notifications:
                continue
            if name_from_site in my_players:
                print(f"Found your player {name_from_site}")
                sent_notifications.add(name_from_site)'''