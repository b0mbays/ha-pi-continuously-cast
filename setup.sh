#!/bin/bash

pushd /opt/ha-cast

echo "Installing pip3.."
apt-get -y install python3 python3-pip

echo "***Installing requirements..."
pip3 install -r /opt/ha-cast/requirements.txt

echo "Creating a new user for the service.."
useradd -r -s /bin/false hacast_user

echo "Move the service file to the system folder"
cp /opt/ha-cast/hacast.service /etc/systemd/system/

echo "Reload the systemctl daemon"
systemctl daemon-reload

echo "Enable the service to start on boot"
systemctl enable hacast.service

echo "Set permissions for the log file"
touch /opt/ha-cast/ha-cast.log
chown hacast_user:hacast_user /opt/ha-cast/ha-cast.log
chmod 664 /opt/ha-cast/ha-cast.log

echo "Set permissions for the catt command"
chown hacast_user:hacast_user $(which catt)
chmod u+x $(which catt)

echo "Start the service"
systemctl start hacast.service

echo "Service has started. Please check the log file for more info!"
