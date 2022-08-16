from kivymd.app import MDApp
from kivy.lang import Builder













Main ="""
MDScreen:
    name: "Main"
    MDBottomNavigation:
        pannel_colour: '0,1,0,1'
        MDBottomNavigationItem:
            name: 'screen 1'
            text: "Python"
            icon: 'language-python'
            MDLabel: 
                text: "hi"
                halign: "center"               
        MDBottomNavigationItem:
            name: 'screen 2'
            text: "Java"
            icon: 'android'
            MDLabel:
                text: "world"
                halign : 'center'
        MDBottomNavigationItem:
            name: 'screen 3'
            text: "Swift"
            icon: 'apple'
            MDLabel:
                text: "hello"
                halign : 'center'
         



"""


   



class Myapp(MDApp):
    def build(self):
        screen = Builder.load_string(Main)
        # sm.add_widget(Builder.load_string(Splash))
        return screen
    #     Clock.schedule_once(self.home, 10)

    # def home(self, dt):
    #     sm.current = "Main"
    


Myapp().run() 
