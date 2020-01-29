import tkinter as tk

window = tk.Tk()

window.title("Rebound Predictor Tool")

label = tk.Button(window, text = "Rebound tool").pack()

image = tk.PhotoImage(file="./assets/HockeyRinkZone.png")
label = tk.Label(image=image)
label.pack()

window.mainloop()
