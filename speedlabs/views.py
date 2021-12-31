from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .helper import *
from .utils import error_handling
from .api_mapping import api_mapping



@api_view(['GET', 'POST'])
def MyView(request):

    '''
    This functions check if necessary arguements are present 
    in the request data object and then it calls a suitable 
    function according to the name mentioned in the api key
    '''
    #check basic error handling
    isError, output = error_handling(request)
    response = Response()
    #if error return response with error = True
    if isError:
        return output
    ans = output.data
    #try calling the function with the api
    flag = False
    if 1 :
        error, err_desc, result = api_mapping[request.data['api']](request)
        if not error:
            ans['result'] = result
        else:
            ans['result'] = {}
            ans['result']['message'] = err_desc
            ans['result']['error'] = "true"
            flag = True
    #api entered is wrong so return a error
    # except Exception as e:
    #     print(e)
    #     ans['result'] = {}
    #     ans['result']['error'] = "true"
    #     ans['result']['message'] = "Wrong Api"
    #     flag = True
    
    if flag:
        status_code = status.HTTP_400_BAD_REQUEST
    else:
        status_code = status.HTTP_200_OK
    response.data = ans
    response.status_code = status_code
    return response
            


