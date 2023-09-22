import os
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FallOutTransition
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivy_garden.mapview import MapView,MapMarker
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from googletrans import Translator
from kivymd.uix.textfield import MDTextField
import threading
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from kivy.clock import Clock
import pygame
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivymd.uix.card import MDCard
from googletrans import LANGUAGES
from kivy.uix.anchorlayout import AnchorLayout
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDFloatingActionButton
from kivy.lang import Builder
from googletrans.models import Translated
import time
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import datetime


kivy.require('1.11.1')

class TranslatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'voice'
        start_point_box = BoxLayout(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            padding=(2, 2, 2, 2),
            spacing=2
        )
        self.input_lang = MDTextField(
            hint_text="Enter your first Language",
                        mode = "rectangle",
                        icon_right = "microphone",
                        pos_hint = {"center_x": 0.5, "center_y": 0.5},
                        size_hint = (0.8, None),
                        height = dp(48)
        )
        start_point_box.add_widget(self.input_lang)
        end_point_box = BoxLayout(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            padding=(2, 2, 2, 2),
            spacing=2
        )
        self.output_lang = MDTextField(
            hint_text="Enter your second Language:",
            mode="rectangle",
            icon_right="microphone",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, None),
            height=dp(48)
        )
        end_point_box.add_widget(self.output_lang)
        self.icon = MDIconButton(icon="microphone", pos_hint={'center_x': 0.5, 'center_y': 0.4},theme_text_color='Custom',text_color=(1,1,1,1),md_bg_color=(0, 0, 0, 1))
        button = MDIconButton(icon='arrow-left', pos_hint={'center_x': 0.06, 'center_y': 0.95},
                                 size_hint_x=None, width=300)
        self.recognized_label = MDLabel(text="Recognized Text:", pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.recognized_label.font_name = 'Poppins-SemiBold.ttf'

        self.add_widget(self.recognized_label)
        self.translated_label = MDLabel(text="Translated Text:", pos_hint={'center_x': 0.5, 'center_y': 0.1})
        self.translated_label.font_name = 'Poppins-SemiBold.ttf'
        self.add_widget(self.translated_label)
        button.bind(on_press=self.back)
        self.add_widget(button)
        self.icon.bind(on_press=self.start_listening)
        self.add_widget(self.icon)
        self.add_widget(start_point_box)
        self.add_widget(end_point_box)

    def start_listening(self, *args):
        self.icon.disabled = True
        thread = threading.Thread(target=self.process_voice)

        thread.start()

        # here below i can set the timer for duration of mic listening
        threading.Timer(10, self.stop_listening).start()

    def stop_listening(self):
        self.icon.disabled = False  # Enable the button after recording
        self.icon.unbind(on_press=self.stop_listening)
        self.icon.bind(on_press=self.start_listening)

    def process_voice(self):
        recognizer = sr.Recognizer()
        print('speak now:')

        with sr.Microphone() as source:
            audio = recognizer.listen(source, phrase_time_limit=10)

        try:
            text = recognizer.recognize_google(audio, language=self.input_lang.text)
            self.recognized_label.text = "Recognized Text: " + text
        except sr.UnknownValueError:
            self.recognized_label.text = "Speech recognition could not understand audio"
        except sr.RequestError as e:
            self.recognized_label.text = "Could not request results from speech recognition service; {0}".format(e)

        else:
            if text:
                Clock.schedule_once(lambda dt: self.update_translation(text))
        print(threading.active_count())
        print(threading.enumerate())

    def update_translation(self, text):
        translator = Translator()
        translation = translator.translate(text, dest=self.output_lang.text)
        self.translated_label.text = "Translated Text: " + translation.text
        converted_audio = gTTS(text=translation.text, lang=self.output_lang.text)
        audio_path = "hello.mp3"
        converted_audio.save(audio_path)

        pygame.mixer.init()

        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(audio_path)
        print(threading.active_count())
        print(threading.enumerate())

    def back(self, *args):
        self.manager.current = 'main'



class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'map'
        layout = FloatLayout()
        mapview = MapView(lon=78.476, lat=17.3850, zoom=8)
        marker = MapMarker(lat=17.3850, lon=78.476)
        mapview.add_widget(marker)
        layout.add_widget(mapview)
        self.add_widget(layout)
        back_button = MDRectangleFlatButton(text='Back')
        back_button.bind(on_press=self.back)
        self.add_widget(back_button)

    def back(self,*args):
        self.manager.current = 'main'



class AppScreen(Screen):
    def __init__(self, **kwargs):
        super(AppScreen, self).__init__(**kwargs)
        self.name = 'icon'
        layout = FloatLayout()
        self.image = Image(source='pngicon.png', size_hint=(None, None),
                           size=(100, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.image)
        self.add_widget(layout)

    def on_enter(self, *args):
        self.zoom_in_animation()

    def zoom_in_animation(self):
        start_size = (100, 100)
        target_size = (500, 500)
        start_pos = (Window.width / 2 - start_size[0] / 2, Window.height / 2 - start_size[1] / 2)
        target_pos = (Window.width / 2 - target_size[0] / 2, Window.height / 2 - target_size[1] / 2)

        self.image.size = start_size
        self.image.pos = start_pos

        anim = Animation(size=target_size, pos=target_pos, duration=2, t='out_quad')
        anim.start(self.image)
        anim.bind(on_complete=self.change_screen)

    def change_screen(self, *args):
        self.manager.current = 'main'

    def clear_screen(self):
        self.manager.clear_widgets()




class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")

        wellabel = MDLabel(text='Welcome to\nSITI EXPRESS', pos_hint={'center_x': 0.56, 'center_y': 0.92})
        wellabel.font_name = 'Poppins-Bold'
        wellabel.font_size = '23sp'
        self.add_widget(wellabel)

        quolabel = MDLabel(text="<-- Let's Start the Journey -->", pos_hint={'center_x': 0.59, 'center_y': 0.09})
        quolabel.font_name = 'Poppins-Italic'
        quolabel.font_size = '20sp'
        self.add_widget(quolabel)

        glayout = GridLayout(cols=2, spacing="20dp", padding="20dp", pos_hint={'center_x': 0.5, 'center_y': 0.5})
        glayout.size_hint_y = None
        glayout.bind(minimum_height=glayout.setter("height"))

        card1 = MDCard(orientation="vertical", padding="8dp", size_hint=(1, None), height=dp(210),
                       elevation=3, ripple_behavior=True, ripple_color=get_color_from_hex("4DD0E1"),
                       on_release=self.switch_screen2)

        b1 = BoxLayout(orientation="vertical")
        a1 = AnchorLayout(anchor_x='center', anchor_y='top')
        image = Image(
            source="number.jpg",
            size_hint=(None, None),
            size=("110dp", "110dp")
        )
        a1.add_widget(image)

        label1 = MDLabel(text="Search by\nBus number",
                         size_hint=(1, None),
                         pos_hint={'center_x': 0.5, 'center_y': 0.2},
                         height="70dp"
                         )
        label1.font_name = 'Poppins-Bold.ttf'
        label1.font_size = "15sp"
        b1.add_widget(a1)
        b1.add_widget(label1)
        card1.add_widget(b1)
        glayout.add_widget(card1)

        card10 = MDCard(orientation="vertical", padding="8dp", size_hint=(1, None), height=dp(210),
                        elevation=3, ripple_behavior=True, ripple_color=get_color_from_hex("4DD0E1"),
                        on_release=self.switch_screen1)
        b2 = BoxLayout(orientation="vertical")
        a2 = AnchorLayout(anchor_x='center', anchor_y='top', pos_hint={'center_y': 1})
        image = Image(
            source="name.jpg",
            size_hint=(None, None),
            size=("110dp", "110dp")
        )
        a2.add_widget(image)

        label1 = MDLabel(text=" Search by\n Start Point &\n End Point",
                         pos_hint={'center_x': 0.5, 'center_y': 0.2},
                         size_hint=(1, None),
                         height="70dp",
                         )
        label1.font_name = 'Poppins-Bold.ttf'
        label1.font_size = "15sp"
        b2.add_widget(a2)
        b2.add_widget(label1)
        card10.add_widget(b2)
        glayout.add_widget(card10)

        card11 = MDCard(orientation="vertical", padding="8dp", size_hint=(1, None), height=dp(210),
                        elevation=3, ripple_behavior=True, ripple_color=get_color_from_hex("4DD0E1"),
                        on_release=self.voice)
        b11 = BoxLayout(orientation="vertical")
        a11 = AnchorLayout(anchor_x='center', anchor_y='top', pos_hint={'center_y': 1})
        image = Image(
            source="google.png",
            size_hint=(None, None),
            size=("110dp", "110dp")
        )
        a11.add_widget(image)

        label11 = MDLabel(text="Translator",
                          pos_hint={'center_x': 0.5, 'center_y': 0.2},
                          size_hint=(1, None),
                          height="70dp",
                          )
        label11.font_name = 'Poppins-Bold.ttf'
        label11.font_size = "15sp"
        b11.add_widget(a11)
        b11.add_widget(label11)
        card11.add_widget(b11)
        glayout.add_widget(card11)

        card12 = MDCard(orientation="vertical", padding="8dp", size_hint=(1, None), height=dp(210),
                        elevation=3, ripple_behavior=True, ripple_color=get_color_from_hex("4DD0E1"),
                        on_release=self.map)
        b12 = BoxLayout(orientation="vertical")
        a12 = AnchorLayout(anchor_x='center', anchor_y='top', pos_hint={'center_y': 1})
        image = Image(
            source="map.png",
            size_hint=(None, None),
            size=("110dp", "110dp")
        )
        a12.add_widget(image)

        label12 = MDLabel(text="Map Navigation",
                          pos_hint={'center_x': 0.5, 'center_y': 0.2},
                          size_hint=(1, None),
                          height="70dp",
                          )
        label12.font_name = 'Poppins-Bold.ttf'
        label12.font_size = "15sp"
        b12.add_widget(a12)
        b12.add_widget(label12)
        card12.add_widget(b12)
        glayout.add_widget(card12)

        self.add_widget(glayout)

        self.layout = BoxLayout(orientation='vertical')
        self.button = MDRectangleFlatButton(text='Give Feedback', pos_hint={'center_x': 0.8, 'center_y': 0.1},
                                            text_color=(0, 0, 0, 1),
                                            line_color=(0, 0, 0, 1), line_width=2,
                                            on_press=self.go_to_feedback_screen)
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)

    def go_to_feedback_screen(self, instance):
        self.manager.current = 'feedback'

    def switch_screen1(self, instance):
        self.manager.current = 'screen_for_sp_ep'

    def switch_screen2(self, instance):
        self.manager.get_screen('screen_for_bus_number').clear_input_fields()
        self.manager.get_screen('results_for_bus_number').clear_labels()
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'screen_for_bus_number'

    def voice(self, *args):
        self.manager.current = 'voice'

    def map(self, *args):
        self.manager.current = 'map'



class FeedbackScreen(Screen):
    def __init__(self, **kwargs):
        super(FeedbackScreen, self).__init__(**kwargs)


        self.name_input = MDTextField(hint_text='Name',
                                      size_hint=(0.8, None),
                                      height="48dp",
                                      pos_hint={'center_x': 0.5,'center_y': 0.9}
                                      )
        self.gmail_input = MDTextField(hint_text='Gmail Address',
                                       size_hint=(0.8, None),
                                       height="48dp",
                                       pos_hint={'center_x': 0.5,'center_y': 0.7}
                                       )
        self.feedback_input = MDTextField(hint_text='Feedback',
                                          mode="rectangle",
                                          height=dp(50),
                                          size_hint=(0.8, None),
                                          pos_hint={'center_x': 0.5,'center_y': 0.5}
                                          )

        self.submit_button = MDRectangleFlatButton(text='Submit',pos_hint = {'center_x': 0.5, 'center_y': 0.3},
                                                   text_color=(0, 0, 0, 1),
                                                   line_color=(0, 0, 0, 1),
                                                   line_width=2,
                                                   on_press=self.submit_feedback
                                                   )
        self.back_button = MDRectangleFlatButton(text='Back to Home Screen',pos_hint = {'center_x': 0.5, 'center_y': 0.2},
                                                 text_color=(0, 0, 0, 1),
                                                 line_color=(0, 0, 0, 1),
                                                 line_width=2,
                                                 on_press=self.go_to_home_screen
                                                 )

        self.add_widget(self.name_input)
        self.add_widget(self.gmail_input)
        self.add_widget(self.feedback_input)
        self.add_widget(self.submit_button)
        self.add_widget(self.back_button)


    def submit_feedback(self, instance):
        name = self.name_input.text
        gmail = self.gmail_input.text
        feedback = self.feedback_input.text

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"feedback_{timestamp}.txt"

        with open(filename, 'w') as file:
            file.write(f"Name: {name}\n")
            file.write(f"Gmail Address: {gmail}\n")
            file.write(f"Feedback: {feedback}\n")

        self.name_input.text = ''
        self.gmail_input.text = ''
        self.feedback_input.text = ''

    def go_to_home_screen(self, instance):
        self.manager.current = 'main'



class RoundedBoxLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.md_bg_color = [1, 1, 1, 1]
        self.size_hint_y = None
        self.adaptive_height = True
        self.radius = [50, 50, 0, 0]
        self.padding = [0, 0, 0, 90]


# SECOND SCREEN
class Screen_for_sp_ep(MDScreen):
    def __init__(self, **kwargs):
        super(Screen_for_sp_ep, self).__init__(**kwargs)
        self.md_bg_color = (1,1,1,1)
        self.layout = FloatLayout()
        alabel = MDLabel(text='Where would You Like to go' ,pos_hint={'center_x' :0.55 ,'center_y' :0.9})
        alabel.font_name = 'Poppins-SemiBold.ttf'
        alabel.font_size = '23sp'
        self.add_widget(alabel)
        blabel = MDLabel(text='Today?' ,pos_hint={'center_x' :0.55 ,'center_y' :0.9})
        blabel.font_name = 'Poppins-Bold.ttf'
        blabel.font_size = "25"
        self.add_widget(blabel)
        hyderabad_lat = 17.385044
        hyderabad_lon = 78.486671
        zoom_level = 13
        mapview = MapView(lat=hyderabad_lat,
                          lon=hyderabad_lon,
                          zoom=zoom_level,
                          pos_hint={'center_x': 0.5, 'center_y': 0.8},
                          size_hint=(1.5, 0.7)
                          )
        self.layout.add_widget(mapview)
        rounded_box_layout = RoundedBoxLayout(pos_hint={'center_x' :0.5 ,'center_y' :0.5})
        rounded_box_layout.md_bg_color = (1,1,1,1)
        self.layout.add_widget(rounded_box_layout)
        buttonback = MDFloatingActionButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.13, "center_y": 0.94},
            size_hint=(None, None),
            size=(48, 48),
            md_bg_color=(0, 0, 0, 1)
        )
        buttonback.bind(on_release=self.back)
        self.layout.add_widget(buttonback)
        layout3 = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(200), dp(200)))
        layout3.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.layout.add_widget(layout3)

        start_point_box = BoxLayout(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.38},
            padding=(2, 2, 2, 2),
            spacing=2
        )
        self.start_point_input = MDTextField(
            hint_text="Enter the Start point",
                        mode = "rectangle",
                        icon_right = "magnify",
                        pos_hint = {"center_x": 0.5, "center_y": 0.5},
                        size_hint = (0.8, None),
                        height = dp(48),

        )
        start_point_box.add_widget(self.start_point_input)
        self.layout.add_widget(start_point_box)
        end_point_box = BoxLayout(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            padding=(2, 2, 2, 2),
            spacing=2
        )
        self.end_point_input = MDTextField(
            hint_text="Enter the End point:",
            mode="rectangle",
            icon_right="magnify",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, None),
            height=dp(48),

        )
        end_point_box.add_widget(self.end_point_input)
        self.layout.add_widget(end_point_box)
        search_button = MDRectangleFlatButton(text='Search', pos_hint={'center_x': 0.5, 'center_y': 0.1} ,text_color=(0 ,0 ,0 ,1)
                                              ,line_color=(0 ,0 ,0 ,1) ,line_width=2)
        search_button.bind(on_release=self.search)
        self.layout.add_widget(search_button)
        self.add_widget(self.layout)

    def back(self,*args):
        self.manager.current = 'main'

    def clear_input_fields(self):
        self.start_point_input.text = ""
        self.end_point_input.text = ""

    def switch_screen(self, *args):
        self.manager.current = 'main'

    bus_routes_for_sp_ep = {"25s": ["Suchitra", "Suchitra X Road", "Loyola college", "BHEL quarters", "PV junction Bus Stop",
                            "Father balaiah nagar", "Old alwal (IG Statue)", "Old alwal Bus Stop",
                              "Temple alwal Bus Stop", "Alwal police Station Bus Stop", "Alwal bus stop",
                              "Ram nagar–Alwal", "Lothkunta bus Stop", "Family quarter"
                                , "EME bus stop", "Lalbazar",
                              "Tirumalgherry bus Stop", "Trimulgherry X Roads", "RTO trimulgherry", "Tirumalagiri",
                              "Karkhana Temple Arch", "Vikarampuri", "HPS High School", "Patny",
                              "Patny center", "Clock tower", "Secunderabad Junction"],
                "227": ["Bhadurpally X Roads", "Bhadurpally village", "Maisammaguda","Appreal Park ", "Dulapally","Kompally","Prajay",
                       "NCL north avenue","Balaji hospital","Angadipet","Jeedimetla ","Suchitra circle","Dairy farm","M.M.R.Gardens",
                        "Bowenpally Checkpost", "Bowenpally Police Station","Tadbund","Paradise","Patny",
                        "Clock tower","Secunderabad junction"],
                "1D": ["Dilsukhnagar bus Station (Opposite Side)", "T.V.Tower / Moosaram Bagh", "Malakpet super Bazar", "Malakpet chermas",
                      "Yashoda hospital","Chaderghat","Koti womens College","Koti maternity Hospital","Sultan bazar",
                      "Ram koti Bus Stop","Blood bank","Y.M.C.A.","Narayanaguda","Narayanaguda","RTC X road","Golconda X roads",
                      "Musheerabad police Station","Gandhi hospital bus stop","Bhoiguda","Secunderabad/Chilkalguda circle Bus Stop",
                      "Secunderabad rathifile bus station"],
                "1Z/229": ["Medchal bus terminal","Medchal Ambedkar Chowrasta","Medchal chekpost","Cmr college",
                          "Kandlakoya bus stop","Prestige","Gundla pochampally","Kompally","Dollapally X Road","Prajay",
                          "Cine planet kompally","NCL north avenue","Angadipeta","Jeedimetla ","Suchitra circle","Dairy farm","M.M.R.Gardens","Bowenpally Checkpost",
                       "Bowenpally Police Station","Tadbund","Paradise","Mahatma gandhi road,125","Ranigunj bus stop",
                         "Boats club bus stop","DBR mills","Tank bund","Mini tankbund","Secretariat",
                          "Accountant general(A & G)Office/Birla Mandir","Assembly","Nampally grand plaza","Nampally",
                          "Nampally haj house","Gandhi Bhavan","Mozamjahi market(Gandhi Bhavan)","Osmangunj","Afzalgunj Bus Station",
                         "Nayapul","Madina","City college","Petla burj","Puranapool out post","Puranapool mastan gati",
                          "Bahadurpura police station","Bahadurpura","Nehru Zoological Park","Thadban","Mir alam tank filter beds",
                           " Danama jhopdi","Hasan nagar","Raghavendra colony","Sardar Vallabhbhai Patel National Police Academy","Aramghar X Roads" ],
                 "1V": ["Secunderabad rathifile bus station","Gandhi hospital bus stop","Raja delux","Chikkadpally bus stop",
                       "YMCA","Kachiguda","Ram koti bus stop","Koti maternity Hospital","Chaderghat bus stop","Yashoda hospital",
                       "Malakpet super bazar","TV tower/Moosaram bagh","Dilsukhnagar","Chaitanyapuri","Kothapet","Doctors colony bus stop",
                       "LBNagar metro station","LB nagar","Chintalkunta bus stop","Vishnu theatre","Ganesha temple",
                        "Red tank bus stop","NGO's Colony"],
                  "1J": ["Secunderabad rathifile bus station","Gandhi hospital bus stop","Raja delux","Chikkadpally bus stop",
                        "Narayanaguda","YMCA","Kachiguda X Road","Koti maternity Hospital","Koti womens college",
                        "Chaderghat","Central bus station(C.B.S.)","Afzalgunj central library","Osmania hospital",
                         "Jumerat bazar","Dhoolpet","Bheem nagar","Jiyaguda","Cargil Nagar","Jiyaguda Kht"],
                  "1D/V": ["NGOS colony","Vaidehi Nagar","Gauthami nagar bus stop","Vanasthalipuram","Complex vanasthalipuram",
                          "Ganesh Temple","	Panama Godowns","Vishnu theatre","Chinthalkunta Bus Stop",
                           "Old chintalkunta checkpost","LB nagar","LB nagar Metro station","Doctors colony bus stop",
                          "Green Hills Colony","Ashta Lakshmi Bus Stop","Kothapet bus stop","Fruit Market/Shalini Theatre",
                          "Chaitanyapur","Dilsukhnagar","Moosarambagh","Super bazar bus stop","Malakpet",
                           "Yashoda hospital bus stop","Nalgonda X Road","Chaderghat bus stop","Koti womens college",
                           "Koti Maternity Hospital","Sultan bazar bus stop","Ram koti bus stop","Kachiguda X Road",
                          "Kachiguda","YMCA","Narayanaguda bus stop","Chikkadpally bus stop","Musheerabad bus stop",
                          "Golconda X Road","Raja delux bus stop","Musheerabad","Gandhi hospital",
                          "Bhoiguda west bus stop","Chilkalguda circle bus stop","Rathifile bus station"],
                   "5K/188": ["Kalimandir","Bandlaguda","Suncity","Sai Ram Nagar(Langar House)","Bapu Ghat",
                             "Bapu Nagar","Langar House Bus Stop","Nanalnagar Bus Stop","Rethibowli","Mehdipatnam Bus Stop",
                              "Sarojini Bus Stop"," Nmdc Bus Stop","Golconda Hotel","Masab Tank Bus Stop","Mahavir Hospital",
                              "Lakdikapool Bus Stop"," Ranigunj Bus Stop","Bible House","Bata(Rp Road)" ,"James Street",
                             "Mahaboob College","Patny","Clock Tower"," Secunderabad Junction"],
                   "5K": ["Secunderabad rathifile bus station","Clock tower","Patny ","Bata","Bible house","Boats club","Tank bund",
                         "DBR Mills","Secretariat","Telephone bhavan","Saifabad","Lakdikapul Metro station","Ac guards",
                         "Masab tank puspak","Mahavir bus stop","Golconda hotel","Potti sriramulu nagar bus stop",
                         "Masab Tank","NMDC bus stop","Sarojini devi eye hospital","Mehdipatnam bus stop"],
                   "5R": ["Kowkoor","Water tank","Risala bazar","Sadhana Mandir","Bollaram","Raithu bazar","Alwal bus station",
                         "Ram nagar alwal","Lothkunta bus stop","Maruti nagar","Family quarter bus stop","Eme bus stop",
                          "Lalbazar","Tirumalgherry bus stop","Hanuman temple(Tirumalgherry)","Karkhana temple arch",
                         "Karkhana","Vikrampuri","Jubilee Bus Station","Patny","Bata","Bible house","Boats club","Tank bund",
                         "DBR Mills","Secretariat","Telephone bhavan","Saifabad","Lakdikapul Metro station","Ac guards",
                         "NMDC bus stop","Sarojini devi eye hospital","Mehdipatnam bus stop"],
                   "5K/92": ["Rajendra nagar bus stop","Extension Education Institute (EEI)","Budvel bus stop",
                            "Dairy farm bus stop","Happy home bus stop","Upperpally X Road","Shiva nagar",
                            "Hyderguda X Road","Attapur X Road","Laxmi nagar","Rethibowli","Mehdipatnam corner",
                            "Sarojini Devi Eye hospital","NMDC bus stop","Masab Tank","Ac Guards",
                             "Lakdikapol Metro station","Secunderabad rathifile bus station","Clock towe","Patny ",
                             "Bata","Bible house","Boats club","Tank bund", "DBR Mills"],
                    "5M": ["Secunderabad rathifile bus station","Clock tower","Patny ","Bata","Bible house","Boats club","Tank bund",
                         "DBR Mills","Secretariat","Telephone bhavan","Lakdikapul Metro station","Ac guards",
                         "Masab tank","Vijay nagar colony","Mallepally chowk","Asif nagar","Amba theatre","Mehdipatnam bus station"],
                    "10KM/224G": ["Secunderabad raithfile bus stop","Parade ground Metro station","Paradise Metro station",
                                 "Yatri nivas/Anand theatre","Begumpet police line","Begumpet/Prakash nagar","Rasoolpura",
                                 "Begumpet","Begumpet bus stop","Begumpet Railway station north","Greenlands bus stop",
                                 "Lal Bungalow ameerpet","Sheeshmahal Bus Stop","Satyam Theatre Cross Roads","Mythrivanam",
                                 "SR Nagar","ESI hospital","ESI hospital Metro Station","Erragadda FCI","Erragadda","Prem nagar",
                                 "Bharat Nagar","Moosapet Bus Stop","Kukatpally Bus Depot","Kukatpally Y Junction",
                                  "Kukatpally Bus Stop","Vivekanadanagar Colony Rdr Hospital","KPHB","JNTU","Nizampet X Roads",
                                 "Vasanth Nagar","Hydernagar Bus Stop","Hyder Nagar","Miyapur Metro Station","Miyapur X Roads",
                                 "B.K. Enclave","Aparna Company","Kousalya Colony","Bachupally","Vignan Jyothi College",
                                 "Pragathi Nagar Bus Stop","Bowram Pet","Bowram Pet Chowrasta","Bowrampet Maisamma Temple",
                                 "Gandi maisamma"],
                     "10H": ["Secunderabad bus station(Gurudwara)","Clock Tower","Patny","Swapnalok Complex","Paradise Metro Station",
                            "Yatri Nivas /Anand Theatre","Begumpet Police Line","Prakash Nagar","Begumpet","Begumpet Bus Stop",
                            "Begumpet Railway Station North","Greenlands Bus Stop","Lal Bungalow Ameerpet","Sheeshmahal Bus Stop",
                            "Satyam Theatre Cross Roads","Yousufguda Checkpost","Srinagar X Road / Indira Nagar X Road","Venkatagiri",
                            "Road Number 1","Jubilee Check Post","Peadamma Temple","Rainbow Park","Live Life Hospital",
                            "Madhapur Police Station Bus Stop","Madhapur Timber Depot","Hitech City","Shilparamam Bus Stop",
                            "Hitech City Bus Stop","Kondapur","Kothaguda X Roads","Kondapur Bus Depot"],
                     "10": ["Secunderabad Railway Station","Secunderabad bus station(Gurudwara)","Clock Tower","Patny","Swapnalok Complex","Paradise Metro Station",
                            "Yatri Nivas /Anand Theatre","Begumpet Police Line","Rasoolpura", "Begumpet","Begumpet bus stop",
                            "Begumpet Railway station north","Greenlands bus stop","Lal Bungalow ameerpet","Sheeshmahal Bus Stop",
                            "Ameerpet","Mythrivanam","SR nagar","ESI hospital Metro Station","Erragadda FCI","Erragadda",
                            "Sanath Nagar Police Station","Sanath Nagar","Sanath Nagar Bus Depot"],
                     "10F": ["Secunderabad Railway Station","Secunderabad bus station(Gurudwara)","Clock Tower","Paradise Metro Station",
                            "Yatri nivas/Anand theatre","Begumpet police line","Begumpet/Prakash nagar","Rasoolpura","Begumpet",
                            "Begumpet bus stop","Begumpet Railway station north","Greenlands bus stop",
                            "Lal Bungalow ameerpet","Sheeshmahal Bus Stop","Satyam Theatre Cross Roads","Mythrivanam",
                            "SR Nagar","ESI hospital","ESI hospital Metro Station","Erragadda FCI","Erragadda","Prem nagar",
                            "Mothi Nagar","Borabanda Bus Station"],
                     "10JP": ["Kukatpally Bus Depot","Kukatpally Y Junction","Sangeeth Nagar","Kukatpally Bus Stop",
                             "Sumithra Nagar Bus Stop","Vivekanadanagar Colony Rdr Hospital","Food World","KPHB","JNTU",
                             "Nizampet X Roads","JNTU college","Nizampet Village","Kesenaris","Rajiv Gandhi Nagar",
                             "Rajeev Gandhi Nagar 2","Bachupally"],
                     "10HA": ["Allwyn Colony Bus Stop","Jagadgiri Gutta Bus Stop","Papi Reddy Nagar","Gandhi Nagar Bus Stop",
                             "Giri Nagar","IDPL Bus Stop","Balanagar Bus Stop","Shobana","Ferozeguda","New Bowenpally Bus Stop",
                             "Chinnathokata","Tadbund Bus Stop","Sikh Village Rd","	Paradise Bus Stop","patny","Clock Tower",
                             "Secunderabad Junction"],
                     "10KJ": ["Jagadgiri Gutta Bus Stop","Pragathi Nagar Bus Stop","Asbestas Colony Bus Stop","Kukatpally Bus Stop",
                             "Moosapet Bus Stop","Bharat Nagar(Moosapet) Bus Stop","Erragadda","ESI Bus Stop","S R Nagar",
                             "Mytrivanam","Ameerpet Bus Station","Sheeshamahal","Greenlands","Begumpet Railway Station",
                             "Prakash Nagar Bus Stop","Rasoolpura","Police Lines-Begumpet Bus Stop","Anand Theatre","Paradise Bus Stop",
                             "patny","Clock tower","Secunderabad Junction"],
                     "10KM": ["Secunderabad raithfile bus stop","Parade ground Metro station","Paradise Metro station",
                                 "Yatri nivas/Anand theatre","Begumpet police line","Begumpet/Prakash nagar","Rasoolpura",
                                 "Begumpet","Begumpet bus stop","Begumpet Railway station north","Greenlands bus stop",
                                 "Lal Bungalow ameerpet","Sheeshmahal Bus Stop","Satyam Theatre Cross Roads","Mythrivanam",
                                 "SR Nagar","ESI hospital","ESI hospital Metro Station","Erragadda FCI","Erragadda","Prem nagar",
                                 "Bharat Nagar","Moosapet Bus Stop","Kukatpally Bus Depot","Kukatpally Y Junction",
                                  "Kukatpally Bus Stop","Vivekanadanagar Colony Rdr Hospital","KPHB","JNTU","Nizampet X Roads",
                                 "Vasanth Nagar","Hydernagar Bus Stop","Hyder Nagar","Miyapur Metro Station","Miyapur X Roads",],
                     "24B/281": ["Secunderabad/Chilkalguda Circle","Alugadda Baavi South Bus Stop","Mettuguda","Tarnaka Uppal Stop",
                                 "Habsiguda","National Geophysical Research Institute (N.G.R.I)","Survey Of India","Uppal Sub Station",
                                 "Uppal Bus Station","Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot","Medipally",
                                 "Central Power Research Institute","Narapally","Vijaypuri Colony","Jodimetla X Road","Annojiguda",
                                 "Shiva Reddy Guda Bus Stop","Ghatkesar Bus Stop"],
                      "24": ["Secunderbad junction","Patny","Vikrampur bus stop","Hanuman temple(Tirumalagiri)","Tirumalagiri bus stop",
                            "Lalbazar","Lalbazar circle","Nagmandir","CTW bus stop","EME center","Ammuguda Bazar",
                             "Yapral water tank bus stop","Yapral bus stop"],
                       "24S/273": ["Gandimaisamma","Bahadurpally X Roads","Bahadurpally","Maisammaguda","Dulapally","Dollapally X Road",
                                  "Prajay","NCL North Avenue","Balaji Hospital","Angadipeta","Jeedimetla ","Suchitra circle","Suchitra X Road",
                                  "Loyola College","Bhel Quarters","Pv Junction Bus Stop","Father Balaiah Nagar","Ig Statue","Old Alwal",
                                  "Temple Alwal","Alwal Police Station","Alwal Bus Stop","Ram Nagar","Lothkunta Bus Stop",
                                  "Family Quarter Bus Stop","Eme Bus Stop","Lalbazar","Lalbazar circle","Kv School X Road","Rk Puram Bridge",
                                  "Gk Colony","Neredmet Cross Road, 599","Vayupuri","Sainikpuri","Officer’S Colony",
                                  "Doctor As Rao Nagar Road","A.S. Rao Nagar","North Kamala Nagar","ECIL X Roads"],
                        "24B": ["Secunderbad junction","Secunderabad YMCA","Patny","Vikrampuri","Karkhana","Hanuman Temple (Tirumalgirri)",
                               "Tirumalgirii Bus Stop","Lalbazar X Road","Lalbazar Circle","Guruvayurappan Temple","Nagmandir",
                               "Eme War Memorial","Eagle Chowk","EME Center","Ammuguda Bazar","Jai Jawahar Nagar","Yapral Circle",
                               "Yapral Bus Stop","Swarnandhra Colony","Gks Pride","Balaji Nagar Poultry Farm","Balaji Nagar"],
                        "24S": ["ECIL X Roads","North Kamala Nagar","Radhika X Rds","Bhashyam As Rao Nagar","Officer’S Colony",
                               "Vayupuri","Neredmet X Road","Secunderabad Central","Robert Road","Kv School X Road","Aoc",
                               "Lalbazar","Eme Bus Stop","Lothkunta Bus Stop","Alwal Bus Station","Alwal Police Station",
                               "Temple Alwal","Old Alwal","Ig Statue","Father Balaiah Nagar","Loyola college","Suchitra X Road"],
                        "25S/229":["Medchal bus terminal","Medchal Ambedkar Chowrasta","Medchal chekpost","Cmr college",
                                   "Kandlakoya bus stop","Prestige","Gundla pochampally","Kompally","Dollapally X Road","Prajay",
                                   "Cine planet kompally","NCL north avenue","Angadipeta","Jeedimetla ","Suchitra circle","Loyola college",
                                   "Bhel Quarters","Pv Junction Bus Stop","Father Balaiah Nagar","Ig Statue","Old Alwal","Temple Alwal",
                                  "Alwal Police Station","Alwal Bus Station","Lothkunta Bus Stop","Family Quarter Bus Stop",
                                  "Eme Bus Stop","Lalbazar","Tirumalgirii Bus Stop","Tirumalgirii X roads","Hanuman Temple (Tirumalgirri)",
                                  "Karkhana Temple Arch","Karkhana","Vikrampuri","Jubilee Bus Station","Patny","Secunderabad YMCA","Secunderbad junction"],
                        "25M/SN": ["Secunderbad junction","Secunderabad YMCA","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                   "Karkhana Temple Arch","Hanuman Temple (Tirumalgirri)","Tirumalgirii X roads","Tirumalgirii Bus Stop",
                                 "Lalbazar","Eme Bus Stop","Family Quarter Bus Stop","Maruti Nagar","Lothkunta Bus Stop","Alwal Bus Station",
                                  "Alwal Police Station","Temple Alwal","Old Alwal","Ig Statue","Select Talkies","Macha Bolaram",
                                  "MG Nagar","Gopalnagar X Roads","Hanuman Temple","Sanjeev Reddy Garden","Railway Colony","ARK Homes",
                                  "Sarannagar "],
                          "25A": ["Secunderbad junction","Secunderabad YMCA","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                   "Karkhana Temple Arch","Hanuman Temple (Tirumalgirri)","Tirumalgirii X roads","Tirumalgirii Bus Stop",
                                 "Lalbazar","Eme Bus Stop","Family Quarter Bus Stop","Lothkunta Bus Stop","Alwal Bus Station",
                                  "Alwal Police Station","Temple Alwal","Old Alwal","Ig Statue","Surya Nagar"],
                          "25M": ["Secunderbad junction","Secunderabad YMCA","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                   "Karkhana Temple Arch","Hanuman Temple (Tirumalgirri)","Tirumalgirii X roads","Tirumalgirii Bus Stop",
                                 "Lalbazar","Eme Bus Stop","Family Quarter Bus Stop","Lothkunta Bus Stop","Alwal Bus Station",
                                  "Alwal Police Station","Temple Alwal","Old Alwal","Ig Statue","Mg Nagar"],
                          "107JS": ["Secunderabad raithfile bus stop","Chilakalguda - Mylargadda Road","Namalagundu","Warasiguda Bus Stop",
                                   "Arts College MMTS Boudhanagarstop","Jamai-Osmania MMTS Station","No 5 Street",
                                    "Koundinya Medical & General Store","Adikmet","Vidhya Nagar","Vivekananda College Vidyanagar",
                                   "Ou Engineering College","Shivam","Sri Kusuma Haranatha/Prashanth Nagar","Syndicate Bank New Nallakunta",
                                   "6 Number","Amberpet 6 Number","Amberpet Police Station","Amberpet Police Lines","Amberpet Ali Cafe",
                                   "Sripuram Colony","Tower/Moosaram Bagh","Dilsukhnagar","Chaitanyapuri","Kothapet X Road Petrol Pump",
                                   "Saroor Nagar / Huda Complex","Mro Office","Venkateswara Colony","Saroor Nagar"],
                           "107V/R": ["LB Nagar","LB nagar Metro Station","Doctors Colony Bus Stop","Victoria Memorial Metro Station",
                                     "Dwaraka Nagar / Ashtalakshmi Temple","Pvt Market","Kothapet Fruit Market","Chaitanyapuri Metro Station",
                                     "Chaitanyapuri","Dilsukhnagar Bus Station","Moosaram Bagh","Moosarambagh Rta Office","Amberpet Ali Cafe",
                                     "Amberpet Police Lines","Amberpet 6 Number","Syndicate Bank New Nallakunta","Prashanth Nagar Bus Stop",
                                     "Ou Engineering College","Vivekananda College Vidya Nagar Stop","Vidyanagar","RTC Bhavan","RTC X Road",
                                     "Golconda X Roads","Musheerabad Police Station","Gandhi Hospital Bus Stop","Bhoiguda","Chilkalguda",
                                     "Secunderabad/Chilkalguda Circle Bus Stop","Secunderabad Rathifile Bus Station"],
                           "107VR": ["LB Nagar","LB nagar Metro Station","Doctors Colony Bus Stop","Victoria Memorial Metro Station",
                                     "Dwaraka Nagar / Ashtalakshmi Temple","Pvt Market","Kothapet Fruit Market","Chaitanyapuri Metro Station",
                                     "Chaitanyapuri","Dilsukhnagar Bus Station"],
                           "219/220K": ["Secunderabad Railway Station","Clock Tower","Swapnalok Complex","Paradise","Tadbund",
                                       "Chinna Thokata","Bowenpally X Road","Ferozeguda","Ferozeguda Bhel","Balanagar X Roads",
                                       "IDPL","Sai Nagar (Bala Nagar)","Prashanth Nagar","Sangeeth Nagar","Kukatpally Bus Stop",
                                       "Sumithra Nagar Bus Stop","Vivekanadanagar Colony Rdr Hospital","KPHB","JNTU","Nizampet X Roads",
                                       "Vasanth Nagar","Hydernagar","Miyapur Metro Station","Miyapur Busstop","Allwyn X Roads",
                                       "Madinaguda / Deepthisree Nagar","Huda Colony Bustop","Gangaram Bus Stop","Chandanagar",
                                       "Lingampally Bus Station","Nalagandla","Tellapur","Osman Sagar Road","Kollur bus stop"],
                           "219/229": ["Medchal bus terminal","Medchal Ambedkar Chowrasta","Medchal chekpost","Cmr college",
                                        "Kandlakoya bus stop","Prestige","Gundla pochampally","Kompally","Dollapally X Road","Prajay",
                                      "Cine planet kompally","NCL north avenue","Angadipeta","Jeedimetla ","Suchitra circle","Dairy farm","M.M.R.Gardens","Bowenpally Checkpost",
                                      "Bowenpally Police Station","New Bowenpally","Ferozeguda","Balanagar X Roads / Citd","IDPL","Sai Nagar (Bala Nagar)",
                                      "Kukatpally Y Junction","Kukatpally Bus Stop","Kukatpally Crossroads","Sumithra Nagar Bus Stop",
                                      "Vivekananda Nagar Bus Stop","KPHB","KPHB Vishwanth Theater","JNTU","Nizampet X Roads","Vasanth Nagar",
                                      "Hyder Nagar","Miyapur Metro Station","Miyapur X Roads","Allwyn X Roads","Mythrinagar Bus Stop",
                                      "Madinaguda","Huda Colony Bustop","Gangaram Bus Stop","Gangaram D.C.B.Bank","Chandanagar",
                                      "Lingampally Bus Station","Lingampally","Jyothi Nagar","Ashok Nagar","Beeramguda Bus Stop",
                                      "Sri Sai Nagar","Bhel Pushpak","Rc Puram","Icrisat","Patancheru","Depot Arch","Patancheru Bus Station"],
                            "25J": ["Secunderabad Railway Station","Secunderabad YMCA","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                 "Hanuman Temple (Tirumalgirri)","Tirumalgiri Bus Stop","Lalbazar","Eme Bus Stop","Family Quarter Bus Stop",
                                 "Lothkunta Bus Stop","Ram Nagar Alwal","Alwal Bus Station","Alwal Police Station","Temple Alwal","Old Alwal",
                                 "Ig Statue","Father Balaiah Nagar","Pv Junction Bus Stop","Bhel Quarters","Suchitra X Road",
                                 "Jidimetla Village","Subhash Nagar","Jeedimetla Bus Stop"],
                            "45J": ["Jeedimetla Depot","Jeedimetla Substation Bus Stop","Shapur Nagar","Gajula Ramam X Road","Hmt Factory",
                                   "Chintal","District Bus Stop IDPL Colony","IDPL Colony","Balanagar","Fateh Nagar X Road",
                                   "Valmiki Nagar","Fateh Nagar","Balakampet","Satyam Theatre Cross Roads","Ameerpet","Sheeshmahal",
                                   "Lal Bungalow Ameerpet","Greenlands Bus Stop","Begumpet Railway Station North","Begumpet Bus Stop",
                                   "Shamlal North","Begumpet","Prakash Nagar","Begumpet Police Lines","Yatri Nivas","Anand Theatre",
                                   "Paradise Metro Station","Paradise Bus Stop","MG Road","Ranigunj Bus Stop","Krishna Nagar (Bholapur)",
                                   "Musheerabad Police Station","Golconda X Road","RTC X Road"],
                            "1J": ["Afzalgunj","Gowliguda Bus Depot","Central Bus Station (CBS)","Bank Street Koti","Koti Maternity Hospital",
                                  "Sultan Bazar","Kachiguda X Road","YMCA","Narayanaguda","Chikkadpally Bus Stop","Golconda X Roads",
                                  "Gandhi Hospital Bus Stop","Secunderabad Tsrtc Rathifile Bus Station"],
                            "23GF": ["Secunderabad Railway Station","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                    "Karkhana Temple Arch","Hanuman Temple Tirumalgirri","RTC Colony Gun Rock Road","Teachers Colony",
                                    "Subash Nagar","Military Dairy Farm Road","Greenfieldcolony"],
                            "9F": ["Mothi Nagar","Kalyan Nagar","Sriram Nagar","Karmika Nagar","Rahmath Nagar Bus Stop","Jawahar Nagar",
                                  "Bright School","Panjagutta Colony Bus Stop","Nims","Erramanzil","Khairatabad Rta","Khairatabad Bus Stop",
                                  "Lakdikapul","Lakdikapul Metro Station","Assembly","Nampally","Mozamjahi Market ","High Court",
                                  "Charminar Bus Station","Shah Ali Banda X Road","Lal Darwaza","Falaknuma Bus Station"],
                            "229D": ["Medchal bus terminal","Medchal Ambedkar Chowrasta","Medchal chekpost","Cmr college",
                                      "Kandlakoya bus stop","Prestige","Gundla pochampally","Kompally","Dollapally X Road","Prajay",
                                      "Cine planet kompally","NCL north avenue","Angadipeta","Jeedimetla ","Suchitra circle","Dairy farm","MMR Gardens","Bowenpally Checkpost",
                                   "Bowenpally Police Station","Tadbund","Paradise","Mahatma gandhi road","Ranigunj Bus Stop","Tank Bund",
                                    "Assembly","Nampally","Mozamjahi Market","Nayapul","Salarjung Museum","Owaisi Chowk Dabeerpura",
                                    "Dabeerpura","Chanchalguda"],
                             "8X": ["Ranigunj Bus Depot","Raniganj","Boats Club","Bible House","Bata","Patny Center","Clock Tower",
                                   "Secunderabad Railway Station","TSRTC Rathifile Bus Station"],
                            "225CL": ["Lingampally Bus Stop","Chanda Nagar"," Miyapur Bus Stop","Miyapur X Roads"," Hydernagar",
                                     "Nizampet","Jntu bus stop"," Kphb Colony Bus Stop ","Sumithra Nagar","Kukatpally Bus Stop",
                                     "Moosapet Bus Stop","Bharat Nagar(Moosapet) Bus Stop ","Esi Bus Stop","S R Nagar",
                                     "Mytrivanam","Ameerpet Bus Station","Panjagutta Bus Stop","Erramanzil Bus Stop","Khairatabad Bus Stop",
                                     " Lakdikapool Bus Stop"," Assembly","Public Gardens Nampally","Nampally"," Gandhi Bhavan Bus Stop",
                                     "Putlibowli","Koti Bus Stop","Afzalgunj Bus Stop"],
                             "2C": ["Barkas","Charminar Bus Stop","Osmania Hospital","Afzalgunj Bus Stop","Cbs Bus Stop","Chaderghat Bus Stop",
                                   "Kachiguda Railway Station","Barkatpura","Nallakunta Bus Stop","Shankar Mutt","Rtc Cross roads",
                                   "Golconda X Roads","Musheerabad Bus Stop","Gandhi Hospital","Bhoiguda","Secunderabad Junction"],
                             "5C": ["Secunderabad Junction","Paradise","Mahatma Gandhi Road","Ranigunj Bus Stop","Tank Bund",
                                   "Lakdikapul Metro Station","Masab Tank / Potti Sriramulu Nagar","Sarojini Devi Eye Hospital",
                                   "Rethibowli","Nanal Nagar","Salarjung Colony Bus Stop","Brindavan Colony Road"],
                              "123": ["Narsingi Bus Stop","Narayanamma Engineering College","Shaikpet Nala","Tolichowki",
                                     "Galaxy Bus Stop","Salarjung Colony Bus Stop","Rethibowli Bus Stop","Mehdipatnam Bus Station"],
                              "119": ["Golconda Fort","Quli Qutub Shah Tombs","Salarjung Colony Bus Stop","Rethibowli Bus Stop",
                                      "Mehdipatnam Bus Station","Sarojini Devi Eye Hospital","Lakdikapul","Assembly","Nampally",
                                     "Nampally Station Road"],
                              "245": ["Secunderabad Junction","Alugadda Bhavi","Mettuguda Bus Stop","Railway Degree College",
                                     "Tarnaka Bus Stop","Habsiguda Bus Stop","Ngri","Uppal X Road Bus Stop","Uppal Bus Stop",
                                     "Ferzajiguda","Boduppal Kaman","Uppal Depot","Narapally","Ghatkesar Bus Stop","Aushapur",
                                     "Nemuragomla","Dayara"],
                              "113K": ["Chengicherla Bus Depot","RTC Colony","Chengicherla X Road","Kamala Nagar","	Uppal Bus Depot",
                                      "Boduppal","Pochamma Temple","Uppal Bus Stop","Uppal Gandhi Statue","Uppal Sub Station",
                                      "	Uppal X Road Bus Stop","Ramanthapur","Tilak Nagar Bus Stop","Fever Hospital Bus Stop",
                                      "Baghlingampally","Chikkadpally","Barkatpura","Amberpet Bus Station","Uppal X Road Bus Stop",
                                      "Gandhi Statue","Uppal Bus Stop"],
                             "49M": ["Secunderabad Junction","Clock Tower","Patny","Paradise Bus Stop","Anand Theatre",
                                    "Police Lines-Begumpet Bus Stop","Begumpet Railway Station","Greenlands","Panjagutta Bus Stop",
                                    "Banjara Hills","Masab Tank Bus Stop","Sarojini Bus Stop","Mehdipatnam Bus Stop"],
                              "218D": [" Patancheru Bus Stop","Lingampally Bus Stop","Jntu bus stop","Kukatpally Bus Stop",
                                      "Esi Bus Stop","S R Nagar","Ameerpet Bus Station","Panjagutta Bus Stop","Somajiguda",
                                      "Khairatabad Bus Stop","Lakdikapool Bus Stop","Abids Bus Stop","Koti Bus Stop","Malakpet",
                                      "Chaderghat Bus Stop","Dilsukhnagar Bus Station"],
                             "3K": ["Kushaiguda","ECIL X Roads","SP Nagar","Unani Hospital","Nrm College","Moula Ali Railway Colony",
                                   "Lalapet Bus Stop","Tarnaka","Tarnaka Tsrtc Hospital","Arts College Bus Stop","Jamia Osmania ",
                                   "Nallakunta","Fever Hospital","Barkatpura","Kachiguda X Road","Badi Chowdi","Koti Bus Terminal",
                                   "Koti Maternity Hospital","Koti","Putili Bowli","Central Bus Station","Afzalgunj Bus Station"],
                             "222A": ["Patancheru","Bhel Pushpak","Beeramguda Bus Stop","Lingampally","Chandanagar","Gangaram ",
                                     "Huda Colony Bustop","Mythrinagar Bus Stop","Allwyn X Roads","Hafeezpet","Botanical Garden",
                                     "Kondapur X Road","Kondapur","Shilparamam Bus Stop","Hitech City","Madhapur Police Station ",
                                     "Jubilee Hills Check Post Bus Stop","Lv Prasad Bus Stop","TV 9","Taj Krishna","Masab Tank Bus Stop",
                                     "Lakdikapul","Lakdikapul Metro Station","Assembly","Nizam College","Abids","Koti Bus Terminal"],
                              "113M": ["Mehdipatnam Bus Station","Sarojini Devi Eye Hospital","Masab Tank","Lakdikapul Metro Station",
                                      "Saifabad","Telephone Bhavan","Secretariat","Liberty","Himayath Nagar Bus Stop","Narayanaguda",
                                      "Chikkadpally Bus Stop","Baghlingampally","Barkatpura","Ramanthapur Colony ",
                                      "Uppal X Roads","Uppal Metro Station","Uppal Gandhi Statue","Uppal Bus Station"],
                            "300": ["Uppal X Roads","Uppal Metro Station","Saraswathi Nagar","Nagole","Alkapuri","Kamineni Hospital ",
                                    "LB nagar","Sagar Ring Road Owaisi Way","T.K.R.Kaman ","Champapet X Roads","Owaisi Hospital",
                                   "Midhani Depot","Kanchanbagh Gate","Baba Nagar","Chandrayanagutta","Bandlaguda","Durganagar",
                                   "Aramghar X Roads","Shivarampally X Road","Upperpally X Road","Hyderguda X Road","Attapur X Road",
                                   "Rethibowli","Rethibowli Bus Stop","Mehdipatnam Bus Station"],
                        "16A/47LI": ["Continental Hospitals","Infotech","ICICI","Wipro Nanakramguda","Infosys","Gpra","Indra Nagar","Telecom Nagar",
                                    "Cyberabad Police Commisioner Office","Biodiversity Park","Skyview Rmz","Lumbini Avenue","Raidurg",
                                     "Cyber Towers / Shilparamam","Hitech City","Image Garden","Madhapur Petrol Pump",
                                     "Madhapur Police Station Bus Stop","Live Life Hospital","Rainbow Park","Usha Kiran Movies",
                                     "Jubilee Hills Check Post Bus Stop","Lv Prasad Bus Stop","Sri Nagar Colony Bus Stop","Ameerpet Elephant House",
                                    "Ameerpet","Lal Bungalow Ameerpet","Greenlands Bus Stop","Begumpet","Shamlal North","Begumpet",
                                    "Prakash Nagar","Yatri Nivas /Anand Theatre","Sd Road","Swapnalok Complex","Patny Center Chandana Bros",
                                    "Navketan Complex Clock Tower","Secunderabad YMCA","W Marredpally Cross","East Maredpally","Shenoy Nursing Home",
                                    "West Marredpally","Aoc Center A","Aoc Gouha Road","Aoc Chowk","Safilguda","Krupa Complex","Vinayak Nagar",
                                     "Neredmet Old Ps","Vajpayee Nagar","Vayupuri Bus Stop","Sainikpuri","Officer’S Colony","A.S. Rao Nagar","ECIL X Road"],
                         "102CJ": ["Janapriya Colony","Lenin Nagar Bus Stop","Balapur X Road","Midhani Township","Dhatu Nagar","Bdl",
                                   "Pisalabanda","Midhani Company","Drdo Township","Midhani Bus Depot","Owaisi Hospital","Santosh Nagar","Is Sadan","Madannapet",
                                  "Saidabad X Roads","APSEB Office Saidabad","Chanchalguda","Chanchalguda Jail","Malakpet GOVT. Hospital","Nalgonda X Roads",
                                   "Chaderghat","Koti Womens College","Shankar Mutt"],
                        "41K": ["Central Bus Station (CBS)","MGBS","Putili Bowli","Koti","Mozamjahi Market","GPO","Abids","Nampally","Assembly","Lakdikapul Metro Station",
                                "Lakdikapul","Chintal Basti","Khairatabad","Khairatabad Rta","Erramanzil","Nims","Ameerpet","Mythrivanam","SR Nagar",
                                "ESI Hospital Metro Station","Erragadda FCI","Erragadda","Sanath Nagar Police Station","Sanath Nagar","Fateh Nagar","Valmiki Nagar",
                                "Fateh Nagar X Road","Hal","IDPL Colony","District Bus Stop IDPL Colony","Giri Nagar","Asbestos Colony","Ranga Reddy Kamaan",
                                "Papi Reddy Nagar","Outpost Station","Jagadgirigutta"],
                        "104A": ["Almasguda","Almasguda P.G.College","Prashanthi Hills","Sita Homes Colony","Meerpet Swimming Pool","Meerpet X Road",
                                 "Lalitha Nagar X Road","Jillelguda","VV Nagar","Meerpet Cheruvu","Gayatri Nagar X Road","TKR Kaman / Shakti Nagar","Kranti Nagar",
                                 "Karmanghat X Road","Karmanghat","Green Park Colony","RTC Colony","Champapet","Santosh Nagar","Is Sadan","Saidabad",
                                 "Jaihind Hotel","APSEB Office Saidabad","Government Press","Chanchalguda","Malakpet Sohail Hotel","Nalgonda X Roads","Chaderghat",
                                 "Koti Womens College"],
                        "156H": ["NGO Colony","Ganesha Temple","Chinthalkunta","LB Nagar Ring Road","LBNagar Metro Station","Doctors Colony",
                                 "Dwaraka Nagar Ashtalakshmi Temple","Chaitanyapuri","Dilsukhnagar","TVTower","Moosaram Bagh","Amberpet Ali Cafe",
                                 "Amberpet Police Lines","Tilak Nagar","Fever Hospital","Barkatpura","Baghlingampally","Chikkadpally","Narayanaguda",
                                 "Urdu Hall","Liberty","Lakdikapul Metro Station","Masab Tank","Potti Sriramulu Nagar","Masab Tank","NMDC","Sarojini Devi Eye Hospital",
                                 "Mehdipatnam"],
                        "9K/283K": ["Koti Bus Terminal","Koti","Mozamjahi Market","Abids","Nampally Station Road","Nampally","Nampally Grand Plaza",
                                    "Assembly","Lakdikapul Metro Station","Lakdikapul","Chintal Basti","Chintal Basthi Bus Stop","Khairtabad","Eenadu",
                                    "Khairatabad Rta","Erramanzil","Nims","Panjagutta Colony","Punjagutta","Ameerpet","Mythrivanam","SR Nagar","ESIHospital",
                                    "ESIHospital Metro Station","Erragadda","Prem Nagar","Bharat Nagar","Moosapet","Kukatpally Bus Depot","Sai Nagar","IDPL",
                                    "Niper","Balanagar X Roads","Balanagar","Hal","Water Tank","IDPL Chowrasta","Ganesh Nagar","Chintal","Chintal Chowrasta",
                                    "Hmt Factory","Gajula Ramam X Road","Shapur Nagar","Jeedimetla","Jeedimetla Bus Depot","Saibaba Nagar","Suraram Colony"],
                        "100A": ["Nampally","Gandhi Bhavan","Mozamjahi Market Gandhi Bhavan","Abids","Bank Street Koti","Koti","Shankar Mutt",
                                 "Koti Womens College","Chaderghat","Nalgonda X Roads","Yashoda Hospital","Malakpet Chermas","Malakpet Super Bazar",
                                 "Saleem Nagar","TV Tower","Moosaram Bagh","Dilsukhnagar","Chaitanyapuri","Fruit Market","Shalini Theatre","Kothapet",
                                 "Kothapet X Road Petrol Pump","Babu Jagjeevan Ram Bhavan Telephone Colony Arch","Telephone Colony","Rk Puram",
                                 "Baba Temple Alkapuri","Alkapuri"],
                        "171": ["Secunderabad","Secunderabad YMCA","Parade Ground Metro Station","Paradise","Tadbund","Bowenpally X Road","Ferozeguda",
                                "Raju Colony","Balanagar","Hal","Chintal","Chintal Chowrasta","Hmt Factory","Raamaaram X Road","Hal Colony","Gajularamaram"],
                        "9X/283D": ["Suraram Colony","Suraram X-Road","Saibad X Road","Jeedimetla Bus Depot","Jeedimetla Substation","Shapur Nagar",
                                    "Hmt Factory","Chintal Chowrasta","Ganesh Nagar","IDPL Colony","Hal","Balanagar X Roads","Niper","IDPL","Prashanth Nagar",
                                    "Kukatpally Bus Depot","Moosapet","Bharath Nagar","Prem Nagar","Erragadda","ESI Hospital Metro Station","Mythrivanam",
                                    "Ameerpet","Panjagutta Colony","Nims","Erramanzil","Khairatabad Rta","Khairatabad","Chintal Basti","Telephone Bhavan",
                                    "Assembly","Nampally Grand Plaza","Nampally","Mozamjahi Market Gandhi Bhavan","Afzalgunj Central Library",
                                    "Gowliguda Bus Depot","Central Bus Station","CBS"],
                        "220V": ["Mehdipatnam Corner","Mehdipatnam","Rethibowli","Salarjung Colony","Flour Mill","Langer Houz","Bapunagar","Bapu Ghat",
                                 "Chavella Road","Ramdevguda","Ibrahim Bagh","Hanuman Temple","Manchrevula X Road","Indra Nagar","Nanak Ram Guda","Iit",
                                 "Gachibowli Stadium","Hyderabad Central University Gate 2","Masjid Banda","Hcu","Hcu Depot","Bhagyanagar Colony",
                                 "Alind Doyens Colony","Gulmohar Park","Lingampally","Serlingampalli","Tara Nagar","Lingampally Bus Station"],
                        "251N": ["Narkhoda","Indra Nagar","Rallagudem","Shamshabad","Shamshabad Market","Satamrai","Gagan Pahad","AG College",
                                 "Aramghar","Aramghar X Roads","Sardar Vallabhbhai Patel National Police Academy","Raghavendra Colony",
                                 "Hasan Nagar","Danama Jhopdi","Mir Alam Tank Filter Beds","Thadban","Nehru Zoological Park","Bahadurpura",
                                 "Bahadurpura Police Station","Puranapool Mastan Gati","Puranapool","Puranapool Out Post","Petla Burj",
                                 "City College","High Court","Afzalgunj"],
                        "65": ["Tolichowki","Salarjung Colony","Nanal Nagar","Rethibowli","Mehdipatnam Bus Station","Sarojini Devi Eye Hospital",
                               "NMDC","Masab Tank","Ac Guards","Lakdikapul","Assembly","Basheerbagh","Nizam College","Abids","Abids Big Bazar",
                               "Bank Street Koti","Koti Bus Terminal","Koti","Putili Bowli","MGBS","Gowliguda Bus Depot"],
                        "11": ["VBIT Ascendas IT Park","Ascendas","Raheja Mindspace C Gate","Raidurg","Cyber Towers","Shilparamam",
                               "Hitech City","Image Garden","Madhapur Petrol Pump","Madhapur Police Station","Live Life Hospital",
                               "Rainbow Park","Peddamma Temple","Usha Kiran Movies","Jubli Check Post Chiranjeevi Eye Bank","Venkatagiri",
                               "Srinagar X Road","Indira Nagar X Road","Yousufguda Checkpost","Yousufguda Basti","State Home","Sarathi Studio",
                               "Mythrivanam","SR Nagar","ESI Hospital","ESI Hospital Metro Station"],
                        "3": ["Afzalgunj Central Library","Central Bus Station CBS","Chaderghat","Kachiguda Station Road",
                              "Kachiguda","Kachiguda Bus Station","Tourist Hotel","Fever Hospital","Nallakunta","Shankarmutt",
                              "Vidyanagar","Vidhya Nagar","Adikmet","Ramnagar Gundu","Ladies Hostel","Manikeshwari Nagar",
                              "Tarnaka Hospital Stop","Tarnaka","White House","Lalapet","HMT Bearings","ZTS X Road","Carbide",
                              "Hb Colony 1st Phase","Nrm College","Laxmi Nagar","Unani Hospital","SP Nagar","Kushaiguda Depot",
                              "ECIL X Roads","Kushaiguda"],
                        "2": ["Secunderabad Railway Station","Secunderabad Tsrtc Rathifile Bus Station","Secunderabad",
                              "Chilkalguda Circle","Chilakalaguda","Chilkalguda","Bhoiguda","Gandhi Hospital","Musheerabad X Road",
                              "Musheerabad Police Station","Raja Delux","Golconda X Road","RTC X Road","R.T.C.Bhavan","VST",
                              "Shankar Mutt","Nallakunta","Fever Hospital","Barkatpura","Kachiguda","Nimboliadda","Chaderghat",
                              "Chaderghat","Central Bus Station","CBS","Gowliguda Bus Depot","Afzalgunj Bus Station"],
                        "9M": ["Central Bus Station","CBS","Upcoming Arrivals","Central Bus Station","Gowliguda Bus Depot",
                               "Afzalgunj Bus Station","Afzalgunj","Osmangunj","Mozamjahi Market Gandhi Bhavan","Gandhi Bhavan","Nampally",
                               "Nampally Grand Plaza","Assembly","Lakdikapul Metro Station","Lakdikapul","Chintal Basti",
                               "Chintal Basthi Bus Stop","Khairtabad","Eenadu","Khairatabad Rta","Erramanzil","Nims","Panjagutta Colony",
                               "Ameerpet","Ameerpet Metro Station","Mythrivanam","SR Nagar","SR Nagar","ESI Hospital","ESI Hospital Metro Station",
                               "Erragadda","Sanath Nagar Police Station","Sanath Nagar","Sanath Nagar Bus Depot"],
                        "10B": ["Secunderabad Railway Station","Secunderabad Bus Station","Swimming Pool North","Paradise South",
                                "Anand Theatre","Police Lines South","Begumpet Old Airport","Shoppers Stop South","Shyam Lal South",
                                "Begumpet","Begumpet Railway Station","Greenlands","Nagarjuna Hills","Panjagutta Colony","Ameerpet",
                                "Mytrivanam","SR Nagar","ESI","Rythu Bazar Erragadda","Erragadda FCI","Erragadda Gokul Theater",
                                "Allwyn Erragadda","Erragadda","Prem Nagar","Bharat Nagar"],
                        "3B": ["Afzalgunj Central Library","Central Bus Station","CBS","Chaderghat","Koti Womens College",
                               "Koti Maternity Hospital","Sultan Bazar","Ram Koti","Kachiguda X Road","YMCA","Reddy College Narayanaguda",
                               "Barkatpura Circle","Fever Hospital","Nallakunta","Vidyanagar","Vidhya Nagar","Adikmet","Ramnagar Gundu",
                               "Jamia Osmania","Ladies Hostel","Manikeshwari Nagar","Tarnaka Hospital Stop","Tarnaka Uppal Stop",
                               "Habsiguda","National Geophysical Research Institute","NGRI","Kalyanpuri Colony Uppal"],
                    "47Y/90U": ["Uppal X Roads","Survey Of India","National Geophysical Research Institute","NGRI","Habsiguda",
                             "Tarnaka Aaradhana","Mettuguda","Alugadda Baavi South","Chilakalaguda","Secunderabad Tsrtc Rathifile Bus Station",
                             "Secunderabad Railway Station","Clock Tower","Swimming Pool North","Paradise Metro Station","Yatri Nivas",
                             "Anand Theatre","Begumpet","Prakash Nagar","Prakash Nagar","Begumpet","Begumpet","Greenlands",
                             "Lal Bungalow Ameerpet","Sheeshmahal","Satyam Theatre Cross Roads","Sarathi Studio","Yousufguda Basti",
                             "Yousufguda Checkpost","Srinagar X Road","Indira Nagar X Road","Venkatagiri","Road Number 37 Check Post",
                             "Journalist Colony Kbr Park","Filmnagar Entrance Sbi","Film Nagar Film Chambers","Film Nagar"],
                        "29H": ["Apurupa Colony","SR Naik Nagar Main","Jeedimetla Bus Depot","Jeedimetla Substation","Shapur Nagar Bus Stand",
                                "Shapur Nagar","Gajula Ramam X Road","Hmt Factory","Chintal Chowrasta","Chintal","Ganesh Nagar",
                                "District Bus Stop IDPL Colony","IDPL Colony","Water Tank","Hal","Balanagar","Raju Colony","Ferozeguda",
                                "New Bowenpally","Bowenpally X Road Junction","Chinna Thokatta Request","Ashish Gardens","Tar Bund Bus Stop",
                                "Pratap Colony","Paradise","Paradise Petrol Bunk Towards Stn Busstop","Swimming Pool North","Patni Junction",
                                "Navketan Complex Clock Tower","Secunderabad Bus Station Gurudwara"],
                        "15H": ["Secunderabad Towards Uppal","TSRTC Rathifile Bus Station","Chilkalguda","Alugadda Bhavi",
                                "Railway Hospital","Mettuguda","Lalaguda Junction","New Bridge","North Lalaguda","Masjid Lalaguda",
                                "Lalguda Railway Quarters","Santhi Nagar Lalaguda","Ram Theatre","Lalapet","RPF Training Centre",
                                "Industrial Estate","ZTS X Road","Carbide","HB Play Ground","Mangapuram","N.R.M. Degree College",
                                "Indira Nagar","Laxmi Nagar","Moulali Unani Dispensary","S.P. Nagar","Kushaiguda Depot","Kamla Nagar",
                                "ECIL X Road","ECIL X Road Bus Terminal","Kushaiguda","Nagarjuna Colony","Chakripuram","Nagaram Road",
                                "Chakripuram Road","Vijaya Hospital Road Nagaram","Nagaram","Sudha Hospital Dammaiguda X Road Nagaram",
                                "Rampally X Road","6th Phase KPHB","Icomm Tele Limited","Bandlaguda","Bhavani Nagar","RG Colony Panchayat Office",
                                "Rajiv Gruhakalpa Colony"],
                        "211P": ["Medchal","Medchal Bus Stop","Medchal Chekpost","Medchal Gubba","CMR College of Engineering and Technology",
                                 "Dongala Maya Sabha","Thumkunta","Medchal X Road Thummukunta","Sports School","Hakimpet","Nisa CISF","Kot Temple",
                                 "Water Tank","Risala Bazar","risala","sadhana mandhir","Bolarum","Bollaram","Lakadawala","Rythu Bazar","Alwal",
                                 "Ram Nagar – Alwal","Lothkuntap","EME","Lal Bazar","Tirumalgherry","Hanuman Temple Tirumalgherry","Karkhana Temple Arch",
                                 "Vikarampuri","HPS High School","Jubilee Bus Stop East 1","Patny","Patny North","Clock Tower",
                                 "Secunderabad Bus Station 2"],
                        "8R": ["Chinnamangabram","Mile Stone","Reddy Pally","Chanda Nagar X Road","Appo Jigudda","Chilkur","Balaji Temple X Road",
                               "Himyat Nagar Village","Chilkur Balaji Temple X Road","Aziz Nagar","Aziz Nagar 2","Aziz Nagar 1",
                               "Sri Nidhi International School","Chilkur Engineering College","Old Aziz Nagar X Road",
                               "Police Academy","AP Police Academy-2","Kalimandir","Peerancheru","Bandlaguda X Road","Suncity",
                               "Sairam Nagar","Chavella Road","Bapu Ghat","Langar House","Flour Mill","Salarjung Colony",
                               "Nala Nagar","Rethi Bowli","Mehdipatnam","Mehdipatnam Amba Theatre"],
                        "104G": ["Koti Womens College","Chaderghat","Nalgonda Cross Roads","Sohail Hotel","Chanchalguda","Chanchalguda Jail",
                             "Saidabad","Saidabad X Road","Saidabad","IS Sadan","Champapet Brilliant GL School","RTC Colony Champapet",
                             "Green Park Colony Bus Stop","Karmanghat X Road","Kranti Nagar","Gayatri Nagar X Road","VV Nagar","Jillelguda",
                             "Lalitha Nagar X Road","Meerpet X Road","Meerpet Swimming pool","Sita Homes Colony","Prashanthi Hills","Almasguda"],
                        "29R": ["Railapoor","Girmapur","Medchal Railway Station","Medchal","Medchal Chekpost","Medchal Gubba",
                                "CMR College of Engineering and Technology","Kandlakoya","Gundlapochampalli","Kompally",
                                "Dollapally X Road/Kompally Chorwsta","Cine Planet","NCL","NCL Balaji Hospital","Santa Sriram Estate",
                                "Jeedimetla Deewan Dhaba","Suchitra","Military Dairy Farm","Mmr Garden Bus Bay","Priyadarshini Hotel",
                                "New Bowenpally","Chinna thokatta Request Bus Stop","Ashish Gardens","Tar Bund","Pratap Colony","Paradise",
                                "Paradise BSNL Complex","Paradise","MG Road","James Street East","Ranigunj"],
                        "127J":["Jubilee Hills","Jubilee Check Post","Lv Prasad","Banjara Hills Road No.1 Water Tank","Taj Krishna","Care Hospital",
                               "Chintal Basti","Masab Tank","Ac Guards","Lakdikapul","Lakdikapul Metro Station","Assembly","Basheerbagh",
                                   "Nizam College","Abids","Mozamjahi Market","Koti"],
                       "71A":["Charminar","Pathar Gatti","High Court","Afzal Gunj","Chatrapathi Shivaji Pul","Gowliguda Depot",
                              "Central","Mahatma Gandhi","Chaderghat","Kachiguda Kamela","Golnaka 6 Number","Sree Ramana","Gandhi Statue",
                                "Irani Hotel","TV Studio Ramanthapur","TV Studio","Ramanthapur Colony","Ramanthapur Hyderabad Public School",
                                "Ramanthapur Church","Modern Foods","Uppal X Roads","Chilkanagar","Uppal Gandhi Statue","Uppal"],
                       "102A":["Mahaveer College","Bandlaguda","Kesavagiri","Chandrayanagutta","Drdl","Baba Nagar","Anurag Lab","Drdl",
                               "Midhani Depot","Owaisi Hospital","Santosh Nagar","Is Sadan","Saidabad HFEC Function Hall","Jaihind Hotel",
                               "APSEB Office Saidabad","Government Press","Chanchalguda","Sohail Hotel","Nalgonda X Roads","Chaderghat",
                                "Koti Women's College"],
                       "116N":["Nanak Ram Guda","Gpra","Khajaguda X Road","Hs Dargha","Narayanamma Engineering College","Shaikpet Nala",
                                "Tolichowki","Galaxy","Salarjung Colony","Nanal Nagar","Rethibowli","Mehdipatnam","Mehdipatnam Corner",
                                "Asif Nagar","Mallepally","Sitaram Bagh","Aghapura","Nampally","Abids","Mozamjahi Market","Putlibowli",
                                "Koti Bus Terminal"],
                       "218/18M":["Mehdipatnam","Sarojini Devi Eye Hospital","N.M.D.C.","Masab Tank","Care Hospital",
                                "Banjara Hills Road No 1 Water Tank","Panjagutta","Panjagutta Colony","Ameerpet","Mythrivanam",
                                "S.R.Nagar","E.S.I.Hospital Metro Station","Erragadda F.C.I.","Bharat Nagar","Moosapet",
                                "Kukatpally Bus Depot","Kukatpally Y Junction","Kukatpally","Sumithra Nagar","KPHB","Nizampet X Roads",
                                "Hydernagar","Miyapur Metro Station","Miyapur X Roads","Miyapur","Allwyn X Roads","Madinaguda","Huda Colony",
                                "Gangaram","Chandanagar","Lingampally","Jyothi Nagar","Sri Sai Nagar","Beeramguda","R.C. Puram","Icrisat",
                                "Patancheru","Isnapur X Road","Rudraram Gate","Gitam University"],
                       "300/216":["LB Nagar","Sagar Ring Road Owaisi Way","T K R Kaman","Shakti Nagar","Gayatri Nagar X Road","Manda Mallamma",
                                "Champapet X Roads","Owaisi Hospital","Midhani Depot","Drdl","Anurag Lab","Baba Nagar","Dlrl",
                                "Chandrayanagutta","Keshavagiri","Bandlaguda","Chandrayangutta Bandlaguda","Oddamgudem Stop 1",
                                "Mylardevpally","Durga Nagar Katedan","Durganagar","Aramghar X Roads","Shivarampally X Road",
                                "Weaker Section Colony","Shivarampally Quarters","Dairy Farm","Happy Homes Ring Road","Upperpally X Road",
                                "Shiva Nagar","Hyderguda X Road","Attapur X Road","Ring Road","Jyothi Nagar","Laxmi Nagar","Rethibowli",
                                "Nanal Nagar","Salarjung Colony","Toli Chowki","Galaxy","Brindavan Colony Road","Shaikpet Nala",
                                "Narayanamma Engineering College","Dargah Tombs Road","Lid Cap","Khajaguda X Road","Raidurgam",
                                "Nanal Nagar","Roda Mistry College","Gachi Bowli","Telecom Nagar","Gachibowli X Roads","Indra Nagar",
                                "Nanak Ram Guda","Iit","Gachibowli Stadium","Hyderabad Central University Gate 2","Masjid Banda","Hcu",
                                "Hcu Telephone Exchange","Hcu Depot","Bhagyanagar Colony","Doyens Colony","Alind Doyens Colony",
                                "Gulmohar Park","Lingampally Station","Serlingampalli","Tara Nagar","Lingampally"],
                       "156/216":["Lingampally","Tara Nagar","Serlingampalli","Gulmohar Colony","Alind Doyens Colony","Bhagyanagar Colony",
                                "Hcu Bus Depot","Hcu Telephone Exchange","Hyderabad Central University","Hyderabad Central University Gate 2",
                                "Gachibowli Stadium","Iiit","Gpra","Indra Nagar","Telecom Nagar","Roda Mistry College","Khajaguda X Road",
                                "Hs Dargha","Narayanamma Engineering College","Shaikpet Nala","Tolichowki","Galaxy","Salarjung Colony",
                                "Nanal Nagar","Rethibowli","Mehdipatnam","Sarojini Devi Eye Hospital","NMDC","Masab Tank","Ac Guards",
                                "Lakdikapul","Lakdikapul Metro","Assembly","Nampally Grand Plaza","Nampally","Mozamjahi Market","Abids",
                                "Bank Street Koti","Shankar Mutt","Chaderghat","Yashoda Hospital","Malakpet Super Bazar","T.V.Tower",
                                "Moosaram Bagh","Dilsukhnagar","Chaitanyapuri","Kothapet","Doctors Colony","LB Nagar Metro","LB Nagar",
                                "Chintalkunta","Vishnu Theatre","Sushma Theater","Autonagar","High Court Colony Deer Park","Bhagyalatha",
                                "Lecturers Colony","Thorrur X Road","Hayath Nagar Bus"],
                       "5k/92":["Secunderabad","Clock Tower","Patny Center","Bata","Bible House","Boats Club","Boats Club","Tank Bund",
                                "DBR Mills","Lakdikapul Metro","Ac Guards","Masab Tank","Masab Tank","Potti Sriramulu Nagar","NMDC",
                                "Sarojini Devi Eye Hospital","Mehdipatnam Corner","Rethibowli","Laxmi Nagar","Attapur X Road","Hyderguda X Road",
                                "Shiva Nagar","Upperpally X Road","Happy Homes Ring Road","Rajendra Nagar Bus Depot",
                                "Extension Education Institute"],
                       "18/219":["Uppal","Boduppal X Road","Peerjadiguda Kaman","Uppal","Uppal Gandhi Statue","Uppal Sub Station",
                                "Uppal X Roads","Survey Of India","National Geophysical Research Institute","Habsiguda","Tarnaka Aaradhana",
                                "Railway Degree College","Mettuguda","Alugadda Baavi South","Chilkalguda Circle","Secunderabad Tsrtc Rathifile",
                                "Secunderabad","Secunderabad YMCA","Swimming Pool North","Paradise","Airport Backside","Tadbund",
                                "Ashish Gardens","Chinna Thokata","Bowenpally X Road","Ferozeguda","Raju Colony","Balanagar X Roads",
                                "Citd","Niper","IDPL","Prashanth Nagar","Kukatpally Y Junction","Kukatpally","Sumithra Nagar","KPHB",
                                "JNTU","Nizampet X Roads","Hydernagar","Miyapur Metro","Miyapur","Allwyn X Roads","Madinaguda","Madinaguda",
                                "Deepthisree Nagar","Huda Colony","Gangaram","Chandanagar","Lingampally"],
                       "6H":["Tolichowki","Salarjung Colony","Nanal Nagar","Mehdipatnam","Sarojini Devi Eye Hospital","NMDC","Masab Tank",
                                "Ac Guards","Lakdikapul Metro","Lakdikapul Metro","Telephone Bhavan","Secretariat","Liberty","Himayath Nagar",
                                "Narayanaguda","Chikkadpally","Baghlingampally","Barkatpura","Shankar Mutt","Fever Hospital","Nallakunta",
                                "Vidyanagar","Adikmet","Ramnagar Gundu","Jamia Osmania","Osmania University","Manikeshwari Nagar",
                                "Tarnaka Uppal","Habsiguda","Hmt Nagar","Nacharam","Nacharam ESI Hospital","IDA Nacharam X Road",
                                "Janapriya","Mallapur","Noma Function Hall","HBP lay Ground","Nrm College","Unani Hospital","SP Nagar",
                                "Kushaiguda Depot","South Kamalanagar","ECIL X Roads"],
                       "45":["ESI Hospital Metro","ESI Hospital","SR Nagar","SR Nagar","Mythrivanam","Ameerpet Metro",
                                "Ameerpet Elephant House","Ameerpet","Sheeshmahal","Lal Bungalow Ameerpet","Greenlands",
                                "Begumpet Railway Station North","Begumpet Hps Gate1","Begumpet","Shamlal North","Begumpet",
                                "Prakash Nagar","Begumpet","Prakash Nagar","Begumpet Police Lines","Yatri Nivas","Anand Theatre",
                                "Paradise Metro","Paradise","MG Road","Ranigunj","Boats Club","Jeera","Kavadiguda Signal","Kalpana",
                                "Krishna Nagar","Musheerabad Police","Raja Delux","Golconda X Road","RTC X Road","RTC Bhavan","Vst"],
                       "21":["Venkatapuram Colony","Venkatapuram X Road","Vaishnavi Matha Temple","Bhatia Bakery","Lothkunta",
                             "Family Quarter","Eme","Lalbazar","Tirumalgherry","Tirumalagiri","Karkhana Temple Arch","Vikrampuri",
                             "Jubilee","Patny","Parade Ground Metro","Secunderabad YMCA","Secunderabad"],
                       "9":["Jeedimetla","Jeedimetla Substation","Hmt Factory","Chintal","Ganesh Nagar","Hal","Balanagar",
                                "Fateh Nagar X Road","Valmiki Nagar","Fateh Nagar","Sanath Nagar","Sanath Nagar Police Station",
                                "Erragadda","Erragadda FCI","ESI Hospital Metro","SR Nagar","Mythrivanam","Ameerpet","Nims","Erramanzil",
                                "Khairatabad","Chintal Basti","Lakdikapul Metro","Assembly","Nampally Station Road","Koti Bus Terminal",
                                "Putili Bowli","Central Bus Station","Gowliguda Bus Depot","Afzalgunj","Charminar"],
                       "5":["Chilakalaguda","Secunderabad","Chilkalguda Circle","Secunderabad Tsrtc Rathifile","Secunderabad Railway",
                                "Secunderabad","Clock Tower","Patny Center Chandana Bros","Swapnalok Complex","Paradise",
                                "Mahatma Gandhi Road 125","MG Road","Ranigunj","Boats Club","Boats Club","DBR Mills","Tank Bund",
                                "DBR Mills","Mini Tankbund","Secretariat","Accountant General Office","Birla Mandir","Lakdikapul Metro",
                                "Ac Guards","Masab Tank","Potti Sriramulu Nagar","NMDC","Sarojini Devi Eye Hospital","Mehdipatnam Corner",
                                "Mehdipatnam"],
                         "219/272G": ["Gandimaisamma","Bahadurpally X Roads","Suraram X Road","Saibad X Road","Jeedimetla Bus Depot",
                             "Jeedimetla Substation Bus Stop","Shapur Nagar","HMT Factory","Chintal Chowrasta","Ganesh Nagar",
                             "District Bus Stop IDPL Colony","IDPL Colony","HAL","Balanagar X Roads","Prashanth Nagar","Kukatpally",
                             "KPHB Colony","JNTU","Nizampet X Roads","Vasanth Nagar","Hydernagar","Miyapur Metro Station","Miyapur Bus Stop",
                             "Allwyn X Roads","Madinaguda","Huda Colony","Gangaram Bus Stop","Chandanagar","Lingampally Bus Station",
                             "Jyothi Nagar","Ashok Nagar","Sri Sai Nagar","Beeramguda","Bhel Pushpak","RC Puram","Railway Station Gate",
                             "ICRISAT","Patancheru","Patancheru Market","Patancheru Bus Station"],
                "219": ["Patancheru Bus Station","Patancheru Market","Patancheru","ICRISAT","Railway Station Gate","RC Puram",
                        "Bhel Pushpak","Beeramguda","Sri Sai Nagar","Ashok Nagar","Jyothi Nagar","Lingampally","Chandanagar",
                        "Gangaram Bus Stop","Huda Colony Bus Stop","Madinaguda","Mythri Nagar","Allwyn X Roads","Miyapur",
                        "Miyapur X Roads","Miyapur Metro Station","Hyder Nagar","Nizampet X Roads","JNTU","KPHB Colony","Kukatpally",
                        "Y-Junction","Prashanth Nagar","Balanagar X Roads","Shobana","Ferozguda","New Bowenpally","Tadbund","Paradise",
                        "Patny","Clock Tower","Secunderabad Junction"],
                "229": ["Secunderabad Bus Station","Clock Tower","Patny","Paradise","Tadbund","Chinna Thokata","Bowenpally Police Station",
                        "Bowenpally Check Post","MMR Gardens","Military Dairy Farm","Suchitra Circle","Jeedimetla Village",
                        "Angadipeta","NCL Balaji hospital","Ganga Enclave","NCL North Avenue","Cine Planet Kompally","Prajay",
                        "Dollapally X Road","Kompally","Vaishnavi Constructions","Farm Area Bus Stop","Kompally Bridge",
                        "Gundlapochampally","Prestige","Kandlakoya Bus Stop","CMR college","Medchal Gubba","Medchal Checkpost",
                        "Medchal Ambedkar Chowrasta","Medchal"],
                "277D": ["Ibrahimpatnam Bus Station","Ibrahimpatnam Chowrasta","Upparguda X Road","Sheriguda Bus Stop",
                         "Sri Indu Engineering College","Mangalpally X Road","Koheda X Road","Bongulur X Roads Bus Stop",
                         "Manneguda X Road","Ragannaguda","Brahmanpally","Tuerkyamjal X Road","Injapur Cheruvu Katta","Injapur",
                         "Swami Narayana Colony","Sagar Complex Bus Stop","BN Reddy Nagar","Hasthinapuram South",
                         "Hasthinapur North(RTO Office)","Omkar Nagar Bus Stop","Sagar Ring Road","Sagar X Road","LB Nagar",
                         "LB Nagar Metro Station","Doctors Colony Bus Stop","Kothapet","Chaitanyapuri","Dilsukhnagar","TV Tower",
                         "Moosaram Bagh","Malakpet Super Bazar","Yashoda Hospital","Nalgonda X Road","Chaderghat Bus Stop",
                         "Chaderghat","Azampura","Imlibun","Darulshifa","Gowliguda Bus Stop","CBS(Central Bus Stop)"],
                "277H": ["Ibrahimpatnam Bus Station","Ibrahimpatnam Bus Station","Ibrahimpatnam Chowrasta","Upparguda X Road","Sheriguda",
                         "Sri Indu College","Mangalpally X Road","Koheda X Road","Bonguluru X Road","Manneguda X Road","Ragannaguda",
                         "Brahmanpally","Turkayamjal X Road","Telangana Chowrasta - Turka Yamjal X Road","Injapur Cheruvu Katta","Injapur",
                         "Injapur Hanuman Temple Stop","Gurram Guda X Road","Swami Narayana Colony","Sagar Complex Bus Stop",
                         "BN Reddy Nagar","Teachers Colony","Hastinapur South (Naveena College)","Hastinapur Central",
                         "Hastinapuram North Bus Stop","Hastinapur North (Rto Office)","Omkar Nagar","LB Nagar","Sagar X Road","LB Nagar",
                         "Chintal Kunta Checkpost","Chintalkunta Bus Stop","Vishnu Theatre","Panama Godown","Sushma Theater","Autonagar",
                         "High Court Colony Deer Park","Bhagyalatha","Lecturers Colony","Hayathnagar Depot"],
                 "277M": ["MM Kunta","Water Tank Manneguda X Road","Manneguda X Road","Ragannaguda","Brahmanpally","Turkayamjal X Road",
                          "Telangana Chowrasta - Turka Yamjal X Road","Injapur Cheruvu Katta","Injapur","Injapur Hanuman Temple Stop",
                          "Gurram Guda X Road","Swami Narayana Colony","Sagar Complex Bus Stop","BN Reddy Nagar","Teachers Colony",
                          "Hastinapur Central","Hastinapuram North Bus Stop","Panama Godown Bus Stop","Omkar Nagar","LB Nagar",
                          "Sagar X Road","Bairamalguda","Aware Global Hospital","Karmanghat","Green Park Colony Bus Stop",
                          "Champapet RTC Colony / Ibp","Champapet (Brilliant Gl School)","Santosh Nagar","Is Sadan",
                          "Saidabad H.F.E.C. Function Hall","Jaihind Hotel","APSEB Office Saidabad","Government Press","Chanchalguda",
                          "Sohail Hotel Bus Stop","Nalgonda X Roads","Chaderghat Bus Stop","Chaderghat","Koti Womens College"],
                "277Y": ["Is Sadan","Saidabad HFEC Function Hall","Chanchalguda","Nalgonda X Roads","Chaderghat Bus Stop","Chaderghat",
                         "Putili Bowli","Koti","Shankar Mutt"],
                "277P": ["Yashoda Hospital","Malakpet Sohail Hotel","Dabeerpura","Saidabad","Is Sadan",
                         "Santosh Nagar","Champapet","RTC Colony (Champapet)","Green Park Colony","Karmanghat Bus Stop",
                         "Aware Global Hospital","Bairamalguda","Sagar X Road","Sagar Ring Road","Omkar Nagar Bus Stop",
                         "Hastinapur North (Rto Office)","Hasthinapuram South","BN Reddy Nagar","Sagar Complex Bus Stop",
                         "Swami Narayana Colony","Injapur","Injapur Cheruvu Katta","Turkyamjal X Road","Ragannaguda",
                         "Bongulur X Roads Bus Stop","Koheda X Road","Sri Indu Engineering College","Sheriguda Bus Stop",
                         "Ibrahimpatnam Chowrasta","Ibrahimpatnam","Polkampally","Manyaguda","Kothagudem","Annamacharya Engineering College",
                         "Bata Singaram","Mount Opera","Abdullapur","Kavadi Pally","Tarmaz Pet Chowrasta","Crusher Machines","Sattupally",
                         "Bacharam","Korremula 2","Maktha","Yellamma Temple","Venkatadri Township","Ou Colony Bus Stop","Vijaypuri Colony",
                         "Pocharam Village Main Road"],
                "277": ["Central Bus Station (CBS)","Chaderghat","Chaderghat","Chaderghat Bus Stop",
                        "Malakpet Sohail Hotel","Chanchalguda","Government Press","APSEB Office Saidabad","Saidabad","Jaihind Hotel",
                        "Saidabad","Is Sadan","Santosh Nagar","Champapet Road","Champapet","RTC Colony (Champapet)","RTC Colony",
                        "Green Park Colony","Karmanghat Bus Stop","Karmanghat","Aware Global Hospital","Bairamalguda","Sagar X Road",
                        "Sagar Ring Road","Omkar Nagar Bus Stop","Hastinapur North (Rto Office)","Hastinapur X Road",
                        "Hastinapuram Bus Stop","Hastinapur Central","Hasthinapuram South","Teachers Colony","BN Reddy Nagar",
                        "Sagar Complex Bus Stop","Swami Narayana Colony","Gurram Guda X Road","Injapur","Injapur Cheruvu Katta",
                        "Telangana Chowrasta - Turka Yamjal X Road","Turkyamjal X Road","Brahmanpally","Ragannaguda","Manneguda X Road",
                        "Bongulur X Roads Bus Stop","Koheda X Road","Mangalpally X Road","Sri Indu Engineering College",
                        "Sheriguda Bus Stop","Upparguda X Road","Ibrahimpatnam Chowrasta","Ibrahimpatnam Bus Station"],
                "277N": ["Koti Womens College","Chaderghat","Chaderghat Bus Stop","Nalgonda X Roads","Yashoda Hospital",
                         "Malakpet Chermas","Malakpet Super Bazar","Saleem Nagar","TV Tower","Moosaram Bagh","Dilsukhnagar","Dilsukhnagar",
                         "Dilsukhnagar Bus Station","Chaitanyapuri","Kothapet","Doctors Colony Bus Stop","LB Nagar Metro Station","LB Nagar",
                         "Sagar X Road","Sagar Ring Road","Omkar Nagar Bus Stop","Hastinapur North (Rto Office)","Hasthinapuram South",
                         "BN Reddy Nagar","Sagar Complex Bus Stop","Swami Narayana Colony","Gurram Guda X Road","Rajyalakshmi Nagar",
                         "Gurram Guda Village","Aditya Colony Road","Gold Phase Colony","Jay Suryapatnam","Kamma Guda",
                         "Mvsr Engineering College","Nadargul"],
                "277MP": ["Ibrahimpatnam Bus Station","Ibrahimpatnam Bus Station","Ibrahimpatnam Chowrasta",
                          "Upparguda X Road","Sheriguda","Sri Indu College","Mangalpally X Road","Koheda X Road","Bonguluru X Road",
                          "Manneguda X Road","Ragannaguda","Brahmanpally","Turkayamjal X Road","Telangana Chowrasta - Turka Yamjal X Road",
                          "Injapur Cheruvu Katta","Injapur","Injapur Hanuman Temple Stop","Gurram Guda X Road","Swami Narayana Colony",
                          "Sagar Complex Bus Stop","BN Reddy Nagar","Teachers Colony","Hastinapur Central","Hastinapuram North Bus Stop",
                          "Panama Godown Bus Stop","Omkar Nagar","LB Nagar","Sagar X Road","Bairamalguda","Aware Global Hospital","Karmanghat",
                          "Green Park Colony Bus Stop","Champapet RTC Colony / Ibp","Champapet (Brilliant Gl School)","Santosh Nagar",
                          "Is Sadan","Saidabad FEC Function Hall","Jaihind Hotel","APSEB Office Saidabad","Government Press","Chanchalguda",
                          "Sohail Hotel Bus Stop","Nalgonda X Roads","Chaderghat Bus Stop","Chaderghat","Azampura","Imlibun","MGBS",
                          "Mgbs City Alighting","Central Bus Station (CBS)","Gowliguda Bus Depot","Afzalgunj","Osmangunj",
                          "Mozamjahi Market (Gandhi Bhavan)","Gandhi Bhavan","Nampally","Nampally Grand Plaza","Assembly",
                          "Lakdikapul Metro Station","AC Guards","Masab Tank","Potti Sriramulu Nagar","NMDC","Sarojini Devi Eye Hospital",
                          "Mehdipatnam Corner","Mehdipatnam Bus Station"],
                "280N": ["Secunderabad","Chilkalguda Circle","Alugadda Baavi South Bus Stop","Mettuguda",
                         "Tarnaka Uppal Stop","Habsiguda","National Geophysical Research Institute (NGRI)","Survey Of India",
                         "Uppal Sub Station","Uppal Bus Station","Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot","Medipally",
                         "Central Power Research Institute","Narapally","Vijaypuri Colony","Jodimetla X Road","Annojiguda",
                         "Shiva Reddy Guda Bus Stop","Edulabad X Road","Ghatkesar Bypass Junction","Ghstkesar Police Station Bus Stop",
                         "Nfc Nagar Arch","Community Hall Stop Nfc Nagar","Kv School Nfc Nagar","Nfc Nagar"],
                "280S": ["Jubilee Bus Station","Patny","Sangeeth","Secunderabad Tsrtc Rathifile Bus Station","Secunderabad",
                         "Chilkalguda Circle","Alugadda Baavi South Bus Stop","Mettuguda","Tarnaka Uppal Stop","Habsiguda",
                         "National Geophysical Research Institute (NGRI)","Survey Of India","Uppal Sub Station","Uppal Bus Station",
                         "Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot","Medipally","Central Power Research Institute","Narapally",
                         "Vijaypuri Colony","Jodimetla X Road","Annojiguda","Shiva Reddy Guda Bus Stop","Edulabad X Road",
                         "Ghatkesar Bypass Junction","Ghstkesar Police Station Bus Stop","Nfc Nagar Arch","Marripally Guda","Edulabad"],
                "280": ["Secunderabad","Chilkalguda Circle","Upcoming Arrivals","Alugadda Baavi South Bus Stop","Mettuguda",
                        "Tarnaka Uppal Stop","Habsiguda","National Geophysical Research Institute (NGRI)","Survey Of India",
                        "Uppal Sub Station","Uppal Bus Station","Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot","Medipally",
                        "Central Power Research Institute","Narapally","Vijaypuri Colony","Jodimetla X Road","Annojiguda",
                        "Shiva Reddy Guda Bus Stop","Ghatkesar Bus Stop"],
                 "280B": ["Bogaram","Kondapur Village 280b","Ghatkesar Bus Stop","Shiva Reddy Guda Bus Stop",
                          "Annojiguda","Vaibhav Colony","Jodimetla X Road","Vijaypuri Colony","Narapally","Central Power Research Institute",
                          "Chengicherla X Road","Medipally","Canaranagar Bus Stop","Uppal Bus Depot","Boduppal X Road","Peerjadiguda Kaman",
                          "Uppal Bus Station","Uppal Gandhi Statue","Uppal Sub Station","Uppal X Roads","Survey Of India",
                          "National Geophysical Research Institute (Ngri)","Habsiguda Bus Stop","Tarnaka Aaradhana Bus Stop",
                          "Railway Degree College","Mettuguda","Alugadda Baavi South","Chilakalaguda"],
                  "290U/463": ["Jubilee Bus Station","Jubilee Bus Station","Secunderabad YMCA",
                               "Secunderabad Bus Station (Gurudwara)","Secunderabad Railway Station","Secunderabad Tsrtc Rathifile Bus Station",
                               "Secunderabad Tsrtc Rathifile Bus Station","Secunderabad","Chilkalguda Circle","Alugadda Baavi South Bus Stop",
                               "Mettuguda Metro Station","Mettuguda","Nin/Water Tank","Tarnaka Metro Station","Tarnaka Uppal Stop",
                               "Tarnaka Pushpak Bus Stop","Habsiguda","National Geophysical Research Institute (NGRI)","Survey Of India",
                               "Uppal X Roads","Uppal X Road Bus Stop","Uppal X Roads","Uppal Metro Station","Saraswathi Nagar",
                               "Mamatha Nagar Colony","Nagole","Alkapuri","Rajeev Gandhi Nagar","Kamineni","Kamineni Hospital Bus Stop",
                               "Central Bank Colony","LB Nagar","Chintal Kunta Checkpost","Chintalkunta Bus Stop","Vishnu Theatre",
                               "Panama Godown","Sushma Theater","Autonagar","High Court Colony Deer Park","Bhagyalatha","Bhagyalatha",
                               "Lecturers Colony","Hayathnagar Depot","Thorrur X Road","Hayath Nagar Bus Station","Word And Deed School Bus Stop",
                               "Laxmireddy Palem","Pedda Amberpet","Pedda Amberpet X Road","Shanti Nagar","ORR Peddamberpet","ORR Gandicheruvu",
                               "Kanakadurga Nagar","SGM College","Ramoji Film City","Abdullapurmet","Jafferguda X Road","Singareni Colony",
                               "Mount Opera","Bata Singaram","Sai Nagar Township","Deshmukhi Saint M College","Deshmukhi"],
                   "290S": ["Secunderabad","Chilkalguda Circle","Alugadda Baavi South Bus Stop","Mettuguda","Tarnaka Uppal Stop",
                            "Habsiguda","National Geophysical Research Institute (NGRI)","Survey Of India","Uppal X Roads","Nagole","Alkapuri",
                            "Kamineni Hospital Bus Stop","LB Nagar","Chintal Kunta Checkpost","Chintalkunta Bus Stop","Panama Godown",
                            "Ganesha Temple","Sampurna","Rythu Bazar","Kamla Nagar","Subhadra Nagar (Vanasthalipuram)","Shanti Nagar (Vanasthalipuram)",
                            "Lecturers Colony","Hayathnagar Depot","Hayath Nagar Bus Station","Word And Deed School Bus Stop","Laxmireddy Palem",
                            "Pedda Amberpet","Sadasiva Heavens","Gandi Cheruvu X Road","Narayana Ias Academy","Upperguda","Koheda Gate X Roads",
                            "Umer Khan Guda Stop","Sanghi Nagar"],
                  "290A": ["Anajpur","Gayathri Nagar","Majeedpur X Road","Surmaiguda","Lashkarguda","Kanakadurga Nagar","Abdullapurmet",
                           "Ramoji Film City","SGM College","Kanakadurga Nagar","ORR Peddamberpet","Shanti Nagar","Pedda Amberpet X Road",
                           "Pedda Amberpet","Laxma Reddy Palem","Word & Deed Colony","Hayath Nagar Bus Station","Hayathnagar Depot",
                           "Lecturers Colony","Bhagyalatha","High Court Colony","Autonagar","Sushma Theatre Bus Stop","Panama Godown Bus Stop",
                           "Vishnu Theatre","Chinthalkunta Bus Stop","Chintalkunta Checkpost","LB Nagar Ring Road","LB Nagar",
                           "Central Bank Colony","Kamineni Hospital Bus Stop","Kamineni Bus Stop","Rajeev Gandhi Nagar","Alkapuri","Nagole",
                           "Mamatha Nagar Colony","Inner Ring Road","Uppal Metro Station","Uppal X Roads","Survey Of India",
                           "National Geophysical Research Institue (NGRI)","Habsiguda Bus Stop","Tarnaka Aaradhana Bus Stop",
                           "Tarnaka Metro Station","Railway Degree College","Mettuguda","Mettuguda Metro Station","Alugadda Baavi South",
                           "Chilakalaguda","Secunderabad","Chilkalguda Circle Bus Stop","Secunderabad Tsrtc Rathifile Bus Station",
                           "Secunderabad Railway Station","Secunderabad Bus Station (Gurudwara)","Secunderabad YMCA","Jubilee Bus Station"],
                  "222A": ["Patancheru","Depot Arch","Icrisat","Bhel Pushpak","Beeramguda","Beeramguda Bus Stop","Jyothi Nagar","Lingampally",
                           "Chandanagar","Gangaram Bus Stop","Huda Colony Bustop","Madinaguda","Deepthisree Nagar","Mythrinagar Bus Stop",
                           "Allwyn X Roads","Hafeezpet","Botanical Garden","Kondapur X Road","Kondapur","Shilparamam Bus Stop","Hitech City",
                           "Image Garden Bus Stop","Madhapur Petrol Pump","Madhapur Police Station Bus Stop","Live Life Hospital",
                           "Usha Kiran Movies","Jubilee Hills Check Post Bus Stop","Lv Prasad Bus Stop","TV9","Nagarjuna Circle",
                           "Vengal Rao Park","Taj Krishna","Care Hospital","Chintal Basti Bus Stop","Masab Tank Bus Stop","Ac Guards",
                           "Lakdikapul","Lakdikapul Metro Station","Assembly","Nizam College","Abids","Abids (Big Bazar)","Bank Street Koti",
                           "Koti Bus Terminal"],
                  "195": ["Bachupally X Road","BK Enclave","Miyapur Metro Station","Hyder Nagar","Nizampet X Roads","JNTU","Rythu Bazar Kp",
                          "KPHB Colony Mig","Forum Mall / K.P.H.B.Circle","Malaysian Township","Ck Tanda","Hitech City","Cyber Towers",
                          "Shilparamam","Raidurg","Lumbini Avenue","Gachi Bowli","Telecom Nagar","Gachibowli X Roads","Indra Nagar",
                          "Nanak Ram Guda","Infosys","Wipro Nanakramguda","ICICI","Infotech","Continental Hospitals","Waverock"],
                  "288D": ["Chilkur Balaji Temple","Himyat Nagar Village","Aziz Nagar","Vif College","Rane Company","Old Aziz Nagar X Road",
                           "Pbel City","Kalimandir Bus Stop","Peerancheru","Bandlaguda X Road","Raghuram Nagar","Sun City","Bapu Ghat",
                           "Flour Mill","Nala Nagar","Mehdipatnam Bus Station"],
                  "127K": ["Kondapur Bus Depot","Kondapur X Road","Paulo Travels","Kothaguda Bus Stop","Kondapur","Hitex Kaman",
                           "Shilparamam Bus Stop","Hitech City","Image Garden Bus Stop","Madhapur Petrol Pump","Madhapur Police Station Bus Stop",
                           "Live Life Hospital","Rainbow Park","Peddamma Temple Bus Stop","Usha Kiran Movies","Jubilee Check Post",
                           "Road Number 37 Check Post","Journalist Colony Kbr Park","Apollo Hospital","Banjara Hills Bus Stop",
                           "Mla Colony Bus Stop","Acb Office","Durga Enclave","Banjara Hills Kaman","Familia Hospital","Bhola Nagar",
                           "Chintal Basti Bus Stop","Ambedkar Nagar (Chinthal Basthi)","Masab Tank Bus Stop","Ac Guards","Lakdikapul",
                           "Lakdikapul Metro Station","Assembly","Nizam College","Abids","Abids (Big Bazar)","Bank Street Koti","Koti",
                           "Koti Bus Terminal"],
                   "218": ["Patancheru","Depot Arch","Icrisat","Rc Puram","Bhel Pushpak","Beeramguda","Sri Sai Nagar","Jyothi Nagar","Lingampally",
                           "Chandanagar","Gangaram Bus Stop","Madinaguda","Deepthisree Nagar","Mythrinagar Bus Stop","Allwyn X Roads","Miyapur",
                           "Miyapur X Roads","Miyapur Metro Station","Hyder Nagar","Nizampet X Roads","JNTU","KPHB","Vivekananda Nagar Bus Stop",
                           "Kukatpally Bus Stop","Kukatpally Y Junction","Kukatpally Bus Depot","Moosapet","Bharath Nagar","Prem Nagar","Erragadda",
                           "Erragadda FCI","ESI Hospital Metro Station","SR Nagar","Mythrivanam","Ameerpet Bus Stop","Panjagutta Colony Bus Stop",
                           "Nims","Erramanzil","Khairatabad Rta","Khairatabad Bus Stop","Shaadan College","Lakdikapul","Assembly","Nizam College",
                           "Abids","Abids (Big Bazar)","Bank Street Koti","Koti Bus Terminal"],
                    "113K/L": ["Lingampally Bus Station","Chandanagar","Gangaram Bus Stop","Huda Colony Bustop","Madinaguda","Deepthisree Nagar",
                               "Mythrinagar Bus Stop","Allwyn X Roads","Miyapur","Miyapur Metro Station","Hyder Nagar","Vasanth Nagar","JNTU","KPHB",
                               "Vivekananda Nagar Bus Stop","Sumithra Nagar Bus Stop","Kukatpally Crossroads","Kukatpally Govt College",
                               "Kukatpally Y Junction","Kukatpally Bus Depot","Moosapet","Bharath Nagar","Prem Nagar","Erragadda","Erragadda FCI",
                               "ESI Hospital Metro Station","SR Nagar","Mythrivanam","Ameerpet Bus Stop","Panjagutta Colony Bus Stop","Nims",
                               "Erramanzil","Khairatabad Rta","Khairatabad Bus Stop","Chintal Basti","Lakdikapul Metro Station","Saifabad",
                               "Telephone Bhavan","Secretariat","Liberty","Himayath Nagar Bus Stop","Narayanaguda","Chikkadpally Bus Stop",
                               "Baghlingampally","Barkatpura","Fever Hospital","Tilak Nagar Bus Stop","6 Number","Sree Ramana Bus Stop",
                               "Irani Hotel Bus Stop","Ramanthapur Colony Bus Stop","Ramanthapur Church","Uppal X Roads","Uppal Metro Station",
                               "Uppal Gandhi Statue","Pochamma Temple","Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot"]



                                 }

    def find_bus_route(self, start_point, end_point):
        for route, stops in self.bus_routes_for_sp_ep.items():
            if start_point in stops and end_point in stops:
                start_index = stops.index(start_point)
                end_index = stops.index(end_point)
                if start_index < end_index:
                    route_stops = stops[start_index:end_index + 1]
                else:
                    route_stops = stops[end_index:start_index + 1][::-1]

                return route, route_stops

        return None, None

    def search(self, instance):
        sp = self.start_point_input.text
        ep = self.end_point_input.text

        bus_route_for_sp_ep, stops_between = self.find_bus_route(sp, ep)

        if bus_route_for_sp_ep and stops_between:
            result = f"The Bus Route from {sp} to {ep} is covered by Bus Number -> {bus_route_for_sp_ep}\n"
            results = ''
            results += f"The stops between {sp} and {ep} are:\n-->"
            results += '\n-->'.join(stops_between)
        else:
            results = ''
            button = MDRectangleFlatButton(text='back', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                           text_color=(0, 0, 0, 1), line_color=(0, 0, 0, 1), line_width=2)
            self.dialog = MDDialog(text='Please enter search point and end point', buttons=[button])
            button.bind(on_press=self.close)
            self.dialog.open()
            return


        self.manager.get_screen('results_for_sp&ep').show_results(results,result)
        self.manager.current = 'results_for_sp&ep'
        self.clear_input_fields()
        self.clear_input_fields()

    def close(self, *args):
        self.dialog.dismiss()


class ResultsScreen_for_sp_ep(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen_for_sp_ep, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.label1 = MDLabel(pos_hint={"center_x": 0.55, "center_y": 0.9})
        self.label1.font_name = 'Poppins-Bold.ttf'
        self.label1.font_size = '19sp'
        self.add_widget(self.label1)
        sv = ScrollView(size_hint_y=0.85)
        g = GridLayout(cols=1, spacing="20dp", padding="20dp")
        g.size_hint_y = None
        g.bind(minimum_height=g.setter("height"))
        self.result_label = MDLabel(size_hint_y=None, height=dp(1300))
        self.result_label.font_name = 'Poppins-SemiBold.ttf'
        self.result_label.font_size = '18sp'
        g.add_widget(self.result_label)
        sv.add_widget(g)
        self.add_widget(sv)
        self.add_widget(self.layout)

    def show_results(self, results,result):
        self.label1.text = result
        self.result_label.text = "".join(results)

        back_button = MDRectangleFlatButton(text='Go to Main Screen', pos_hint={'center_x': 0.5, 'center_y': 0.04},
                                            text_color=(0, 0, 0, 1), line_color=(0, 0, 0, 1), line_width=2)
        back_button.bind(on_release=self.switch_screen)
        self.layout.add_widget(back_button)

    def switch_screen(self, instance):
        self.manager.current = 'main'


class Screen_for_Busnumber(Screen):
    def __init__(self, **kwargs):
        super(Screen_for_Busnumber, self).__init__(**kwargs)
        self.layout = FloatLayout()

        start_point_box = BoxLayout(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=(2, 2, 2, 2),
            spacing=2
        )

        self.search_bus_number = MDTextField(
            hint_text="Enter your bus number",
            mode="rectangle",
            icon_right="magnify",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, None),
            height=dp(48),

        )
        start_point_box.add_widget(self.search_bus_number)
        self.layout.add_widget(start_point_box)

        # Add search button
        search_button = MDRectangleFlatButton(text='Search', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                              text_color=(0, 0, 0, 1), line_color=(0, 0, 0, 1), line_width=2)
        search_button.bind(on_release=self.search)
        self.layout.add_widget(search_button)

        self.add_widget(self.layout)

        back_button = MDRectangleFlatButton(text='Go to Main Screen', pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                            text_color=(0, 0, 0, 1), line_color=(0, 0, 0, 1), line_width=2)
        back_button.bind(on_release=self.switch_screen)
        self.layout.add_widget(back_button)

    def clear_input_fields(self):
        self.search_bus_number.text = ""

    def switch_screen(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main'

    def search(self, instance):
        bus_number = self.search_bus_number.text
        if bus_number in bus_routes:
            self.manager.get_screen('results_for_bus_number').update_results(bus_number)
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'results_for_bus_number'
        else:
            button = MDRectangleFlatButton(text='back', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                           text_color=(0, 0, 0, 1), line_color=(0, 0, 0, 1), line_width=2)
            self.dialog = MDDialog(text='Please enter a bus number', buttons=[button])
            button.bind(on_press=self.close)
            self.dialog.open()

    def close(self,*args):
        self.dialog.dismiss()


bus_routes = {"25s": ["Suchitra", "Suchitra X Road", "Loyola college", "BHEL quarters", "PV junction Bus Stop",
              "Father balaiah nagar", "Old alwal (IG Statue)", "Old alwal Bus Stop",
                              "Temple alwal Bus Stop", "Alwal police Station Bus Stop", "Alwal bus stop",
                              "Ram nagar–Alwal", "Lothkunta bus Stop", "Family quarter"
                                , "EME bus stop", "Lalbazar",
                              "Tirumalgherry bus Stop", "Trimulgherry X Roads", "RTO trimulgherry", "Tirumalagiri",
                              "Karkhana Temple Arch", "Vikarampuri", "HPS High School", "Patny",
                              "Patny center", "Clock tower", "Secunderabad Junction"],
                "227": ["Bhadurpally X Roads", "Bhadurpally village", "Maisammaguda","Appreal Park ", "Dulapally","Kompally","Prajay",
                       "NCL north avenue","Balaji hospital","Angadipet","Jeedimetla ","Suchitra circle","Dairy farm","M.M.R.Gardens",
                        "Bowenpally Checkpost", "Bowenpally Police Station","Tadbund","Paradise","Patny",
                        "Clock tower","Secunderabad junction"],
                "1D": ["Dilsukhnagar bus Station (Opposite Side)", "T.V.Tower / Moosaram Bagh", "Malakpet super Bazar", "Malakpet chermas",
                      "Yashoda hospital","Chaderghat","Koti womens College","Koti maternity Hospital","Sultan bazar",
                      "Ram koti Bus Stop","Blood bank","Y.M.C.A.","Narayanaguda","Narayanaguda","RTC X road","Golconda X roads",
                      "Musheerabad police Station","Gandhi hospital bus stop","Bhoiguda","Secunderabad/Chilkalguda circle Bus Stop",
                      "Secunderabad rathifile bus station"],
                "1Z/229": ["Medchal bus terminal","Medchal Ambedkar Chowrasta","Medchal chekpost","Cmr college",
                          "Kandlakoya bus stop","Prestige","Gundla pochampally","Kompally","Dollapally X Road","Prajay",
                          "Cine planet kompally","NCL north avenue","Angadipeta","Jeedimetla ","Suchitra circle","Dairy farm","M.M.R.Gardens","Bowenpally Checkpost",
                       "Bowenpally Police Station","Tadbund","Paradise","Mahatma gandhi road,125","Ranigunj bus stop",
                         "Boats club bus stop","DBR mills","Tank bund","Mini tankbund","Secretariat",
                          "Accountant general(A & G)Office/Birla Mandir","Assembly","Nampally grand plaza","Nampally",
                          "Nampally haj house","Gandhi Bhavan","Mozamjahi market(Gandhi Bhavan)","Osmangunj","Afzalgunj Bus Station",
                         "Nayapul","Madina","City college","Petla burj","Puranapool out post","Puranapool mastan gati",
                          "Bahadurpura police station","Bahadurpura","Nehru Zoological Park","Thadban","Mir alam tank filter beds",
                           " Danama jhopdi","Hasan nagar","Raghavendra colony","Sardar Vallabhbhai Patel National Police Academy","Aramghar X Roads" ],
                 "1V": ["Secunderabad rathifile bus station","Gandhi hospital bus stop","Raja delux","Chikkadpally bus stop",
                       "YMCA","Kachiguda","Ram koti bus stop","Koti maternity Hospital","Chaderghat bus stop","Yashoda hospital",
                       "Malakpet super bazar","TV tower/Moosaram bagh","Dilsukhnagar","Chaitanyapuri","Kothapet","Doctors colony bus stop",
                       "LBNagar metro station","LB nagar","Chintalkunta bus stop","Vishnu theatre","Ganesha temple",
                        "Red tank bus stop","NGO's Colony"],
                  "1J": ["Secunderabad rathifile bus station","Gandhi hospital bus stop","Raja delux","Chikkadpally bus stop",
                        "Narayanaguda","YMCA","Kachiguda X Road","Koti maternity Hospital","Koti womens college",
                        "Chaderghat","Central bus station(C.B.S.)","Afzalgunj central library","Osmania hospital",
                         "Jumerat bazar","Dhoolpet","Bheem nagar","Jiyaguda","Cargil Nagar","Jiyaguda Kht"],
                  "1D/V": ["NGOS colony","Vaidehi Nagar","Gauthami nagar bus stop","Vanasthalipuram","Complex vanasthalipuram",
                          "Ganesh Temple","	Panama Godowns","Vishnu theatre","Chinthalkunta Bus Stop",
                           "Old chintalkunta checkpost","LB nagar","LB nagar Metro station","Doctors colony bus stop",
                          "Green Hills Colony","Ashta Lakshmi Bus Stop","Kothapet bus stop","Fruit Market/Shalini Theatre",
                          "Chaitanyapur","Dilsukhnagar","Moosarambagh","Super bazar bus stop","Malakpet",
                           "Yashoda hospital bus stop","Nalgonda X Road","Chaderghat bus stop","Koti womens college",
                           "Koti Maternity Hospital","Sultan bazar bus stop","Ram koti bus stop","Kachiguda X Road",
                          "Kachiguda","YMCA","Narayanaguda bus stop","Chikkadpally bus stop","Musheerabad bus stop",
                          "Golconda X Road","Raja delux bus stop","Musheerabad","Gandhi hospital",
                          "Bhoiguda west bus stop","Chilkalguda circle bus stop","Rathifile bus station"],
                   "5K/188": ["Kalimandir","Bandlaguda","Suncity","Sai Ram Nagar(Langar House)","Bapu Ghat",
                             "Bapu Nagar","Langar House Bus Stop","Nanalnagar Bus Stop","Rethibowli","Mehdipatnam Bus Stop",
                              "Sarojini Bus Stop"," Nmdc Bus Stop","Golconda Hotel","Masab Tank Bus Stop","Mahavir Hospital",
                              "Lakdikapool Bus Stop"," Ranigunj Bus Stop","Bible House","Bata(Rp Road)" ,"James Street",
                             "Mahaboob College","Patny","Clock Tower"," Secunderabad Junction"],
                   "5K": ["Secunderabad rathifile bus station","Clock tower","Patny ","Bata","Bible house","Boats club","Tank bund",
                         "DBR Mills","Secretariat","Telephone bhavan","Saifabad","Lakdikapul Metro station","Ac guards",
                         "Masab tank puspak","Mahavir bus stop","Golconda hotel","Potti sriramulu nagar bus stop",
                         "Masab Tank","NMDC bus stop","Sarojini devi eye hospital","Mehdipatnam bus stop"],
                   "5R": ["Kowkoor","Water tank","Risala bazar","Sadhana Mandir","Bollaram","Raithu bazar","Alwal bus station",
                         "Ram nagar alwal","Lothkunta bus stop","Maruti nagar","Family quarter bus stop","Eme bus stop",
                          "Lalbazar","Tirumalgherry bus stop","Hanuman temple(Tirumalgherry)","Karkhana temple arch",
                         "Karkhana","Vikrampuri","Jubilee Bus Station","Patny","Bata","Bible house","Boats club","Tank bund",
                         "DBR Mills","Secretariat","Telephone bhavan","Saifabad","Lakdikapul Metro station","Ac guards",
                         "NMDC bus stop","Sarojini devi eye hospital","Mehdipatnam bus stop"],
                   "5K/92": ["Rajendra nagar bus stop","Extension Education Institute (EEI)","Budvel bus stop",
                            "Dairy farm bus stop","Happy home bus stop","Upperpally X Road","Shiva nagar",
                            "Hyderguda X Road","Attapur X Road","Laxmi nagar","Rethibowli","Mehdipatnam corner",
                            "Sarojini Devi Eye hospital","NMDC bus stop","Masab Tank","Ac Guards",
                             "Lakdikapol Metro station","Secunderabad rathifile bus station","Clock towe","Patny ",
                             "Bata","Bible house","Boats club","Tank bund", "DBR Mills"],
                    "5M": ["Secunderabad rathifile bus station","Clock tower","Patny ","Bata","Bible house","Boats club","Tank bund",
                         "DBR Mills","Secretariat","Telephone bhavan","Lakdikapul Metro station","Ac guards",
                         "Masab tank","Vijay nagar colony","Mallepally chowk","Asif nagar","Amba theatre","Mehdipatnam bus station"],
                    "10KM/224G": ["Secunderabad raithfile bus stop","Parade ground Metro station","Paradise Metro station",
                                 "Yatri nivas/Anand theatre","Begumpet police line","Begumpet/Prakash nagar","Rasoolpura",
                                 "Begumpet","Begumpet bus stop","Begumpet Railway station north","Greenlands bus stop",
                                 "Lal Bungalow ameerpet","Sheeshmahal Bus Stop","Satyam Theatre Cross Roads","Mythrivanam",
                                 "SR Nagar","ESI hospital","ESI hospital Metro Station","Erragadda FCI","Erragadda","Prem nagar",
                                 "Bharat Nagar","Moosapet Bus Stop","Kukatpally Bus Depot","Kukatpally Y Junction",
                                  "Kukatpally Bus Stop","Vivekanadanagar Colony Rdr Hospital","KPHB","JNTU","Nizampet X Roads",
                                 "Vasanth Nagar","Hydernagar Bus Stop","Hyder Nagar","Miyapur Metro Station","Miyapur X Roads",
                                 "B.K. Enclave","Aparna Company","Kousalya Colony","Bachupally","Vignan Jyothi College",
                                 "Pragathi Nagar Bus Stop","Bowram Pet","Bowram Pet Chowrasta","Bowrampet Maisamma Temple",
                                 "Gandi maisamma"],
                     "10H": ["Secunderabad bus station(Gurudwara)","Clock Tower","Patny","Swapnalok Complex","Paradise Metro Station",
                            "Yatri Nivas /Anand Theatre","Begumpet Police Line","Prakash Nagar","Begumpet","Begumpet Bus Stop",
                            "Begumpet Railway Station North","Greenlands Bus Stop","Lal Bungalow Ameerpet","Sheeshmahal Bus Stop",
                            "Satyam Theatre Cross Roads","Yousufguda Checkpost","Srinagar X Road / Indira Nagar X Road","Venkatagiri",
                            "Road Number 1","Jubilee Check Post","Peadamma Temple","Rainbow Park","Live Life Hospital",
                            "Madhapur Police Station Bus Stop","Madhapur Timber Depot","Hitech City","Shilparamam Bus Stop",
                            "Hitech City Bus Stop","Kondapur","Kothaguda X Roads","Kondapur Bus Depot"],
                     "10": ["Secunderabad Railway Station","Secunderabad bus station(Gurudwara)","Clock Tower","Patny","Swapnalok Complex","Paradise Metro Station",
                            "Yatri Nivas /Anand Theatre","Begumpet Police Line","Rasoolpura", "Begumpet","Begumpet bus stop",
                            "Begumpet Railway station north","Greenlands bus stop","Lal Bungalow ameerpet","Sheeshmahal Bus Stop",
                            "Ameerpet","Mythrivanam","SR nagar","ESI hospital Metro Station","Erragadda FCI","Erragadda",
                            "Sanath Nagar Police Station","Sanath Nagar","Sanath Nagar Bus Depot"],
                     "10F": ["Secunderabad Railway Station","Secunderabad bus station(Gurudwara)","Clock Tower","Paradise Metro Station",
                            "Yatri nivas/Anand theatre","Begumpet police line","Begumpet/Prakash nagar","Rasoolpura","Begumpet",
                            "Begumpet bus stop","Begumpet Railway station north","Greenlands bus stop",
                            "Lal Bungalow ameerpet","Sheeshmahal Bus Stop","Satyam Theatre Cross Roads","Mythrivanam",
                            "SR Nagar","ESI hospital","ESI hospital Metro Station","Erragadda FCI","Erragadda","Prem nagar",
                            "Mothi Nagar","Borabanda Bus Station"],
                     "10JP": ["Kukatpally Bus Depot","Kukatpally Y Junction","Sangeeth Nagar","Kukatpally Bus Stop",
                             "Sumithra Nagar Bus Stop","Vivekanadanagar Colony Rdr Hospital","Food World","KPHB","JNTU",
                             "Nizampet X Roads","JNTU college","Nizampet Village","Kesenaris","Rajiv Gandhi Nagar",
                             "Rajeev Gandhi Nagar 2","Bachupally"],
                     "10HA": ["Allwyn Colony Bus Stop","Jagadgiri Gutta Bus Stop","Papi Reddy Nagar","Gandhi Nagar Bus Stop",
                             "Giri Nagar","IDPL Bus Stop","Balanagar Bus Stop","Shobana","Ferozeguda","New Bowenpally Bus Stop",
                             "Chinnathokata","Tadbund Bus Stop","Sikh Village Rd","	Paradise Bus Stop","patny","Clock Tower",
                             "Secunderabad Junction"],
                     "10KJ": ["Jagadgiri Gutta Bus Stop","Pragathi Nagar Bus Stop","Asbestas Colony Bus Stop","Kukatpally Bus Stop",
                             "Moosapet Bus Stop","Bharat Nagar(Moosapet) Bus Stop","Erragadda","ESI Bus Stop","S R Nagar",
                             "Mytrivanam","Ameerpet Bus Station","Sheeshamahal","Greenlands","Begumpet Railway Station",
                             "Prakash Nagar Bus Stop","Rasoolpura","Police Lines-Begumpet Bus Stop","Anand Theatre","Paradise Bus Stop",
                             "patny","Clock tower","Secunderabad Junction"],
                     "10KM": ["Secunderabad raithfile bus stop","Parade ground Metro station","Paradise Metro station",
                                 "Yatri nivas/Anand theatre","Begumpet police line","Begumpet/Prakash nagar","Rasoolpura",
                                 "Begumpet","Begumpet bus stop","Begumpet Railway station north","Greenlands bus stop",
                                 "Lal Bungalow ameerpet","Sheeshmahal Bus Stop","Satyam Theatre Cross Roads","Mythrivanam",
                                 "SR Nagar","ESI hospital","ESI hospital Metro Station","Erragadda FCI","Erragadda","Prem nagar",
                                 "Bharat Nagar","Moosapet Bus Stop","Kukatpally Bus Depot","Kukatpally Y Junction",
                                  "Kukatpally Bus Stop","Vivekanadanagar Colony Rdr Hospital","KPHB","JNTU","Nizampet X Roads",
                                 "Vasanth Nagar","Hydernagar Bus Stop","Hyder Nagar","Miyapur Metro Station","Miyapur X Roads",],
                     "24B/281": ["Secunderabad/Chilkalguda Circle","Alugadda Baavi South Bus Stop","Mettuguda","Tarnaka Uppal Stop",
                                 "Habsiguda","National Geophysical Research Institute (N.G.R.I)","Survey Of India","Uppal Sub Station",
                                 "Uppal Bus Station","Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot","Medipally",
                                 "Central Power Research Institute","Narapally","Vijaypuri Colony","Jodimetla X Road","Annojiguda",
                                 "Shiva Reddy Guda Bus Stop","Ghatkesar Bus Stop"],
                      "24": ["Secunderbad junction","Patny","Vikrampur bus stop","Hanuman temple(Tirumalagiri)","Tirumalagiri bus stop",
                            "Lalbazar","Lalbazar circle","Nagmandir","CTW bus stop","EME center","Ammuguda Bazar",
                             "Yapral water tank bus stop","Yapral bus stop"],
                       "24S/273": ["Gandimaisamma","Bahadurpally X Roads","Bahadurpally","Maisammaguda","Dulapally","Dollapally X Road",
                                  "Prajay","NCL North Avenue","Balaji Hospital","Angadipeta","Jeedimetla ","Suchitra circle","Suchitra X Road",
                                  "Loyola College","Bhel Quarters","Pv Junction Bus Stop","Father Balaiah Nagar","Ig Statue","Old Alwal",
                                  "Temple Alwal","Alwal Police Station","Alwal Bus Stop","Ram Nagar","Lothkunta Bus Stop",
                                  "Family Quarter Bus Stop","Eme Bus Stop","Lalbazar","Lalbazar circle","Kv School X Road","Rk Puram Bridge",
                                  "Gk Colony","Neredmet Cross Road, 599","Vayupuri","Sainikpuri","Officer’S Colony",
                                  "Doctor As Rao Nagar Road","A.S. Rao Nagar","North Kamala Nagar","ECIL X Roads"],
                        "24B": ["Secunderbad junction","Secunderabad YMCA","Patny","Vikrampuri","Karkhana","Hanuman Temple (Tirumalgirri)",
                               "Tirumalgirii Bus Stop","Lalbazar X Road","Lalbazar Circle","Guruvayurappan Temple","Nagmandir",
                               "Eme War Memorial","Eagle Chowk","EME Center","Ammuguda Bazar","Jai Jawahar Nagar","Yapral Circle",
                               "Yapral Bus Stop","Swarnandhra Colony","Gks Pride","Balaji Nagar Poultry Farm","Balaji Nagar"],
                        "24S": ["ECIL X Roads","North Kamala Nagar","Radhika X Roads","Bhashyam As Rao Nagar","Officer’S Colony",
                               "Vayupuri","Neredmet X Road","Secunderabad Central","Robert Road","Kv School X Road","Aoc",
                               "Lalbazar","Eme Bus Stop","Lothkunta Bus Stop","Alwal Bus Station","Alwal Police Station",
                               "Temple Alwal","Old Alwal","Ig Statue","Father Balaiah Nagar","Loyola college","Suchitra X Road"],
                        "25S/229":["Medchal bus terminal","Medchal Ambedkar Chowrasta","Medchal chekpost","Cmr college",
                                   "Kandlakoya bus stop","Prestige","Gundla pochampally","Kompally","Dollapally X Road","Prajay",
                                   "Cine planet kompally","NCL north avenue","Angadipeta","Jeedimetla ","Suchitra circle","Loyola college",
                                   "Bhel Quarters","Pv Junction Bus Stop","Father Balaiah Nagar","Ig Statue","Old Alwal","Temple Alwal",
                                  "Alwal Police Station","Alwal Bus Station","Lothkunta Bus Stop","Family Quarter Bus Stop",
                                  "Eme Bus Stop","Lalbazar","Tirumalgirii Bus Stop","Tirumalgirii X roads","Hanuman Temple (Tirumalgirri)",
                                  "Karkhana Temple Arch","Karkhana","Vikrampuri","Jubilee Bus Station","Patny","Secunderabad YMCA","Secunderbad junction"],
                        "25M/SN": ["Secunderbad junction","Secunderabad YMCA","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                   "Karkhana Temple Arch","Hanuman Temple (Tirumalgirri)","Tirumalgirii X roads","Tirumalgirii Bus Stop",
                                 "Lalbazar","Eme Bus Stop","Family Quarter Bus Stop","Maruti Nagar","Lothkunta Bus Stop","Alwal Bus Station",
                                  "Alwal Police Station","Temple Alwal","Old Alwal","Ig Statue","Select Talkies","Macha Bolaram",
                                  "MG Nagar","Gopalnagar X Roads","Hanuman Temple","Sanjeev Reddy Garden","Railway Colony","ARK Homes",
                                  "Sarannagar "],
                          "25A": ["Secunderbad junction","Secunderabad YMCA","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                   "Karkhana Temple Arch","Hanuman Temple (Tirumalgirri)","Tirumalgirii X roads","Tirumalgirii Bus Stop",
                                 "Lalbazar","Eme Bus Stop","Family Quarter Bus Stop","Lothkunta Bus Stop","Alwal Bus Station",
                                  "Alwal Police Station","Temple Alwal","Old Alwal","Ig Statue","Surya Nagar"],
                          "25M": ["Secunderbad junction","Secunderabad YMCA","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                   "Karkhana Temple Arch","Hanuman Temple (Tirumalgirri)","Tirumalgirii X roads","Tirumalgirii Bus Stop",
                                 "Lalbazar","Eme Bus Stop","Family Quarter Bus Stop","Lothkunta Bus Stop","Alwal Bus Station",
                                  "Alwal Police Station","Temple Alwal","Old Alwal","Ig Statue","Mg Nagar"],
                          "107JS": ["Secunderabad raithfile bus stop","Chilakalguda - Mylargadda Road","Namalagundu","Warasiguda Bus Stop",
                                   "Arts College MMTS Boudhanagarstop","Jamai-Osmania MMTS Station","No 5 Street",
                                    "Koundinya Medical & General Store","Adikmet","Vidhya Nagar","Vivekananda College Vidyanagar",
                                   "Ou Engineering College","Shivam","Sri Kusuma Haranatha/Prashanth Nagar","Syndicate Bank New Nallakunta",
                                   "6 Number","Amberpet 6 Number","Amberpet Police Station","Amberpet Police Lines","Amberpet Ali Cafe",
                                   "Sripuram Colony","Tower/Moosaram Bagh","Dilsukhnagar","Chaitanyapuri","Kothapet X Road Petrol Pump",
                                   "Saroor Nagar / Huda Complex","Mro Office","Venkateswara Colony","Saroor Nagar"],
                           "107V/R": ["LB Nagar","LB nagar Metro Station","Doctors Colony Bus Stop","Victoria Memorial Metro Station",
                                     "Dwaraka Nagar / Ashtalakshmi Temple","Pvt Market","Kothapet Fruit Market","Chaitanyapuri Metro Station",
                                     "Chaitanyapuri","Dilsukhnagar Bus Station","Moosaram Bagh","Moosarambagh Rta Office","Amberpet Ali Cafe",
                                     "Amberpet Police Lines","Amberpet 6 Number","Syndicate Bank New Nallakunta","Prashanth Nagar Bus Stop",
                                     "Ou Engineering College","Vivekananda College Vidya Nagar Stop","Vidyanagar","RTC Bhavan","RTC X Road",
                                     "Golconda X Roads","Musheerabad Police Station","Gandhi Hospital Bus Stop","Bhoiguda","Chilkalguda",
                                     "Secunderabad/Chilkalguda Circle Bus Stop","Secunderabad Rathifile Bus Station"],
                           "107VR": ["LB Nagar","LB nagar Metro Station","Doctors Colony Bus Stop","Victoria Memorial Metro Station",
                                     "Dwaraka Nagar / Ashtalakshmi Temple","Pvt Market","Kothapet Fruit Market","Chaitanyapuri Metro Station",
                                     "Chaitanyapuri","Dilsukhnagar Bus Station"],
                           "219/220K": ["Secunderabad Railway Station","Clock Tower","Swapnalok Complex","Paradise","Tadbund",
                                       "Chinna Thokata","Bowenpally X Road","Ferozeguda","Ferozeguda Bhel","Balanagar X Roads",
                                       "IDPL","Sai Nagar (Bala Nagar)","Prashanth Nagar","Sangeeth Nagar","Kukatpally Bus Stop",
                                       "Sumithra Nagar Bus Stop","Vivekanadanagar Colony Rdr Hospital","KPHB","JNTU","Nizampet X Roads",
                                       "Vasanth Nagar","Hydernagar","Miyapur Metro Station","Miyapur Busstop","Allwyn X Roads",
                                       "Madinaguda / Deepthisree Nagar","Huda Colony Bustop","Gangaram Bus Stop","Chandanagar",
                                       "Lingampally Bus Station","Nalagandla","Tellapur","Osman Sagar Road","Kollur bus stop"],
                           "219/229": ["Medchal bus terminal","Medchal Ambedkar Chowrasta","Medchal chekpost","Cmr college",
                                        "Kandlakoya bus stop","Prestige","Gundla pochampally","Kompally","Dollapally X Road","Prajay",
                                      "Cine planet kompally","NCL north avenue","Angadipeta","Jeedimetla ","Suchitra circle","Dairy farm","M.M.R.Gardens","Bowenpally Checkpost",
                                      "Bowenpally Police Station","New Bowenpally","Ferozeguda","Balanagar X Roads / Citd","IDPL","Sai Nagar (Bala Nagar)",
                                      "Kukatpally Y Junction","Kukatpally Bus Stop","Kukatpally Crossroads","Sumithra Nagar Bus Stop",
                                      "Vivekananda Nagar Bus Stop","KPHB","KPHB Vishwanth Theater","JNTU","Nizampet X Roads","Vasanth Nagar",
                                      "Hyder Nagar","Miyapur Metro Station","Miyapur X Roads","Allwyn X Roads","Mythrinagar Bus Stop",
                                      "Madinaguda","Huda Colony Bustop","Gangaram Bus Stop","Gangaram D.C.B.Bank","Chandanagar",
                                      "Lingampally Bus Station","Lingampally","Jyothi Nagar","Ashok Nagar","Beeramguda Bus Stop",
                                      "Sri Sai Nagar","Bhel Pushpak","Rc Puram","Icrisat","Patancheru","Depot Arch","Patancheru Bus Station"],
                            "25J": ["Secunderabad Railway Station","Secunderabad YMCA","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                 "Hanuman Temple (Tirumalgirri)","Tirumalgiri Bus Stop","Lalbazar","Eme Bus Stop","Family Quarter Bus Stop",
                                 "Lothkunta Bus Stop","Ram Nagar Alwal","Alwal Bus Station","Alwal Police Station","Temple Alwal","Old Alwal",
                                 "Ig Statue","Father Balaiah Nagar","Pv Junction Bus Stop","Bhel Quarters","Suchitra X Road",
                                 "Jidimetla Village","Subhash Nagar","Jeedimetla Bus Stop"],
                            "45J": ["Jeedimetla Depot","Jeedimetla Substation Bus Stop","Shapur Nagar","Gajula Ramam X Road","Hmt Factory",
                                   "Chintal","District Bus Stop IDPL Colony","IDPL Colony","Balanagar","Fateh Nagar X Road",
                                   "Valmiki Nagar","Fateh Nagar","Balakampet","Satyam Theatre Cross Roads","Ameerpet","Sheeshmahal",
                                   "Lal Bungalow Ameerpet","Greenlands Bus Stop","Begumpet Railway Station North","Begumpet Bus Stop",
                                   "Shamlal North","Begumpet","Prakash Nagar","Begumpet Police Lines","Yatri Nivas","Anand Theatre",
                                   "Paradise Metro Station","Paradise Bus Stop","MG Road","Ranigunj Bus Stop","Krishna Nagar (Bholapur)",
                                   "Musheerabad Police Station","Golconda X Road","RTC X Road"],
                            "1J": ["Afzalgunj","Gowliguda Bus Depot","Central Bus Station (CBS)","Bank Street Koti","Koti Maternity Hospital",
                                  "Sultan Bazar","Kachiguda X Road","YMCA","Narayanaguda","Chikkadpally Bus Stop","Golconda X Roads",
                                  "Gandhi Hospital Bus Stop","Secunderabad Tsrtc Rathifile Bus Station"],
                            "23GF": ["Secunderabad Railway Station","Patny","Jubilee Bus Station","Vikrampuri","Karkhana",
                                    "Karkhana Temple Arch","Hanuman Temple Tirumalgirri","RTC Colony Gun Rock Road","Teachers Colony",
                                    "Subash Nagar","Military Dairy Farm Road","Greenfieldcolony"],
                            "9F": ["Mothi Nagar","Kalyan Nagar","Sriram Nagar","Karmika Nagar","Rahmath Nagar Bus Stop","Jawahar Nagar",
                                  "Bright School","Panjagutta Colony Bus Stop","Nims","Erramanzil","Khairatabad Rta","Khairatabad Bus Stop",
                                  "Lakdikapul","Lakdikapul Metro Station","Assembly","Nampally","Mozamjahi Market ","High Court",
                                  "Charminar Bus Station","Shah Ali Banda X Road","Lal Darwaza","Falaknuma Bus Station"],
                            "229D": ["Medchal bus terminal","Medchal Ambedkar Chowrasta","Medchal chekpost","Cmr college",
                                      "Kandlakoya bus stop","Prestige","Gundla pochampally","Kompally","Dollapally X Road","Prajay",
                                      "Cine planet kompally","NCL north avenue","Angadipeta","Jeedimetla ","Suchitra circle","Dairy farm","MMR Gardens","Bowenpally Checkpost",
                                   "Bowenpally Police Station","Tadbund","Paradise","Mahatma gandhi road","Ranigunj Bus Stop","Tank Bund",
                                    "Assembly","Nampally","Mozamjahi Market","Nayapul","Salarjung Museum","Owaisi Chowk Dabeerpura",
                                    "Dabeerpura","Chanchalguda"],
                             "8X": ["Ranigunj Bus Depot","Raniganj","Boats Club","Bible House","Bata","Patny Center","Clock Tower",
                                   "Secunderabad Railway Station","TSRTC Rathifile Bus Station"],
                            "225CL": ["Lingampally Bus Stop","Chanda Nagar"," Miyapur Bus Stop","Miyapur X Roads"," Hydernagar",
                                     "Nizampet","Jntu bus stop"," Kphb Colony Bus Stop ","Sumithra Nagar","Kukatpally Bus Stop",
                                     "Moosapet Bus Stop","Bharat Nagar(Moosapet) Bus Stop ","Esi Bus Stop","S R Nagar",
                                     "Mytrivanam","Ameerpet Bus Station","Panjagutta Bus Stop","Erramanzil Bus Stop","Khairatabad Bus Stop",
                                     " Lakdikapool Bus Stop"," Assembly","Public Gardens Nampally","Nampally"," Gandhi Bhavan Bus Stop",
                                     "Putlibowli","Koti Bus Stop","Afzalgunj Bus Stop"],
                             "2C": ["Barkas","Charminar Bus Stop","Osmania Hospital","Afzalgunj Bus Stop","Cbs Bus Stop","Chaderghat Bus Stop",
                                   "Kachiguda Railway Station","Barkatpura","Nallakunta Bus Stop","Shankar Mutt","Rtc Cross roads",
                                   "Golconda X Roads","Musheerabad Bus Stop","Gandhi Hospital","Bhoiguda","Secunderabad Junction"],
                             "5C": ["Secunderabad Junction","Paradise","Mahatma Gandhi Road","Ranigunj Bus Stop","Tank Bund",
                                   "Lakdikapul Metro Station","Masab Tank / Potti Sriramulu Nagar","Sarojini Devi Eye Hospital",
                                   "Rethibowli","Nanal Nagar","Salarjung Colony Bus Stop","Brindavan Colony Road"],
                              "123": ["Narsingi Bus Stop","Narayanamma Engineering College","Shaikpet Nala","Tolichowki",
                                     "Galaxy Bus Stop","Salarjung Colony Bus Stop","Rethibowli Bus Stop","Mehdipatnam Bus Station"],
                              "119": ["Golconda Fort","Quli Qutub Shah Tombs","Salarjung Colony Bus Stop","Rethibowli Bus Stop",
                                      "Mehdipatnam Bus Station","Sarojini Devi Eye Hospital","Lakdikapul","Assembly","Nampally",
                                     "Nampally Station Road"],
                              "245": ["Secunderabad Junction","Alugadda Bhavi","Mettuguda Bus Stop","Railway Degree College",
                                     "Tarnaka Bus Stop","Habsiguda Bus Stop","Ngri","Uppal X Road Bus Stop","Uppal Bus Stop",
                                     "Ferzajiguda","Boduppal Kaman","Uppal Depot","Narapally","Ghatkesar Bus Stop","Aushapur",
                                     "Nemuragomla","Dayara"],
                              "113K": ["Chengicherla Bus Depot","RTC Colony","Chengicherla X Road","Kamala Nagar","	Uppal Bus Depot",
                                      "Boduppal","Pochamma Temple","Uppal Bus Stop","Uppal Gandhi Statue","Uppal Sub Station",
                                      "	Uppal X Road Bus Stop","Ramanthapur","Tilak Nagar Bus Stop","Fever Hospital Bus Stop",
                                      "Baghlingampally","Chikkadpally","Barkatpura","Amberpet Bus Station","Uppal X Road Bus Stop",
                                      "Gandhi Statue","Uppal Bus Stop"],
                             "49M": ["Secunderabad Junction","Clock Tower","Patny","Paradise Bus Stop","Anand Theatre",
                                    "Police Lines-Begumpet Bus Stop","Begumpet Railway Station","Greenlands","Panjagutta Bus Stop",
                                    "Banjara Hills","Masab Tank Bus Stop","Sarojini Bus Stop","Mehdipatnam Bus Stop"],
                              "218D": [" Patancheru Bus Stop","Lingampally Bus Stop","Jntu bus stop","Kukatpally Bus Stop",
                                      "Esi Bus Stop","S R Nagar","Ameerpet Bus Station","Panjagutta Bus Stop","Somajiguda",
                                      "Khairatabad Bus Stop","Lakdikapool Bus Stop","Abids Bus Stop","Koti Bus Stop","Malakpet",
                                      "Chaderghat Bus Stop","Dilsukhnagar Bus Station"],
                             "3K": ["Kushaiguda","ECIL X Roads","SP Nagar","Unani Hospital","Nrm College","Moula Ali Railway Colony",
                                   "Lalapet Bus Stop","Tarnaka","Tarnaka Tsrtc Hospital","Arts College Bus Stop","Jamia Osmania ",
                                   "Nallakunta","Fever Hospital","Barkatpura","Kachiguda X Road","Badi Chowdi","Koti Bus Terminal",
                                   "Koti Maternity Hospital","Koti","Putili Bowli","Central Bus Station","Afzalgunj Bus Station"],
                             "222A": ["Patancheru","Bhel Pushpak","Beeramguda Bus Stop","Lingampally","Chandanagar","Gangaram ",
                                     "Huda Colony Bustop","Mythrinagar Bus Stop","Allwyn X Roads","Hafeezpet","Botanical Garden",
                                     "Kondapur X Road","Kondapur","Shilparamam Bus Stop","Hitech City","Madhapur Police Station ",
                                     "Jubilee Hills Check Post Bus Stop","Lv Prasad Bus Stop","TV 9","Taj Krishna","Masab Tank Bus Stop",
                                     "Lakdikapul","Lakdikapul Metro Station","Assembly","Nizam College","Abids","Koti Bus Terminal"],
                              "113M": ["Mehdipatnam Bus Station","Sarojini Devi Eye Hospital","Masab Tank","Lakdikapul Metro Station",
                                      "Saifabad","Telephone Bhavan","Secretariat","Liberty","Himayath Nagar Bus Stop","Narayanaguda",
                                      "Chikkadpally Bus Stop","Baghlingampally","Barkatpura","Ramanthapur Colony ",
                                      "Uppal X Roads","Uppal Metro Station","Uppal Gandhi Statue","Uppal Bus Station"],
                            "300": ["Uppal X Roads","Uppal Metro Station","Saraswathi Nagar","Nagole","Alkapuri","Kamineni Hospital ",
                                    "LB nagar","Sagar Ring Road Owaisi Way","T.K.R.Kaman ","Champapet X Roads","Owaisi Hospital",
                                   "Midhani Depot","Kanchanbagh Gate","Baba Nagar","Chandrayanagutta","Bandlaguda","Durganagar",
                                   "Aramghar X Roads","Shivarampally X Road","Upperpally X Road","Hyderguda X Road","Attapur X Road",
                                   "Rethibowli","Rethibowli Bus Stop","Mehdipatnam Bus Station"],
                        "16A/47LI": ["Continental Hospitals","Infotech","ICICI","Wipro Nanakramguda","Infosys","Gpra","Indra Nagar","Telecom Nagar",
                                    "Cyberabad Police Commisioner Office","Biodiversity Park","Skyview Rmz","Lumbini Avenue","Raidurg",
                                     "Cyber Towers / Shilparamam","Hitech City","Image Garden","Madhapur Petrol Pump",
                                     "Madhapur Police Station Bus Stop","Live Life Hospital","Rainbow Park","Usha Kiran Movies",
                                     "Jubilee Hills Check Post Bus Stop","Lv Prasad Bus Stop","Sri Nagar Colony Bus Stop","Ameerpet Elephant House",
                                    "Ameerpet","Lal Bungalow Ameerpet","Greenlands Bus Stop","Begumpet","Shamlal North","Begumpet",
                                    "Prakash Nagar","Yatri Nivas /Anand Theatre","Sd Road","Swapnalok Complex","Patny Center Chandana Bros",
                                    "Navketan Complex Clock Tower","Secunderabad YMCA","W Marredpally Cross","East Maredpally","Shenoy Nursing Home",
                                    "West Marredpally","Aoc Center A","Aoc Gouha Road","Aoc Chowk","Safilguda","Krupa Complex","Vinayak Nagar",
                                     "Neredmet Old Ps","Vajpayee Nagar","Vayupuri Bus Stop","Sainikpuri","Officer’S Colony","A.S. Rao Nagar","ECIL X Road"],
                         "102CJ": ["Janapriya Colony","Lenin Nagar Bus Stop","Balapur X Road","Midhani Township","Dhatu Nagar","Bdl",
                                   "Pisalabanda","Midhani Company","Drdo Township","Midhani Bus Depot","Owaisi Hospital","Santosh Nagar","Is Sadan","Madannapet",
                                  "Saidabad X Roads","APSEB Office Saidabad","Chanchalguda","Chanchalguda Jail","Malakpet GOVT. Hospital","Nalgonda X Roads",
                                   "Chaderghat","Koti Womens College","Shankar Mutt"],
                        "41K": ["Central Bus Station (CBS)","MGBS","Putili Bowli","Koti","Mozamjahi Market","GPO","Abids","Nampally","Assembly","Lakdikapul Metro Station",
                                "Lakdikapul","Chintal Basti","Khairatabad","Khairatabad Rta","Erramanzil","Nims","Ameerpet","Mythrivanam","SR Nagar",
                                "ESI Hospital Metro Station","Erragadda FCI","Erragadda","Sanath Nagar Police Station","Sanath Nagar","Fateh Nagar","Valmiki Nagar",
                                "Fateh Nagar X Road","Hal","IDPL Colony","District Bus Stop IDPL Colony","Giri Nagar","Asbestos Colony","Ranga Reddy Kamaan",
                                "Papi Reddy Nagar","Outpost Station","Jagadgirigutta"],
                        "104A": ["Almasguda","Almasguda P.G.College","Prashanthi Hills","Sita Homes Colony","Meerpet Swimming Pool","Meerpet X Road",
                                 "Lalitha Nagar X Road","Jillelguda","VV Nagar","Meerpet Cheruvu","Gayatri Nagar X Road","TKR Kaman / Shakti Nagar","Kranti Nagar",
                                 "Karmanghat X Road","Karmanghat","Green Park Colony","RTC Colony","Champapet","Santosh Nagar","Is Sadan","Saidabad",
                                 "Jaihind Hotel","APSEB Office Saidabad","Government Press","Chanchalguda","Malakpet Sohail Hotel","Nalgonda X Roads","Chaderghat",
                                 "Koti Womens College"],
                        "156H": ["NGO Colony","Ganesha Temple","Chinthalkunta","LB Nagar Ring Road","LBNagar Metro Station","Doctors Colony",
                                 "Dwaraka Nagar Ashtalakshmi Temple","Chaitanyapuri","Dilsukhnagar","TVTower","Moosaram Bagh","Amberpet Ali Cafe",
                                 "Amberpet Police Lines","Tilak Nagar","Fever Hospital","Barkatpura","Baghlingampally","Chikkadpally","Narayanaguda",
                                 "Urdu Hall","Liberty","Lakdikapul Metro Station","Masab Tank","Potti Sriramulu Nagar","Masab Tank","NMDC","Sarojini Devi Eye Hospital",
                                 "Mehdipatnam"],
                        "9K/283K": ["Koti Bus Terminal","Koti","Mozamjahi Market","Abids","Nampally Station Road","Nampally","Nampally Grand Plaza",
                                    "Assembly","Lakdikapul Metro Station","Lakdikapul","Chintal Basti","Chintal Basthi Bus Stop","Khairtabad","Eenadu",
                                    "Khairatabad Rta","Erramanzil","Nims","Panjagutta Colony","Punjagutta","Ameerpet","Mythrivanam","SR Nagar","ESIHospital",
                                    "ESIHospital Metro Station","Erragadda","Prem Nagar","Bharat Nagar","Moosapet","Kukatpally Bus Depot","Sai Nagar","IDPL",
                                    "Niper","Balanagar X Roads","Balanagar","Hal","Water Tank","IDPL Chowrasta","Ganesh Nagar","Chintal","Chintal Chowrasta",
                                    "Hmt Factory","Gajula Ramam X Road","Shapur Nagar","Jeedimetla","Jeedimetla Bus Depot","Saibaba Nagar","Suraram Colony"],
                        "100A": ["Nampally","Gandhi Bhavan","Mozamjahi Market Gandhi Bhavan","Abids","Bank Street Koti","Koti","Shankar Mutt",
                                 "Koti Womens College","Chaderghat","Nalgonda X Roads","Yashoda Hospital","Malakpet Chermas","Malakpet Super Bazar",
                                 "Saleem Nagar","TV Tower","Moosaram Bagh","Dilsukhnagar","Chaitanyapuri","Fruit Market","Shalini Theatre","Kothapet",
                                 "Kothapet X Road Petrol Pump","Babu Jagjeevan Ram Bhavan Telephone Colony Arch","Telephone Colony","Rk Puram",
                                 "Baba Temple Alkapuri","Alkapuri"],
                        "171": ["Secunderabad","Secunderabad YMCA","Parade Ground Metro Station","Paradise","Tadbund","Bowenpally X Road","Ferozeguda",
                                "Raju Colony","Balanagar","Hal","Chintal","Chintal Chowrasta","Hmt Factory","Raamaaram X Road","Hal Colony","Gajularamaram"],
                        "9X/283D": ["Suraram Colony","Suraram X-Road","Saibad X Road","Jeedimetla Bus Depot","Jeedimetla Substation","Shapur Nagar",
                                    "Hmt Factory","Chintal Chowrasta","Ganesh Nagar","IDPL Colony","Hal","Balanagar X Roads","Niper","IDPL","Prashanth Nagar",
                                    "Kukatpally Bus Depot","Moosapet","Bharath Nagar","Prem Nagar","Erragadda","ESI Hospital Metro Station","Mythrivanam",
                                    "Ameerpet","Panjagutta Colony","Nims","Erramanzil","Khairatabad Rta","Khairatabad","Chintal Basti","Telephone Bhavan",
                                    "Assembly","Nampally Grand Plaza","Nampally","Mozamjahi Market Gandhi Bhavan","Afzalgunj Central Library",
                                    "Gowliguda Bus Depot","Central Bus Station","CBS"],
                        "220V": ["Mehdipatnam Corner","Mehdipatnam","Rethibowli","Salarjung Colony","Flour Mill","Langer Houz","Bapunagar","Bapu Ghat",
                                 "Chavella Road","Ramdevguda","Ibrahim Bagh","Hanuman Temple","Manchrevula X Road","Indra Nagar","Nanak Ram Guda","Iit",
                                 "Gachibowli Stadium","Hyderabad Central University Gate 2","Masjid Banda","Hcu","Hcu Depot","Bhagyanagar Colony",
                                 "Alind Doyens Colony","Gulmohar Park","Lingampally","Serlingampalli","Tara Nagar","Lingampally Bus Station"],
                        "251N": ["Narkhoda","Indra Nagar","Rallagudem","Shamshabad","Shamshabad Market","Satamrai","Gagan Pahad","AG College",
                                 "Aramghar","Aramghar X Roads","Sardar Vallabhbhai Patel National Police Academy","Raghavendra Colony",
                                 "Hasan Nagar","Danama Jhopdi","Mir Alam Tank Filter Beds","Thadban","Nehru Zoological Park","Bahadurpura",
                                 "Bahadurpura Police Station","Puranapool Mastan Gati","Puranapool","Puranapool Out Post","Petla Burj",
                                 "City College","High Court","Afzalgunj"],
                        "65": ["Tolichowki","Salarjung Colony","Nanal Nagar","Rethibowli","Mehdipatnam Bus Station","Sarojini Devi Eye Hospital",
                               "NMDC","Masab Tank","Ac Guards","Lakdikapul","Assembly","Basheerbagh","Nizam College","Abids","Abids Big Bazar",
                               "Bank Street Koti","Koti Bus Terminal","Koti","Putili Bowli","MGBS","Gowliguda Bus Depot"],
                        "11": ["VBIT Ascendas IT Park","Ascendas","Raheja Mindspace C Gate","Raidurg","Cyber Towers","Shilparamam",
                               "Hitech City","Image Garden","Madhapur Petrol Pump","Madhapur Police Station","Live Life Hospital",
                               "Rainbow Park","Peddamma Temple","Usha Kiran Movies","Jubli Check Post Chiranjeevi Eye Bank","Venkatagiri",
                               "Srinagar X Road","Indira Nagar X Road","Yousufguda Checkpost","Yousufguda Basti","State Home","Sarathi Studio",
                               "Mythrivanam","SR Nagar","ESI Hospital","ESI Hospital Metro Station"],
                        "3": ["Afzalgunj Central Library","Central Bus Station CBS","Chaderghat","Kachiguda Station Road",
                              "Kachiguda","Kachiguda Bus Station","Tourist Hotel","Fever Hospital","Nallakunta","Shankarmutt",
                              "Vidyanagar","Vidhya Nagar","Adikmet","Ramnagar Gundu","Ladies Hostel","Manikeshwari Nagar",
                              "Tarnaka Hospital Stop","Tarnaka","White House","Lalapet","HMT Bearings","ZTS X Road","Carbide",
                              "Hb Colony 1st Phase","Nrm College","Laxmi Nagar","Unani Hospital","SP Nagar","Kushaiguda Depot",
                              "ECIL X Roads","Kushaiguda"],
                        "2": ["Secunderabad Railway Station","Secunderabad Tsrtc Rathifile Bus Station","Secunderabad",
                              "Chilkalguda Circle","Chilakalaguda","Chilkalguda","Bhoiguda","Gandhi Hospital","Musheerabad X Road",
                              "Musheerabad Police Station","Raja Delux","Golconda X Road","RTC X Road","R.T.C.Bhavan","VST",
                              "Shankar Mutt","Nallakunta","Fever Hospital","Barkatpura","Kachiguda","Nimboliadda","Chaderghat",
                              "Chaderghat","Central Bus Station","CBS","Gowliguda Bus Depot","Afzalgunj Bus Station"],
                        "9M": ["Central Bus Station","CBS","Upcoming Arrivals","Central Bus Station","Gowliguda Bus Depot",
                               "Afzalgunj Bus Station","Afzalgunj","Osmangunj","Mozamjahi Market Gandhi Bhavan","Gandhi Bhavan","Nampally",
                               "Nampally Grand Plaza","Assembly","Lakdikapul Metro Station","Lakdikapul","Chintal Basti",
                               "Chintal Basthi Bus Stop","Khairtabad","Eenadu","Khairatabad Rta","Erramanzil","Nims","Panjagutta Colony",
                               "Ameerpet","Ameerpet Metro Station","Mythrivanam","SR Nagar","SR Nagar","ESI Hospital","ESI Hospital Metro Station",
                               "Erragadda","Sanath Nagar Police Station","Sanath Nagar","Sanath Nagar Bus Depot"],
                        "10B": ["Secunderabad Railway Station","Secunderabad Bus Station","Swimming Pool North","Paradise South",
                                "Anand Theatre","Police Lines South","Begumpet Old Airport","Shoppers Stop South","Shyam Lal South",
                                "Begumpet","Begumpet Railway Station","Greenlands","Nagarjuna Hills","Panjagutta Colony","Ameerpet",
                                "Mytrivanam","SR Nagar","ESI","Rythu Bazar Erragadda","Erragadda FCI","Erragadda Gokul Theater",
                                "Allwyn Erragadda","Erragadda","Prem Nagar","Bharat Nagar"],
                        "3B": ["Afzalgunj Central Library","Central Bus Station","CBS","Chaderghat","Koti Womens College",
                               "Koti Maternity Hospital","Sultan Bazar","Ram Koti","Kachiguda X Road","YMCA","Reddy College Narayanaguda",
                               "Barkatpura Circle","Fever Hospital","Nallakunta","Vidyanagar","Vidhya Nagar","Adikmet","Ramnagar Gundu",
                               "Jamia Osmania","Ladies Hostel","Manikeshwari Nagar","Tarnaka Hospital Stop","Tarnaka Uppal Stop",
                               "Habsiguda","National Geophysical Research Institute","NGRI","Kalyanpuri Colony Uppal"],
                    "47Y/90U": ["Uppal X Roads","Survey Of India","National Geophysical Research Institute","NGRI","Habsiguda",
                             "Tarnaka Aaradhana","Mettuguda","Alugadda Baavi South","Chilakalaguda","Secunderabad Tsrtc Rathifile Bus Station",
                             "Secunderabad Railway Station","Clock Tower","Swimming Pool North","Paradise Metro Station","Yatri Nivas",
                             "Anand Theatre","Begumpet","Prakash Nagar","Prakash Nagar","Begumpet","Begumpet","Greenlands",
                             "Lal Bungalow Ameerpet","Sheeshmahal","Satyam Theatre Cross Roads","Sarathi Studio","Yousufguda Basti",
                             "Yousufguda Checkpost","Srinagar X Road","Indira Nagar X Road","Venkatagiri","Road Number 37 Check Post",
                             "Journalist Colony Kbr Park","Filmnagar Entrance Sbi","Film Nagar Film Chambers","Film Nagar"],
                        "29H": ["Apurupa Colony","SR Naik Nagar Main","Jeedimetla Bus Depot","Jeedimetla Substation","Shapur Nagar Bus Stand",
                                "Shapur Nagar","Gajula Ramam X Road","Hmt Factory","Chintal Chowrasta","Chintal","Ganesh Nagar",
                                "District Bus Stop IDPL Colony","IDPL Colony","Water Tank","Hal","Balanagar","Raju Colony","Ferozeguda",
                                "New Bowenpally","Bowenpally X Road Junction","Chinna Thokatta Request","Ashish Gardens","Tar Bund Bus Stop",
                                "Pratap Colony","Paradise","Paradise Petrol Bunk Towards Stn Busstop","Swimming Pool North","Patni Junction",
                                "Navketan Complex Clock Tower","Secunderabad Bus Station Gurudwara"],
                        "15H": ["Secunderabad Towards Uppal","TSRTC Rathifile Bus Station","Chilkalguda","Alugadda Bhavi",
                                "Railway Hospital","Mettuguda","Lalaguda Junction","New Bridge","North Lalaguda","Masjid Lalaguda",
                                "Lalguda Railway Quarters","Santhi Nagar Lalaguda","Ram Theatre","Lalapet","RPF Training Centre",
                                "Industrial Estate","ZTS X Road","Carbide","HB Play Ground","Mangapuram","N.R.M. Degree College",
                                "Indira Nagar","Laxmi Nagar","Moulali Unani Dispensary","S.P. Nagar","Kushaiguda Depot","Kamla Nagar",
                                "ECIL X Road","ECIL X Road Bus Terminal","Kushaiguda","Nagarjuna Colony","Chakripuram","Nagaram Road",
                                "Chakripuram Road","Vijaya Hospital Road Nagaram","Nagaram","Sudha Hospital Dammaiguda X Road Nagaram",
                                "Rampally X Road","6th Phase KPHB","Icomm Tele Limited","Bandlaguda","Bhavani Nagar","RG Colony Panchayat Office",
                                "Rajiv Gruhakalpa Colony"],
                        "211P": ["Medchal","Medchal Bus Stop","Medchal Chekpost","Medchal Gubba","CMR College of Engineering and Technology",
                                 "Dongala Maya Sabha","Thumkunta","Medchal X Road Thummukunta","Sports School","Hakimpet","Nisa CISF","Kot Temple",
                                 "Water Tank","Risala Bazar","risala","sadhana mandhir","Bolarum","Bollaram","Lakadawala","Rythu Bazar","Alwal",
                                 "Ram Nagar – Alwal","Lothkuntap","EME","Lal Bazar","Tirumalgherry","Hanuman Temple Tirumalgherry","Karkhana Temple Arch",
                                 "Vikarampuri","HPS High School","Jubilee Bus Stop East 1","Patny","Patny North","Clock Tower",
                                 "Secunderabad Bus Station 2"],
                        "8R": ["Chinnamangabram","Mile Stone","Reddy Pally","Chanda Nagar X Road","Appo Jigudda","Chilkur","Balaji Temple X Road",
                               "Himyat Nagar Village","Chilkur Balaji Temple X Road","Aziz Nagar","Aziz Nagar 2","Aziz Nagar 1",
                               "Sri Nidhi International School","Chilkur Engineering College","Old Aziz Nagar X Road",
                               "Police Academy","AP Police Academy-2","Kalimandir","Peerancheru","Bandlaguda X Road","Suncity",
                               "Sairam Nagar","Chavella Road","Bapu Ghat","Langar House","Flour Mill","Salarjung Colony",
                               "Nala Nagar","Rethi Bowli","Mehdipatnam","Mehdipatnam Amba Theatre"],
                        "104G": ["Koti Womens College","Chaderghat","Nalgonda Cross Roads","Sohail Hotel","Chanchalguda","Chanchalguda Jail",
                             "Saidabad","Saidabad X Road","Saidabad","IS Sadan","Champapet Brilliant GL School","RTC Colony Champapet",
                             "Green Park Colony Bus Stop","Karmanghat X Road","Kranti Nagar","Gayatri Nagar X Road","VV Nagar","Jillelguda",
                             "Lalitha Nagar X Road","Meerpet X Road","Meerpet Swimming pool","Sita Homes Colony","Prashanthi Hills","Almasguda"],
                        "29R": ["Railapoor","Girmapur","Medchal Railway Station","Medchal","Medchal Chekpost","Medchal Gubba",
                                "CMR College of Engineering and Technology","Kandlakoya","Gundlapochampalli","Kompally",
                                "Dollapally X Road/Kompally Chorwsta","Cine Planet","NCL","NCL Balaji Hospital","Santa Sriram Estate",
                                "Jeedimetla Deewan Dhaba","Suchitra","Military Dairy Farm","Mmr Garden Bus Bay","Priyadarshini Hotel",
                                "New Bowenpally","Chinna thokatta Request Bus Stop","Ashish Gardens","Tar Bund","Pratap Colony","Paradise",
                                "Paradise BSNL Complex","Paradise","MG Road","James Street East","Ranigunj"],
                        "127J":["Jubilee Hills","Jubilee Check Post","Lv Prasad","Banjara Hills Road No.1 Water Tank","Taj Krishna","Care Hospital",
                               "Chintal Basti","Masab Tank","Ac Guards","Lakdikapul","Lakdikapul Metro Station","Assembly","Basheerbagh",
                                   "Nizam College","Abids","Mozamjahi Market","Koti"],
                       "71A":["Charminar","Pathar Gatti","High Court","Afzal Gunj","Chatrapathi Shivaji Pul","Gowliguda Depot",
                              "Central","Mahatma Gandhi","Chaderghat","Kachiguda Kamela","Golnaka 6 Number","Sree Ramana","Gandhi Statue",
                                "Irani Hotel","TV Studio Ramanthapur","TV Studio","Ramanthapur Colony","Ramanthapur Hyderabad Public School",
                                "Ramanthapur Church","Modern Foods","Uppal X Roads","Chilkanagar","Uppal Gandhi Statue","Uppal"],
                       "102A":["Mahaveer College","Bandlaguda","Kesavagiri","Chandrayanagutta","Drdl","Baba Nagar","Anurag Lab","Drdl",
                               "Midhani Depot","Owaisi Hospital","Santosh Nagar","Is Sadan","Saidabad HFEC Function Hall","Jaihind Hotel",
                               "APSEB Office Saidabad","Government Press","Chanchalguda","Sohail Hotel","Nalgonda X Roads","Chaderghat",
                                "Koti Women's College"],
                       "116N":["Nanak Ram Guda","Gpra","Khajaguda X Road","Hs Dargha","Narayanamma Engineering College","Shaikpet Nala",
                                "Tolichowki","Galaxy","Salarjung Colony","Nanal Nagar","Rethibowli","Mehdipatnam","Mehdipatnam Corner",
                                "Asif Nagar","Mallepally","Sitaram Bagh","Aghapura","Nampally","Abids","Mozamjahi Market","Putlibowli",
                                "Koti Bus Terminal"],
                       "218/18M":["Mehdipatnam","Sarojini Devi Eye Hospital","N.M.D.C.","Masab Tank","Care Hospital",
                                "Banjara Hills Road No 1 Water Tank","Panjagutta","Panjagutta Colony","Ameerpet","Mythrivanam",
                                "S.R.Nagar","E.S.I.Hospital Metro Station","Erragadda F.C.I.","Bharat Nagar","Moosapet",
                                "Kukatpally Bus Depot","Kukatpally Y Junction","Kukatpally","Sumithra Nagar","KPHB","Nizampet X Roads",
                                "Hydernagar","Miyapur Metro Station","Miyapur X Roads","Miyapur","Allwyn X Roads","Madinaguda","Huda Colony",
                                "Gangaram","Chandanagar","Lingampally","Jyothi Nagar","Sri Sai Nagar","Beeramguda","R.C. Puram","Icrisat",
                                "Patancheru","Isnapur X Road","Rudraram Gate","Gitam University"],
                       "300/216":["LB Nagar","Sagar Ring Road Owaisi Way","T K R Kaman","Shakti Nagar","Gayatri Nagar X Road","Manda Mallamma",
                                "Champapet X Roads","Owaisi Hospital","Midhani Depot","Drdl","Anurag Lab","Baba Nagar","Dlrl",
                                "Chandrayanagutta","Keshavagiri","Bandlaguda","Chandrayangutta Bandlaguda","Oddamgudem Stop 1",
                                "Mylardevpally","Durga Nagar Katedan","Durganagar","Aramghar X Roads","Shivarampally X Road",
                                "Weaker Section Colony","Shivarampally Quarters","Dairy Farm","Happy Homes Ring Road","Upperpally X Road",
                                "Shiva Nagar","Hyderguda X Road","Attapur X Road","Ring Road","Jyothi Nagar","Laxmi Nagar","Rethibowli",
                                "Nanal Nagar","Salarjung Colony","Toli Chowki","Galaxy","Brindavan Colony Road","Shaikpet Nala",
                                "Narayanamma Engineering College","Dargah Tombs Road","Lid Cap","Khajaguda X Road","Raidurgam",
                                "Nanal Nagar","Roda Mistry College","Gachi Bowli","Telecom Nagar","Gachibowli X Roads","Indra Nagar",
                                "Nanak Ram Guda","Iit","Gachibowli Stadium","Hyderabad Central University Gate 2","Masjid Banda","Hcu",
                                "Hcu Telephone Exchange","Hcu Depot","Bhagyanagar Colony","Doyens Colony","Alind Doyens Colony",
                                "Gulmohar Park","Lingampally Station","Serlingampalli","Tara Nagar","Lingampally"],
                       "156/216":["Lingampally","Tara Nagar","Serlingampalli","Gulmohar Colony","Alind Doyens Colony","Bhagyanagar Colony",
                                "Hcu Bus Depot","Hcu Telephone Exchange","Hyderabad Central University","Hyderabad Central University Gate 2",
                                "Gachibowli Stadium","Iiit","Gpra","Indra Nagar","Telecom Nagar","Roda Mistry College","Khajaguda X Road",
                                "Hs Dargha","Narayanamma Engineering College","Shaikpet Nala","Tolichowki","Galaxy","Salarjung Colony",
                                "Nanal Nagar","Rethibowli","Mehdipatnam","Sarojini Devi Eye Hospital","NMDC","Masab Tank","Ac Guards",
                                "Lakdikapul","Lakdikapul Metro","Assembly","Nampally Grand Plaza","Nampally","Mozamjahi Market","Abids",
                                "Bank Street Koti","Shankar Mutt","Chaderghat","Yashoda Hospital","Malakpet Super Bazar","T.V.Tower",
                                "Moosaram Bagh","Dilsukhnagar","Chaitanyapuri","Kothapet","Doctors Colony","LB Nagar Metro","LB Nagar",
                                "Chintalkunta","Vishnu Theatre","Sushma Theater","Autonagar","High Court Colony Deer Park","Bhagyalatha",
                                "Lecturers Colony","Thorrur X Road","Hayath Nagar Bus"],
                       "5k/92":["Secunderabad","Clock Tower","Patny Center","Bata","Bible House","Boats Club","Boats Club","Tank Bund",
                                "DBR Mills","Lakdikapul Metro","Ac Guards","Masab Tank","Masab Tank","Potti Sriramulu Nagar","NMDC",
                                "Sarojini Devi Eye Hospital","Mehdipatnam Corner","Rethibowli","Laxmi Nagar","Attapur X Road","Hyderguda X Road",
                                "Shiva Nagar","Upperpally X Road","Happy Homes Ring Road","Rajendra Nagar Bus Depot",
                                "Extension Education Institute"],
                       "18/219":["Uppal","Boduppal X Road","Peerjadiguda Kaman","Uppal","Uppal Gandhi Statue","Uppal Sub Station",
                                "Uppal X Roads","Survey Of India","National Geophysical Research Institute","Habsiguda","Tarnaka Aaradhana",
                                "Railway Degree College","Mettuguda","Alugadda Baavi South","Chilkalguda Circle","Secunderabad Tsrtc Rathifile",
                                "Secunderabad","Secunderabad YMCA","Swimming Pool North","Paradise","Airport Backside","Tadbund",
                                "Ashish Gardens","Chinna Thokata","Bowenpally X Road","Ferozeguda","Raju Colony","Balanagar X Roads",
                                "Citd","Niper","IDPL","Prashanth Nagar","Kukatpally Y Junction","Kukatpally","Sumithra Nagar","KPHB",
                                "JNTU","Nizampet X Roads","Hydernagar","Miyapur Metro","Miyapur","Allwyn X Roads","Madinaguda","Madinaguda",
                                "Deepthisree Nagar","Huda Colony","Gangaram","Chandanagar","Lingampally"],
                       "6H":["Tolichowki","Salarjung Colony","Nanal Nagar","Mehdipatnam","Sarojini Devi Eye Hospital","NMDC","Masab Tank",
                                "Ac Guards","Lakdikapul Metro","Lakdikapul Metro","Telephone Bhavan","Secretariat","Liberty","Himayath Nagar",
                                "Narayanaguda","Chikkadpally","Baghlingampally","Barkatpura","Shankar Mutt","Fever Hospital","Nallakunta",
                                "Vidyanagar","Adikmet","Ramnagar Gundu","Jamia Osmania","Osmania University","Manikeshwari Nagar",
                                "Tarnaka Uppal","Habsiguda","Hmt Nagar","Nacharam","Nacharam ESI Hospital","IDA Nacharam X Road",
                                "Janapriya","Mallapur","Noma Function Hall","HBP lay Ground","Nrm College","Unani Hospital","SP Nagar",
                                "Kushaiguda Depot","South Kamalanagar","ECIL X Roads"],
                       "45":["ESI Hospital Metro","ESI Hospital","SR Nagar","SR Nagar","Mythrivanam","Ameerpet Metro",
                                "Ameerpet Elephant House","Ameerpet","Sheeshmahal","Lal Bungalow Ameerpet","Greenlands",
                                "Begumpet Railway Station North","Begumpet Hps Gate1","Begumpet","Shamlal North","Begumpet",
                                "Prakash Nagar","Begumpet","Prakash Nagar","Begumpet Police Lines","Yatri Nivas","Anand Theatre",
                                "Paradise Metro","Paradise","MG Road","Ranigunj","Boats Club","Jeera","Kavadiguda Signal","Kalpana",
                                "Krishna Nagar","Musheerabad Police","Raja Delux","Golconda X Road","RTC X Road","RTC Bhavan","Vst"],
                       "21":["Venkatapuram Colony","Venkatapuram X Road","Vaishnavi Matha Temple","Bhatia Bakery","Lothkunta",
                             "Family Quarter","Eme","Lalbazar","Tirumalgherry","Tirumalagiri","Karkhana Temple Arch","Vikrampuri",
                             "Jubilee","Patny","Parade Ground Metro","Secunderabad YMCA","Secunderabad"],
                       "9":["Jeedimetla","Jeedimetla Substation","Hmt Factory","Chintal","Ganesh Nagar","Hal","Balanagar",
                                "Fateh Nagar X Road","Valmiki Nagar","Fateh Nagar","Sanath Nagar","Sanath Nagar Police Station",
                                "Erragadda","Erragadda FCI","ESI Hospital Metro","SR Nagar","Mythrivanam","Ameerpet","Nims","Erramanzil",
                                "Khairatabad","Chintal Basti","Lakdikapul Metro","Assembly","Nampally Station Road","Koti Bus Terminal",
                                "Putili Bowli","Central Bus Station","Gowliguda Bus Depot","Afzalgunj","Charminar"],
                       "5":["Chilakalaguda","Secunderabad","Chilkalguda Circle","Secunderabad Tsrtc Rathifile","Secunderabad Railway",
                                "Secunderabad","Clock Tower","Patny Center Chandana Bros","Swapnalok Complex","Paradise",
                                "Mahatma Gandhi Road 125","MG Road","Ranigunj","Boats Club","Boats Club","DBR Mills","Tank Bund",
                                "DBR Mills","Mini Tankbund","Secretariat","Accountant General Office","Birla Mandir","Lakdikapul Metro",
                                "Ac Guards","Masab Tank","Potti Sriramulu Nagar","NMDC","Sarojini Devi Eye Hospital","Mehdipatnam Corner",
                                "Mehdipatnam"],
                         "219/272G": ["Gandimaisamma","Bahadurpally X Roads","Suraram X Road","Saibad X Road","Jeedimetla Bus Depot",
                             "Jeedimetla Substation Bus Stop","Shapur Nagar","HMT Factory","Chintal Chowrasta","Ganesh Nagar",
                             "District Bus Stop IDPL Colony","IDPL Colony","HAL","Balanagar X Roads","Prashanth Nagar","Kukatpally",
                             "KPHB Colony","JNTU","Nizampet X Roads","Vasanth Nagar","Hydernagar","Miyapur Metro Station","Miyapur Bus Stop",
                             "Allwyn X Roads","Madinaguda","Huda Colony","Gangaram Bus Stop","Chandanagar","Lingampally Bus Station",
                             "Jyothi Nagar","Ashok Nagar","Sri Sai Nagar","Beeramguda","Bhel Pushpak","RC Puram","Railway Station Gate",
                             "ICRISAT","Patancheru","Patancheru Market","Patancheru Bus Station"],
                "219": ["Patancheru Bus Station","Patancheru Market","Patancheru","ICRISAT","Railway Station Gate","RC Puram",
                        "Bhel Pushpak","Beeramguda","Sri Sai Nagar","Ashok Nagar","Jyothi Nagar","Lingampally","Chandanagar",
                        "Gangaram Bus Stop","Huda Colony Bus Stop","Madinaguda","Mythri Nagar","Allwyn X Roads","Miyapur",
                        "Miyapur X Roads","Miyapur Metro Station","Hyder Nagar","Nizampet X Roads","JNTU","KPHB Colony","Kukatpally",
                        "Y-Junction","Prashanth Nagar","Balanagar X Roads","Shobana","Ferozguda","New Bowenpally","Tadbund","Paradise",
                        "Patny","Clock Tower","Secunderabad Junction"],
                "229": ["Secunderabad Bus Station","Clock Tower","Patny","Paradise","Tadbund","Chinna Thokata","Bowenpally Police Station",
                        "Bowenpally Check Post","MMR Gardens","Military Dairy Farm","Suchitra Circle","Jeedimetla Village",
                        "Angadipeta","NCL Balaji hospital","Ganga Enclave","NCL North Avenue","Cine Planet Kompally","Prajay",
                        "Dollapally X Road","Kompally","Vaishnavi Constructions","Farm Area Bus Stop","Kompally Bridge",
                        "Gundlapochampally","Prestige","Kandlakoya Bus Stop","CMR college","Medchal Gubba","Medchal Checkpost",
                        "Medchal Ambedkar Chowrasta","Medchal"],
                "277D": ["Ibrahimpatnam Bus Station","Ibrahimpatnam Chowrasta","Upparguda X Road","Sheriguda Bus Stop",
                         "Sri Indu Engineering College","Mangalpally X Road","Koheda X Road","Bongulur X Roads Bus Stop",
                         "Manneguda X Road","Ragannaguda","Brahmanpally","Tuerkyamjal X Road","Injapur Cheruvu Katta","Injapur",
                         "Swami Narayana Colony","Sagar Complex Bus Stop","BN Reddy Nagar","Hasthinapuram South",
                         "Hasthinapur North(RTO Office)","Omkar Nagar Bus Stop","Sagar Ring Road","Sagar X Road","LB Nagar",
                         "LB Nagar Metro Station","Doctors Colony Bus Stop","Kothapet","Chaitanyapuri","Dilsukhnagar","TV Tower",
                         "Moosaram Bagh","Malakpet Super Bazar","Yashoda Hospital","Nalgonda X Road","Chaderghat Bus Stop",
                         "Chaderghat","Azampura","Imlibun","Darulshifa","Gowliguda Bus Stop","CBS(Central Bus Stop)"],
                "277H": ["Ibrahimpatnam Bus Station","Ibrahimpatnam Bus Station","Ibrahimpatnam Chowrasta","Upparguda X Road","Sheriguda",
                         "Sri Indu College","Mangalpally X Road","Koheda X Road","Bonguluru X Road","Manneguda X Road","Ragannaguda",
                         "Brahmanpally","Turkayamjal X Road","Telangana Chowrasta - Turka Yamjal X Road","Injapur Cheruvu Katta","Injapur",
                         "Injapur Hanuman Temple Stop","Gurram Guda X Road","Swami Narayana Colony","Sagar Complex Bus Stop",
                         "BN Reddy Nagar","Teachers Colony","Hastinapur South (Naveena College)","Hastinapur Central",
                         "Hastinapuram North Bus Stop","Hastinapur North (Rto Office)","Omkar Nagar","LB Nagar","Sagar X Road","LB Nagar",
                         "Chintal Kunta Checkpost","Chintalkunta Bus Stop","Vishnu Theatre","Panama Godown","Sushma Theater","Autonagar",
                         "High Court Colony Deer Park","Bhagyalatha","Lecturers Colony","Hayathnagar Depot"],
                 "277M": ["MM Kunta","Water Tank Manneguda X Road","Manneguda X Road","Ragannaguda","Brahmanpally","Turkayamjal X Road",
                          "Telangana Chowrasta - Turka Yamjal X Road","Injapur Cheruvu Katta","Injapur","Injapur Hanuman Temple Stop",
                          "Gurram Guda X Road","Swami Narayana Colony","Sagar Complex Bus Stop","BN Reddy Nagar","Teachers Colony",
                          "Hastinapur Central","Hastinapuram North Bus Stop","Panama Godown Bus Stop","Omkar Nagar","LB Nagar",
                          "Sagar X Road","Bairamalguda","Aware Global Hospital","Karmanghat","Green Park Colony Bus Stop",
                          "Champapet RTC Colony / Ibp","Champapet (Brilliant Gl School)","Santosh Nagar","Is Sadan",
                          "Saidabad H.F.E.C. Function Hall","Jaihind Hotel","APSEB Office Saidabad","Government Press","Chanchalguda",
                          "Sohail Hotel Bus Stop","Nalgonda X Roads","Chaderghat Bus Stop","Chaderghat","Koti Womens College"],
                "277Y": ["Is Sadan","Saidabad HFEC Function Hall","Chanchalguda","Nalgonda X Roads","Chaderghat Bus Stop","Chaderghat",
                         "Putili Bowli","Koti","Shankar Mutt"],
                "277P": ["Yashoda Hospital","Malakpet Sohail Hotel","Dabeerpura","Saidabad","Is Sadan",
                         "Santosh Nagar","Champapet","RTC Colony (Champapet)","Green Park Colony","Karmanghat Bus Stop",
                         "Aware Global Hospital","Bairamalguda","Sagar X Road","Sagar Ring Road","Omkar Nagar Bus Stop",
                         "Hastinapur North (Rto Office)","Hasthinapuram South","BN Reddy Nagar","Sagar Complex Bus Stop",
                         "Swami Narayana Colony","Injapur","Injapur Cheruvu Katta","Turkyamjal X Road","Ragannaguda",
                         "Bongulur X Roads Bus Stop","Koheda X Road","Sri Indu Engineering College","Sheriguda Bus Stop",
                         "Ibrahimpatnam Chowrasta","Ibrahimpatnam","Polkampally","Manyaguda","Kothagudem","Annamacharya Engineering College",
                         "Bata Singaram","Mount Opera","Abdullapur","Kavadi Pally","Tarmaz Pet Chowrasta","Crusher Machines","Sattupally",
                         "Bacharam","Korremula 2","Maktha","Yellamma Temple","Venkatadri Township","Ou Colony Bus Stop","Vijaypuri Colony",
                         "Pocharam Village Main Road"],
                "277": ["Central Bus Station (CBS)","Chaderghat","Chaderghat","Chaderghat Bus Stop",
                        "Malakpet Sohail Hotel","Chanchalguda","Government Press","APSEB Office Saidabad","Saidabad","Jaihind Hotel",
                        "Saidabad","Is Sadan","Santosh Nagar","Champapet Road","Champapet","RTC Colony (Champapet)","RTC Colony",
                        "Green Park Colony","Karmanghat Bus Stop","Karmanghat","Aware Global Hospital","Bairamalguda","Sagar X Road",
                        "Sagar Ring Road","Omkar Nagar Bus Stop","Hastinapur North (Rto Office)","Hastinapur X Road",
                        "Hastinapuram Bus Stop","Hastinapur Central","Hasthinapuram South","Teachers Colony","BN Reddy Nagar",
                        "Sagar Complex Bus Stop","Swami Narayana Colony","Gurram Guda X Road","Injapur","Injapur Cheruvu Katta",
                        "Telangana Chowrasta - Turka Yamjal X Road","Turkyamjal X Road","Brahmanpally","Ragannaguda","Manneguda X Road",
                        "Bongulur X Roads Bus Stop","Koheda X Road","Mangalpally X Road","Sri Indu Engineering College",
                        "Sheriguda Bus Stop","Upparguda X Road","Ibrahimpatnam Chowrasta","Ibrahimpatnam Bus Station"],
                "277N": ["Koti Womens College","Chaderghat","Chaderghat Bus Stop","Nalgonda X Roads","Yashoda Hospital",
                         "Malakpet Chermas","Malakpet Super Bazar","Saleem Nagar","TV Tower","Moosaram Bagh","Dilsukhnagar","Dilsukhnagar",
                         "Dilsukhnagar Bus Station","Chaitanyapuri","Kothapet","Doctors Colony Bus Stop","LB Nagar Metro Station","LB Nagar",
                         "Sagar X Road","Sagar Ring Road","Omkar Nagar Bus Stop","Hastinapur North (Rto Office)","Hasthinapuram South",
                         "BN Reddy Nagar","Sagar Complex Bus Stop","Swami Narayana Colony","Gurram Guda X Road","Rajyalakshmi Nagar",
                         "Gurram Guda Village","Aditya Colony Road","Gold Phase Colony","Jay Suryapatnam","Kamma Guda",
                         "Mvsr Engineering College","Nadargul"],
                "277MP": ["Ibrahimpatnam Bus Station","Ibrahimpatnam Bus Station","Ibrahimpatnam Chowrasta",
                          "Upparguda X Road","Sheriguda","Sri Indu College","Mangalpally X Road","Koheda X Road","Bonguluru X Road",
                          "Manneguda X Road","Ragannaguda","Brahmanpally","Turkayamjal X Road","Telangana Chowrasta - Turka Yamjal X Road",
                          "Injapur Cheruvu Katta","Injapur","Injapur Hanuman Temple Stop","Gurram Guda X Road","Swami Narayana Colony",
                          "Sagar Complex Bus Stop","BN Reddy Nagar","Teachers Colony","Hastinapur Central","Hastinapuram North Bus Stop",
                          "Panama Godown Bus Stop","Omkar Nagar","LB Nagar","Sagar X Road","Bairamalguda","Aware Global Hospital","Karmanghat",
                          "Green Park Colony Bus Stop","Champapet RTC Colony / Ibp","Champapet (Brilliant Gl School)","Santosh Nagar",
                          "Is Sadan","Saidabad FEC Function Hall","Jaihind Hotel","APSEB Office Saidabad","Government Press","Chanchalguda",
                          "Sohail Hotel Bus Stop","Nalgonda X Roads","Chaderghat Bus Stop","Chaderghat","Azampura","Imlibun","MGBS",
                          "Mgbs City Alighting","Central Bus Station (CBS)","Gowliguda Bus Depot","Afzalgunj","Osmangunj",
                          "Mozamjahi Market (Gandhi Bhavan)","Gandhi Bhavan","Nampally","Nampally Grand Plaza","Assembly",
                          "Lakdikapul Metro Station","AC Guards","Masab Tank","Potti Sriramulu Nagar","NMDC","Sarojini Devi Eye Hospital",
                          "Mehdipatnam Corner","Mehdipatnam Bus Station"],
                "280N": ["Secunderabad","Chilkalguda Circle","Alugadda Baavi South Bus Stop","Mettuguda",
                         "Tarnaka Uppal Stop","Habsiguda","National Geophysical Research Institute (NGRI)","Survey Of India",
                         "Uppal Sub Station","Uppal Bus Station","Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot","Medipally",
                         "Central Power Research Institute","Narapally","Vijaypuri Colony","Jodimetla X Road","Annojiguda",
                         "Shiva Reddy Guda Bus Stop","Edulabad X Road","Ghatkesar Bypass Junction","Ghstkesar Police Station Bus Stop",
                         "Nfc Nagar Arch","Community Hall Stop Nfc Nagar","Kv School Nfc Nagar","Nfc Nagar"],
                "280S": ["Jubilee Bus Station","Patny","Sangeeth","Secunderabad Tsrtc Rathifile Bus Station","Secunderabad",
                         "Chilkalguda Circle","Alugadda Baavi South Bus Stop","Mettuguda","Tarnaka Uppal Stop","Habsiguda",
                         "National Geophysical Research Institute (NGRI)","Survey Of India","Uppal Sub Station","Uppal Bus Station",
                         "Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot","Medipally","Central Power Research Institute","Narapally",
                         "Vijaypuri Colony","Jodimetla X Road","Annojiguda","Shiva Reddy Guda Bus Stop","Edulabad X Road",
                         "Ghatkesar Bypass Junction","Ghstkesar Police Station Bus Stop","Nfc Nagar Arch","Marripally Guda","Edulabad"],
                "280": ["Secunderabad","Chilkalguda Circle","Upcoming Arrivals","Alugadda Baavi South Bus Stop","Mettuguda",
                        "Tarnaka Uppal Stop","Habsiguda","National Geophysical Research Institute (NGRI)","Survey Of India",
                        "Uppal Sub Station","Uppal Bus Station","Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot","Medipally",
                        "Central Power Research Institute","Narapally","Vijaypuri Colony","Jodimetla X Road","Annojiguda",
                        "Shiva Reddy Guda Bus Stop","Ghatkesar Bus Stop"],
                 "280B": ["Bogaram","Kondapur Village 280b","Ghatkesar Bus Stop","Shiva Reddy Guda Bus Stop",
                          "Annojiguda","Vaibhav Colony","Jodimetla X Road","Vijaypuri Colony","Narapally","Central Power Research Institute",
                          "Chengicherla X Road","Medipally","Canaranagar Bus Stop","Uppal Bus Depot","Boduppal X Road","Peerjadiguda Kaman",
                          "Uppal Bus Station","Uppal Gandhi Statue","Uppal Sub Station","Uppal X Roads","Survey Of India",
                          "National Geophysical Research Institute (Ngri)","Habsiguda Bus Stop","Tarnaka Aaradhana Bus Stop",
                          "Railway Degree College","Mettuguda","Alugadda Baavi South","Chilakalaguda"],
                  "290U/463": ["Jubilee Bus Station","Jubilee Bus Station","Secunderabad YMCA",
                               "Secunderabad Bus Station (Gurudwara)","Secunderabad Railway Station","Secunderabad Tsrtc Rathifile Bus Station",
                               "Secunderabad Tsrtc Rathifile Bus Station","Secunderabad","Chilkalguda Circle","Alugadda Baavi South Bus Stop",
                               "Mettuguda Metro Station","Mettuguda","Nin/Water Tank","Tarnaka Metro Station","Tarnaka Uppal Stop",
                               "Tarnaka Pushpak Bus Stop","Habsiguda","National Geophysical Research Institute (NGRI)","Survey Of India",
                               "Uppal X Roads","Uppal X Road Bus Stop","Uppal X Roads","Uppal Metro Station","Saraswathi Nagar",
                               "Mamatha Nagar Colony","Nagole","Alkapuri","Rajeev Gandhi Nagar","Kamineni","Kamineni Hospital Bus Stop",
                               "Central Bank Colony","LB Nagar","Chintal Kunta Checkpost","Chintalkunta Bus Stop","Vishnu Theatre",
                               "Panama Godown","Sushma Theater","Autonagar","High Court Colony Deer Park","Bhagyalatha","Bhagyalatha",
                               "Lecturers Colony","Hayathnagar Depot","Thorrur X Road","Hayath Nagar Bus Station","Word And Deed School Bus Stop",
                               "Laxmireddy Palem","Pedda Amberpet","Pedda Amberpet X Road","Shanti Nagar","ORR Peddamberpet","ORR Gandicheruvu",
                               "Kanakadurga Nagar","SGM College","Ramoji Film City","Abdullapurmet","Jafferguda X Road","Singareni Colony",
                               "Mount Opera","Bata Singaram","Sai Nagar Township","Deshmukhi Saint M College","Deshmukhi"],
                   "290S": ["Secunderabad","Chilkalguda Circle","Alugadda Baavi South Bus Stop","Mettuguda","Tarnaka Uppal Stop",
                            "Habsiguda","National Geophysical Research Institute (NGRI)","Survey Of India","Uppal X Roads","Nagole","Alkapuri",
                            "Kamineni Hospital Bus Stop","LB Nagar","Chintal Kunta Checkpost","Chintalkunta Bus Stop","Panama Godown",
                            "Ganesha Temple","Sampurna","Rythu Bazar","Kamla Nagar","Subhadra Nagar (Vanasthalipuram)","Shanti Nagar (Vanasthalipuram)",
                            "Lecturers Colony","Hayathnagar Depot","Hayath Nagar Bus Station","Word And Deed School Bus Stop","Laxmireddy Palem",
                            "Pedda Amberpet","Sadasiva Heavens","Gandi Cheruvu X Road","Narayana Ias Academy","Upperguda","Koheda Gate X Roads",
                            "Umer Khan Guda Stop","Sanghi Nagar"],
                  "290A": ["Anajpur","Gayathri Nagar","Majeedpur X Road","Surmaiguda","Lashkarguda","Kanakadurga Nagar","Abdullapurmet",
                           "Ramoji Film City","SGM College","Kanakadurga Nagar","ORR Peddamberpet","Shanti Nagar","Pedda Amberpet X Road",
                           "Pedda Amberpet","Laxma Reddy Palem","Word & Deed Colony","Hayath Nagar Bus Station","Hayathnagar Depot",
                           "Lecturers Colony","Bhagyalatha","High Court Colony","Autonagar","Sushma Theatre Bus Stop","Panama Godown Bus Stop",
                           "Vishnu Theatre","Chinthalkunta Bus Stop","Chintalkunta Checkpost","LB Nagar Ring Road","LB Nagar",
                           "Central Bank Colony","Kamineni Hospital Bus Stop","Kamineni Bus Stop","Rajeev Gandhi Nagar","Alkapuri","Nagole",
                           "Mamatha Nagar Colony","Inner Ring Road","Uppal Metro Station","Uppal X Roads","Survey Of India",
                           "National Geophysical Research Institue (NGRI)","Habsiguda Bus Stop","Tarnaka Aaradhana Bus Stop",
                           "Tarnaka Metro Station","Railway Degree College","Mettuguda","Mettuguda Metro Station","Alugadda Baavi South",
                           "Chilakalaguda","Secunderabad","Chilkalguda Circle Bus Stop","Secunderabad Tsrtc Rathifile Bus Station",
                           "Secunderabad Railway Station","Secunderabad Bus Station (Gurudwara)","Secunderabad YMCA","Jubilee Bus Station"],
                  "222A": ["Patancheru","Depot Arch","Icrisat","Bhel Pushpak","Beeramguda","Beeramguda Bus Stop","Jyothi Nagar","Lingampally",
                           "Chandanagar","Gangaram Bus Stop","Huda Colony Bustop","Madinaguda","Deepthisree Nagar","Mythrinagar Bus Stop",
                           "Allwyn X Roads","Hafeezpet","Botanical Garden","Kondapur X Road","Kondapur","Shilparamam Bus Stop","Hitech City",
                           "Image Garden Bus Stop","Madhapur Petrol Pump","Madhapur Police Station Bus Stop","Live Life Hospital",
                           "Usha Kiran Movies","Jubilee Hills Check Post Bus Stop","Lv Prasad Bus Stop","TV9","Nagarjuna Circle",
                           "Vengal Rao Park","Taj Krishna","Care Hospital","Chintal Basti Bus Stop","Masab Tank Bus Stop","Ac Guards",
                           "Lakdikapul","Lakdikapul Metro Station","Assembly","Nizam College","Abids","Abids (Big Bazar)","Bank Street Koti",
                           "Koti Bus Terminal"],
                  "195": ["Bachupally X Road","BK Enclave","Miyapur Metro Station","Hyder Nagar","Nizampet X Roads","JNTU","Rythu Bazar Kp",
                          "KPHB Colony Mig","Forum Mall / K.P.H.B.Circle","Malaysian Township","Ck Tanda","Hitech City","Cyber Towers",
                          "Shilparamam","Raidurg","Lumbini Avenue","Gachi Bowli","Telecom Nagar","Gachibowli X Roads","Indra Nagar",
                          "Nanak Ram Guda","Infosys","Wipro Nanakramguda","ICICI","Infotech","Continental Hospitals","Waverock"],
                  "288D": ["Chilkur Balaji Temple","Himyat Nagar Village","Aziz Nagar","Vif College","Rane Company","Old Aziz Nagar X Road",
                           "Pbel City","Kalimandir Bus Stop","Peerancheru","Bandlaguda X Road","Raghuram Nagar","Sun City","Bapu Ghat",
                           "Flour Mill","Nala Nagar","Mehdipatnam Bus Station"],
                  "127K": ["Kondapur Bus Depot","Kondapur X Road","Paulo Travels","Kothaguda Bus Stop","Kondapur","Hitex Kaman",
                           "Shilparamam Bus Stop","Hitech City","Image Garden Bus Stop","Madhapur Petrol Pump","Madhapur Police Station Bus Stop",
                           "Live Life Hospital","Rainbow Park","Peddamma Temple Bus Stop","Usha Kiran Movies","Jubilee Check Post",
                           "Road Number 37 Check Post","Journalist Colony Kbr Park","Apollo Hospital","Banjara Hills Bus Stop",
                           "Mla Colony Bus Stop","Acb Office","Durga Enclave","Banjara Hills Kaman","Familia Hospital","Bhola Nagar",
                           "Chintal Basti Bus Stop","Ambedkar Nagar (Chinthal Basthi)","Masab Tank Bus Stop","Ac Guards","Lakdikapul",
                           "Lakdikapul Metro Station","Assembly","Nizam College","Abids","Abids (Big Bazar)","Bank Street Koti","Koti",
                           "Koti Bus Terminal"],
                   "218": ["Patancheru","Depot Arch","Icrisat","Rc Puram","Bhel Pushpak","Beeramguda","Sri Sai Nagar","Jyothi Nagar","Lingampally",
                           "Chandanagar","Gangaram Bus Stop","Madinaguda","Deepthisree Nagar","Mythrinagar Bus Stop","Allwyn X Roads","Miyapur",
                           "Miyapur X Roads","Miyapur Metro Station","Hyder Nagar","Nizampet X Roads","JNTU","KPHB","Vivekananda Nagar Bus Stop",
                           "Kukatpally Bus Stop","Kukatpally Y Junction","Kukatpally Bus Depot","Moosapet","Bharath Nagar","Prem Nagar","Erragadda",
                           "Erragadda FCI","ESI Hospital Metro Station","SR Nagar","Mythrivanam","Ameerpet Bus Stop","Panjagutta Colony Bus Stop",
                           "Nims","Erramanzil","Khairatabad Rta","Khairatabad Bus Stop","Shaadan College","Lakdikapul","Assembly","Nizam College",
                           "Abids","Abids (Big Bazar)","Bank Street Koti","Koti Bus Terminal"],
                    "113K/L": ["Lingampally Bus Station","Chandanagar","Gangaram Bus Stop","Huda Colony Bustop","Madinaguda","Deepthisree Nagar",
                               "Mythrinagar Bus Stop","Allwyn X Roads","Miyapur","Miyapur Metro Station","Hyder Nagar","Vasanth Nagar","JNTU","KPHB",
                               "Vivekananda Nagar Bus Stop","Sumithra Nagar Bus Stop","Kukatpally Crossroads","Kukatpally Govt College",
                               "Kukatpally Y Junction","Kukatpally Bus Depot","Moosapet","Bharath Nagar","Prem Nagar","Erragadda","Erragadda FCI",
                               "ESI Hospital Metro Station","SR Nagar","Mythrivanam","Ameerpet Bus Stop","Panjagutta Colony Bus Stop","Nims",
                               "Erramanzil","Khairatabad Rta","Khairatabad Bus Stop","Chintal Basti","Lakdikapul Metro Station","Saifabad",
                               "Telephone Bhavan","Secretariat","Liberty","Himayath Nagar Bus Stop","Narayanaguda","Chikkadpally Bus Stop",
                               "Baghlingampally","Barkatpura","Fever Hospital","Tilak Nagar Bus Stop","6 Number","Sree Ramana Bus Stop",
                               "Irani Hotel Bus Stop","Ramanthapur Colony Bus Stop","Ramanthapur Church","Uppal X Roads","Uppal Metro Station",
                               "Uppal Gandhi Statue","Pochamma Temple","Peerjadiguda Kaman","Boduppal X Road","Uppal Bus Depot"]




              }

class ResultsScreen_for_bus_number(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen_for_bus_number, self).__init__(**kwargs)
        self.layout = FloatLayout()

        self.results_label = MDLabel(text='', halign='center')
        self.results_label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.layout.add_widget(self.results_label)

        self.add_widget(self.layout)

    def show_results(self, result):
        if result:
            self.results_label.text = "The Bus Number is: \n" + result

        else:
            self.results_label.text = "No bus route found between the given points."

    def update_results(self, bus_number):

        if bus_number in bus_routes:
            routes = bus_routes[bus_number]
            label1 = MDLabel(text="  The routes for Bus Number are:", pos_hint={"center_x": 0.5, "center_y": 0.9})
            label1.font_name = 'Poppins-Bold.ttf'
            label1.font_size = '22sp'
            sv = ScrollView(size_hint_y=0.85)
            g = GridLayout(cols=1, spacing="20dp", padding="20dp")
            g.size_hint_y = None
            g.bind(minimum_height=g.setter("height"))
            routes = bus_routes[bus_number]
            self.results_label = MDLabel(text="\n--> ".join(routes), size_hint_y=None, height=dp(1000))
            self.results_label.font_name = 'Poppins-SemiBold.ttf'
            self.results_label.font_size = "18sp"
            g.add_widget(self.results_label)
            sv.add_widget(g)
            self.add_widget(sv)
            self.add_widget(label1)
            back_button = MDIconButton(icon='arrow-left', pos_hint={'center_x': 0.06, 'center_y': 0.96})
            back_button.bind(on_release=self.switch_screen)
            self.add_widget(back_button)

        else:
            self.results_label.text = f"Bus Number {bus_number} does not exist."
            back_button = MDRectangleFlatButton(text='Go to Main Screen', pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                                text_color=(0, 0, 0, 1), line_color=(0, 0, 0, 1), line_width=2)
            back_button.bind(on_release=self.switch_screen)
            self.add_widget(back_button)()
            self.clear_screen()
    def clear_labels(self):
        self.results_label.text = ''

    def switch_screen(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main'


class SITI_EXPRESS(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AppScreen(name='icon'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(Screen_for_sp_ep(name='screen_for_sp_ep'))
        sm.add_widget(Screen_for_Busnumber(name='screen_for_bus_number'))
        sm.add_widget(TranslatorScreen(name='voice'))
        sm.add_widget(MapScreen(name='map'))
        sm.add_widget(ResultsScreen_for_bus_number(name='results_for_bus_number'))
        sm.add_widget(ResultsScreen_for_sp_ep(name='results_for_sp&ep'))
        sm.add_widget(FeedbackScreen(name='feedback'))

        return sm

if __name__ == '__main__':
    Window.size = (360, 640)
    SITI_EXPRESS().run()