from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time

def get_matches(target_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Looking for tommorows date
    
    
    scraped_data = []

    try:
        driver.get(url)
        time.sleep(5) 
        
        
        names = driver.find_elements(By.CLASS_NAME, "t-name")
        times = driver.find_elements(By.CLASS_NAME, "time")
        
        
        
        temp_players = []
        for name in names:
            
            links = name.find_elements(By.TAG_NAME, "a")
            if links:
                temp_players.append(links[0].text.strip())
        
     
        num_matches = min(len(temp_players) // 2, len(times))
        
        for i in range(num_matches):
            p1 = temp_players[i*2]
            p2 = temp_players[i*2 + 1]
            m_time = times[i].text.strip()
            
            if p1 and p2:
                scraped_data.append({"p1": p1, "p2": p2, "time": m_time})
                
    except Exception as e:
        print(f"Greška pri skeniranju: {e}")
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