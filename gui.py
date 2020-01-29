import tkinter as tk

window = tk.Tk()

window.title("Rebound Predictor Tool")

label = tk.Button(window, text = "Rebound tool").pack()

image = tk.PhotoImage(file="./assets/HockeyRinkZone.png")
label = tk.Label(image=image)
label.pack()

# Display x-y of mouse
# Will use this to detect where puck is placed
def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

window.bind('<Motion>', motion)

window.mainloop()
