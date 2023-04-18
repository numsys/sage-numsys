import json 

import urllib
import urllib.parse
import urllib.error
import urllib.request
import sage
from sage.all import *
def call_server(url, query_parameters=None, post_data=None, headers=None, debug=False):
    if query_parameters is None:
        query_parameters = {}

    query_parameters_encoded = urllib.parse.urlencode(query_parameters)

    if debug:
        print('Url:', url +"?" + urllib.parse.urlencode(query_parameters, doseq=True))


    if post_data == None:
        data = None
    else:
        data = urllib.parse.urlencode(post_data).encode("utf-8")
        if debug:
            print("Data:", urllib.parse.urlencode(post_data, doseq=True))
    try:
        request = urllib.request.Request(url+"?"+query_parameters_encoded,data=data, headers={"Accept" : "application/json"})
#        request.get_method = lambda: "POST"
        contents = urllib.request.urlopen(request).read()
        response_json = contents.decode('utf-8').replace('\0', '')
        return json.loads(response_json)
    except urllib.error.HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    #    print 'Url:', url+"?"+urllib.unquote(urllib.urlencode(postData, doseq=True)).decode('utf8') 
        print('Url:', url +"?" + urllib.urlencode(post_data, doseq=True))
        print(e.read())
    except urllib.error.URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        

import numpy as np

class ServerJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, sage.matrix.matrix0.Matrix):
            return list(obj)
        if isinstance(obj, sage.modules.free_module_element.FreeModuleElement):
            return list(obj)
        if isinstance(obj, Integer):
            return int(obj)
        if isinstance(obj, np.int_):
            return int(obj)
        elif isinstance(obj, np.ndarray):
            return list(obj)
        elif type(obj).__module__=='numpy': # if value is numpy.*: > to python list
            return obj.tolist()
        elif isinstance(obj, np.float):
            return np.rint(obj).astype('int')
        else:
            return super(ServerJsonEncoder, self).default(obj)
            
            
