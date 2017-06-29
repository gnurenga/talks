import requests
import re
#http://admin:12345678@192.168.1.100/Set.cmd?CMD=SetPower&P60=1&P61=1&P62=1&P63=0


class commands(object):
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    def __init__(self, ip='localhost:5000'):
        self.ip_address = ip
        self.query = {}
        self.user = 'admin'
        self.passw = '12345678'

    def form_query(self, state, cmd, port):
        port = self.get_port_no(port)
        self.query = {port: state}
        return self.query

    def get_port_no(self, port_no):
        port = 'P6' + str(port_no)
        return port

    def clean_html(self, data):
        exp = re.compile('<.*?>')
        text = re.sub(exp, "", data)
        return text.rstrip()

    def send_cmds(self, cmd, port=None, state=None):
        url = 'http://{}:{}@{}/SetCmd?CMD={}'\
              .format(self.user,
                      self.passw,
                      self.ip_address,
                      cmd)
        print url
        if cmd == 'SetPower':
            self.form_query(state, cmd, port)
            self.req = requests.get(url, params=self.query)
            return True
        elif cmd == 'GetPower':
            self.req = requests.get(url)
            data = self.clean_html(self.req.text)
            return data
        else:
            return False

        return self.req.text


# c = commands('localhost:5000')

# c.send_cmds('SetPower', 2, 1)
# c.send_cmds('SetPower', 3, 1)
# print c.send_cmds('GetPower')

