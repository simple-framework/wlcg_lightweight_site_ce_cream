#!/bin/bash
#copy host certificates
echo "Copying host certificates..."
cp /etc/simple_grid/host_certificates/hostcert.pem /etc/grid-security/
cp /etc/simple_grid/host_certificates/hostkey.pem /etc/grid-security/

#set permissions
echo "Setting permissions for host certificates..."
chmod 600 /etc/grid-security/hostkey.pem
chmod 644 /etc/grid-security/hostcert.pem
echo "Done"

# set permissions on yaim directory
chmod 700 -R /etc/simple_grid/config/*

# update /etc/hosts
# modify /etc/hosts
#!/bin/sh

# Append container hosts file
hosts_container_file=/etc/simple_grid/config/hosts-container.conf
host_container_content=`cat $hosts_container_file`
hosts_file=/etc/hosts

if grep -Fxq "$host_container_content" $hosts_file
then
  echo "hosts file has been set, skipping"
else
#Remove last line
echo "$(head -n -1 $hosts_file )" > $hosts_file
#Add host container ip address
echo -e "$(cat $hosts_container_file )\n $(cat $hosts_file)" > $hosts_file
fi

#move configuration files to the correct place
cp /etc/simple_grid/config/wn-list.conf /root/
cp /etc/simple_grid/config/users.conf /root/
cp /etc/simple_grid/config/groups.conf /root/
cp /etc/simple_grid/config/edgusers.conf /root/

# Fix delay on bdii startup service
sed -i 's/sleep 2/sleep 10/g' /etc/init.d/bdii
sed -i 's/sleep 2/sleep 10/g' /etc/rc.d/init.d/bdii

# Update CA-EGI-policy
yum update -y ca-policy-egi-core

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
        -s /etc/simple_grid/config/cream-info.def \
        -n creamCE \
        -n TORQUE_server \
        -n TORQUE_utils \

# start daemons
service crond start
