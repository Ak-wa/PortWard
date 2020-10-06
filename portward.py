import os
import subprocess
import argparse
import time



class PortWard:
    def __init__(self, hostfile, emailfile):
        self.emailfile = emailfile
        self.mailcommand = ""
        self.hostfile = hostfile
        self.result = """PortWard Report
Following IPs have critical ports open:

"""

                
    def send_mail(self):
        with open(self.emailfile) as emails:
            for email in emails:
                email = email.rstrip()
                self.mailcommand = f"echo '{self.result}' | mail -s 'PortWard Threat identified' {email}"
                
                print(f"[+] Sending email out to {email}")
                os.system(self.mailcommand)
                print("[+] Email sent out")
        
        
    def scan_targets(self, hostfile):
        with open(hostfile) as targets:
            for target in targets:
                target = target.rstrip()
                print(f"[+] Scanning {target}")
                output = subprocess.Popen(f"nmap {target} -p3389-3395 --open -Pn | grep open", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0]
                if "open" in output.decode("utf-8"):
                    print("| " + output.decode("utf-8"))
                    self.result += (f"{target}:\n" + output.decode("utf-8"))
                else:
                    print(f"[-] No critical Port found on host {target}\n")


    def run(self):
        print("""
  ____            _ __        __            _ 
 |  _ \ ___  _ __| |\ \      / /_ _ _ __ __| |
 | |_) / _ \| '__| __\ \ /\ / / _` | '__/ _` |
 |  __/ (_) | |  | |_ \ V  V / (_| | | | (_| |
 |_|   \___/|_|   \__| \_/\_/ \__,_|_|  \__,_|
        Minimalistic Port Surveillance 
        
        """)
        self.scan_targets(self.hostfile)
        self.send_mail()
        zeit = time.ctime()
        print("Scan finished on: " + zeit)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("hostfile", help="host/target file to scan")
    parser.add_argument("emailfile", help="emails to send results to")
    args = parser.parse_args()
    portward = PortWard(hostfile=args.hostfile,emailfile=args.emailfile)
    portward.run()
    
