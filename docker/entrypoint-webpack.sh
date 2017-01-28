#!/bin/bash

# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or
# fallback

#USER_ID=${LOCAL_USER_ID:-9001}
#GROUP_ID=${LOCAL_GROUP_ID:-9001}

USER=webpack
GROUP=webpack

USER_ID="$(stat -c '%u' /usr/src/app)" 
GROUP_ID="$(stat -c '%g' /usr/src/app)"
echo "Starting with UID : $USER_ID GID: $GROUP_ID"

groupadd -g $GROUP_ID $GROUP
useradd --shell /bin/bash -u $USER_ID -g $GROUP -o -c "" -m $USER
export HOME=/home/$USER

/usr/local/bin/gosu $USER_ID:$GROUP_ID bash -c 'npm install && npm run build'

echo "Running $@"
exec /usr/local/bin/gosu $USER_ID:$GROUP_ID "$@"
