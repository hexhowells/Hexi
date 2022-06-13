#!/bin/sh
### BEGIN INIT INFO
# Provides:		audio
# Required-Start:	$remote_fs $syslog
# Required-Stop:	$remote_fs $syslog
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	init audio speaker
# Description:		play continuous audio through speaker to stop popping sounds
### END INIT INFO

aplay -t raw -r 48000 -c 2 -f s16_LE /dev/zero &
