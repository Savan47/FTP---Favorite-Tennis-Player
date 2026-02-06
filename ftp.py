import os
from scraper import get_tomorrow_matches
import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv
from random import randint
import time
SENT_NOTIFICATIONS = set()
load_dotenv("emailpass.env")


class TennisMatch:
    def __init__(self, p1, p2, time):
        self.p1 = p1
        self.p2 = p2
        self.time = time

    def __str__(self):
        return f"🎾 {self.p1} vs {self.p2} u {self.time}"

def main():
    target = input("Koga tražimo? ").lower()
    target_players = []
    target_players.append(target)

    while True:
        # Pozivamo funkciju iz drugog fajla
        raw_data = get_tomorrow_matches()
        
        # Pretvaramo sirove podatke u tvoje objekte (klase)
        matches = [TennisMatch(d['p1'], d['p2'], d['time']) for d in raw_data]
        
        # Logika za proveru
        found = False
        for m in matches:
            for target in target_players:
                if target.lower() in m.p1.lower() or target.lower() in m.p2.lower():
                    found = True
                    match_id = f"{m.p1}-{m.p2}-{m.time}"

                    if match_id not in SENT_NOTIFICATIONS:
                        print(f"New match found: {m}. Sending email...")
                        send_notification(m)


                        SENT_NOTIFICATIONS.add(match_id)

                    else:
                        print(f"Match {m} is already register, i am skipping sending")
        if not found:
            print("There is no matches for searched players")



        print("Bot is resting")
        wait_time = randint(7200, 10800)
        time.sleep(wait_time)
                
        

def send_notification(match_object):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    receiver_email = "96kakashi@gmail.com"
    msg = EmailMessage()
    msg['Subject'] = f"🎾 Match Alert: {match_object.p1} is playing!"
    msg['From'] = sender_email
    msg['To'] = receiver_email #will be added additionaly

    content = (f"Hello, we have good news!\n\n"
        f"Your selected player is playing tomorrow: \n"
        f"{match_object} at: {match_object.time}\n\n"
        f"You are receiving this because you signed up for 'FTP - Favorite Tennis Player'."
                )
    msg.set_content(content)



    if not sender_password:
        print("GREŠKA: Python uopšte ne vidi EMAIL_PASS u .env fajlu!")
        return
    else:
        print(f"DEBUG: Pokušavam login za {sender_email} sa lozinkom od {len(sender_password)} karaktera.")

    try:
        context = ssl.create_default_context() # Dodajemo i context za svaki slučaj
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context) # Ubaci context ovde
            server.ehlo()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

        
if __name__ == "__main__":
    main()