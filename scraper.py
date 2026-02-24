from __future__ import annotations
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_matches(target_url: str, timeout: int = 20) -> List[Dict[str, str]]:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, timeout)

    data: List[Dict[str, str]] = []

    try:
        driver.get(target_url)

        # Wait until at least one time cell exists
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.time, td.first.time")))

        # Each match starts on a row that has a time cell + a player cell
        # Opponent is on the NEXT <tr>
        match_start_rows = driver.find_elements(
            By.XPATH,
            "//tr[td[contains(@class,'time') or contains(@class,'first time')]]"
            "[td[contains(@class,'t-name')]]"
        )

        for row in match_start_rows:
            # time
            try:
                t = row.find_element(By.CSS_SELECTOR, "td.time, td.first.time").text.strip()
            except:
                continue

            # only keep real scheduled times like 14:00
            if ":" not in t or len(t) > 5:
                continue

            # player 1 (in this row)
            try:
                p1 = row.find_element(By.CSS_SELECTOR, "td.t-name a").text.strip()
            except:
                continue

            # player 2 (in next row)
            try:
                p2 = row.find_element(By.XPATH, "following-sibling::tr[1]//td[contains(@class,'t-name')]//a").text.strip()
            except:
                continue

            if p1 and p2:
                data.append({"p1": p1, "p2": p2, "time": t})

    finally:
        driver.quit()

    return data