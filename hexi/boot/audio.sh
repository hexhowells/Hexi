#!/bin/sh
aplay -t raw -r 48000 -c 2 -f s16_LE /dev/zero &
