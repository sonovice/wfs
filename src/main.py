# -*- coding: utf-8 -*-

__author__ = 'Simon Waloschek'

DEBUG = False

import os

import RPi.GPIO as GPIO
    
PIN_LAMP = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_LAMP, GPIO.OUT)  # Siap Lampe
GPIO.output(PIN_LAMP, True)


from kivy.app import App
from kivy import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from _thread import start_new_thread
from functools import partial
import logging
from relais import Relais
from iosono import Iosono
from siap import Siap

logging.getLogger().setLevel(logging.DEBUG)

relais_list = {'Schwalbennest': Relais(1),  # Schwalbennest
               'DeckeLinks':    Relais(2),  # Decke links
               'DeckeRechts':   Relais(3),  # Decke rechts
               'SIAP':          Relais(4),  # Engine1
               'MADI':          Relais(5),  # Madi & Subsystem
               'Iosono':        Relais(6),  # Engines
               'Keller':        Relais(7)}  # Keller


class ScreenBoot(Screen):
    BOOT_TIME = 80  # Zeit, wann auf nächsten Screen geschaltet wird

    def boot(self):
		
	
        # GUI zurücksetzen
        self.ids.boot_button.disabled = True
        self.ids.boot_progress.max = ScreenBoot.BOOT_TIME
        self.ids.boot_progress.value = 0
        self.incr_progress()

        if not DEBUG:
            # Verstaerker sicherheitshalber ausschalten
            Clock.schedule_once(lambda dt: relais_list['Keller']       .turn_off(),         0)
            Clock.schedule_once(lambda dt: relais_list['Schwalbennest'].turn_off(),         1)
            Clock.schedule_once(lambda dt: relais_list['DeckeLinks']   .turn_off(),         2)
            Clock.schedule_once(lambda dt: relais_list['DeckeRechts']  .turn_off(),         3)            

            # Relais einschalten
            Clock.schedule_once(partial(self.set_text, 'Peripherie wird eingeschaltet'),    0)
            Clock.schedule_once(lambda dt: relais_list['Iosono']       .turn_off(),         7)
            Clock.schedule_once(lambda dt: relais_list['MADI']         .turn_on(),          8)
            Clock.schedule_once(lambda dt: relais_list['SIAP']         .turn_on(),          9)

            Clock.schedule_once(partial(self.set_text, 'Computer werden hochgefahren'),    38)
            Clock.schedule_once(lambda dt: relais_list['Iosono']       .turn_on(),         38)

            Clock.schedule_once(partial(self.set_text, 'Verstärker werden eingeschaltet'), 67)
            Clock.schedule_once(lambda dt: relais_list['Keller']       .turn_on(),         67)
            Clock.schedule_once(lambda dt: relais_list['Schwalbennest'].turn_on(),         68)
            Clock.schedule_once(lambda dt: relais_list['DeckeLinks']   .turn_on(),         69)
            Clock.schedule_once(lambda dt: relais_list['DeckeRechts']  .turn_on(),         70)

            # Callback wenn abgeschlossen
            Clock.schedule_once(lambda dt: self.finished_boot(),     ScreenBoot.BOOT_TIME + 1)
        else:
            self.finished_boot()
        # '''

    def finished_boot(self):
        GPIO.output(PIN_LAMP, False)
        start_new_thread(Siap.set_preset, (0, ))

        # GUI aufräumen
        if not DEBUG:
            self.parent.ids.screen_main.ids.slider_volume.value = Iosono.get_volume()
        self.parent.ids.screen_main.ids.text_volume.text =\
            str(int(self.parent.ids.screen_main.ids.slider_volume.value)) + ' dB'
        self.parent.current = 'screen_main'
        self.ids.boot_button.disabled = False
        self.ids.boot_progress.value = 0
        self.set_text('System ist ausgeschaltet')

        logging.debug('System hochgefahren')

    def set_text(self, text, _=0):
        self.ids.boot_text.text = text

    def incr_progress(self):
        self.ids.boot_progress.value += 1
        if self.ids.boot_progress.value < ScreenBoot.BOOT_TIME:
            Clock.schedule_once(lambda dt: self.incr_progress(), 1)


class ScreenShutdown(Screen):
    if not DEBUG:
        SHUTDOWN_TIME = 60
    else:
        SHUTDOWN_TIME = 1

    def shutdown(self):
        # GUI zurücksetzen
        self.ids.shutdown_button_yes.disabled = True
        self.ids.shutdown_button_no.disabled = True
        self.ids.shutdown_progress.max = ScreenShutdown.SHUTDOWN_TIME
        self.ids.shutdown_progress.value = 0
        self.incr_progress()

        # Iosono-Computer herunterfahren
        if not DEBUG:
            start_new_thread(Iosono.shutdown, ())
            Clock.schedule_once(lambda dt: relais_list['Schwalbennest'].turn_off(),  0)
            Clock.schedule_once(lambda dt: relais_list['DeckeLinks']   .turn_off(),  1)
            Clock.schedule_once(lambda dt: relais_list['DeckeRechts']  .turn_off(),  2)
            Clock.schedule_once(lambda dt: relais_list['Keller']       .turn_off(), 35)
            Clock.schedule_once(lambda dt: relais_list['MADI']         .turn_off(), 36)
            Clock.schedule_once(lambda dt: relais_list['SIAP']         .turn_off(), 37)

        Clock.schedule_once(lambda dt: self.finished_shutdown(), ScreenShutdown.SHUTDOWN_TIME + 1)

    def finished_shutdown(self):
        GPIO.output(PIN_LAMP, True)
        # GUI aufräumen
        self.parent.current = 'screen_boot'
        self.ids.shutdown_button_yes.disabled = False
        self.ids.shutdown_button_no.disabled = False
        self.ids.shutdown_progress.value = 0
        self.set_text('System ist eingeschaltet')

        logging.debug('System heruntergefahren')

    def set_text(self, text, _=0):
        self.ids.shutdown_text.text = text

    def incr_progress(self):
        self.ids.shutdown_progress.value += 1
        if self.ids.shutdown_progress.value < ScreenShutdown.SHUTDOWN_TIME:
            Clock.schedule_once(lambda dt: self.incr_progress(), 1)


class ScreenMain(Screen):
    def set_amps(self, amps):
        if amps:
            Clock.schedule_once(lambda dt: relais_list['Keller']       .turn_off(),         0)
            Clock.schedule_once(lambda dt: relais_list['Schwalbennest'].turn_off(),         1)
            Clock.schedule_once(lambda dt: relais_list['DeckeLinks']   .turn_off(),         2)
            Clock.schedule_once(lambda dt: relais_list['DeckeRechts']  .turn_off(),         3)
            Clock.schedule_once(lambda dt: GPIO.output(PIN_LAMP, True),                     5)
			
        else:
            Clock.schedule_once(lambda dt: relais_list['Keller']       .turn_on(),          0)
            Clock.schedule_once(lambda dt: relais_list['Schwalbennest'].turn_on(),          1)
            Clock.schedule_once(lambda dt: relais_list['DeckeLinks']   .turn_on(),          2)
            Clock.schedule_once(lambda dt: relais_list['DeckeRechts']  .turn_on(),          3)
            Clock.schedule_once(lambda dt: GPIO.output(PIN_LAMP, False),                    5)

    def set_mute(self, mute):
        if mute:
            self.set_volume(-60.0)
        else:
            self.set_volume(self.ids.slider_volume.value)

    def set_volume(self, vol):
        if not DEBUG:
            # start_new_thread(Iosono.set_volume, (int(vol), ))
            Iosono.set_volume(int(vol))

    def play_demo(self, name):
        if not DEBUG:
            start_new_thread(Iosono.set_preset, (name,))
            # Clock.schedule_once(lambda dt: partial(Iosono.set_preset, name)(), 0)

    def stop_demo(self):
        if not DEBUG:
            start_new_thread(Iosono.stop_preset, ())
            # Clock.schedule_once(lambda dt: Iosono.stop_preset(), 0)

    def set_siap_preset(self, number):
        if not DEBUG:
            start_new_thread(Iosono.set_preset, ('1 SIAP wfs',))
            start_new_thread(Siap.set_preset, (number, ))
            self.disable_siap_buttons()
            Clock.schedule_once(lambda dt: self.enable_siap_buttons(), 60)

    def enable_siap_buttons(self):
        for id_name in self.ids:
            if id_name.count('siap_button'):
                self.ids[id_name].disabled = False

    def disable_siap_buttons(self):
        for id_name in self.ids:
            if id_name.count('siap_button'):
                self.ids[id_name].disabled = True

    def set_mode_siap(self):
        if not DEBUG:
            start_new_thread(Iosono.set_preset, ('1 SIAP wfs',))
            # Clock.schedule_once(lambda dt: partial(Iosono.set_preset, '1 SIAP wfs')(), 0)
            preset = Siap.get_status()[5]
            for id_name in self.ids:
                if id_name.count('siap_button'):
                    self.ids[id_name].state = 'normal'
            self.ids['siap_button_' + str(preset)].state = 'down'

    def set_mode_demo(self):
        if not DEBUG:
            start_new_thread(Iosono.stop_preset, ())
            for id_name in self.ids:
                if id_name.count('demo_button'):
                    self.ids[id_name].state = 'normal'
            self.ids.demo_button_0.state = 'down'

    def set_mode_saw(self):
        if not DEBUG:
            start_new_thread(Iosono.set_preset, ('2 SAW', ))


class WfsRemote(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return WfsRemote()


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), 'kivy_config.ini')
    Config.read(config_path)
    
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '480')
    Config.set('graphics', 'resizable', '0')
    #Config.set('graphics', 'fullscreen', '1')
    if not DEBUG:
        Config.set('graphics', 'show_cursor', '0')

    MainApp().run()
