#!/bin/bash
while true; do
    if ! pgrep -f 'lint' && ! pgrep -f 'git clone'; then
        rm -rf /tmp/*
    fi
    sleep 600
done