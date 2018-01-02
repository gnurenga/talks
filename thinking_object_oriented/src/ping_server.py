"""Usage: ./ping_server.py
   
This code will check the status of each server given
in the server.yaml file is up or down.

If any transition of state from up to down or down to up
the recipients mentioned in the to_mail_ids will get 
alert mail.

"""

from ruamel.yaml import YAML
from time import sleep
import requests
import subprocess
import io
import os

from_mail_id = "gnurenga@outlook.com" 
to_mail_ids = ["sakthirengaraj@gmil.com"]

yaml=YAML()
with open("server.yaml", 'r') as stream:
    data = yaml.load(stream)

    
class ServerStatus:
    def __init__(self, servername, ip):
        """Initialize the server state
        
        Select the server name and ip to check the state of the
        server
        
        Args:
            servername: Name of the server as string
            ip: Ip address of the given server in string
        """
        self.servername = servername
        self.serverip = ip
        self.current_state = "up"
        self.previous_state = "up"
        

    def is_system_up(self, ip):
        """ Check the given Server Ip is reachable or not

        Returns: 
              True or False. True if the Ip is reachable
              False if the server is not reachable
        """
        
        with io.open(os.devnull, 'wb') as devnull:
            try:
                subprocess.check_call(
                    ['ping', '-c3', ip],
                    stdout=devnull, stderr=devnull)
            except subprocess.CalledProcessError:
                return False
            else:
                return True

    def check_server(self):
        """Helper function to maintain the state of the server either up or
        down.
        """
        if self.is_system_up(self.serverip) == True:
            self.current_state = "up"
        else:
            self.current_state = "down"

    def get_state(self):
        """Helper function to return current state and previous state of
        the given server as a dictionary
        """
        return {"current_state":self.current_state, 
                "previous_state":self.previous_state}


    def send_message(self, message_status, message_server):
        """ Send message will trigger a mail to sent using mail gun rest API
        Args:
            message_status: string message about the server status down or up
            message_server: string message about the server IP
        return:
            Integer: Status code of request http call
        """

        # return requests.post(
        #     "https://api.mailgun.net/v3/samples.mailgun.org/messages",
        #     auth=("api", "key-3ax6xnjp29jd6fds4gc373sgvjxteol0"),
        #     data={"from": from_mail_id,
        #           "to": to_mail_ids,
        #           "subject": message_status + ",ip is " + message_server,
        #           "text": "Alert: " + message_status + ",ip is " + message_server})
        print message_status + message_server


    def run_check(self):
        """Main function of the ServerStatus class. Which will maintain the 
        server status for each run. If the server current state and previous state
        is same, It wont trigger the mail.
        
        If the server current state and previous state is not equal then it will trigger 
        the mail and update the previous state with current state.

        There by we will get mail if there is any transition from up to down or 
        down to up
        """
        
        self.check_server()

        if self.current_state != self.previous_state:
            self.previous_state = self.current_state
            self.send_message(self.servername + " is " + self.current_state, " ip is " + self.serverip)
            

def main():
    """ This part of code implements the actuall logic.

    This function will maintain each server as an object instantiated from the class
    ServerStatus in a dictionary servers={}. 

    In an Infinite loop each server status object run_check() will get executed and
    state of each server is maintained for every 5 mins.
    """
    global data

    instance_server = [server for server in data.iterkeys()]
    servers = {}


    for index, serv in enumerate(data.iterkeys()):
        servers[instance_server[index]] = ServerStatus(data[serv][0], data[serv][1])

    while True:
        for server in servers.iterkeys():
            servers[server].run_check()

        sleep(30)
        

if __name__ == "__main__":
    main()
