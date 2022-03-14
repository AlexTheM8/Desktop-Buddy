import pyautogui
import random
import tkinter as tk

start_x = 1400
start_y = 900
x = start_x
y = start_y
cycle = 0
check = 0
face_right = True
dig_num = 0
bark_num = dig_num + 1
idle_to_sleep_num = 13
idle_num = [i for i in range(bark_num + 1, idle_to_sleep_num)]
walk_left = [i + idle_to_sleep_num + 1 for i in range(3)]
walk_right = [i + max(walk_left) + 1 for i in range(3)]
run_left = [i + max(walk_right) + 1 for i in range(4)]
run_right = [i + max(run_left) + 1 for i in range(4)]
sleep_num = [i for i in range(max(run_right) + 1, 35)]
sleep_num.remove(max(sleep_num) - 1)
event_number = min(idle_num)
impath = './images\\'


# transfer random no. to event
def event(cycle, check, event_number, x, loc_y):
    global face_right
    if event_number in idle_num:
        check = 0
        frame = idle[cycle] if face_right else idle_left[cycle]
        window.after(180, update, cycle, check, event_number, x, loc_y)
    elif event_number == idle_to_sleep_num:
        check = 1
        frame = idle_to_sleep[cycle] if face_right else idle_to_sleep_left[cycle]
        window.after(200, update, cycle, check, event_number, x, loc_y)
    elif event_number in walk_left:
        check = 4
        face_right = False
        frame = walk_positive[cycle]
        window.after(90, update, cycle, check, event_number, x, loc_y)
    elif event_number in walk_right:
        check = 5
        face_right = True
        frame = walk_negative[cycle]
        window.after(90, update, cycle, check, event_number, x, loc_y)
    elif event_number in sleep_num:
        check = 2
        frame = sleep[cycle] if face_right else sleep_left[cycle]
        window.after(400, update, cycle, check, event_number, x, loc_y)
    elif event_number == max(sleep_num) - 1:
        check = 3
        frame = sleep_to_idle[cycle] if face_right else sleep_to_idle_left[cycle]
        window.after(100, update, cycle, check, event_number, x, loc_y)
    elif event_number in run_left:
        check = 6
        face_right = False
        frame = run_positive[cycle]
        window.after(90, update, cycle, check, event_number, x, loc_y)
    elif event_number in run_right:
        check = 7
        face_right = True
        frame = run_negative[cycle]
        window.after(90, update, cycle, check, event_number, x, loc_y)
    elif event_number == dig_num:
        check = 8
        frame = dig_right[cycle] if face_right else dig_left[cycle]
        window.after(50, update, cycle, check, event_number, x, loc_y)
    elif event_number == bark_num:
        check = 9
        frame = bark_right[cycle] if face_right else bark_left[cycle]
        window.after(90, update, cycle, check, event_number, x, loc_y)
    label.configure(image=frame)


# making gif work
def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1)
    return cycle, event_number


def update(cycle, check, event_number, x, loc_y):
    # idle
    if check == 0:
        cycle, event_number = gif_work(cycle, idle, event_number, dig_num, min(sleep_num) - 1)
    # idle to sleep
    elif check == 1:
        cycle, event_number = gif_work(cycle, idle_to_sleep, event_number, min(sleep_num), min(sleep_num))
    # sleep
    elif check == 2:
        cycle, event_number = gif_work(cycle, sleep, event_number, min(sleep_num), max(sleep_num))
    # sleep to idle
    elif check == 3:
        cycle, event_number = gif_work(cycle, sleep_to_idle, event_number, min(idle_num), min(idle_num))
    # walk toward left
    elif check == 4:
        cycle, event_number = gif_work(cycle, walk_positive, event_number, dig_num, min(sleep_num) - 1)
        x -= 5
    # walk towards right
    elif check == 5:
        cycle, event_number = gif_work(cycle, walk_negative, event_number, dig_num, min(sleep_num) - 1)
        x -= -5
    # run left
    elif check == 6:
        x -= 20
        cycle, event_number = gif_work(cycle, run_positive, event_number, dig_num, min(sleep_num) - 1)
    # run right
    elif check == 7:
        x -= -20
        cycle, event_number = gif_work(cycle, run_negative, event_number, dig_num, min(sleep_num) - 1)
    elif check == 8:
        cycle, event_number = gif_work(cycle, dig_left, event_number, dig_num, min(sleep_num) - 1)
    elif check == 9:
        cycle, event_number = gif_work(cycle, bark_left, event_number, dig_num, min(sleep_num) - 1)
    if x not in range(limits[0], limits[1]):
        event_number = random.choice((min(walk_left), min(run_left))) if x >= limits[1] \
            else random.choice((min(walk_right), min(run_right)))
        cycle = 0
    window.after(1, event, cycle, check, event_number, x, loc_y)
    window.geometry('130x130+' + str(x) + '+' + str(loc_y))


window = tk.Tk()
limits = (-abs(window.winfo_screenwidth() - 90), window.winfo_screenwidth() - 20)
# call buddy's action gif
idle = [tk.PhotoImage(file=impath + 'boney_idle_right.gif', format='gif -index %i' % i) for i in range(8)]
idle_left = [tk.PhotoImage(file=impath + 'boney_idle_left.gif', format='gif -index %i' % i) for i in range(8)]
idle_to_sleep = [tk.PhotoImage(file=impath + 'boney_change_to_sleep_right.gif', format='gif -index %i' % i) for i in
                 range(4)]
idle_to_sleep_left = [tk.PhotoImage(file=impath + 'boney_change_to_sleep.gif', format='gif -index %i' % i) for i in
                      range(4)]
sleep = [tk.PhotoImage(file=impath + 'boney_sleep_right.gif', format='gif -index %i' % i) for i in range(12)]
sleep_left = [tk.PhotoImage(file=impath + 'boney_sleep_left.gif', format='gif -index %i' % i) for i in range(12)]
sleep_to_idle = [tk.PhotoImage(file=impath + 'boney_change_to_idle_right.gif', format='gif -index %i' % i) for i in
                 range(7)]
sleep_to_idle_left = [tk.PhotoImage(file=impath + 'boney_change_to_idle.gif', format='gif -index %i' % i) for i in
                      range(7)]
walk_positive = [tk.PhotoImage(file=impath + 'boney_walk_left.gif', format='gif -index %i' % i) for i in range(12)]
walk_negative = [tk.PhotoImage(file=impath + 'boney_walk_right.gif', format='gif -index %i' % i) for i in range(12)]
run_positive = [tk.PhotoImage(file=impath + 'boney_run_left.gif', format='gif -index %i' % i) for i in range(12)]
run_negative = [tk.PhotoImage(file=impath + 'boney_run_right.gif', format='gif -index %i' % i) for i in range(12)]
bark_left = [tk.PhotoImage(file=impath + 'boney_bark_left.gif', format='gif -index %i' % i) for i in range(15)]
bark_right = [tk.PhotoImage(file=impath + 'boney_bark_right.gif', format='gif -index %i' % i) for i in range(15)]
dig_left = [tk.PhotoImage(file=impath + 'boney_dig_left.gif', format='gif -index %i' % i) for i in range(20)]
dig_right = [tk.PhotoImage(file=impath + 'boney_dig_right.gif', format='gif -index %i' % i) for i in range(20)]
# window configuration
label = tk.Label(window, bd=0, bg='red')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'red')
window.wm_attributes("-topmost", 1)
label.pack()
# loop the program
window.after(1, update, cycle, check, event_number, x, y)
window.mainloop()
