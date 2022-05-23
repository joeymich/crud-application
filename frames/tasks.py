import json
import random
import tkinter as tk
from tkinter import ttk

class Task():
    def __init__(self, profile_id='', keywords='', size='', color='', proxy_id='', id=''):
        self.data = {}
        self.data['profile_id'] = profile_id
        self.data['keywords'] = keywords
        self.data['size'] = size
        self.data['color'] = color
        self.data['proxy_id'] = proxy_id
        if id:
            self.data['id'] = id
        else:
            self.data['id'] = self.fetch_id()

    def get_description(self):
        with open('data/profiles.json') as f:
            profiles = json.load(f)
        profile_name = 'PROFILE DELETED'
        for profile in profiles:
            if profile['id'] == self.data['profile_id']:
                profile_name = profile['profile_name']
                break
        proxy_name = 'PROXY DELETED'
        with open('data/proxies.json') as f:
            proxies = json.load(f)
        for proxy in proxies:
            if proxy['id'] == self.data['proxy_id']:
                proxy_name = proxy['name']
                break
        if self.data['proxy_id'] == -1:
            proxy_name = 'None'
        return [profile_name, self.data['keywords'], self.data['size'], self.data['color'], proxy_name]

    def fetch_id(self):
        with open('data/tasks.json') as f:
            all_tasks = json.load(f)
        ids = []
        for task in all_tasks:
            if 'id' in task:
                ids.append(task['id'])
        if ids:
            while True:
                id = random.randrange(0, 999)
                if id not in ids:
                    return id
        else:
            return random.randrange(0, 999)

class TasksFrame(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.captcha_server = None

        columns = ('profile', 'keywords', 'size', 'color', 'proxy')

        tree_container = tk.Frame(self)
        tree_container.pack(fill='both', expand=1)

        scroll = ttk.Scrollbar(tree_container, orient='vertical')
        self.tree = ttk.Treeview(tree_container, yscrollcommand=scroll.set, columns=columns, show='headings', height=0)
        scroll.config(command=self.tree.yview)
        scroll.pack(side='right', fill='y')

        for column in columns:
            self.tree.column(column, width=0, anchor='center')
            self.tree.heading(column, text=column)

        self.tasks = []

        self.load_tasks()
        self.set_rows()

        self.tree.pack(fill='both', expand=1)

        def add_task():
            AddTasksForm(self, self.tasks)

        def edit_task():
            try:
                for row in self.tree.selection():
                    index = self.tree.index(row)
                    selected_task = self.tasks[index]
                    EditTasksForm(self, self.tasks, task=selected_task, index=index)
            except IndexError:
                print('Must select a row')

        def delete_task():
            try:
                indexes = []
                for row in self.tree.selection():
                    indexes.append(self.tree.index(row))
                for index in sorted(indexes, reverse=1):
                    del self.tasks[index]
                self.update_json()
                self.set_rows()
            except IndexError:
                print('Must select a row')

        def delete_all():
            self.tasks.clear()
            self.update_json()
            self.set_rows()

        def start_task():
            rows = self.tree.selection()
            for row in rows:
                print('starting task')

        def stop_task():
            rows = self.tree.selection()
            for row in rows:
                print('stopping task')
            
        button_container = ttk.Frame(self)
        button_container.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_container, text='Add Task', command=add_task).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container, text='Delete All', command=delete_all).pack(side='left', padx=(2.5, 0))
        ttk.Button(button_container, text='Start', command=start_task).pack(side='right', padx=(2.5, 0))
        ttk.Button(button_container, text='Stop', command=stop_task).pack(side='right', padx=(0, 2.5))

        button_container_center = ttk.Frame(button_container)
        button_container_center.pack(side='bottom')

        ttk.Button(button_container_center, text='Edit', command=edit_task).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container_center, text='Delete', command=delete_task).pack(side='left', padx=(2.5, 0))

    def update_json(self):
        tasks = []
        for task in self.tasks:
            tasks.append(task.data)
        with open('data/tasks.json', 'w') as f:
            json.dump(tasks, f)

    def load_tasks(self):
        self.tasks = []
        with open('data/tasks.json') as f:
            tasks_json = json.load(f)
        for task in tasks_json:
            self.tasks.append(Task(**task))

    def set_rows(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.tasks:
            self.tree.insert('', 'end', values=task.get_description())

class TasksForm(tk.Toplevel):
    def __init__(self, parent, tasks, task=None):
        super().__init__(parent)

        self.resizable(0, 0)

        self.background = ttk.Frame(self)
        self.background.pack(fill='both', expand=1)

        self.parent = parent
        self.tasks = tasks

        self.profile = tk.StringVar()
        self.keywords = tk.StringVar()
        self.size = tk.StringVar()
        self.color = tk.StringVar()
        self.proxy = tk.StringVar()

        self.variables = [self.profile, self.keywords, self.size, self.color, self.proxy]

        if task is not None:
            for i, item in enumerate(self.variables):
                item.set(task.get_description()[i])

        container = ttk.Frame(self.background)

        ttk.Label(container, text='profile').grid(row=0, column=0, sticky='w')
        with open('data/profiles.json') as f:
            profiles_json = json.load(f)
        profiles = [profile['profile_name'] for profile in profiles_json]
        if task is None:
            self.profile.set(profiles[0])
        ttk.OptionMenu(container, self.profile, self.profile.get(), *profiles).grid(row=1, column=0, sticky='ew', columnspan=2)

        ttk.Label(container, text='keywords').grid(row=2, column=0, sticky='w')
        ttk.Entry(container, textvariable=self.keywords).grid(row=3, column=0, sticky='ew', columnspan=2)

        ttk.Label(container, text='size').grid(row=4, column=0, sticky='w', padx=(0, 2.5))
        ttk.Entry(container, textvariable=self.size).grid(row=5, column=0, sticky='w', padx=(0, 2.5))

        ttk.Label(container, text='color').grid(row=4, column=1, sticky='w', padx=(2.5, 0))
        ttk.Entry(container, textvariable=self.color).grid(row=5, column=1, sticky='w', padx=(2.5, 0))

        ttk.Label(container, text='proxy').grid(row=6, column=0, sticky='w')
        proxies = ['None']
        with open('data/proxies.json') as f:
            proxies_json = json.load(f)
        proxies += [proxy['name'] for proxy in proxies_json]
        if task is None:
            self.proxy.set(proxies[0])
        ttk.OptionMenu(container, self.proxy, self.proxy.get(), *proxies).grid(row=7, column=0, sticky='ew', columnspan=2)

        container.pack(padx=20, pady=10)

    def get_vars(self):
        profile_id = -1
        profile_name = self.profile.get()
        with open('data/profiles.json') as f:
            profiles_json = json.load(f)
        for profile in profiles_json:
            if profile['profile_name'] == profile_name:
                profile_id = profile['id']
                break
        proxy_id = -1
        proxy_name = self.proxy.get()
        with open('data/proxies.json') as f:
            proxies_json = json.load(f)
        for proxy in proxies_json:
            if proxy['name'] == proxy_name:
                proxy_id = proxy['id']
                break
        return [profile_id, self.keywords.get(), self.size.get(), self.color.get(), proxy_id]

class AddTasksForm(TasksForm):
    def __init__(self, parent, tasks):
        TasksForm.__init__(self, parent, tasks)

        def add():
            self.tasks.append(Task(*self.get_vars()))
            self.parent.update_json()
            self.parent.set_rows()

        def clear():
            for var in self.variables:
                var.set('')

        button_container = ttk.Frame(self.background)
        button_container.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_container, text='Add', command=add).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container, text='Clear', command=clear).pack(side='left', padx=(2.5, 0))

class EditTasksForm(TasksForm):
    def __init__(self, parent, tasks, task=None, index=0):
        TasksForm.__init__(self, parent, tasks, task=task)
        
        def update():
            self.tasks[index] = Task(*self.get_vars())
            self.parent.update_json()
            self.parent.set_rows()

        def clear():
            for var in self.variables:
                var.set('')

        button_container = ttk.Frame(self.background)
        button_container.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_container, text='Update', command=update).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container, text='Clear', command=clear).pack(side='left', padx=(2.5, 0))