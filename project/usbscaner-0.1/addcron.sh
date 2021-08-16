#!/bin/bash
touch /var/spool/cron/crontabs/root
if !(grep "usbscanner.py" /var/spool/cron/crontabs/root); then
  echo '*/2 * * * * /usr/bin/env /opt/usbscanner_0.1/usbscanner.py' >> /var/spool/cron/crontabs/root
fi
service cron restart
