#!/bin/bash

# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or
# fallback

USER_ID=${LOCAL_USER_ID:-9001}
GROUP_ID=${LOCAL_GROUP_ID:-9001}

echo "Starting with UID : $USER_ID"
groupadd -g $GROUP_ID flask
useradd --shell /bin/bash -u $USER_ID -g flask -o -c "" -m flask
export HOME=/home/flask

# Block until the manifest file appears.
# TODO Figure out why the docker-compose.yml links and depends_on
# don't take care of this.
while : ; do
  [[ -f "/usr/src/app/src/build/manifest.json" ]] && break
  echo "Pausing until file exists."
  sleep 5 
done

exec /usr/local/bin/gosu flask "$@"
