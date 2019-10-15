from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase

class CreateAccountWindow(Screen):
    n = ObjectProperty(None)
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.n.text != "" and self.username.text != "" and self.password != "":
            added = db.add_user(self.username.text, self.password.text, self.n.text)
            if added == 1:
                self.reset()
                sm.current = "login"
            elif added == 2:
                PassTooShort()
            else:
                AccAlreadyExists()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.username.text = ""
        self.password.text = ""
        self.n.text = ""


class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.username.text, self.password.text):
            MainWindow.current = self.username.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.username.text = ""
        self.password.text = ""


class MainWindow(Screen):
    current = ""

    def logOut(self):
        sm.current = "login"


class WindowManager(ScreenManager):
    pass



# Invalid input handling functions
def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username\nor password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Invalid fields. Try again.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

def AccAlreadyExists():
    pop = Popup(title='Invalid Form (User Exists)',
                  content=Label(text='Enter a unique\nUsername.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

def PassTooShort():
    pop = Popup(title='Invalid Form (Password Too Short)',
                  content=Label(text='Password is too short. Try again.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()



kv = Builder.load_file("main.kv")

sm = WindowManager()
db = DataBase("users.db")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()
else:
    print("Some type of error has occurred")