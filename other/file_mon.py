#!/usr/bin/python3
# apt install python3-watchdog

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

PATH='/home/oper/.config/yandex-browser-beta'

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        print(event)

    def on_deleted(self, event):
        print(event)

    def on_moved(self, event):
        print(event)


observer = Observer()
observer.schedule(Handler(), path=PATH, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1000)
except KeyboardInterrupt:
    observer.stop()
observer.join()
 
