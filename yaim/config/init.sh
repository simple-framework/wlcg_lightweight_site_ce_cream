#!/bin/bash
#copy host certificates
echo "Copying host certificates..."
cp /config/host-certificates/hostcert.pem /etc/grid-security/
cp /config/host-certificates/hostkey.pem /etc/grid-security/

#set permissions
echo "Setting permissions for host certificates..."
chmod 600 /etc/grid-security/hostkey.pem
chmod 644 /etc/grid-security/hostcert.pem
echo "Done"

# set permissions on yaim directory
chmod 700 -R /config/*

#move configuration files to the correct place
cp /config/wn-list.conf /root/
cp /config/users.conf /root/
cp /config/groups.conf /root/
cp /config/edgusers.conf /root/

#run YAIM
ln -s /usr/share/java/bcprov-1.58.jar /usr/share/java/bcprov.jar
if grep -Fxq "creationTime  TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP," /etc/glite-ce-cream/populate_creamdb_mysql.sql
then
  echo "No changes made to populate_creamdb_mysql.sql"
else
  LINE_NUMBER=$(grep -n "creationTime  TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP" /etc/glite-ce-cream/populate_creamdb_mysql.sql | cut -d: -f -1)
  echo "Line Number is ${LINE_NUMBER}"
  sed -ie $LINE_NUMBER's/$/, &/' /etc/glite-ce-cream/populate_creamdb_mysql.sql
fi
service rsyslog start
service sshd start
echo "Starting YAIM..."
/opt/glite/yaim/bin/yaim -c  \
        -s /config/cream-info.def \
        -n creamCE \
        -n TORQUE_server \
        -n TORQUE_utils \

# start daemons
service crond start