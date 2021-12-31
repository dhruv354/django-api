
import string
import base64
import json
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from companion import  Learn_Usage
from datetime import datetime


# print (datetime.fromisoformat(date_string))
from connector import connect_default_via_pymssql
conn = connect_default_via_pymssql()

def  learn_test_per_user_course(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.coursewise_analysis_1()
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


def  learn_test_course(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.coursewise_analysis_2()
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





def  learn_test_time_per_user_course(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.coursewise_analysis_3()
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


def  learn_test_per_user_subject(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.subjectwise_analysis_1()
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


def  learn_test_subject(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.subjectwise_analysis_2()
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





def  learn_test_time_per_user_subject(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.subjectwise_analysis_3()
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





def  learn_affiliation_analysis(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.affiliationwise_analysis()
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





def  learn_daily_test_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.daily_trend_1()
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





def daily_learn_test(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.daily_trend_2()
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





def  learn_daily_test_time_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.daily_trend_3()
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






def  learn_weekly_test_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.weekly_trend_1()
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





def weekly_learn_test(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.weekly_trend_2()
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





def  learn_weekly_test_time_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.weekly_trend_3()
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






def  learn_monthly_test_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.monthly_trend_1()
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





def monthly_learn_test(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.monthly_trend_2()
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





def  learn_monthly_test_time_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.monthly_trend_3()
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






def  learn_yearly_test_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.yearly_trend_1()
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





def yearly_learn_test(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.yearly_trend_2()
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





def  learn_yearly_test_time_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.yearly_trend_3()
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






def  learn_quarterly_test_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.quarterly_trend_1()
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





def quarterly_learn_test(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.quarterly_trend_2()
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





def  learn_quarterly_test_time_per_user(request):
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
    
    practice_session =  Learn_Usage(conn, start_date, end_date)
    result = practice_session.quarterly_trend_3()
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









