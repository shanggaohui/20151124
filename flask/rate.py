#-*-coding:utf:8-*-

from flask import json
from flask import Flask
from flask import request

RATE = 0.16

app = Flask(__name__)
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    
    return False

@app.route('/api/rate', methods=['GET'])
def getRate():
    data = {'RMB_to_USD_rate': RATE}
    data_string = json.dumps(data)
    return data_string

@app.route('/api/rate', methods=['POST'])
def getResult():
    return '{"key": "value"}'
    data = json.loads(request.data or '{}')
    data_string = None
    if data is None or data == {}:
        return None

    for value in data.itervalues():
        if value == '' or value == None or not is_number(value):
            data_string = 'Invalid'
            return data_string

    if 'RMB' not in data and 'USD' not in data:
        data_string = 'Invalid'
        return data_string

    if 'RMB' in data:
        result = float(data.get('RMB'))*RATE
        data = {'USD':result}
        data_string = json.dumps(data)
        return data_string

    if 'USD' in data:
        result = float(data.get('USD'))/RATE
        data = {'RMB':result}
        data_string = json.dumps(data)
        return data_string

    return data_string




if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0')
