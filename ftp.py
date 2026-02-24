import os
import re
from scraper import get_matches
import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv
from random import randint
import time
from datetime import datetime, timedelta
import threading
import traceback
import json
from matcher import is_player_match, is_doubles
load_dotenv("emailpass.env")
print("EMAIL_USER exists?", bool(os.getenv("EMAIL_USER")))
print("EMAIL_PASS exists?", bool(os.getenv("EMAIL_PASS")))


target_players = []
class TennisMatch:
    def __init__(self, p1, p2, time):
        self.p1 = p1
        self.p2 = p2
        self.time = time

    def __str__(self):
        return f"🎾 {self.p1} vs {self.p2} u {self.time}"

def main():
    user_email = input("Email: ").strip()
    target = input("Koga tražimo? ").strip().lower()
    start_player_checking(user_email, [target])


def name_tokens(s: str) -> list[str]:
    # keep only letter groups as tokens, lowercase
    return re.findall(r"[a-z]+", s.lower())

def is_player_match(player_input: str, p1: str, p2: str) -> bool:
    player = player_input.strip().lower()
    p1_tokens = name_tokens(p1)
    p2_tokens = name_tokens(p2)

    # If user types "First Last"
    parts = player.split()
    if len(parts) >= 2:
        first, last = parts[0], parts[-1]
        first_initial = first[0]
        return (
            (last in p1_tokens and first_initial in p1_tokens) or
            (last in p2_tokens and first_initial in p2_tokens)
        )

    # If user types just one word like "fils"
    key = parts[0] if parts else ""
    return (key in p1_tokens) or (key in p2_tokens)
    
                
def load_sent_notifications():
    if os.path.exists("sent_matches.json"):
        try:
            with open("sent_matches.json", "r") as f:
                return set(json.load(f))    
        except:
            return set()
    return set()
SENT_NOTIFICATIONS = load_sent_notifications()

def save_sent_notification(match_id):
    SENT_NOTIFICATIONS.add(match_id)

    with open("sent_matches.json", "w") as f:
        json.dump(list(SENT_NOTIFICATIONS), f, indent=2)

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


def start_player_checking(user_email, initial_players):
    global target_players
    target_players = initial_players
    is_bot_active.set()

    while is_bot_active.is_set():
        print(f"Trenutno pratim: {target_players}")
        try:
            print("Bot is checking matches...")
            time_now = datetime.now()

            tomorrow = datetime.now() + timedelta(days=1)
            today = datetime.now()
            tomorrow_url = f"https://www.tennisexplorer.com/matches/?day={tomorrow.day:02d}&month={tomorrow.month:02d}&type=all&year={tomorrow.year}"
            today_url = f"https://www.tennisexplorer.com/matches/?type=all&year={today.year}&month={today.month:02d}&day={today.day:02d}"
            tomorrow_data = get_matches(tomorrow_url, timeout=25)
            today_data = get_matches(today_url, timeout=25)
            
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

                # ✅ Skip doubles
                if is_doubles(m.p1, m.p2):
                    continue

                for player_name in target_players:
                    match_found = is_player_match(player_name, m.p1, m.p2)
        
                    if match_found:
                        found = True
                        print("MATCH FOUND FOR:", player_name, "=>", m.p1, "vs", m.p2, "at", m.time)




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
                                
                                save_sent_notification(reminder_id)

                            
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
                                save_sent_notification(match_id)
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


        wait_seconds = randint(7200, 10800)  # 2 to 3 hours
        for _ in range(wait_seconds // 5):
            if not is_bot_active.is_set():
                break
            time.sleep(5)
def stop_checking():
    is_bot_active.clear()
    print("Bot stop signal received")

        
if __name__ == "__main__":
    main()