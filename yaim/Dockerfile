
FROM cern/slc6-base
MAINTAINER Mayank Sharma (mayank.sharma@cern.ch)
########################
#   Misc packages
########################

#install sudo, wget and openssh-clients
RUN yum install -y \
	sudo \
	wget \
    openssh-clients \
	openssh-server

########################
#        UMD 4
########################

# install yum-priorities
RUN yum install -y \
	yum-priorities

# Install (for now) the SL6 repo details for UMD-3, because currently it has
# most of the necessary components:
RUN yum install -y \
	http://repository.egi.eu/sw/production/umd/4/sl6/x86_64/updates/umd-release-4.1.3-1.el6.noarch.rpm

#########################
#    Torque + Maui
#########################

#Torque + Maui are most easily obtained from the EGI third-party repository
RUN wget -O /etc/yum.repos.d/EGI-third-party.repo \
	http://repository.egi.eu/community/software/third.party.distribution/1.0/releases/repofiles/sl-6-x86_64.repo

#Let it override the unsupported Torque from EPEL:

RUN echo -e 'protect=1\npriority=1' >> /etc/yum.repos.d/EGI-third-party.repo 

#The third-party repo Torque version looks old, but all known serious
#vulnerabilities have been patched by experts in EGI.

#Maui is no longer officially supported by anyone AFAIK, but as long as the
#firewall configurations limit the access as advertised, we need not be too
#concerned about that.

#########################
#     Configuration
#########################

RUN yum -y install  \
	ca-policy-egi-core \
	emi-cream-ce \
	emi-torque-server \
	emi-torque-utils


# for compatibility between different versions...

RUN ln -s /var/spool/pbs /var/lib/torque
RUN mkdir /var/spool/pbs/checkpoint

# work around an old bug...
RUN perl -pi.bak -e 's/while.*]/for i in `seq 10`/' /etc/init.d/pbs_server

# generate ssh host keys
RUN service sshd start

# Mount Volume for configuration parameters
VOLUME /config

# init script on launch
#ENTRYPOINT ["/ce-config/init.sh"]


