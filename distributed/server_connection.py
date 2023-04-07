import json 

import urllib
import urllib.request

def call_server(url, queryParameters={}, postData=None, headers={}, debug=False):

    queryParametersEncoded = urllib.parse.urlencode(queryParameters)
    if debug:
        print('Url:', url+"?"+urllib.parse.urlencode(queryParameters, doseq=True))
    if postData == None:
        data = None
    else:
        data = urllib.parse.urlencode(postData)
        if debug:
            print("Data:", urllib.parse.urlencode(postData, doseq=True) )
    try:
        request = urllib.request.Request(url+"?"+queryParametersEncoded,data=data, headers={"Accept" : "application/json"})
#        request.get_method = lambda: "POST"
        contents = urllib.request.urlopen(request).read()
        response_json = contents.decode('utf-8').replace('\0', '')
        return json.loads(response_json)
    except urllib.error.HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    #    print 'Url:', url+"?"+urllib.unquote(urllib.urlencode(postData, doseq=True)).decode('utf8') 
        print('Url:', url+"?"+urllib.urlencode(postData, doseq=True) )
        print(e.read())
    except urllib.error.URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        

import numpy as np

class ServerJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,np.int_):
            return int(obj)
        elif isinstance(obj,np.ndarray):
            return list(obj)
        elif type(obj).__module__=='numpy': # if value is numpy.*: > to python list
            return obj.tolist()
        elif isinstance(np.float):
            return np.rint(obj).astype('int')
        else:
            return super(ServerJsonEncoder, self).default(obj)
            
            
