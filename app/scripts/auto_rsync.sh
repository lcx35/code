#!/bin/bash

localdir=$1
remotedir=$2
remoteip=$3
user=$4
password=$5

/usr/bin/expect <<EOF
spawn /usr/bin/rsync -az --exclude=.git --delete ${localdir} ${user}@${remoteip}:${remotedir}
expect {
"*yes/no" {send "yes\r"; exp_continue}
"*password:" {send "${password}\r"}
}
expect "*#"
EOF


