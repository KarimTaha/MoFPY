from flask import Flask, request, jsonify, make_response, abort, json
from subprocess import Popen
from flask_cors import CORS, cross_origin
import subprocess
import requests
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def index():
    res = request.json
    if not res or not 'username' in res or not 'password' in res or not 'entity' in res or not 'transfer' in res or not 'transferSegment' in res:
        abort(400)
    cred = open("C:\\users\\user 4\\desktop\\creds.txt", "w")
    rtp = open("C:\\users\\user 4\\desktop\\rtp.txt", "w")

    cred.write("Username: "+res['username']+"\n")
    cred.write("Password: "+res['password'])

    rtp.write("Entity: "+res['entity']+"\n")
    rtp.write("Transfer: "+res['transfer']+"\n")
    rtp.write("Transfer Segment: "+res['transferSegment']+"\n")

    p = Popen("test.bat", cwd=r"C:\users\user 4\desktop", stdout=subprocess.PIPE)
    # stdout, stderr = p.communicate()
    rtp.write(p.stdout.read())

    return "POST method was successfuly called!"



@app.route('/logIn', methods=['GET'])
def logIn():
    headers = {'Authorization':'Basic '+request.headers.get('auth')}
    r = requests.get('http://94.200.95.142:3285/HyperionPlanning/rest/11.1.2.4/applications/', headers=headers)
    return str(r.status_code)




@app.route('/getData', methods=['GET'])
def getData():
    req = request.headers
    url = req.get('url')
    auth = req.get('auth')
    headers = {'Authorization':'Basic '+auth}
    r = requests.get(url, headers=headers)
    requestResult = open("C:\\users\\user 4\\desktop\\requestResult.txt", "a")
    requestResult.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n")
    return r.text



@app.route('/getDetails', methods=['GET'])
def getDetails():
    req = request.headers
    url = req.get('url')
    auth = req.get('auth')
    entity = req.get('entity')
    transfer = req.get('transfer')
    segment = req.get('segment')

    one = "mdxQuery= Select {[Selection Account],[Selection Location],[Selection Activity "
    two = "],[Source],[Destination]} ON COLUMNS, Non Empty {[All Line Items].Children} ON ROWS FROM MOF_BT.MOF_BT WHERE "
    three = "([Period].[Annual Value],[FY17],[Fund Transfer],[Stage 1 - Working],[Department NSP],["
    four = "],[Input View],[Activity NSP],[Location NSP],[Project NSP],[Account NSP],["

    query = one + entity + two + three + entity + four +transfer + "],["+segment + "])"


    headers = {'Authorization':'Basic '+auth}
    body = query
    # requestResult = open("C:\\users\\user 4\\desktop\\detailsReq.txt", "w")
    # requestResult.write(url)
    r = requests.post(url, headers=headers, data=query)
    return r.text



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Wrong URL'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'Error': 'Bad request, check parameters'}),400)

if __name__ == '__main__':
    app.run(debug=True)
