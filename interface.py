import customtkinter as ctk
import threading
from ftp import start_player_checking
from ftp import target_players

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

        #Button for list
        self.btn_show_list = ctk.CTkButton(
        master=self, 
        text="Players you follow", 
        command=self.open_players_list,
        fg_color="gray25",
        hover_color="gray35")
        self.btn_show_list.pack(pady=10, padx=20)

        # Status label
        self.label_status = ctk.CTkLabel(self, text="Status: Ready", text_color="gray")
        self.label_status.pack(pady=10)

        # x button in windows frame
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        from ftp import is_bot_active
        is_bot_active.clear() 
        self.destroy()
    

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

    def open_players_list(self):
        import ftp
        list_window = ctk.CTkToplevel(self)
        list_window.title("Players you follow")
        list_window.geometry("350x450")

        #icon
        def set_icon():
            try:
                list_window.iconbitmap("icon.ico")
            except:
                print("Icon file not found, using default.")
                pass
        list_window.after(200, set_icon)


        list_window.attributes('-topmost', True)

        ctk.CTkLabel(list_window, text="Following list", font=("Roboto", 16, "bold")).pack(pady=15)

        scroll_frame = ctk.CTkScrollableFrame(list_window, width=300, height=300)
        scroll_frame.pack(pady = 10, padx = 10, fill="both", expand=True)

        

        def refresh_list():
            for widget in scroll_frame.winfo_children():
                widget.destroy()

            if not ftp.target_players:
                ctk.CTkLabel(scroll_frame, text = "No players followed.").pack(pady=20)
                return
            
            for player in ftp.target_players:
                row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                row.pack(fill="x", pady = 5)

                ctk.CTkLabel(row, text = player.capitalize()).pack(side="left", padx = 10)

                btn_remove = ctk.CTkButton(
                    master = row,
                    text = "Remove",
                    width= 60,
                    height= 25,
                    fg_color= "#CC3333",
                    hover_color = "#992222",
                    command=lambda p=player: remove_and_refresh(p)
                )
                btn_remove.pack(side="right", padx = 10)

        def remove_and_refresh(name):
            if name in ftp.target_players:
                ftp.target_players.remove(name)
                refresh_list()
        refresh_list()
        

if __name__ == "__main__":
    app = TennisApp()
    app.mainloop()
