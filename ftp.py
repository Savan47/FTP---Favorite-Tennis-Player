import os
from scraper import get_matches
import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv
from random import randint
import time
from datetime import datetime, timedelta
import threading
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
    start_player_checking(target, target_players)
    
                
        

def send_notification(match_object, target, user_email):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    receiver_email = user_email

    msg = EmailMessage()
    msg['Subject'] = f"🎾 Match Alert: {target.title()} is playing!"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    content = (f"Hello, we have good news!\n\n"
        f"Your selected player {target.title()} is playing tomorrow: \n"
        f"{match_object.p1} vs {match_object.p2} at: {match_object.time}\n\n"
        f"You are receiving this because you signed up for 'FTP - Favorite Tennis Player'."
                )
    msg.set_content(content)



    if not sender_password:
        print("GREŠKA: Python uopšte ne vidi EMAIL_PASS u .env fajlu!")
        return
    else:
        print(f"DEBUG: Pokušavam login za {sender_email} sa lozinkom od {len(sender_password)} karaktera.")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context) 
            server.ehlo()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


is_bot_active = threading.Event()


def start_player_checking(user_email, target_players):
    is_bot_active.set()

    while is_bot_active.is_set():
        print("Bot is checking matches...")
        time_now = datetime.now()

        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_url = f"https://www.tennisexplorer.com/matches/?type=all&year={tomorrow.year}&month={tomorrow.month:02d}&day={tomorrow.day:02d}"
        today_url = f"https://www.tennisexplorer.com/matches/?type=all&year={today.year}&month={today.month:02d}&day={today.day:02d}"
        tomorrow_data = get_matches(tomorrow_url)
        today_data = get_matches(today_url)
        all_matches = tomorrow_data + today_data
        
        matches = [TennisMatch(d['p1'], d['p2'], d['time']) for d in all_matches]
        
        # Check logic
        found = False
        for m in matches:
            for player_name in target_players:
                search_parts = player_name.lower().split()
                match_found = any(part in m.p1.lower() or part in m.p2.lower() for part in search_parts if len(part) > 2)

                if match_found:
                    found = True
                    match_id = f"{m.p1}-{m.p2}-{m.time}"
                #15 min before match
                    reminder_id = f"{m.p1}-{m.p2}-{m.time}-REMINDER"
                    try:
                        match_time_obj = datetime.strptime(m.time, "%H:%M").replace(
                            year=time_now.year, month=time_now.month, day=time_now.day
                        )
                        
                        
                        if match_time_obj < time_now:
                            match_time_obj += timedelta(days=1)

                        
                        reminder_time = match_time_obj - timedelta(minutes=15)
                        seconds_to_wait = (reminder_time - time_now).total_seconds()

                        if seconds_to_wait > 0 and reminder_id not in SENT_NOTIFICATIONS:
                            print(f"Reminder scheduled for {m.p1} in {seconds_to_wait/3600:.2f} hours.")
                            
                            
                            subject = f"🎾 URGENT: {m.p1.title()} starts in 15 minutes!"
                            body = f"Get ready! Match at {m.time}."
                            
                            
                            t = threading.Timer(seconds_to_wait, send_notification, args=[user_email, subject, body])
                            t.start()
                            
                            SENT_NOTIFICATIONS.add(reminder_id)

                        
                        elif -900 < seconds_to_wait <= 0 and reminder_id not in SENT_NOTIFICATIONS:
                        
                            send_notification(user_email, subject, body)
                            SENT_NOTIFICATIONS.add(reminder_id)

                    except ValueError:
                        print(f"Time of the match {m.time} not in HH:MM format, skipping..")




                    if match_id not in SENT_NOTIFICATIONS:
                        print(f"New match found: {m}. Sending email...")
                        send_notification(m, player_name.capitalize(), user_email)
                        SENT_NOTIFICATIONS.add(match_id)
                    else:
                        print(f"Match {m} is already registered, skipping...")
        if not found:
            print("There is no matches for searched players")


        for _ in range(randint(7200, 10800) // 5):
            if not is_bot_active.is_set():
                break
            time.sleep(5)
def stop_checking():
    is_bot_active.clear()
    print("Bot stop signal received")

        
if __name__ == "__main__":
    main()