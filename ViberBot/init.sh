#!/usr/bin/env bash

# NGINX settings
sudo rm -rf /etc/nginx/sites-enabled/*
sudo chmod 777 nginx.conf
sudo cp -v nginx.conf /etc/nginx/sites-enabled/nginx.conf
sudo nginx -t
sudo /etc/init.d/nginx restart

# Supervisor settings
sudo cp -v gunicorn.conf /etc/supervisor/conf.d/
sudo service supervisor restart

# Create a systemd Unit File
sudo cp -v ViberBotDjango.service /etc/systemd/system/
sudo systemctl enable ViberBotDjango.service
sudo systemctl start ViberBotDjango.service
sudo systemctl daemon-reload


