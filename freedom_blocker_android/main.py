from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.utils import platform
import threading

# Mocking for Windows development
try:
    from android.permissions import request_permissions, Permission
    from permissions import check_usage_stats_permission, request_usage_stats_permission, check_overlay_permission, request_overlay_permission
    from jnius import autoclass
except ImportError:
    # Mock functions for Windows
    def check_usage_stats_permission(): return True
    def request_usage_stats_permission(): pass
    def check_overlay_permission(): return True
    def request_overlay_permission(): pass

from config import ConfigManager

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # Determine config path
        if platform == 'android':
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            files_dir = PythonActivity.mActivity.getFilesDir().getAbsolutePath()
            self.config = ConfigManager(files_dir + '/config.json')
        else:
            self.config = ConfigManager('config.json')

        # Header
        self.add_widget(Label(text="Freedom Blocker", font_size='24sp', size_hint_y=None, height=50))
        
        # Status Label
        self.status_label = Label(text="Service Stopped", color=(1, 0, 0, 1), size_hint_y=None, height=30)
        self.add_widget(self.status_label)
        
        # Permissions Buttons
        self.create_permission_buttons()
        
        # Block List Input
        input_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.app_input = TextInput(hint_text="Package Name (e.g. com.facebook.katana)", multiline=False)
        add_btn = Button(text="Block", size_hint_x=0.3)
        add_btn.bind(on_release=self.add_app)
        input_layout.add_widget(self.app_input)
        input_layout.add_widget(add_btn)
        self.add_widget(input_layout)
        
        # Block List View
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.list_layout)
        self.add_widget(scroll)
        
        # Service Control
        self.service_btn = Button(text="Start Service", size_hint_y=None, height=60, background_color=(0, 1, 0, 1))
        self.service_btn.bind(on_release=self.toggle_service)
        self.add_widget(self.service_btn)
        
        self.refresh_list()
        self.check_service_status()

    def create_permission_buttons(self):
        layout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        
        btn_usage = Button(text="Grant Usage Stats")
        btn_usage.bind(on_release=lambda x: request_usage_stats_permission())
        layout.add_widget(btn_usage)
        
        btn_overlay = Button(text="Grant Overlay")
        btn_overlay.bind(on_release=lambda x: request_overlay_permission())
        layout.add_widget(btn_overlay)
        
        self.add_widget(layout)

    def add_app(self, instance):
        app_name = self.app_input.text.strip()
        if app_name:
            self.config.add_blocked_app(app_name)
            self.app_input.text = ""
            self.refresh_list()

    def remove_app(self, app_name):
        self.config.remove_blocked_app(app_name)
        self.refresh_list()

    def refresh_list(self):
        self.list_layout.clear_widgets()
        for app in self.config.get_blocked_apps():
            row = BoxLayout(size_hint_y=None, height=40)
            row.add_widget(Label(text=app, halign='left'))
            del_btn = Button(text="X", size_hint_x=None, width=40, background_color=(1, 0, 0, 1))
            del_btn.bind(on_release=lambda x, a=app: self.remove_app(a))
            row.add_widget(del_btn)
            self.list_layout.add_widget(row)

    def toggle_service(self, instance):
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            activity = PythonActivity.mActivity
            service_name = 'org.freedom.freedomblocker.ServiceBlockingservice' # defined in built apk
            
            # Simple toggle logic based on label for now
            # In reality we should check if service is running
            if self.service_btn.text == "Start Service":
                service = autoclass(service_name)
                service.start(activity, "")
                self.service_btn.text = "Stop Service"
                self.service_btn.background_color = (1, 0, 0, 1)
                self.status_label.text = "Service Running"
                self.status_label.color = (0, 1, 0, 1)
            else:
                self.service_btn.text = "Start Service"
                self.service_btn.background_color = (0, 1, 0, 1)
                self.status_label.text = "Service Stopped"
                self.status_label.color = (1, 0, 0, 1)
                # Stopping service is harder in Kivy/p4a usually needs a command
        else:
            print("Would start service on Android")

    def check_service_status(self):
        # Todo: check if service is actually running
        pass

class FreedomApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    FreedomApp().run()
