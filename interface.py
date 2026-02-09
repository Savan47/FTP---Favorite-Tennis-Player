import customtkinter as ctk
import threading
from ftp import start_player_checking

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TennisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FTP - Favorite Tennis Player")
        self.geometry("450x400")
        self.is_running = False

        # Adding icon
        try:
            self.iconbitmap("icon.ico")
        except:
            print("Icon file not found, using default.")

        # -- UI ELEMENTS --
        self.label_title = ctk.CTkLabel(self, text = "🎾 Tennis Match Notifier", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=(20, 5))

        # Subtitle text
        self.label_subtitle = ctk.CTkLabel(
            self, 
            text="Serving you match alerts in real-time.", 
            font=("Roboto", 12, "italic"),
            text_color="gray"
        )
        self.label_subtitle.pack(pady=(0, 20))


        # Email field
        self.entry_email = ctk.CTkEntry(self, placeholder_text="Your Email...", width=300)
        self.entry_email.pack(pady=10)

        #Players field
        self.entry_players = ctk.CTkEntry(self, placeholder_text = "Players (split by comma)...", width=300)
        self.entry_players.pack(pady=10)

        #Buttons
        self.btn_start = ctk.CTkButton(self, text = "Start Bot", command=self.run_bot, fg_color="green", hover_color="#056608")
        self.btn_start.pack(pady=10)

        self.btn_stop = ctk.CTkButton(self, text = "Stop Bot", command=self.stop_bot, fg_color= "red", hover_color="#8b0000")
        self.btn_stop.pack(pady=10)

        # Status label
        self.label_status = ctk.CTkLabel(self, text="Status: Ready", text_color="gray")
        self.label_status.pack(pady=10)

    def run_bot(self):
        if not self.is_running:
            email = self.entry_email.get()
            players_raw = self.entry_players.get()

            if not email or not players_raw:
                self.label_status.configure(text="Status: Please fill all fields!", text_color="red")
                return
            
            player_list = [p.strip() for p in players_raw.split(",")]
            self.is_running = True
            self.label_status.configure(text="Status: Bot is running...", text_color="green")

            self.thread = threading.Thread(target=start_player_checking, args=(email, player_list), daemon=True)
            self.thread.start()

    def stop_bot(self):

        from ftp import is_bot_active
        is_bot_active.clear()
        
        self.is_running = False
        self.label_status.configure(text="Status: Bot stopped( Restart app to reset)", text_color="red")

if __name__ == "__main__":
    app = TennisApp()
    app.mainloop()
