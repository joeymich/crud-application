import tkinter as tk
from tkinter import ttk
from datetime import datetime

from frames import TasksFrame
from frames import ProfilesFrame
from frames import ProxiesFrame

def clock(root):
    clock_container = ttk.Frame(root)
    clock_container.pack(fill='both', expand=0)
    clock = ttk.Label(clock_container)
    clock.pack()
    def set_time():
        date_time = datetime.now().strftime('%Y-%m-%d ')
        hour = int(datetime.now().strftime('%H'))
        if (hour < 12):
            merediem = 'am'
        else:
            merediem = 'pm'
        if (hour == 0 or hour == 12):
            hour = 12
        else:
            hour %= 12
        date_time += str(hour) + datetime.now().strftime(':%M:%S') + ' ' + merediem
        clock.config(text=date_time)
        clock.after(1000, set_time)
    set_time()

def main_frame():
    # window setup
    root = tk.Tk()
    root.geometry('1000x600')
    root.title('Tkinter Crud App')

    # clock
    clock(root)

    # tabs setup
    tabs = ttk.Notebook(root)
    tabs.pack(fill='both', expand=1)

    tasks_tab = TasksFrame()
    profiles_tab = ProfilesFrame(tasks_frame=tasks_tab)
    proxies_tab = ProxiesFrame(tasks_frame=tasks_tab)

    tabs.add(tasks_tab, text='Tasks')
    tabs.add(profiles_tab, text='Profiles')
    tabs.add(proxies_tab, text='Proxies')

    # styling - treeview
    tree_style = ttk.Style()
    tree_style.configure('Treeview', rowheight=50)

    return root

if __name__ == '__main__':
    root = main_frame()
    root.mainloop()