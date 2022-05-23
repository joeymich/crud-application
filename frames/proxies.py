import tkinter as tk
from tkinter import ttk
import json
import random

class Proxy():
    def __init__(self, name='', host='', port='', user='', password='', id=''):
        self.data = {}
        self.data['name'] = name
        self.data['host'] = host
        self.data['port'] = port
        self.data['user'] = user
        self.data['password'] = password
        if id:
            self.data['id'] = id
        else:
            self.data['id'] = self.fetch_id()

    def get_description(self):
        return list(self.data.values())

    def fetch_id(self):
        with open('data/proxies.json') as f:
            all_proxies = json.load(f)
        ids = []
        for proxy in all_proxies:
            if 'id' in proxy:
                ids.append(proxy['id'])
        if ids:
            while True:
                id = random.randrange(0, 999)
                if id not in ids:
                    return id
        else:
            return random.randrange(0, 999)

class ProxiesFrame(ttk.Frame):
    def __init__(self, parent=None, tasks_frame=None):
        super().__init__(parent)

        self.tasks_frame = tasks_frame

        columns = ('name', 'host', 'port', 'user', 'password')

        tree_container = tk.Frame(self)
        tree_container.pack(fill='both', expand=1)

        scroll = ttk.Scrollbar(tree_container, orient='vertical')
        self.tree = ttk.Treeview(tree_container, yscrollcommand=scroll.set, columns=columns, show='headings', height=0)
        scroll.config(command=self.tree.yview)
        scroll.pack(side='right', fill='y')

        for column in columns:
            self.tree.column(column, width=0, anchor='center')
            self.tree.heading(column, text=column)

        self.proxies = []

        self.load_proxies()
        self.set_rows()

        self.tree.pack(fill='both', expand=1)

        def new_proxy():
            AddProxiesForm(self, self.proxies)

        def edit():
            try:
                for row in self.tree.selection():
                    index = self.tree.index(row)
                    selected_proxy = self.proxies[index]
                    EditProxiesForm(self, self.proxies, proxy=selected_proxy, index=index)
            except IndexError:
                print('Must select a row')

        def view():
            pass

        def delete():
            try:
                indexes = []
                for row in self.tree.selection():
                    indexes.append(self.tree.index(row))
                for index in sorted(indexes, reverse=1):
                    del self.proxies[index]
                self.update_json()
                self.set_rows()
                self.tasks_frame.load_tasks()
                self.tasks_frame.set_rows()
            except IndexError:
                print('Must select a row')

        button_container = ttk.Frame(self)
        button_container.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_container, text='Add Proxy', command=new_proxy).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container, text='Edit', command=edit).pack(side='left', padx=2.5)
        ttk.Button(button_container, text='View', command=view).pack(side='left', padx=(2.5, 0))
        ttk.Button(button_container, text='Delete', command=delete).pack(side='right')

    def update_json(self):
        proxies = []
        for proxy in self.proxies:
            proxies.append(proxy.data)
        with open('data/proxies.json', 'w') as f:
            json.dump(proxies, f)

    def load_proxies(self):
        with open('data/proxies.json') as f:
            proxies_json = json.load(f)
        for proxy in proxies_json:
            self.proxies.append(Proxy(**proxy))

    def set_rows(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for proxy in self.proxies:
            self.tree.insert('', 'end', values=proxy.get_description())

class ProxiesForm(tk.Toplevel):
    def __init__(self, parent, proxies, proxy=None, read_only=False):
        super().__init__(parent)

        self.resizable(0, 0)

        self.background = ttk.Frame(self)
        self.background.pack(fill='both', expand=1)

        self.parent = parent
        self.proxies = proxies

        self.name = tk.StringVar()
        self.host = tk.StringVar()
        self.port = tk.StringVar()
        self.user = tk.StringVar()
        self.password = tk.StringVar()
        self.id = ''

        self.variables = [self.name, self.host, self.port, self.user, self.password]

        if proxy is not None:
            for i, item in enumerate(self.variables):
                item.set(list(proxy.data.values())[i])
            self.id = proxy.data['id']

        container = ttk.Frame(self.background)

        ttk.Label(container, text='name').grid(row=0, column=0, sticky='w')
        ttk.Entry(container, textvariable=self.name).grid(row=1, column=0, sticky='ew', columnspan=2)

        ttk.Label(container, text='host').grid(row=2, column=0, sticky='w', padx=(0, 2.5))
        ttk.Entry(container, textvariable=self.host).grid(row=3, column=0, padx=(0, 2.5))

        ttk.Label(container, text='port').grid(row=2, column=1, sticky='w', padx=(2.5, 0))
        ttk.Entry(container, textvariable=self.port).grid(row=3, column=1, padx=(2.5, 0))

        ttk.Label(container, text='user').grid(row=4, column=0, sticky='w', padx=(0, 2.5))
        ttk.Entry(container, textvariable=self.user).grid(row=5, column=0, padx=(0, 2.5))

        ttk.Label(container, text='password').grid(row=4, column=1, sticky='w', padx=(2.5, 0))
        ttk.Entry(container, textvariable=self.password).grid(row=5, column=1, padx=(2.5, 0))

        container.pack(padx=20, pady=10)

    def get_vars(self):
        vars = []
        for var in self.variables:
            vars.append(var.get())
        vars.append(self.id)
        return vars

class AddProxiesForm(ProxiesForm):
    def __init__(self, parent, proxies):
        ProxiesForm.__init__(self, parent, proxies)

        def add():
            self.proxies.append(Proxy(*self.get_vars()))
            self.parent.update_json()
            self.parent.set_rows()

        def clear():
            for var in self.variables:
                var.set('')

        button_container = ttk.Frame(self.background)
        button_container.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_container, text='Add', command=add).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container, text='Clear', command=clear).pack(side='left', padx=(2.5, 0))

class EditProxiesForm(ProxiesForm):
    def __init__(self, parent, profiles, proxy=None, index=0):
        ProxiesForm.__init__(self, parent, profiles, proxy=proxy)

        start_name = proxy.data['name']

        def update():
            self.proxies[index] = Proxy(*self.get_vars())
            self.parent.update_json()
            self.parent.set_rows()
            if self.proxies[index].data['name'] != start_name:
                parent.tasks_frame.load_tasks()
                parent.tasks_frame.set_rows()

        def clear():
            for var in self.variables:
                var.set('')

        button_container = ttk.Frame(self.background)
        button_container.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_container, text='Update', command=update).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container, text='Clear', command=clear).pack(side='left', padx=(2.5, 0))