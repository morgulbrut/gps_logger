# -*- coding: utf-8 -*-
from pyb import UART
from micropyGPS import MicropyGPS
import os # somehow used to make open() work

# Setup the connection to your GPS here
# This example uses UART 3 with RX on pin Y10
# Baudrate is 9600bps, with the standard 8 bits, 1 stop bit, no parity
uart_gps = UART(6, 9600)
uart_bt = UART(1,9600)

pyb.repl_uart(uart_bt) # REPL to bluetooth uart, useful for debuging with the phone

# Instatntiate the micropyGPS object
my_gps = MicropyGPS()


def print_out(string):
    print(string)
    try:
        log = open('/sd/log.txt','a')
        log.write(string+'\n')
        log.close()
    except:
        print('SD Error')

# Continuous Tests for characters available in the UART buffer, any characters are feed into the GPS
# object. When enough char are feed to represent a whole, valid sentence, stat is set as the name of the
# sentence and printed
while True:
    pyb.wfi()
    if uart_gps.any():
        stat = my_gps.update(chr(uart_gps.readchar())) # Note the conversion to to chr, UART outputs ints normally
        if stat:
            ret = ('--------' + stat + '--------\n')
            ret += (my_gps.time_string() + '\n')
            ret += (my_gps.latitude_string()+ '\n')
            ret += (my_gps.longitude_string()+ '\n')
            ret += (my_gps.altitude_string()+ '\n')
            ret += (my_gps.speed_string()+ '\n')
            print_out(ret)
            stat = None
