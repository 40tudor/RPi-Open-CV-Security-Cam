#!/usr/bin/python3

#Captures single images every 30s, creates video with avconv

import os
import time
import picamera
from datetime import datetime as dt, timedelta

mountDrive = input('Mount Flashdrive? ')
if mountDrive == "y":
	os.system('sudo mount /dev/sda1 /mnt/flashdrive')
	print('Mounted flashdrive')

print (dt.now())
start_input=input('Start Time: ')
end_input=input('End Time: ')

st = dt.now().strftime('%Y-%m-%d')+" "+start_input[:2]+":"+start_input[2:4]+":00"
start_time = dt.strptime(st,"%Y-%m-%d %H:%M:%S")
et = dt.now().strftime('%Y-%m-%d')+" "+end_input[:2]+":"+end_input[2:4]+":00"
end_time = dt.strptime(et,"%Y-%m-%d %H:%M:%S")

def wait():
    delay = (start_time-dt.now()).total_seconds()
    print (delay)
    time.sleep(delay)

with picamera.PiCamera() as camera:
    camera.resolution = (1024,768)
    print ('Waiting...')
    wait()
    print ('Starting preview')
    camera.start_preview()
    time.sleep(2)
    camera.annotate_background = picamera.Color('black')

    try:
        for filename in camera.capture_continuous('img{counter:04d}.jpg'):
            camera.annotate_text = dt.now().strftime('%H:%M:%S')
            print ('Captured %s' % filename)
            rem=(end_time-dt.now()).total_seconds()
            print('Minutes Remaining: ' + str(rem/60))
            time.sleep(30)
            if dt.now() >= end_time:
                break
    finally:
        camera.stop_preview()

print ('Creating video')
os.system('./img2vid.sh')
print ('Done creating video')
if mountDrive == "y":
    os.system('sudo cp /home/pi/camera/out.avi /mnt/flashdrive')
    print ('Copied file to flashdrive')
    os.system('sudo umount /mnt/flashdrive')
    print ('unmounted flashdrive')
