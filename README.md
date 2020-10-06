# PortWard - Minimalistic Port Surveillance
![python](https://img.shields.io/pypi/pyversions/Django.svg)
![size](https://img.shields.io/github/size/ak-wa/PortWard/portward.py.svg)
![lastcommit](https://img.shields.io/github/last-commit/ak-wa/PortWard.svg)
![follow](https://img.shields.io/github/followers/ak-wa.svg?label=Follow&style=social)     

PortWard is a tool developed for checking a list of assets/hosts for critical ports (e.g RDP) and sending an email to you with the results, in case of a critical port being open.   

## How does it work?  
* PortWard checks a list of IPs/hostnames for specific Ports using nmap
* In case it finds an IP/hostname with one or more specific ports open   
-> sends an email to you, including those hosts and ports each

## Why PortWard?
* Made for running in Crontab
* Easy to set up and configure
* Minimalistic email design, no unnecessary stuff
* No need for setting up your own server, gmail is perfectly fine
* Easy usable in other projects   

## Setup (Tested on Debian 10 Buster & Kali Linux 2020.1)   
#### Step 1 - prerequisites
```bash
apt install msmtp msmtp-mta mailutils 
git clone https://github.com/Ak-wa/PortWard.git
cd PortWard
pip3 install -r requirements.txt
```

#### Step 2 - setting up portward mail sender   

Enable "less secure apps" in your google account:   
```https://myaccount.google.com/lesssecureapps```

Mail configuration:
`nano /etc/msmtprc`   
with the following content:   
```
# Set default values for all following accounts.
defaults
port 587
tls on
tls_trust_file /etc/ssl/certs/ca-certificates.crt

account gmail
host smtp.gmail.com
from <YOUR EMAIL@gmail.com>
auth on
user <YOUR EMAIL USERNAME>
password <password>

# Set a default account
account default : gmail
```
Making sure the file is not available for everyone:   
```bash
chmod 600 /etc/msmtprc
```

Define mail program:
```nano /etc/mail.rc```
with the following content:   
```set sendmail="/usr/bin/msmtp -t"```   

If you want to change the ports scanned or somehow change the nmap command used, yet in code you have to change the following line:   
```line 35: output = subprocess.Popen(f"nmap {target} -p3389-3395 --open -Pn | grep open", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0]```   


**NOTE**: if you want to know what you are doing, here's the manual: https://marlam.de/msmtp/msmtp.html   
      same applies if you want to **encrypt the password** and not store it in the config.   
      
## Usage
### 1. Command line   
`python3 portward.py <hostfile> <emailfile>`   
`<hostfile>` is your file of target hosts to scan    
`<emailfile>` is your file of emails to send the reports to


### 2. Crontab

```bash
mkdir /usr/share/portward
cp hostfile.txt /usr/share/hostfile.txt
cp emailfile.txt /usr/share/emailfile.txt
```
`crontab -e` with the following **example** content:   
```*/5 * * * *  /usr/bin/python3 /usr/share/portward/portward.py /usr/share/portward/hostfile.txt /usr/share/portward/emailfile.txt | tee /usr/share/portward/portward.log```   
Attention, in this example configuration it will scan the IPs every **5 Minutes**, so make sure to change that.


