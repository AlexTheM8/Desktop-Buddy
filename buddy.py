import pyautogui
import random
import tkinter as tk

start_x = 1400
start_y = 888
x = start_x + 500
y = start_y
cycle = 0
check = 8
face_right = True
dance_num = 0
idle_to_sleep_num = 16
idle_num = [i for i in range(dance_num + 1, idle_to_sleep_num)]
walk_left = [i + idle_to_sleep_num + 1 for i in range(3)]
walk_right = [i + max(walk_left) + 1 for i in range(3)]
run_left = [i + max(walk_right) + 1 for i in range(3)]
run_right = [i + max(run_left) + 1 for i in range(3)]
sleep_num = [i for i in range(max(run_right) + 1, 36)]
sleep_num.remove(max(sleep_num) - 1)
warp_num = max(sleep_num) + 1
land_num = warp_num + 1
event_number = warp_num
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
        window.after(80, update, cycle, check, event_number, x, loc_y)
    elif event_number in walk_right:
        check = 5
        face_right = True
        frame = walk_negative[cycle]
        window.after(80, update, cycle, check, event_number, x, loc_y)
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
        window.after(80, update, cycle, check, event_number, x, loc_y)
    elif event_number in run_right:
        check = 7
        face_right = True
        frame = run_negative[cycle]
        window.after(80, update, cycle, check, event_number, x, loc_y)
    elif event_number == warp_num:
        check = 8
        face_right = True
        frame = warp[cycle]
        window.after(1, update, cycle, check, event_number, x, loc_y)
    elif event_number == land_num:
        check = 9
        face_right = True
        frame = land[cycle]
        window.after(30, update, cycle, check, event_number, x, loc_y)
    elif event_number == dance_num:
        check = 10
        frame = dance[cycle]
        window.after(40, update, cycle, check, event_number, x, loc_y)
    label.configure(image=frame)


# making gif work
def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1)
    return cycle, event_number


def warp_work(loc_y, event_number, cycle):
    drop_length = 18
    if loc_y < start_y - (len(land) - 1) * drop_length:
        loc_y += 2
        cycle = 0
    elif loc_y < start_y:
        loc_y += drop_length
        event_number = land_num
        cycle += 1
    else:
        loc_y = start_y
        event_number = min(idle_num)
        cycle = 0
    return loc_y, event_number, cycle


def update(cycle, check, event_number, x, loc_y):
    # idle
    if check == 0:
        cycle, event_number = gif_work(cycle, idle, event_number, dance_num, min(sleep_num) - 1)
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
        cycle, event_number = gif_work(cycle, walk_positive, event_number, dance_num, min(sleep_num) - 1)
        x -= 5
    # walk towards right
    elif check == 5:
        cycle, event_number = gif_work(cycle, walk_negative, event_number, dance_num, min(sleep_num) - 1)
        x -= -5
    # run left
    elif check == 6:
        x -= 15
        cycle, event_number = gif_work(cycle, run_positive, event_number, dance_num, min(sleep_num) - 1)
    # run right
    elif check == 7:
        x -= -15
        cycle, event_number = gif_work(cycle, run_negative, event_number, dance_num, min(sleep_num) - 1)
    elif check == 8:
        loc_y, event_number, cycle = warp_work(loc_y, event_number, 0)
        x += 1
    elif check == 9:
        loc_y, event_number, cycle = warp_work(loc_y, event_number, cycle)
        x += 8
    elif check == 10:
        cycle, event_number = gif_work(cycle, dance, event_number, dance_num, min(sleep_num) - 1)
    # Warp back in
    if x not in range(limits[0], limits[1]):
        window.after(2000, event, 0, check, warp_num, start_x - 800, -100)
    else:
        window.after(1, event, cycle, check, event_number, x, loc_y)
        window.geometry('333x143+' + str(x) + '+' + str(loc_y))


window = tk.Tk()
limits = (-abs(window.winfo_screenwidth() - 90), window.winfo_screenwidth() - 50)
# call buddy's action gif
idle = [tk.PhotoImage(file=impath + 'kirby_idle.gif', format='gif -index %i' % i) for i in range(7)]
idle_left = [tk.PhotoImage(file=impath + 'kirby_idle_left.gif', format='gif -index %i' % i) for i in range(7)]
idle_to_sleep = [tk.PhotoImage(file=impath + 'kirby_change_to_sleep.gif', format='gif -index %i' % i) for i in range(8)]
idle_to_sleep_left = [tk.PhotoImage(file=impath + 'kirby_change_to_sleep_left.gif', format='gif -index %i' % i) for i in
                      range(8)]
sleep = [tk.PhotoImage(file=impath + 'kirby_sleep.gif', format='gif -index %i' % i) for i in range(6)]
sleep_left = [tk.PhotoImage(file=impath + 'kirby_sleep_left.gif', format='gif -index %i' % i) for i in range(6)]
sleep_to_idle = [tk.PhotoImage(file=impath + 'kirby_change_to_idle.gif', format='gif -index %i' % i) for i in range(9)]
sleep_to_idle_left = [tk.PhotoImage(file=impath + 'kirby_change_to_idle_left.gif', format='gif -index %i' % i) for i in
                      range(9)]
walk_positive = [tk.PhotoImage(file=impath + 'kirby_left.gif', format='gif -index %i' % i) for i in range(10)]
walk_negative = [tk.PhotoImage(file=impath + 'kirby_right.gif', format='gif -index %i' % i) for i in range(10)]
run_positive = [tk.PhotoImage(file=impath + 'kirby_run_left.gif', format='gif -index %i' % i) for i in range(8)]
run_negative = [tk.PhotoImage(file=impath + 'kirby_run_right.gif', format='gif -index %i' % i) for i in range(8)]
warp = [tk.PhotoImage(file=impath + 'Warp_Star.gif', format='gif -index %i' % i) for i in range(1)]
land = [tk.PhotoImage(file=impath + 'kirby_land.gif', format='gif -index %i' % i) for i in range(18)]
dance = [tk.PhotoImage(file=impath + 'kirby_dance.gif', format='gif -index %i' % i) for i in range(186)]
# window configuration
label = tk.Label(window, bd=0, bg='red')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'red')
window.wm_attributes("-topmost", 1)
label.pack()
# loop the program
# window.after(1, update, cycle, check, event_number, x, y)
window.after(1, update, cycle, check, event_number, x, y)
window.mainloop()
