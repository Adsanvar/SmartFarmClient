
val=$(tail -n 1 /etc/xdg/lxsession/LXDE-pi/autostart)
if [ $val == "point-rpi" ]
then
    sudo sh -c "echo '@lxterminal -e ~/Documents/SmartFarmClient/run_app.sh' >> /etc/xdg/lxsession/LXDE-pi/autostart"
    sudo sh -c "echo '@lxterminal -e ~/Documents/SmartFarmClient/localtunnel.sh' >> /etc/xdg/lxsession/LXDE-pi/autostart"
fi

export FLASK_APP=~/Documents/SmartFarmClient/Agriculta
export FLASK_ENV=development
export DEBUG=1
export FLASK_RUN_PORT=5005

# lxterminal -e bash --c "lt --port 5005 --subdomain agriculta"
flask run
