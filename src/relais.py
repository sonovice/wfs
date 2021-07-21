# -*- coding: utf-8 -*-

from binascii import unhexlify
import socket
import logging

__author__ = 'Simon Waloschek'


class Relais(object):
    __PREFIX = '5649545902140114494409BC110200'
    __POSTFIX_ON = 'E1008104'
    __POSTFIX_OFF = 'E1008004'
    __CHECKSUM_OFFSET_ON = 0xCB
    __CHECKSUM_OFFSET_OFF = 0xCA

    _IP = '192.168.1.34'
    _PORT = 12000
    __client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, number):
        self.number = number

    def __send_to_eib(self, msg):
        try:
            self.__client.sendto(unhexlify(msg), (Relais._IP, Relais._PORT))
        except socket.error:
            logging.error('Nachricht konnte nicht an EIB versendet werden')

    def turn_on(self):
        self.__send_to_eib(self.__PREFIX
                           + ('%0.2X' % self.number)
                           + self.__POSTFIX_ON
                           + ('%0.2X' % (self.__CHECKSUM_OFFSET_ON + self.number)))

    def turn_off(self):
        self.__send_to_eib(self.__PREFIX
                           + ('%0.2X' % self.number)
                           + self.__POSTFIX_OFF
                           + ('%0.2X' % (self.__CHECKSUM_OFFSET_OFF + self.number)))
