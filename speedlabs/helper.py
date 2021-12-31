from funcs2 import df_course_question_subject, df_course_ksc, \
df_course, df_video3, check, question_accuracy_plot, get_time_df2, df_user, df_user_session, get_user_logged_in
import plotly.express as px
import plotly
import string
import base64
import json
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt






def question_subset(request):
    
    
    """
    Args: request object that is coming to the endpoint
    Return: PlotlyData, PlotlyLayout, base64PNG, base64SVG
    Type of plot: Question Type districution i.e. their numbers across subject and course
    Working: It takes request object and first it check if subject and course are present ,
            if both are not present then we return error , else we return the data 
            across course and subject both and individually as well
    
    """
    
    returns = request.data['returns']
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    comments =  "This plots requires either course, subject or both as arguements, \
            it then subsets the data on course or subject selected \
            and tells us about the number of each type of questions i.e. Objective, Subjective ,etc. \
            with the selected course and subject"
    
    #try to get coursename and subjectname if present
    try:
        course = request.data['data']['course']
    except:
        course = ''
    try:
        subject = request.data['data']['subject']
    except:
        subject = ''
    output = {}
    data1 = []
    layout = {}
    temp = 0
    if course == '' and subject == '':
        return (True, 'Course and subject both cannot be empty for api question subset', output)
    if course != '' and subject != '':
        df_final = df_course_question_subject[(df_course_question_subject.COURSENAME == course) & (df_course_question_subject.SubjectName == subject)]
        data = dict(df_final.QuestionType.value_counts()) 
        x = list(data.keys())
        y = list(data.values())
        temp += 1
        output['course and subject'] = {'x': x, 'y': y}
        fig = px.pie(values=y, names=x)
        # Export byte object
        # fig = fig.to_json()
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        # decodeit = open('sample.png', 'wb')
        # decodeit.write(base64.b64decode((png_base64)))
        # decodeit.close()
        # print(png_base64)
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
        # data1.append({'values': y, 'labels':x, 'type': 'pie',  'name': 'course and subject', 'hoverinfo': 'label+percent+name', 'hole':.4, 'text':'course and subject'})
        
    elif  course != '':
        df_final = df_course_question_subject[(df_course_question_subject.COURSENAME == course)]
        data = dict(df_final.QuestionType.value_counts()) 
        x = list(data.keys())
        y = list(data.values())
        temp += 1
        output['course'] = {'x': x, 'y': y}
        fig = px.pie(values=y, names=x)
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        # print(png_base64)
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
        # data1.append({'values': y, 'labels':x, 'type': 'pie',   'name': 'course', 'hoverinfo': 'label+percent+name', 'hole':.4, 'text':'course'})
    
    elif subject != '' :
        df_final = df_course_question_subject[(df_course_question_subject.SubjectName == subject)]
        data = dict(df_final.QuestionType.value_counts()) 
        x = list(data.keys())
        y = list(data.values())
        temp += 1
        data1.append({'values': y, 'labels':x, 'type': 'pie',  'name': 'subject', 'hoverinfo': 'label+percent+name',  'hole':.4, 'text':'subject'})
        output['subject'] = {'x': x, 'y': y}
        fig = px.pie(values=y, names=x)
        # Export byte object
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        # print(png_base64)
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
    
    
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
        
    if 'comments' in returns:
        temp['comments']  = comments
    
        
    return (False, '', temp)

def question_accuracy(request):
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    returns = request.data['returns']
    comments = "This plots requires either course, subject or both as arguements, \
            it then subsets the data on course or subject selected \
            and tells us about the mean question type  accuracy on each type of questions i.e. Objective, Subjective ,etc. \
            with the selected course and subject"
    
    
    try:
        course = request.data['data']['course']
    except:
        course = ''
        
    try:
        subject = request.data['data']['subject']
    except:
        subject = ''
        
    output = {}
    data1 = []
    layout = {}
    temp = 0

    if course == '' and subject == '':
        return (True, 'Course and subject both cannot be empty with api question accuracy', output)
    # output = {}
    if course != '' and subject != '':
        df_final = df_course_question_subject[(df_course_question_subject.COURSENAME == course) & (df_course_question_subject.SubjectName == subject)]
        data1 = df_final.groupby('QuestionType', as_index=False).agg(accuracy = ('_QuestionScore', 'mean'))
        output['course and subject'] = data1
        temp += 1
        fig = px.bar(data1, x='QuestionType', y='accuracy',
             hover_data=['QuestionType'], color='accuracy',
              height=400, title=f'It tells QuestionScore mean values i.e average score across different score types with subject {subject} and course {course}')
        
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
        # data1.append({'values': y, 'labels':x, 'type': 'pie',  'name': 'course and subject', 'hoverinfo': 'label+percent+name', 'hole':.4, 'text':'course and subject'})
    elif  course != '':
        df_final1 = df_course_question_subject[(df_course_question_subject.COURSENAME == course)]
        data2 = df_final1.groupby('QuestionType', as_index=False).agg(accuracy = ('_QuestionScore', 'mean'))
        output['course'] = data2
        temp += 1
        fig = px.bar(data2, x='QuestionType', y='accuracy',
             hover_data=['QuestionType'], color='accuracy',
              height=400, title=f'It tells QuestionScore mean values i.e average score across different score types with subject {subject} and course {course}')
        
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
    
    elif subject != '':
        df_final2 = df_course_question_subject[ (df_course_question_subject.SubjectName == subject)]
        data3 = df_final2.groupby('QuestionType', as_index=False).agg(accuracy = ('_QuestionScore', 'mean'))
        output['subject'] = data3
        temp += 1
        fig = px.bar(data3, x='QuestionType', y='accuracy',
             hover_data=['QuestionType'], color='accuracy',
              height=400, title=f'It tells QuestionScore mean values i.e average score across different score types with subject {subject} and course {course}')
        
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
   
   
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
        
    if 'comments' in returns:
        temp['comments'] = comments
    
        
    return (False, '', temp)

# text_analyze
def text_analyze(request):
    error = False
    error_desc = ''
    
    data = request.data
    #check if data is in right format
    output = {}
    print(type(data['data']))
    print(type({}))
    if type(data['data']) != type({}):
        print('here inside checking type')
        error = True
        error_desc = 'data key is not of json type'
        output['error'] = "true"
        output['message'] = error_desc
        
        return (error, error_desc, output)
        
    if 'message' not in data['data'].keys():
        error = True
        error_desc = 'there is not key as message in data key'
        output['error'] = "true"
        output['message'] = error_desc
        
        return (error, error_desc, output)
    
    text = data['data']['message']
    # output = {}
    result = {}

    #calculate number of words
    print('checking varioud text properties')
    print(data['returns'])
    print('characters' in data['returns'])
    if 'characters' in data['returns']:
     
        temp = 0
    # define all letters
        l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in text:
            if i in l:
                temp += 1
        result['characters'] = temp
    
    #calculates number of punctuations
    if 'punctuations' in data['returns']:
        temp = 0
        for i in text:
            if i in string.punctuation:
                temp += 1
        result['punctuations'] = temp
    
    if 'whitespaces' in data['returns']:
        temp = 0
        for i in text:
            if i == ' ':
                temp += 1
        result['whitespaces'] = temp
    
    return (error, error_desc, result)


def ksc(request):
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    returns = request.data['returns']
    error = False
    err_desc = ''
    comments = "This plot doesn't require any kind of arguement, it tells us the total  \
            number of KSC with all courses and subjects"
    
    output = {}
    
    isCourse = 'course' in request.data['data'].keys()
    isSubject = 'subject' in request.data['data'].keys()
    
    if not isCourse and not isSubject:
       error = True
       err_desc = 'enter either course or subject, it cannot be empty'
       return (error, err_desc, output)
   
    if isCourse and isSubject:
       error = True
       err_desc = 'enter just one course or subject for ksc plotting'
       return (error, err_desc, output)
   
    elif isCourse:
        df_course_ksc_temp = df_course_ksc.groupby(['courseid'], as_index=False).agg(ksc_count=('courseid', 'count'))
        df_course_ksc_temp = pd.merge(df_course_ksc_temp, df_course, left_on='courseid', right_on='COURSEID', how='left')
        data = df_course_ksc_temp
        fig = px.bar(df_course_ksc_temp, y='ksc_count', x='COURSENAME', text='ksc_count', title='ksc count with course')
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8)
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
    
    else:
        data = df_course_question_subject.groupby('SubjectName', as_index=False).agg(ksc_count=('SubjectName', 'count'))
        fig = px.bar(data, y='ksc_count', x='SubjectName', text='ksc_count', title='ksc count with subject')
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8)
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
    
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
        
    if 'comments' in returns:
        temp['comments'] = comments
    
        
    return (False, '', temp)
    
        
def videos(request):
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    returns = request.data['returns']
    error = False
    err_desc = ''
    comments = "This plots requires either course or subject, \
            it then subsets the data on course or subject selected \
            and tells us about the number of videos coursewise with subject selected \
            and subjectwise with course selected"
    
    output = {}
     
    try:
        course = request.data['data']['course']
    except:
        course = ''
        
    try:
        subject = request.data['data']['subject']
    except:
        subject = ''
    
    isCourse = 'course' in request.data['data'].keys()
    isSubject = 'subject' in request.data['data'].keys()
    if isCourse and course not in list(df_video3.coursename.values):
        error = True
        err_desc = 'this course do not have any videos try a new course'
        return (error, err_desc, output)
    elif isSubject and subject not in list(df_video3.subjectname.values):
        error = True
        err_desc = 'this subject do not have any videos try a new subject'
        return (error, err_desc, output)
    if not isCourse and not isSubject:
        error = True
        err_desc = 'enter either course or subject, it cannot be empty'
        return (error, err_desc, output)
   
    if isCourse and isSubject:
       error = True
       err_desc = 'enter just one course or subject for number of videos plotting plotting'
       return (error, err_desc, output)
    
   
    elif isCourse:
        df_video_temp = df_video3[(df_video3.coursename == course)]
        df_video_temp = df_video_temp.groupby(['subjectname'], as_index=False).agg(video_count=('subjectname', 'count'))
        fig = px.bar(df_video_temp, x='subjectname', y='video_count', title=f'No. of videos by subject with course- {course}',
        hover_data=['subjectname', 'video_count'], color='video_count', height=400)
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
        
    else:
        df_video_temp = df_video3[(df_video3.subjectname == subject)]
        df_video_temp = df_video_temp.groupby(['coursename'], as_index=False).agg(video_count=('coursename', 'count'))
        fig = px.bar(df_video_temp, x='coursename', y='video_count', title=f'No. of videos by course with subject- {subject}',
        hover_data=['coursename', 'video_count'], color='video_count', height=400)      
        img_bytes_png = plotly.io.to_image(fig, format="png")
        img_bytes_svg = plotly.io.to_image(fig, format="svg")
        png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
        svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
        base64PNG = str(png_base64)
        base64SVG = str(svg_base64)
        fig = fig.to_json()
        data = json.loads(fig)
        plotlyData = data["data"]
        plotlyLayout = data["layout"]
        
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
        
    if 'comments' in returns:
        temp['comments'] = comments
    
        
    return (False, '', temp)


def question_heatmap(request):
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    returns = request.data['returns']
    error = False
    err_desc = ''
    comments = "This plots requires either courseType and questionType, \
             courseType is a prefix which represents school class like \
             6 class , 7/8 class , others(JEE, NEET) and questioType \
            represents  type of question objective, subjective, etc"
    
       
    try:
        courseType = request.data['data']['coursetype']
    except:
        courseType = ''
        
    try:
        questionType = request.data['data']['questiontype']
    except:
        questionType = ''
    
    if courseType == '' and questionType == '':
        error = True
        err_desc = 'you have to enter questionType and courseType so try again'
        return (error, err_desc, {})
    
    QuestionType = questionType
    regex = f'({courseType})*'
    compiled = re.compile(regex)
    df_ = df_course_question_subject.copy()
    if courseType != "Others":
        df_['new'] = df_.COURSENAME.apply(lambda x: False if re.search(compiled, x).group() == '' else True)
    else: 
       df_['new'] = df_.COURSENAME.apply(lambda x: check(x))
    df_temp = df_[(df_.new == True) & (df_.QuestionType == QuestionType)]
    df_temp = df_temp.groupby(['SubjectName', 'COURSENAME'], as_index=True).agg(questions_count=('QuestionId', 'count'))

    df_temp['questions_count'] = df_temp['questions_count']/100
    df_temp = df_temp.unstack(level='COURSENAME')
    df_temp.columns = df_temp.columns.droplevel()
    sns.set(font_scale=2.5)
    # sns.heatmap(df_temp, vmin=0, vmax=450, cmap = 'YlGnBu', linewidth=2.5, linecolor='w', annot = True, fmt = '.0f', annot_kws={'fontsize':22})
    fig = px.imshow(df_temp, zmin=0, zmax=450, facet_col_spacing=0.1, facet_row_spacing=0.1, aspect='auto', color_continuous_scale= "ylgnbu")
    img_bytes_png = plotly.io.to_image(fig, format="png")
    img_bytes_svg = plotly.io.to_image(fig, format="svg")
    png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
    svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
    base64PNG = str(png_base64)
    base64SVG = str(svg_base64)
    fig = fig.to_json()
    data = json.loads(fig)
    plotlyData = data["data"]
    plotlyLayout = data["layout"]
    
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
        
    if 'comments' in returns:
        temp['comments'] = comments
    
        
    return (False, '', temp)


def question_heatmap_total(request):
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    returns = request.data['returns']
    error = False
    err_desc = ''
    comments = "This plot doesn't require any arguement and just plot the total number of questions \
        as heatmap with all the courses and subjects that are present in the database"
    
    
    df_temp = df_course_question_subject.groupby(['SubjectName', 'COURSENAME'], as_index=True).agg(questions_count=('QuestionId', 'count'))
    df_temp['questions_count'] = df_temp['questions_count']/100
    df_temp2 = df_temp.unstack(level='COURSENAME')
    df_temp2.columns = df_temp2.columns.droplevel()
    fig = px.imshow(df_temp2, zmin=0, zmax=450, facet_col_spacing=0.1, facet_row_spacing=0.1, aspect='auto', color_continuous_scale= "ylgnbu")
    img_bytes_png = plotly.io.to_image(fig, format="png")
    img_bytes_svg = plotly.io.to_image(fig, format="svg")
    png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
    svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
    base64PNG = str(png_base64)
    base64SVG = str(svg_base64)
    fig = fig.to_json()
    data = json.loads(fig)
    plotlyData = data["data"]
    plotlyLayout = data["layout"]
    
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
    
    if 'comments' in returns:
        temp['comments'] = comments
    
        
    return (False, '', temp)

def question_hist(request):
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    returns = request.data['returns']
    error = False
    err_desc = ''
    comments =  "This plots requires both course and subject as arguements, \
            it then subsets the data on course and subject selected \
           and plots the question accuracy histogram with that course and subject"
    
       
    try:
        course = request.data['data']['course']
    except:
        course = ''
        
    try:
        subject = request.data['data']['subject']
    except:
        subject = ''
    
    if course == '' or subject == '':
        error = True
        err_desc = 'you must enter both subject and course to see question accuracy'
    
    err, df_temp = question_accuracy_plot(course, subject)
    if err:
        return (True, df_temp, {})

    fig = px.histogram(df_temp, x="QuestionAccuracy",
                   title=f'Histogram of QuestionAccuracy with course {course} and {subject}',
                   opacity=0.8,
                   color_discrete_sequence=['indianred'] # color of histogram bars
                   )
    img_bytes_png = plotly.io.to_image(fig, format="png")
    img_bytes_svg = plotly.io.to_image(fig, format="svg")
    png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
    svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
    base64PNG = str(png_base64)
    base64SVG = str(svg_base64)
    fig = fig.to_json()
    data = json.loads(fig)
    plotlyData = data["data"]
    plotlyLayout = data["layout"]
    
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
        
    if 'comments' in returns:
        temp['comments'] = comments
    
        
    return (False, '', temp)


def login_count(request):
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    returns = request.data['returns']
    error = False
    err_desc = ''
    comments: "This plots requires either start_date, end_date and course\
        and  and plots the login count histogram with the attributes selected"
    
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
    
    try:
        course = request.data['data']['course']
    
    except Exception as e:
        print(e)
        course = ''
        
    if start_date == '' or end_date == '' or course == '':
        error = True
        err_desc = 'either course or start_date or end_date is not mentioned'
        return (error, err_desc, {})

    df = get_time_df2(start_date, end_date)
    df = df[df.COURSENAME == course]
    fig = px.histogram(df, x="login_count", nbins=20, title=f'login count for session time more that 10 min between {start_date} and {end_date} for course{course}')
    img_bytes_png = plotly.io.to_image(fig, format="png")
    img_bytes_svg = plotly.io.to_image(fig, format="svg")
    png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
    svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
    base64PNG = str(png_base64)
    base64SVG = str(svg_base64)
    fig = fig.to_json()
    data = json.loads(fig)
    plotlyData = data["data"]
    plotlyLayout = data["layout"]
    
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
    
    if 'comments' in returns:
        temp['comments'] = comments
    
        
    return (False, '', temp)


def session_time(request):
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    returns = request.data['returns']
    error = False
    err_desc = ''
    comments = "This plots requires either start_date, end_date and course\
        and  and plots the session login time histogram with the attributes selected"
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
    
    try:
        course = request.data['data']['course']
    
    except Exception as e:
        print(e)
        course = ''
        
    if start_date == '' or end_date == '' or course == '':
        error = True
        err_desc = 'either course or start_date or end_date is not mentioned'
        return (error, err_desc, {})

    df = get_time_df2(start_date, end_date)
    df = df[df.COURSENAME == course]
    data = df.session_login_time/60
    fig = px.histogram(data, x="session_login_time", title=f'session login time for more time more that 10 min  for course {course}')
    img_bytes_png = plotly.io.to_image(fig, format="png")
    img_bytes_svg = plotly.io.to_image(fig, format="svg")
    png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
    svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
    base64PNG = str(png_base64)
    base64SVG = str(svg_base64)
    fig = fig.to_json()
    data = json.loads(fig)
    plotlyData = data["data"]
    plotlyLayout = data["layout"]
    
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
        
    if 'comments' in returns:
        temp['comments'] = comments
    
        
    return (False, '', temp)

def last_logged_in(request):
    base64PNG = ""
    base64SVG = ""
    plotlyData = {}
    plotlyLayout = {}
    returns = request.data['returns']
    error = False
    err_desc = ''
    comments: "This plots requires either start_date, end_date and Frequence(Daily as D, Monthly as M and Weekly as W)\
         and plots the number of lastloggedin on a frequency selected between start_date and end_date"
    
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
    
    try:
        freq = request.data['data']['frequency']
    
    except Exception as e:
        print(e)
        freq = ''
        
    if start_date == '' or end_date == '':
        error = True
        err_desc = 'either start_date or end_date is not mentioned'
        return (error, err_desc, {})
    if freq == '':
        freq = 'M'
    freq_map = {
        'M': 'Monthly',
        'W': 'Weekly',
        'D': 'Daily',
        'Y': 'Yearly'
    }
    df = get_user_logged_in(start_date, end_date, freq)
    fig = px.line(df, x='lastloggedin', y='inactive_count', markers=True, title=f'It represents {freq_map[freq]} trend how many students becomes inactive')
    img_bytes_png = plotly.io.to_image(fig, format="png")
    img_bytes_svg = plotly.io.to_image(fig, format="svg")
    png_base64 = base64.b64encode(img_bytes_png).decode('ascii')
    svg_base64 = base64.b64encode(img_bytes_svg).decode('ascii')
    base64PNG = str(png_base64)
    base64SVG = str(svg_base64)
    fig = fig.to_json()
    data = json.loads(fig)
    plotlyData = data["data"]
    plotlyLayout = data["layout"]
    
    result = {
        'plotlyData': plotlyData,
        'plotlyLayout': plotlyLayout,
        'base64SVG': base64SVG,
        'base64PNG': base64PNG,
        'comments': comments
    }
    if len(returns) == 0:
        return (False, '', result)
    
    temp = {}
    if 'plotlyData' in returns:
        temp['plotlyData'] = plotlyData
        
    if 'plotlyLayout' in returns:
        temp['plotlyLayout'] = plotlyLayout
    
    if 'base64SVG' in returns:
        temp['base64SVG'] = base64SVG
    
    if 'base64PNG' in returns:
        temp['base64PNG'] = base64PNG
        
    if 'comments' in returns:
        temp['comments'] = comments
    
        
    return (False, '', temp)


# def practice_usage_session_time_range(request):
#     try:
#         start_date = request.data['data']['start_date']
#     except Exception as e:
#         print(e)
#         start_date = ''
    
#     try:
#         end_date = request.data['data']['end_date']
#     except Exception as e:
#         print(e)
#         end_date = ''
    
#     if start_date == '' or end_date == '':
#         error = True
#         err_desc = 'either start_date or end_date is not mentioned'
#         return (error, err_desc, {})
    
#     start_date = datetime.fromisoformat(start_date)
#     end_date = datetime.fromisoformat(end_date)
    
#     practice_session = Practice_Session_Usage(conn, start_date, end_date)
#     result = practice_session.practice_session_time_histogram_range_split()
#     if len(returns) == 0:
#         return (False, '', result)
    
#     temp = {}
#     if 'plotlyData' in returns:
#         temp['plotlyData'] = result['plotlyData']
        
#     if 'plotlyLayout' in returns:
#         temp['plotlyLayout'] = result['plotlyLayout']
    
#     if 'base64SVG' in returns:
#         temp['base64SVG'] = result['base64SVG']
    
#     if 'base64PNG' in returns:
#         temp['base64PNG'] = result['base64PNG']
        
#     if 'comments' in returns:
#         temp['comments'] = result['comments']
    
        
#     return (False, '', temp)


# def practice_usage_session_time_logscale(request):
#     try:
#         start_date = request.data['data']['start_date']
#     except Exception as e:
#         print(e)
#         start_date = ''
    
#     try:
#         end_date = request.data['data']['end_date']
#     except Exception as e:
#         print(e)
#         end_date = ''
    
#     if start_date == '' or end_date == '':
#         error = True
#         err_desc = 'either start_date or end_date is not mentioned'
#         return (error, err_desc, {})
    
#     start_date = datetime.fromisoformat(start_date)
#     end_date = datetime.fromisoformat(end_date)
    
#     practice_session = Practice_Session_Usage(conn, start_date, end_date)
#     result = practice_session.practice_session_time_histogram_logscale()
#     if len(returns) == 0:
#         return (False, '', result)
    
#     temp = {}
#     if 'plotlyData' in returns:
#         temp['plotlyData'] = result['plotlyData']
        
#     if 'plotlyLayout' in returns:
#         temp['plotlyLayout'] = result['plotlyLayout']
    
#     if 'base64SVG' in returns:
#         temp['base64SVG'] = result['base64SVG']
    
#     if 'base64PNG' in returns:
#         temp['base64PNG'] = result['base64PNG']
        
#     if 'comments' in returns:
#         temp['comments'] = result['comments']
    
        
#     return (False, '', temp)





# def  practice_usage_session_heatmap(request):
#     try:
#         start_date = request.data['data']['start_date']
#     except Exception as e:
#         print(e)
#         start_date = ''
    
#     try:
#         end_date = request.data['data']['end_date']
#     except Exception as e:
#         print(e)
#         end_date = ''
    
#     if start_date == '' or end_date == '':
#         error = True
#         err_desc = 'either start_date or end_date is not mentioned'
#         return (error, err_desc, {})
    
#     start_date = datetime.fromisoformat(start_date)
#     end_date = datetime.fromisoformat(end_date)
    
#     practice_session = Practice_Session_Usage(conn, start_date, end_date)
#     result = practice_session.cwsw_practice_session_heatmap()
#     if len(returns) == 0:
#         return (False, '', result)
    
#     temp = {}
#     if 'plotlyData' in returns:
#         temp['plotlyData'] = result['plotlyData']
        
#     if 'plotlyLayout' in returns:
#         temp['plotlyLayout'] = result['plotlyLayout']
    
#     if 'base64SVG' in returns:
#         temp['base64SVG'] = result['base64SVG']
    
#     if 'base64PNG' in returns:
#         temp['base64PNG'] = result['base64PNG']
        
#     if 'comments' in returns:
#         temp['comments'] = result['comments']
    
        
#     return (False, '', temp)


# def practice_usage_session_time_heatmap(request):
#     try:
#         start_date = request.data['data']['start_date']
#     except Exception as e:
#         print(e)
#         start_date = ''
    
#     try:
#         end_date = request.data['data']['end_date']
#     except Exception as e:
#         print(e)
#         end_date = ''
    
#     if start_date == '' or end_date == '':
#         error = True
#         err_desc = 'either start_date or end_date is not mentioned'
#         return (error, err_desc, {})
    
#     start_date = datetime.fromisoformat(start_date)
#     end_date = datetime.fromisoformat(end_date)
    
#     practice_session = Practice_Session_Usage(conn, start_date, end_date)
#     result = practice_session.cwsw_avg_practice_session_time_heatmap()
#     if len(returns) == 0:
#         return (False, '', result)
    
#     temp = {}
#     if 'plotlyData' in returns:
#         temp['plotlyData'] = result['plotlyData']
        
#     if 'plotlyLayout' in returns:
#         temp['plotlyLayout'] = result['plotlyLayout']
    
#     if 'base64SVG' in returns:
#         temp['base64SVG'] = result['base64SVG']
    
#     if 'base64PNG' in returns:
#         temp['base64PNG'] = result['base64PNG']
        
#     if 'comments' in returns:
#         temp['comments'] = result['comments']
    
        
#     return (False, '', temp)



# def practice_usage_questions_used_heatmap(request):
#     try:
#         start_date = request.data['data']['start_date']
#     except Exception as e:
#         print(e)
#         start_date = ''
    
#     try:
#         end_date = request.data['data']['end_date']
#     except Exception as e:
#         print(e)
#         end_date = ''
    
#     if start_date == '' or end_date == '':
#         error = True
#         err_desc = 'either start_date or end_date is not mentioned'
#         return (error, err_desc, {})
    
#     start_date = datetime.fromisoformat(start_date)
#     end_date = datetime.fromisoformat(end_date)
    
#     practice_session = Practice_Session_Usage(conn, start_date, end_date)
#     result = practice_session.cwsw_questions_used_heatmap()
#     if len(returns) == 0:
#         return (False, '', result)
    
#     temp = {}
#     if 'plotlyData' in returns:
#         temp['plotlyData'] = result['plotlyData']
        
#     if 'plotlyLayout' in returns:
#         temp['plotlyLayout'] = result['plotlyLayout']
    
#     if 'base64SVG' in returns:
#         temp['base64SVG'] = result['base64SVG']
    
#     if 'base64PNG' in returns:
#         temp['base64PNG'] = result['base64PNG']
        
#     if 'comments' in returns:
#         temp['comments'] = result['comments']
    
        
#     return (False, '', temp)


# def practice_usage_unique_questions_used_heatmap(request):
#     try:
#         start_date = request.data['data']['start_date']
#     except Exception as e:
#         print(e)
#         start_date = ''
    
#     try:
#         end_date = request.data['data']['end_date']
#     except Exception as e:
#         print(e)
#         end_date = ''
    
#     if start_date == '' or end_date == '':
#         error = True
#         err_desc = 'either start_date or end_date is not mentioned'
#         return (error, err_desc, {})
    
#     start_date = datetime.fromisoformat(start_date)
#     end_date = datetime.fromisoformat(end_date)
    
#     practice_session = Practice_Session_Usage(conn, start_date, end_date)
#     result = practice_session.cwsw_unique_questions_used_heatmap()
#     if len(returns) == 0:
#         return (False, '', result)
    
#     temp = {}
#     if 'plotlyData' in returns:
#         temp['plotlyData'] = result['plotlyData']
        
#     if 'plotlyLayout' in returns:
#         temp['plotlyLayout'] = result['plotlyLayout']
    
#     if 'base64SVG' in returns:
#         temp['base64SVG'] = result['base64SVG']
    
#     if 'base64PNG' in returns:
#         temp['base64PNG'] = result['base64PNG']
        
#     if 'comments' in returns:
#         temp['comments'] = result['comments']
    
        
#     return (False, '', temp)




# def practice_usage_unique_users_heatmap(request):
#     try:
#         start_date = request.data['data']['start_date']
#     except Exception as e:
#         print(e)
#         start_date = ''
    
#     try:
#         end_date = request.data['data']['end_date']
#     except Exception as e:
#         print(e)
#         end_date = ''
    
#     if start_date == '' or end_date == '':
#         error = True
#         err_desc = 'either start_date or end_date is not mentioned'
#         return (error, err_desc, {})
    
#     start_date = datetime.fromisoformat(start_date)
#     end_date = datetime.fromisoformat(end_date)
    
#     practice_session = Practice_Session_Usage(conn, start_date, end_date)
#     result = practice_session.cwsw_unique_users_heatmap()
#     if len(returns) == 0:
#         return (False, '', result)
    
#     temp = {}
#     if 'plotlyData' in returns:
#         temp['plotlyData'] = result['plotlyData']
        
#     if 'plotlyLayout' in returns:
#         temp['plotlyLayout'] = result['plotlyLayout']
    
#     if 'base64SVG' in returns:
#         temp['base64SVG'] = result['base64SVG']
    
#     if 'base64PNG' in returns:
#         temp['base64PNG'] = result['base64PNG']
        
#     if 'comments' in returns:
#         temp['comments'] = result['comments']
    
        
#     return (False, '', temp)


# def practice_usage_total_time_usage_heatmap(request):
#     try:
#         start_date = request.data['data']['start_date']
#     except Exception as e:
#         print(e)
#         start_date = ''
    
#     try:
#         end_date = request.data['data']['end_date']
#     except Exception as e:
#         print(e)
#         end_date = ''
    
#     if start_date == '' or end_date == '':
#         error = True
#         err_desc = 'either start_date or end_date is not mentioned'
#         return (error, err_desc, {})
    
#     start_date = datetime.fromisoformat(start_date)
#     end_date = datetime.fromisoformat(end_date)
    
#     practice_session = Practice_Session_Usage(conn, start_date, end_date)
#     result = practice_session.cwsw_total_time_spent_heatmap()
#     if len(returns) == 0:
#         return (False, '', result)
    
#     temp = {}
#     if 'plotlyData' in returns:
#         temp['plotlyData'] = result['plotlyData']
        
#     if 'plotlyLayout' in returns:
#         temp['plotlyLayout'] = result['plotlyLayout']
    
#     if 'base64SVG' in returns:
#         temp['base64SVG'] = result['base64SVG']
    
#     if 'base64PNG' in returns:
#         temp['base64PNG'] = result['base64PNG']
        
#     if 'comments' in returns:
#         temp['comments'] = result['comments']
    
        
#     return (False, '', temp)



# def questions_per_practice_session_heatmap(request):
#     try:
#         start_date = request.data['data']['start_date']
#     except Exception as e:
#         print(e)
#         start_date = ''
    
#     try:
#         end_date = request.data['data']['end_date']
#     except Exception as e:
#         print(e)
#         end_date = ''
    
#     if start_date == '' or end_date == '':
#         error = True
#         err_desc = 'either start_date or end_date is not mentioned'
#         return (error, err_desc, {})
    
#     start_date = datetime.fromisoformat(start_date)
#     end_date = datetime.fromisoformat(end_date)
    
#     practice_session = Practice_Session_Usage(conn, start_date, end_date)
#     result = practice_session.cwsw_questions_per_practice_session_heatmap()
#     if len(returns) == 0:
#         return (False, '', result)
    
#     temp = {}
#     if 'plotlyData' in returns:
#         temp['plotlyData'] = result['plotlyData']
        
#     if 'plotlyLayout' in returns:
#         temp['plotlyLayout'] = result['plotlyLayout']
    
#     if 'base64SVG' in returns:
#         temp['base64SVG'] = result['base64SVG']
    
#     if 'base64PNG' in returns:
#         temp['base64PNG'] = result['base64PNG']
        
#     if 'comments' in returns:
#         temp['comments'] = result['comments']
    
        
#     return (False, '', temp)

