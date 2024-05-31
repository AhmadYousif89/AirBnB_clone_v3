#!/usr/bin/env bash
# script that sets up web servers for the deployment of web_static
if ! command -v nginx &> /dev/null
then
    sudo apt update
    sudo apt install nginx -y
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir /data/web_static/shared/
echo "This is a test page!" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '38i\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo service nginx restart
