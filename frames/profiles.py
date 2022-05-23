import tkinter as tk
from tkinter import ttk
import json
import random

class Profile():
    def __init__(self, profile_name='', name='', email='', phone='', address1='', address2='', zip='', city='', state='', country='', cc_num='', cc_month='', cc_year='', ccv='', id=''):
        self.data = {}
        self.data['profile_name'] = profile_name
        self.data['name'] = name
        self.data['email'] = email
        if len(phone) == 10:
            phone = phone[:3] + '-' + phone[3:6] + '-' + phone[6:]
        self.data['phone'] = phone
        self.data['address1'] = address1
        self.data['address2'] = address2
        self.data['zip'] = zip
        self.data['city'] = city
        self.data['state'] = state
        self.data['country'] = country
        if len(cc_num) == 16:
            cc_num = cc_num[:4] + ' ' + cc_num[4:8] + ' ' + cc_num[8:12] + ' ' + cc_num[12:]
        self.data['cc_num'] = cc_num
        self.data['cc_month'] = cc_month
        self.data['cc_year'] = cc_year
        self.data['ccv'] = ccv
        if id:
            self.data['id'] = id
        else:
            self.data['id'] = self.fetch_id()

    def get_description(self):
        return list(self.data.values())[:4]

    def fetch_id(self):
        with open('data/profiles.json') as f:
            all_profiles = json.load(f)
        ids = []
        for profile in all_profiles:
            if 'id' in profile:
                ids.append(profile['id'])
        if ids:
            while True:
                id = random.randrange(0, 999)
                if id not in ids:
                    return id
        else:
            return random.randrange(0, 999)

class ProfilesFrame(ttk.Frame):
    def __init__(self, parent=None, tasks_frame=None):
        super().__init__(parent)

        self.tasks_frame = tasks_frame

        columns = ('profile name', 'name', 'email', 'phone')

        tree_container = tk.Frame(self)
        tree_container.pack(fill='both', expand=1)

        scroll = ttk.Scrollbar(tree_container, orient='vertical')
        self.tree = ttk.Treeview(tree_container, yscrollcommand=scroll.set, columns=columns, show='headings', height=0)
        scroll.config(command=self.tree.yview)
        scroll.pack(side='right', fill='y')

        for column in columns:
            self.tree.column(column, width=0, anchor='center')
            self.tree.heading(column, text=column)

        self.profiles = []

        self.load_profiles()
        self.set_rows()

        self.tree.pack(fill='both', expand=1)

        def delete():
            try:
                indexes = []
                for row in self.tree.selection():
                    indexes.append(self.tree.index(row))
                for index in sorted(indexes, reverse=1):
                    del self.profiles[index]
                self.update_json()
                self.set_rows()
                self.tasks_frame.load_tasks()
                self.tasks_frame.set_rows()
            except IndexError:
                print('Must select a row')

        def add_new_profile():
            AddProfileForm(self, self.profiles)

        def edit():
            try:
                for row in self.tree.selection():
                    index = self.tree.index(row)
                    selected_profile = self.profiles[index]
                    EditProfileForm(self, self.profiles, profile=selected_profile, index=index)
            except IndexError:
                print('Must select a row')

        def view():
            pass

        button_container = ttk.Frame(self)
        button_container.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_container, text='Add Profile', command=add_new_profile).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container, text='Edit', command=edit).pack(side='left', padx=2.5)
        ttk.Button(button_container, text='View', command=view).pack(side='left', padx=(2.5, 0))
        ttk.Button(button_container, text='Delete', command=delete).pack(side='right')

    def update_json(self):
        profiles = []
        for profile in self.profiles:
            profiles.append(profile.data)
        with open('data/profiles.json', 'w') as f:
            json.dump(profiles, f)

    def load_profiles(self):
        with open('data/profiles.json') as f:
            profiles_json = json.load(f)
        for profile in profiles_json:
            self.profiles.append(Profile(**profile))

    def set_rows(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for profile in self.profiles:
            self.tree.insert('', 'end', values=profile.get_description())

class ProfileForm(tk.Toplevel):
    def __init__(self, parent, profiles, profile=None, read_only=False):
        super().__init__(parent)

        self.resizable(0, 0)

        self.background = ttk.Frame(self)
        self.background.pack(fill='both', expand=1)

        self.parent = parent
        self.profiles = profiles

        self.profile_name = tk.StringVar()
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()
        self.address = tk.StringVar()
        self.address2 = tk.StringVar()
        self.zip = tk.StringVar()
        self.city = tk.StringVar()
        self.state = tk.StringVar()
        self.country = tk.StringVar()
        self.cc_num = tk.StringVar()
        self.month = tk.StringVar()
        self.year =  tk.StringVar()
        self.ccv = tk.StringVar()
        self.id = ''

        self.variables = [self.profile_name, self.name, self.email, self.phone, self.address, self.address2, self.zip, self.city, self.state, self.country, self.cc_num, self.month, self.year, self.ccv]

        if profile is not None:
            for i, item in enumerate(self.variables):
                item.set(list(profile.data.values())[i])
            self.id = profile.data['id']

        tabs = ttk.Notebook(self.background)
        tabs.pack(fill='both', expand=1)
        
        shipping = ttk.Frame(tabs)
        shipping.pack(fill='both', expand=1)

        payment = ttk.Frame(tabs)
        payment.pack(fill='both', expand=1)

        tabs.add(shipping, text='shipping')
        tabs.add(payment, text='payment')

        ttk.Label(shipping, text='profile name').grid(row=0, column=0, sticky='w')
        ttk.Entry(shipping, textvariable=self.profile_name).grid(row=1, column=0, sticky='ew', columnspan=2)

        ttk.Label(shipping, text='name').grid(row=2, column=0, sticky='w')
        ttk.Entry(shipping, textvariable=self.name).grid(row=3, column=0, sticky='ew', columnspan=2)

        ttk.Label(shipping, text='email').grid(row=4, column=0, sticky='w', padx=(0, 2.5))
        ttk.Entry(shipping, textvariable=self.email).grid(row=5, column=0, sticky='w', padx=(0, 2.5))

        ttk.Label(shipping, text='phone').grid(row=4, column=1, sticky='w', padx=(2.5, 0))
        ttk.Entry(shipping, textvariable=self.phone).grid(row=5, column=1, sticky='w', padx=(2.5, 0))

        ttk.Label(shipping, text='address').grid(row=6, column=0, sticky='w', padx=(0, 2.5))
        ttk.Entry(shipping, textvariable=self.address).grid(row=7, column=0, sticky='w', padx=(0, 2.5))

        ttk.Label(shipping, text='apt, unit, etc.').grid(row=6, column=1, sticky='w', padx=(2.5, 0))
        ttk.Entry(shipping, textvariable=self.address2).grid(row=7, column=1, sticky='w', padx=(2.5, 0))

        ttk.Label(shipping, text='city').grid(row=8, column=0, sticky='w', padx=(0, 2.5))
        ttk.Entry(shipping, textvariable=self.city).grid(row=9, column=0, sticky='w', padx=(0, 2.5))

        ttk.Label(shipping, text='zip').grid(row=8, column=1, sticky='w', padx=(2.5, 0))
        ttk.Entry(shipping, textvariable=self.zip).grid(row=9, column=1, sticky='w', padx=(2.5, 0))

        ttk.Label(shipping, text='state').grid(row=10, column=0, sticky='w', padx=(0, 2.5))
        states = ('AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY')
        if profile is None:
            self.state.set(states[0])
        ttk.OptionMenu(shipping, self.state, self.state.get(), *states).grid(row=11, column=0, sticky='ew', padx=(0, 2.5))

        ttk.Label(shipping, text='country').grid(row=10, column=1, sticky='w', padx=(2.5, 0))
        countries = ('USA', 'Canada', 'Mexico')
        if profile is None:
            self.country.set(countries[0])
        ttk.OptionMenu(shipping, self.country, self.country.get(), *countries).grid(row=11, column=1, sticky='ew', padx=(2.5, 0))

        # payment
        ttk.Label(payment, text='credit card number').grid(row=0, column=0, sticky='e')
        ttk.Entry(payment, textvariable=self.cc_num).grid(row=0, column=1, sticky='w')
        
        ttk.Label(payment, text='month').grid(row=1, column=0, sticky='e')
        months = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        if profile is None:
            self.month.set(months[0])
        ttk.OptionMenu(payment, self.month, self.month.get(), *months).grid(row=1, column=1, sticky='w')
        
        ttk.Label(payment, text='year').grid(row=2, column=0, sticky='e')
        years = ('2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032')
        if profile is None:
            self.year.set(years[0])
        ttk.OptionMenu(payment,  self.year, self.year.get(), *years).grid(row=2, column=1, sticky='w')

        ttk.Label(payment, text='ccv').grid(row=3, column=0, sticky='e')
        ttk.Entry(payment, textvariable=self.ccv).grid(row=3, column=1, sticky='w')

        # # TODO: add functionality
        # if read_only:
        #     pass

    def get_vars(self):
        vars = []
        for var in self.variables:
            vars.append(var.get())
        vars.append(self.id)
        return vars

class AddProfileForm(ProfileForm):
    def __init__(self, parent, profiles):
        ProfileForm.__init__(self, parent, profiles)
        
        def add():
            self.profiles.append(Profile(*self.get_vars()))
            self.parent.update_json()
            self.parent.set_rows()

        def clear():
            for var in self.variables:
                var.set('')

        button_container = ttk.Frame(self.background)
        button_container.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_container, text='Add', command=add).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container, text='Clear', command=clear).pack(side='left', padx=(2.5, 0))

class EditProfileForm(ProfileForm):
    def __init__(self, parent, profiles, profile=None, index=0):
        ProfileForm.__init__(self, parent, profiles, profile=profile)

        start_name = profile.data['profile_name']

        def update():
            self.profiles[index] = Profile(*self.get_vars())
            self.parent.update_json()
            self.parent.set_rows()
            if self.profiles[index].data['profile_name'] != start_name:
                parent.tasks_frame.load_tasks()
                parent.tasks_frame.set_rows()

        def clear():
            for var in self.variables:
                var.set('')

        button_container = ttk.Frame(self.background)
        button_container.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_container, text='Update', command=update).pack(side='left', padx=(0, 2.5))
        ttk.Button(button_container, text='Clear', command=clear).pack(side='left', padx=(2.5, 0))