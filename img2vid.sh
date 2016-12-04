#!/bin/bash
avconv -y -framerate 24 -f image2 -i img%04d.jpg -c:v h264 -crf 20 out.avi
