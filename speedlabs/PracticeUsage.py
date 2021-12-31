

import string
import base64
import json
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from companion import Practice_Session_Usage
from datetime import datetime


# print (datetime.fromisoformat(date_string))
from connector import connect_default_via_pymssql
conn = connect_default_via_pymssql()

def practice_usage_session_time_range(request):
    returns = request.data['returns']
    try:
        start_date = request.data['data']['start_date']
    except Exception as e:
        print(e)
        start_date = ''
    
    try:
        end_date = request.data['data']['end_date']
    except Exception as e:
        print(e)
        end_date = ''
    
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    practice_session = Practice_Session_Usage(conn, start_date, end_date)
    result = practice_session.practice_session_time_histogram_range_split()
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = result['plotlyData']
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = result['plotlyLayout']
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = result['base64SVG']
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = result['base64PNG']
        
    if 'comments' in returns:
        temp['comments'] = result['comments']
    
        
    return (False, '', temp)


def practice_usage_session_time_logscale(request):
    returns = request.data['returns']
    try:
        start_date = request.data['data']['start_date']
    except Exception as e:
        print(e)
        start_date = ''
    
    try:
        end_date = request.data['data']['end_date']
    except Exception as e:
        print(e)
        end_date = ''
    
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    practice_session = Practice_Session_Usage(conn, start_date, end_date)
    result = practice_session.practice_session_time_histogram_logscale()
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = result['plotlyData']
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = result['plotlyLayout']
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = result['base64SVG']
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = result['base64PNG']
        
    if 'comments' in returns:
        temp['comments'] = result['comments']
    
        
    return (False, '', temp)





def  practice_usage_session_heatmap(request):
    returns = request.data['returns']
    try:
        start_date = request.data['data']['start_date']
    except Exception as e:
        print(e)
        start_date = ''
    
    try:
        end_date = request.data['data']['end_date']
    except Exception as e:
        print(e)
        end_date = ''
    
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    practice_session = Practice_Session_Usage(conn, start_date, end_date)
    result = practice_session.cwsw_practice_session_heatmap()
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = result['plotlyData']
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = result['plotlyLayout']
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = result['base64SVG']
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = result['base64PNG']
        
    if 'comments' in returns:
        temp['comments'] = result['comments']
    
        
    return (False, '', temp)


def practice_usage_session_time_heatmap(request):
    returns = request.data['returns']
    try:
        start_date = request.data['data']['start_date']
    except Exception as e:
        print(e)
        start_date = ''
    
    try:
        end_date = request.data['data']['end_date']
    except Exception as e:
        print(e)
        end_date = ''
    
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    practice_session = Practice_Session_Usage(conn, start_date, end_date)
    result = practice_session.cwsw_avg_practice_session_time_heatmap()
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = result['plotlyData']
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = result['plotlyLayout']
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = result['base64SVG']
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = result['base64PNG']
        
    if 'comments' in returns:
        temp['comments'] = result['comments']
    
        
    return (False, '', temp)



def practice_usage_questions_used_heatmap(request):
    returns = request.data['returns']
    try:
        start_date = request.data['data']['start_date']
    except Exception as e:
        print(e)
        start_date = ''
    
    try:
        end_date = request.data['data']['end_date']
    except Exception as e:
        print(e)
        end_date = ''
    
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    practice_session = Practice_Session_Usage(conn, start_date, end_date)
    result = practice_session.cwsw_questions_used_heatmap()
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = result['plotlyData']
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = result['plotlyLayout']
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = result['base64SVG']
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = result['base64PNG']
        
    if 'comments' in returns:
        temp['comments'] = result['comments']
    
        
    return (False, '', temp)


def practice_usage_unique_questions_used_heatmap(request):
    returns = request.data['returns']
    try:
        start_date = request.data['data']['start_date']
    except Exception as e:
        print(e)
        start_date = ''
    
    try:
        end_date = request.data['data']['end_date']
    except Exception as e:
        print(e)
        end_date = ''
    
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    practice_session = Practice_Session_Usage(conn, start_date, end_date)
    result = practice_session.cwsw_unique_questions_used_heatmap()
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = result['plotlyData']
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = result['plotlyLayout']
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = result['base64SVG']
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = result['base64PNG']
        
    if 'comments' in returns:
        temp['comments'] = result['comments']
    
        
    return (False, '', temp)




def practice_usage_unique_users_heatmap(request):
    returns = request.data['returns']
    try:
        start_date = request.data['data']['start_date']
    except Exception as e:
        print(e)
        start_date = ''
    
    try:
        end_date = request.data['data']['end_date']
    except Exception as e:
        print(e)
        end_date = ''
    
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    practice_session = Practice_Session_Usage(conn, start_date, end_date)
    result = practice_session.cwsw_unique_users_heatmap()
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = result['plotlyData']
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = result['plotlyLayout']
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = result['base64SVG']
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = result['base64PNG']
        
    if 'comments' in returns:
        temp['comments'] = result['comments']
    
        
    return (False, '', temp)


def practice_usage_total_time_usage_heatmap(request):
    returns = request.data['returns']
    try:
        start_date = request.data['data']['start_date']
    except Exception as e:
        print(e)
        start_date = ''
    
    try:
        end_date = request.data['data']['end_date']
    except Exception as e:
        print(e)
        end_date = ''
    
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    practice_session = Practice_Session_Usage(conn, start_date, end_date)
    result = practice_session.cwsw_total_time_spent_heatmap()
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = result['plotlyData']
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = result['plotlyLayout']
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = result['base64SVG']
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = result['base64PNG']
        
    if 'comments' in returns:
        temp['comments'] = result['comments']
    
        
    return (False, '', temp)



def questions_per_practice_session_heatmap(request):
    returns = request.data['returns']
    try:
        start_date = request.data['data']['start_date']
    except Exception as e:
        print(e)
        start_date = ''
    
    try:
        end_date = request.data['data']['end_date']
    except Exception as e:
        print(e)
        end_date = ''
    
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    practice_session = Practice_Session_Usage(conn, start_date, end_date)
    result = practice_session.cwsw_questions_per_practice_session_heatmap()
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = result['plotlyData']
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = result['plotlyLayout']
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = result['base64SVG']
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = result['base64PNG']
        
    if 'comments' in returns:
        temp['comments'] = result['comments']
    
        
    return (False, '', temp)

