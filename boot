#!/bin/sh
xset -dpms     # disable DPMS (Energy Star) features.
xset s off     # disable screen saver
xset s noblank # don't blank the video device
matchbox-window-manager -use_titlebar no &
unclutter &    # hide X mouse cursor unless mouse activated

# execute in an infinite loop so it relaunches if there's a crash
while true
do
  cd menu
  python3 main.py > log.txt 2>&1
done
