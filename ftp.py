# main.py
from scraper import get_tomorrow_matches

class TennisMatch:
    def __init__(self, p1, p2, time):
        self.p1 = p1
        self.p2 = p2
        self.time = time

    def __str__(self):
        return f"🎾 {self.p1} vs {self.p2} u {self.time}"

def main():
    target = input("Koga tražimo? ").lower()
    
    # Pozivamo funkciju iz drugog fajla
    raw_data = get_tomorrow_matches()
    
    # Pretvaramo sirove podatke u tvoje objekte (klase)
    matches = [TennisMatch(d['p1'], d['p2'], d['time']) for d in raw_data]
    
    # Logika za proveru
    found = False
    for m in matches:
        if target in m.p1.lower() or target in m.p2.lower():
            print(f"Pronađen meč: {m}")
            found = True
            
    if not found:
        print("Nema mečeva sutra.")

if __name__ == "__main__":
    main()