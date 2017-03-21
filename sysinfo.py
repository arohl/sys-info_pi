#!/usr/bin/env python3
import sys
import math
import subprocess
from time import sleep
import psutil
import pifacecad


UPDATE_INTERVAL =  1  # 1 seconds
GET_IP_CMD = "hostname --all-ip-addresses"
GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
GET_CORES_CMD = "mpstat -P ALL 1 1"
one_bar = pifacecad.LCDBitmap(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f])
two_bar = pifacecad.LCDBitmap(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x1f])
three_bar = pifacecad.LCDBitmap(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x1f, 0x1f])
four_bar = pifacecad.LCDBitmap(
    [0x00, 0x00, 0x00, 0x00, 0x1f, 0x1f, 0x1f, 0x1f])
five_bar = pifacecad.LCDBitmap(
    [0x00, 0x00, 0x00, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f])
six_bar = pifacecad.LCDBitmap(
    [0x00, 0x00, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f])
seven_bar = pifacecad.LCDBitmap(
    [0x00, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f])
eight_bar = pifacecad.LCDBitmap(
    [0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f])


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_my_ip():
    return run_cmd(GET_IP_CMD)[:-1]

def get_my_temp():
    return run_cmd(GET_TEMP_CMD)[5:9]

def get_my_cores():

    usage = []
    count = 0
    lines = run_cmd(GET_CORES_CMD)
    info = lines.split("\n")
    for i in range(4):
        idle = info[i+4].split()[12]
        usage.append(100.0 - float(idle))

    return usage

def wait_for_ip():
    ip = ""
    while len(ip) <= 0:
        sleep(1)
        ip = get_my_ip()

def show_sysinfo():
    cad.lcd.clear()
    cad.lcd.write("{}\n".format(get_my_ip()))

    cad.lcd.write("T:")

    cad.lcd.set_cursor(8, 1)
    cad.lcd.write("C:")
    sleep(UPDATE_INTERVAL)

def update_sysinfo():
    while True:
        cad.lcd.set_cursor(2, 1)
        cad.lcd.write("{}C ".format(get_my_temp()))

        cad.lcd.set_cursor(10, 1)
        cores = get_my_cores()
        #print ("%4.1f" % cores[0] + " " + "%4.1f" % cores[1] + " " + "%4.1f" % cores[2] + " " + "%4.1f" % cores[3])
       
        for i in range(4):
            index = int(cores[i]/13)
            cad.lcd.write_custom_bitmap(index)
        sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    cad = pifacecad.PiFaceCAD()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()

    if "clear" in sys.argv:
        cad.lcd.clear()
        cad.lcd.display_off()
        cad.lcd.backlight_off()
    else:
        cad.lcd.store_custom_bitmap(0, one_bar)
        cad.lcd.store_custom_bitmap(1, two_bar)
        cad.lcd.store_custom_bitmap(2, three_bar)
        cad.lcd.store_custom_bitmap(3, four_bar)
        cad.lcd.store_custom_bitmap(4, five_bar)
        cad.lcd.store_custom_bitmap(5, six_bar)
        cad.lcd.store_custom_bitmap(6, seven_bar)
        cad.lcd.store_custom_bitmap(7, eight_bar)
        cad.lcd.backlight_on()
        cad.lcd.write("Waiting for IP..")
        wait_for_ip()
        show_sysinfo()
        update_sysinfo()
