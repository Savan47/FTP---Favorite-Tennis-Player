import os
from scraper import get_matches
import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv
from random import randint
import time
from datetime import datetime, timedelta
import threading
import traceback
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
    
                
        

def send_notification(user_email, subject, content):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    receiver_email = user_email

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = user_email

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
        print(f"Email sent successfully to {user_email}!")
    except Exception as e:
        print(f"Failed to send email: {e}")


is_bot_active = threading.Event()


def start_player_checking(user_email, target_players):
    is_bot_active.set()

    while is_bot_active.is_set():
        try:
            print("Bot is checking matches...")
            time_now = datetime.now()

            tomorrow = datetime.now() + timedelta(days=1)
            today = datetime.now()
            tomorrow_url = f"https://www.tennisexplorer.com/matches/?type=all&year={tomorrow.year}&month={tomorrow.month:02d}&day={tomorrow.day:02d}"
            today_url = f"https://www.tennisexplorer.com/matches/?type=all&year={today.year}&month={today.month:02d}&day={today.day:02d}"
            tomorrow_data = get_matches(tomorrow_url)
            today_data = get_matches(today_url)
            
            matches = []
            for d in today_data:
                m = TennisMatch(d['p1'], d['p2'], d['time'])
                m.date_obj = today # Ovo je onaj 'today' koji si već definisao iznad
                matches.append(m)

            for d in tomorrow_data:
                m = TennisMatch(d['p1'], d['p2'], d['time'])
                m.date_obj = tomorrow # Ovo je onaj 'tomorrow' koji si definisao iznad
                matches.append(m)

            

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

                            if ":" not in m.time or len(m.time) > 5:
                                # Ako piše "Live", "Fin", "Canc." - samo preskoči matematiku
                                print(f"Preskačem meč {m.p1} - status: {m.time}")
                                continue
                            

                            match_time_obj = datetime.strptime(m.time, "%H:%M").replace(
                                year=m.date_obj.year, 
                                month=m.date_obj.month, 
                                day=m.date_obj.day
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
                            time_diff = match_time_obj - time_now
                            if 0 < time_diff.total_seconds() <= 86400:           
                                print(f"New match found within 24h: {m}. Sending email...")

                                display_name = player_name.title()
                                subject = f"🎾 Match Alert: {display_name} is playing!"

                                day_text = "today" if match_time_obj.date() == time_now.date() else "tomorrow"

                                body = (f"Hello, we have good news!\n\n"
                                        f"Your selected player {display_name} is playing {day_text}: \n"
                                        f"{m.p1} vs {m.p2} at: {m.time}\n\n"
                                        f"You are receiving this because you signed up for 'FTP - Favorite Tennis Player'."
                                            )
                                send_notification(user_email, subject, body)
                                SENT_NOTIFICATIONS.add(match_id)
                            else:
                                print(f"Match found: {m}, but it's more than 24h away. Waiting for next cycle...")
                        else:
                            print(f"Match {m} is already registered, skipping...")
            if not found:
                print("There is no matches for searched players")
        except Exception as e:
            print(f"❌ CRITICAL ERROR: {e}")
            traceback.print_exc()
            print("tRYING AGAIN IN 5 MINUTES...")
            time.sleep(300) 
            continue 


        for _ in range(randint(5, 15)):#randint(7200, 10800) // 5
            if not is_bot_active.is_set():
                break
            time.sleep(5)
def stop_checking():
    is_bot_active.clear()
    print("Bot stop signal received")

        
if __name__ == "__main__":
    main()