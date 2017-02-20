#!/usr/bin/env bash

# NGINX settings
function nginx_settings
{
    sudo rm -rf /etc/nginx/sites-enabled/*
    sudo chmod 777 nginx.conf
    sudo cp -v nginx.conf /etc/nginx/sites-enabled/nginx.conf
    sudo nginx -t
    sudo /etc/init.d/nginx restart
}

# Supervisor settings
function supervisor_settings
{
    sudo cp -v gunicorn.conf /etc/supervisor/conf.d/
    sudo service supervisor restart
}

# Create a systemd Unit File
function systemd_setttings
{
    sudo cp -v ViberBotDjango.service /etc/systemd/system/
    sudo systemctl enable ViberBotDjango.service
    sudo systemctl start ViberBotDjango.service
    sudo systemctl daemon-reload
}

# Set cron job and restart cron service
function cron_timetable
{
    sudo cp -v run_parser_cron_timetable /etc/cron.d/
    sudo service cron restart
}

# extract options and their arguments into variables.
while [ "$1" != "" ]; do
    case "$1" in
        -h|--help) echo "Use this commands:
                            --start - init all settings;
                            --nginx - restart nginx;
                            --supervisor - restart supervisor settings;
                            --systemd - restart systemd settings;
                            --cron - set and restart cron jobs;
                         " ; shift ;;
        --start) nginx_settings ; supervisor_settings; systemd_setttings;;
        --nginx) nginx_settings;;
        --systemd) systemd_setttings;;
        --supervisor) supervisor_settings;;
        --cron) cron_timetable;;
        *) echo "Internal error!Check --help" ; exit 1 ;;
    esac
done


