__author__ = 'Simon Waloschek'

import socket
import logging
import time


class Iosono(object):
    _IP = '192.168.1.1'
    _PORT = 4444

    @staticmethod
    def __send(msg):
        try:
            Iosono.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Iosono.__client.connect((Iosono._IP, Iosono._PORT))
            Iosono.__client.send((msg + '\n').encode('utf-8'))
            data = ''
            while ':OK:' not in data:
                data += Iosono.__client.recv(2048).decode('utf-8')
            data_list = [s.strip() for s in data.splitlines()]
            del data_list[-1]
            Iosono.__client.close()
            return data_list
        except socket.error:
            logging.error('Verbindung zu Iosono fehlgeschlagen')
            return []

    @staticmethod
    def get_presets():
        return Iosono.__send('controlunit/get_all_presets')

    @staticmethod
    def set_preset(preset):
        data = ''
        while Iosono.get_current_preset() != preset:
            data = Iosono.__send('controlunit/set_preset ' + preset)
        return data

    @staticmethod
    def stop_preset():
        return Iosono.__send('controlunit/stop_current_preset')

    @staticmethod
    def shutdown():
        return Iosono.__send('system/shutdown')

    @staticmethod
    def get_volume():
        data = []
        while data ==  []:
            data = Iosono.__send('controlunit/get_volume')
        return int(data[0])

    @staticmethod
    def set_volume(vol):
        return Iosono.__send('controlunit/set_volume ' + str(vol))

    @staticmethod
    def get_current_preset():
        data = Iosono.__send('controlunit/get_current_preset')
        if data == []:
            return ''
        return data[0]

if __name__ == '__main__':
    print(Iosono.get_presets())
