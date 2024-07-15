#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if it doesn't exist
if ! command -v nginx &>/dev/null;
then
    sudo apt update
    sudo apt install -y nginx
    sudo ufw allow 'Nginx HTTP'
    sudo chown -R "$USER":"$USER" /var/www/html/index.nginx-debian.html
    echo "Hello World!" | sudo tee /var/www/html/index.nginx-debian.html
fi

# Create necessary directories and file
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html

test_index=/data/web_static/releases/test/index.html
echo "Server configuration test for deployment"| sudo tee "$test_index" > /dev/null
# Create symbolic link to test release
symlink=/data/web_static/current

if [ -L "$symlink" ];
then
    sudo rm -rf $symlink
fi
sudo ln -s /data/web_static/releases/test/ "$symlink"
sudo chown -R ubuntu:ubuntu /data/

# Step 2: Add the location block to serve hbnb_static with alias
sudo sed -i '/^server {/a \    location \/hbnb_static\/ {\n        alias \/data\/web_static\/current\/;\n        index index.html;\n    }' /etc/nginx/sites-available/default
if [ -f /etc/nginx/sites-enabled/default ];
then
    sudo rm /etc/nginx/sites-enabled/default
fi
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

sudo service nginx restart
