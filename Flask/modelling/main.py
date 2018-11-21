from kivy.app import App
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.vector import Vector
from random import randint
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider


import random
import os

from model import run_en_csv
from threading import Thread

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SimulatorUI(BoxLayout):
    
    def run_simulation(self):
        print("Simulation Running!")
        output_path = 'output' if not self.output_path else self.output_path
        data_path = 'data' if not self.data_path else self.data_path
        battery_capacity = self.ids.battery_slider.value
        print("Output:", self.output_path, "Data", data_path, "Battery Capacity", battery_capacity)
        self.set_status("Simulation Running")
        t = Thread(target=run_en_csv, args=(output_path, data_path, {'battery_capacity':battery_capacity}, self.set_status))
        t.start()

    
    def set_status(self, message):
        self.ids.status.text = "Status: " + message

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_select_data_folder(self):
        content = LoadDialog(load=self.set_data_folder, cancel=self.dismiss_popup)
        self._popup = Popup(title="Select Data Folder", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
    
    def set_data_folder(self, path, filename):
        # selected = os.path.join(path, filename[0])
        selected = path
        print("Selected", selected)
        self.ids.data_folder.text="Data Folder: "+ selected
        self.data_path = selected
        self.dismiss_popup()

    def show_select_output_folder(self):
        content = LoadDialog(load=self.set_output_folder, cancel=self.dismiss_popup)
        self._popup = Popup(title="Select Output Folder", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
    
    def set_output_folder(self, path, filename):
        # selected = os.path.join(path, filename[0])
        selected = path
        print("Selected", selected)
        self.ids.output_folder.text="Output Folder: "+ selected
        self.output_path = selected
        self.dismiss_popup()


class SimulatorApp(App):
    def build(self):
        sim = SimulatorUI()

        # return Button(text='Hello World')
        return sim

SimulatorApp().run()