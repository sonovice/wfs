# -*- coding: utf-8 -*-

__author__ = 'Waloschek'

from struct import pack, unpack
import socket
import logging


class Siap(object):
    _IP = '192.168.1.76'
    _PORT = 1099

    @staticmethod
    def __send(msg):
        try:
            Siap.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Siap.__client.connect((Siap._IP, Siap._PORT))
            Siap.__client.send(msg)
            data = Siap.__client.recv(2048)
            Siap.__client.close()
            return data
        except socket.error:
            logging.error('Verbindung zu SIAP fehlgeschlagen')
            return ''

    # @staticmethod
    # def get_setup():
    #     data = Siap.__send(pack('<4sII', b'STUQ', 1, 0))
    #     response = unpack('<4s3I', data[0:16])
    #     presets = '' + data[17:]
    #     presets = presets.replace("\x00'", '').replace("\x00,", '')
    #     presets = presets.replace('\xe4', 'ä')
    #     presets = presets.split("\x00\x00\x00")
    #     data_list = []
    #     for p in presets:
    #         if not p.count('USER'):
    #             data_list.append(p.strip())
    #     del data_list[0]
    #     return [response, data_list]

    # @staticmethod
    # def get_preset():
    #     data = Siap.__send(pack('<4sII', b'PRSQ', 1, 0))
    #     response = unpack('<4s4I', data[0:20])
    #     return response

    @staticmethod
    def get_status():
        data = Siap.__send(pack('<4sII', b'STAQ', 1, 0))
        response = unpack('<4s5I', data[0:24])
        return response

    @staticmethod
    def set_preset(number):
        # Siap.__send('PRSC' + pack('<I', 1) + pack('<I', 4) + pack('<I', number))
        while Siap.get_status()[5] != number:
            Siap.__send(pack('<4sIII', b'PRSC', 1, 4, number))