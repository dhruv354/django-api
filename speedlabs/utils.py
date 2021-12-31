from .helper import *
from rest_framework.response import Response
from rest_framework import status
from .api_mapping import api_mapping


def error_handling(request):
    output = {}
    output['result'] = {}
    output['result']['message'] = []
    if 'apikey' not in request.data.keys():
        output['result']['message'].append('api key is missing')
    else:
        output['apikey'] = request.data['apikey']
    if 'apikey' in request.data.keys() and type(request.data['apikey']) != type(''):
        output['result']['message'].append('api type should be string')
    
        
    if 'api' not in request.data.keys():
        output['result']['message'].append('api is missing')
    else:
        output['api'] = request.data['api']
    
    if 'data' not in request.data.keys():
        output['result']['message'].append('data is missing')
    else:
        output['data'] = request.data['data']
        
    if 'returns' not in request.data.keys():
        output['result']['message'].append('returns key is missing')
    else:
        output['returns'] = request.data['returns']
        
    response = Response()
            
    
    if len(output['result']['message']) != 0:
        if 'api key is missing'  in output['result']['message']:
            output['result']['error'] = "true"
            response.data = output
            response.status_code = status.HTTP_401_UNAUTHORIZED
        else:
            output['result']['error'] = "true"
            response.data = output
            response.status_code = status.HTTP_400_BAD_REQUEST
        return (True, response)
           
    result = {}
    result['apikey'] = request.data['apikey']
    result['api'] = request.data['api']
    result['data'] = request.data['data']
    response.data = result
    return (False, response)


