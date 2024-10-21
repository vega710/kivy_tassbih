from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window

class NameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Welcome to Tasbih App',
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )
        
        # Input fields
        self.first_name = TextInput(
            multiline=False,
            hint_text='Entrer Prénom',
            size_hint_y=None,
            height=40
        )
        self.last_name = TextInput(
            multiline=False,
            hint_text='Enter Nom',
            size_hint_y=None,
            height=40
        )
        
        # Start button
        start_button = Button(
            text='Commencer Al Istighfar',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        start_button.bind(on_press=self.validate_and_start)
        
        # Add widgets to layout
        layout.add_widget(title)
        layout.add_widget(self.first_name)
        layout.add_widget(self.last_name)
        layout.add_widget(start_button)
        
        self.add_widget(layout)
    
    def validate_and_start(self, instance):
        if self.first_name.text.strip() and self.last_name.text.strip():
            counter_screen = self.manager.get_screen('counter')
            counter_screen.set_name(
                f"{self.first_name.text} {self.last_name.text}"
            )
            self.manager.current = 'counter'
        else:
            # Show error message if fields are empty
            error_label = Label(
                text='Please fill in both names',
                color=(1, 0, 0, 1),
                size_hint_y=None,
                height=30
            )
            layout = self.children[0]
            if len(layout.children) > 4:  # Remove old error message if exists
                layout.remove_widget(layout.children[0])
            layout.add_widget(error_label, index=len(layout.children))

class CounterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Top section for welcome message with padding
        top_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=80,
            padding=[0, 10, 0, 10]  # Left, top, right, bottom padding
        )
        
        # Welcome message
        self.welcome_label = Label(
            text='Bismilah!',
            font_size='24sp',
            bold=True
        )
        top_section.add_widget(self.welcome_label)
        
        # Content layout for counter and buttons
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=[0, 20, 0, 0]  # Add top padding to create space after welcome message
        )
        
        # Counter display
        self.counter_label = Label(
            text='0',
            font_size='60sp',
            bold=True,
            size_hint_y=None,
            height=120
        )
        
        # Count button
        self.count_button = Button(
            text='Encore',
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.count_button.bind(on_press=self.increment_counter)
        
        # Reset button
        reset_button = Button(
            text='Recommencer',
            size_hint_y=None,
            height=60,
            background_color=(0.7, 0.2, 0.2, 1)
        )
        reset_button.bind(on_press=self.reset_counter_immediately)
        
        # Add widgets to content layout
        content_layout.add_widget(self.counter_label)
        content_layout.add_widget(self.count_button)
        content_layout.add_widget(reset_button)
        
        # Add sections to main layout
        main_layout.add_widget(top_section)
        main_layout.add_widget(content_layout)
        
        self.add_widget(main_layout)
    
    def set_name(self, name):
        self.welcome_label.text = f'Bienvenue, {name}!'
    
    def increment_counter(self, instance):
        self.counter += 1
        self.counter_label.text = str(self.counter)
        
        if self.counter >= 100:
            # Show congrats message
            self.count_button.disabled = True
            congrats_label = Label(
                text='Taqabal Allah!\nVous avez atteint 100!',
                color=(0, 1, 0, 1),
                font_size='24sp',
                size_hint_y=None,
                height=60
            )
            # Insert congrats message below welcome message
            layout = self.children[0]
            content_layout = layout.children[0]  # Get the content layout
            if len(content_layout.children) > 3:  # Check if congrats message exists
                content_layout.remove_widget(content_layout.children[-1])
            content_layout.add_widget(congrats_label, index=len(content_layout.children))
            
            # Reset counter after 3 seconds
            Clock.schedule_once(self.reset_counter, 3)
    
    def reset_counter(self, dt):
        self.counter = 0
        self.counter_label.text = '0'
        self.count_button.disabled = False
        layout = self.children[0]
        content_layout = layout.children[0]
        if len(content_layout.children) > 3:  # Remove congrats message
            content_layout.remove_widget(content_layout.children[-1])
    
    def reset_counter_immediately(self, instance):
        self.counter = 0
        self.counter_label.text = '0'
        self.count_button.disabled = False
        layout = self.children[0]
        content_layout = layout.children[0]
        if len(content_layout.children) > 3:  # Remove congrats message
            content_layout.remove_widget(content_layout.children[-1])

class TasbihApp(App):
    def build(self):
        # Set window size for desktop testing
        Window.size = (400, 600)
        
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(NameScreen(name='name'))
        sm.add_widget(CounterScreen(name='counter'))
        return sm

if __name__ == '__main__':
    TasbihApp().run()