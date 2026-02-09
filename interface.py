import tkinter as tk
import threading
from ftp import start_player_checking

def start_process():
    email = entry_email.get()
    player_input = entry_player.get()

    if not email or not player_input:
        print("Please, fill up all fields!")
        
    
    target_list = [p.strip() for p in player_input.split(",")]

    bot_thread = threading.Thread(
        target = start_player_checking,
        args=(email, target_list),
        daemon=True
    )

    bot_thread.start()
    
    label_status.config(text=f"Bot works for: {player_input}", fg="green")
    button.config(state="disabled")




    







root = tk.Tk()
root.title("FTP - Favorite Tennis Player")
label = tk.Label(root, text="You want to follow matches for tennis player?").grid(row=0, column=0, columnspan=2)


tk.Label(root, text="Enter your email").grid(row=1, column=0)
tk.Label(root, text="Enter your favorite player").grid(row=2, column=0)
entry_email = tk.Entry(root)
entry_player = tk.Entry(root)

entry_email.grid(row=1, column=1)
entry_player.grid(row=2, column=1)

button = tk.Button(root, text="Start the app",command=start_process)
button.grid(row=3, column=0)

label_status = tk.Label(root, text="Waiting...")
label_status.grid(row=4, column=0)



root.mainloop()

