from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.animation import Animation
import os
import re
import datetime


class RegisterScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class Storage:
    def __init__(self, username, email, password):
        self.username= username
        self.email= email
        self.password= password
        self.store_data()

    def store_data(self):
        creation_date= datetime.datetime.now().date()
        if os.path.exists('db.txt'):
            data= f'{self.username};{self.email};{self.password}_{creation_date}'
            with open('db.txt', 'a') as db:
                db.write(data+"\n")


class MainApp(App):
    his_us=""
    his_em=""
    his_pas=''
    his_date=""
    def build(self):
        Window.size=(360, 640)
        return Builder.load_file('main.kv')

    def on_start(self):
        self.error=self.root.ids.re.ids.slid_up.ids.error
        self.error2=self.root.ids.re.ids.error2

    @staticmethod
    def check_data():
        with open('db.txt', 'r') as f:
            content= f.readlines()
        return content

    def anime(self, w):
        target= self.root.ids.re.ids.slid_up
        if w == 'up':
            an= Animation(loc=1, d=0.5)
        elif w == 'in':
            an= Animation(loc=0.06, d=0.5)
        an.start(target)

    def data_receiver(self, un, em, pas):
        email_pattern= '[A-Z]?\w+@\w+.\w+'
        password_pattern= '\w{,5}\d{,5}'
        check_string= f'{un};{em};{pas}'
        self.content= [line[:line.find('-')].strip() for line in self.check_data()]
        if check_string not in self.content:
            if re.search(email_pattern, em) and re.search(password_pattern, pas):
                store= Storage(un, em, pas)
                self.root.ids.re.ids.slid_up.ids.e1.text=""
                self.root.ids.re.ids.slid_up.ids.e2.text=""
                self.root.ids.re.ids.slid_up.ids.e3.text=""
                self.error.text='account created!'
                self.error.color=[0,1,0,1]
            else:
                self.error.text= 'email or passowrd is incorrect!'
                self.error.color=[1,0,0,1]
        else:
            self.error.text= 'this account is already taken!'
            self.error.color=[0,1,0,1]

    def errorer(self, sc):
        if sc == 's':
            self.error.text='empty feilds are not allowed!'
            self.error.color=[1,0,0,1]
        elif sc == 'l':
            self.error2.text='empty feilds are not allowed!'
            self.error2.color=[1,0,0,1]

    def login(self, login_ur, login_pw):
        data= [l.strip() for  l in self.check_data()]
        if data != []:
            for line in data:
                u_e_p, time= line.split('_')
                u, e, p= u_e_p.split(";")
                if u == login_ur and p == login_pw:
                    self.error2.text= 'available account!'
                    self.error2.color=[0,1,0,1]
                    self.root.ids.re.ids.the_ur.text=''
                    self.root.ids.re.ids.the_pw.text=''
                    self.his_us=u
                    self.his_em=e
                    self.his_pas=p
                    self.his_date=time
                    self.go_to_main()
                    break
                else:
                    self.error2.text= 'account doesn\'t exist!'
                    self.error2.color=[1,0,0,1]
        else:
            self.error2.text= 'you need to sign up first!'
            self.error2.color=[1,0,0,1]

    def go_to_main(self):
        self.root.ids.screen_manager.current= 's2'
        self.root.ids.main_sc.ids.l1.text=f'Username: {self.his_us}'
        self.root.ids.main_sc.ids.l2.text=f'Password: {self.his_pas}'
        self.root.ids.main_sc.ids.l3.text=f'Email: {self.his_em}'
        self.root.ids.main_sc.ids.l4.text=f'Date of creation: {self.his_date}'

    def go_back(self):
        self.root.ids.screen_manager.current= 's1'

if __name__ == '__main__':
    app= MainApp()
    app.run()