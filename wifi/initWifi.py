#!/usr/bin/env python
from subprocess import call, check_output

def init_usb(driver, iface):
    class WifiAdaptorNotReady(Exception):
        pass

    def check_command(command, output, exception=False):
        for line in check_output(command).split('\n'):
            if output in line: return True
        if not exception: return False
        else: raise WifiAdaptorNotReady()

    check_command(['lsusb'], driver, exception=True)
    call(['killall', 'NetworkManager'])
    if not check_command(['airmon-ng'], 'mon0'):
        if check_command(['iwconfig'], iface, exception=True):
            check_command(['airmon-ng', 'start', iface], iface)

if __name__ == "__main__":
    init_usb('Atheros', 'wlan1')
