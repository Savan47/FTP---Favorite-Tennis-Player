import tkinter as tk
import threading


def start_process():
    process.start()

root = tk.Tk()
root.title("FTP - Favorite Tennis Player")
label = tk.Label(root, text="You want to follow matches for tennis player?").grid(row=0, column=0, columnspan=2)


tk.Label(root, text="Enter your email").grid(row=1, column=0)
tk.Label(root, text="Enter your favorite player").grid(row=2, column=0)
entry_email = tk.Entry(root)
entry_player = tk.Entry(root)

entry_email.grid(row=1, column=1)
entry_player.grid(row=2, column=1)

button = tk.Button(root, text="Start the app", command=start_process)
button.grid(row=3, column=0)





root.mainloop()

