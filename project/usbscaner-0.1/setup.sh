#!/bin/bash
mkdir /opt/usbscanner_0.1
cp addcron.sh /opt/usbscanner_0.1/addcron.sh
cp usbscanner.py /opt/usbscanner_0.1/usbscanner.py
cp smtp.conf /opt/usbscanner_0.1/smtp.conf 
cp usb_ran_sh.rules /etc/udev/rules.d/usb_ran_sh.rules
cp usbscanner.service /lib/systemd/system/usbscanner.service 
chmod +x /opt/usbscanner_0.1/addcron.sh
chmod +x /opt/usbscanner_0.1/usbscanner.py
chmod 644 /lib/systemd/system/usbscanner.service
systemctl daemon-reload
systemctl enable usbscanner.service
