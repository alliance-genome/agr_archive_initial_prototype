#!/bin/bash

# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or
# fallback

USER_ID=${LOCAL_USER_ID:-9001}
GROUP_ID=${LOCAL_GROUP_ID:-9001}

echo "Starting with UID : $USER_ID"

groupadd -g $GROUP_ID webpack
useradd --shell /bin/bash -u $USER_ID -g webpack -o -c "" -m webpack
export HOME=/home/webpack

/usr/local/bin/gosu webpack bash -c 'npm install && npm run build'

echo "Running $@"

/usr/local/bin/gosu webpack "$@"
