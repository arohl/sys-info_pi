#!/usr/bin/env python3
import sys
import math
import subprocess
from time import sleep
import psutil
import pifacecad


#UPDATE_INTERVAL = 60 * 5  # 5 mins
UPDATE_INTERVAL =  1  # 1 seconds
GET_IP_CMD = "hostname --all-ip-addresses"
GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
TOTAL_MEM_CMD = "free | grep 'Mem' | awk '{print $2}'"
USED_MEM_CMD = "free | grep '\-\/+' | awk '{print $3}'"
pc20_symbol = pifacecad.LCDBitmap(
    [0x00, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x00])
pc40_symbol = pifacecad.LCDBitmap(
    [0x00, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x00])
pc60_symbol = pifacecad.LCDBitmap(
    [0x00, 0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x00])
pc80_symbol = pifacecad.LCDBitmap(
    [0x00, 0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x00])
pc100_symbol = pifacecad.LCDBitmap(
    [0x00, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x00])
temperature_symbol = pifacecad.LCDBitmap(
    [0x4, 0x4, 0x4, 0x4, 0xe, 0xe, 0xe, 0x0])
memory_symbol = pifacecad.LCDBitmap(
    [0xe, 0x1f, 0xe, 0x1f, 0xe, 0x1f, 0xe, 0x0])
temp_symbol_index, memory_symbol_index = 5, 6


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')


def get_my_ip():
    return run_cmd(GET_IP_CMD)[:-1]


def get_my_temp():
    return run_cmd(GET_TEMP_CMD)[5:9]


def get_my_free_mem():
    total_mem = float(run_cmd(TOTAL_MEM_CMD))
    used_mem = float(run_cmd(USED_MEM_CMD))
    mem_perc = used_mem / total_mem
    return "{:.1%}".format(mem_perc)

def get_my_cpu():
    cpup = psutil.cpu_percent(interval=UPDATE_INTERVAL)
    cpu = "{:4.1f}".format(cpup)
    return cpu 

def wait_for_ip():
    ip = ""
    while len(ip) <= 0:
        sleep(1)
        ip = get_my_ip()

def display_pc(percent):
    step_size = 100/5/5
    no_steps = int(math.ceil(percent/step_size))

    for x in range(5):
        if no_steps >= 5:
            cad.lcd.write_custom_bitmap(4)
        elif no_steps > 0:
            cad.lcd.write_custom_bitmap(no_steps - 1)
        else:
            cad.lcd.write(" ")
        no_steps = no_steps - 5
    return 

def show_sysinfo():
    cad.lcd.clear()
    cad.lcd.write("{}\n".format(get_my_ip()))

    cad.lcd.write_custom_bitmap(temp_symbol_index)
    cad.lcd.write(":")

    cad.lcd.set_cursor(8, 1)
    cad.lcd.write_custom_bitmap(memory_symbol_index)
    cad.lcd.write(":")
    sleep(UPDATE_INTERVAL)

def update_sysinfo():
    while True:
        cad.lcd.set_cursor(2, 1)
        cad.lcd.write("{}C ".format(get_my_temp()))

        cad.lcd.set_cursor(10, 1)
        cputime = get_my_cpu()
        display_pc(float(cputime))
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
        cad.lcd.store_custom_bitmap(0, pc20_symbol)
        cad.lcd.store_custom_bitmap(1, pc40_symbol)
        cad.lcd.store_custom_bitmap(2, pc60_symbol)
        cad.lcd.store_custom_bitmap(3, pc80_symbol)
        cad.lcd.store_custom_bitmap(4, pc100_symbol)
        cad.lcd.store_custom_bitmap(temp_symbol_index, temperature_symbol)
        cad.lcd.store_custom_bitmap(memory_symbol_index, memory_symbol)
        cad.lcd.backlight_on()
        cad.lcd.write("Waiting for IP..")
        wait_for_ip()
        show_sysinfo()
        update_sysinfo()
