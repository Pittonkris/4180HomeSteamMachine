
touch 0
# ( bash /home/pi/4180HomeSteamMachine/apps/Steam\ Link/run2.sh & )
sleep 10
touch 1
killall --signal SIGKILL python3
touch 2
killall --signal SIGKILL xinit
touch 3
killall xow
killall Xorg
steamlink
