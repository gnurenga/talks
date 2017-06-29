from flask import Flask, request
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
        'admin': '12345678'
}
app.url_map.strict_slashes = False

PINS = ['P60', 'P61', 'P62', 'P63']

PINS_STATUS = {'P60':'0', 'P61': '0', 'P62':'0', 'P63':'0'}

@auth.get_password
def get_pw(username):
        if username in users:
                return users.get(username)
        return None

@app.route('/')
@auth.login_required
def index():
        return "Hello, %s!" % auth.username()

def get_html_string():
        html_str = '<html>P60={}P61={}P62={}P63={}</html>'.format(PINS_STATUS['P60'],
                                                PINS_STATUS['P61'],
                                                PINS_STATUS['P62'],
                                                PINS_STATUS['P63'])
        
        return html_str

def parse_cmd_args(args):
        global current_status
        if str(args['CMD']) == 'SetPower':
                for key in args:
                        if key in PINS:
                                PINS_STATUS[key] = str(args[key])
                                
                return get_html_string()
        
        if str(args['CMD']) == 'GetPower':
               return get_html_string()
       

@app.route('/SetCmd', methods=['GET','POST'])
def rps():
        if request.method=="GET":
                args=request.args.to_dict()
                ret = parse_cmd_args(args)
                return ret

