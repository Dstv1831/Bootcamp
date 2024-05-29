from tkinter import *
from tkinter import messagebox
import math

# CONSTANTS
BLUE = "#6666ff"
RED = "#ff4d4d"
GREEN = "#00b300"
YELLOW = "#f7f5dd"
BLACK = "#000000"
FONT_NAME = "Comic Sans MS"
WORK_TIME = 25
SHORT_BREAK = 5
LONG_BREAK = 30

# Global variable just need to be declared inside the function,
# when their value inside the function will be affected or changed
reps = 0
mark = ""
timer = ""


# Timer Reset
def reset_timer():
    global reps, mark
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text=f"00:00")
    timer_label.config(text="Ganbatte", fg=BLACK)
    check_label.config(text="")
    reps = 0
    mark = ""


# Timer Mechanism
def start_timer():
    global reps, mark
    reps += 1
    work_sec = WORK_TIME * 60
    short_break_sec = SHORT_BREAK * 60
    long_break_sec = LONG_BREAK * 60
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Rest", fg=BLUE)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=GREEN)
    elif reps % 2 == 1 and reps < 9:
        count_down(work_sec)
        timer_label.config(text="Work", fg=RED)
        mark += "🗸"
    else:
        window.after_cancel(timer)


# Countdown Mechanism
def count_down(count):
    global timer
    # Largest Int below parameter x
    count_min = math.floor(count / 60)
    count_sec = count % 60
    # Python allows you to modify the variable's type by assigning a new type value
    # even after being declared differently on previous parts of the code
    state = ['BREAK', 'REST', 'WORK']
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        if reps % 8 == 0:
            messagebox.showinfo(title="Get some", message=f"{state[1]}")
        elif reps % 2 == 0:
            messagebox.showinfo(title="Take a", message=f"{state[0]}")
        elif reps % 2 == 1:
            messagebox.showinfo(title="Get to", message=f"{state[2]}")
    if reps % 2 == 0:
        check_label.config(text=f"{mark}")


# UI Setup

window = Tk()
window.title("Pomodoro Technique")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text="Ganbatte", font=(FONT_NAME, 30, "bold"), bg=YELLOW, fg=BLACK)
timer_label.grid(column=1, row=0)

canvas = Canvas(width=210, height=280, bg=YELLOW, highlightthickness=0)
pomodoro_image = PhotoImage(file="Tomato.png")
canvas.create_image(105, 130, image=pomodoro_image)
timer_text = canvas.create_text(105, 150, text="00:00", fill="white", font=(FONT_NAME, 20, "bold"))
canvas.grid(column=1, row=1)

check_label = Label(font=(FONT_NAME, 15, "bold"), bg=YELLOW, fg=GREEN)
check_label.grid(column=1, row=2)

green_button = PhotoImage(file="Green.png")
start_button = Button(text="Start", image=green_button, bg=YELLOW, activebackground=YELLOW, border=0,
                      command=start_timer)
start_button.grid(column=0, row=2)

red_button = PhotoImage(file="Red.png")
reset_button = Button(image=red_button, bg=YELLOW, activebackground=YELLOW, border=0, command=reset_timer)
reset_button.grid(column=2, row=2)

window.mainloop()
