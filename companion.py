import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pyodbc
import pymssql
from datetime import datetime
import ipywidgets as widgets
from IPython.display import display
from scipy import stats

# contains helping functions
from helper_vis import *
# contains functions to make connection with database
from connector import *
# contains functions to read data from database
from tableReader import *



################### class containing all functions for Assignment Usage ##################

class Assignment_Usage:
    def __init__(self, conn, start_date, end_date):
        self.conn = conn
        self.start_date = start_date
        self.end_date = end_date
        
        # Join all the tables containing data related to Assignments solved by users
        self.df_CSQE = read_exam_table(conn, start_date, end_date) # from tableReader.py
        self.df_CSQE = self.df_CSQE.dropna(subset=['TotalTimeTaken'])  # drop rows with NaN TotalTimeTaken 
        self.df_CSQE = self.df_CSQE.loc[self.df_CSQE['RoleId']==2]   # to consider only student data
        self.df_CSQE.reset_index(inplace = True)  # reset index
        self.df_CSQE = self.df_CSQE[((stats.zscore(self.df_CSQE['TotalTimeTaken']))<4)] # Removing the outliers
        print(f"Length of data is: {len(self.df_CSQE)}")
        display(self.df_CSQE.head(5))
        
        # copy course, subject, time-taken and examsessionid into a seperate dataframe
        self.dfw = self.df_CSQE[['CourseName', 'SubjectName', 'TotalTimeTaken', 'ExamSessionId']].copy()
        # Group the data by course & subject and get total time for exams & total sessions for all course & subject
        self.df_CSTA = self.dfw.groupby(['CourseName', 'SubjectName'], as_index = False).agg({'TotalTimeTaken': 'sum', 'ExamSessionId': 'nunique'})
        self.df_CSTA['TotalTimeTaken'] = self.df_CSTA['TotalTimeTaken']/60.0    # to convert time in minutes
        self.df_CSTA.rename(columns = {'ExamSessionId': 'TotalSession'}, inplace = True)  # rename the column to TotalSession
        self.df_CSTA['AvgSessionTime'] = self.df_CSTA['TotalTimeTaken']/self.df_CSTA['TotalSession'] # obtain average session time
        
        # copy the course, subject & question info into a seperate dataframe
        self.df_QDCS = self.df_CSQE[['QuestionId', 'CourseName', 'SubjectName']].copy()        
        self.df_QDCS['Unique_Questions'] = self.df_QDCS['QuestionId'].copy() # create a column for unique-questions
        self.df_QDCS['Total_Questions'] = self.df_QDCS['QuestionId'].copy()  # create a column for total-questions
        self.df_QDCS = self.df_QDCS.drop(['QuestionId'], axis = 1) # drop questionid column as required data is already copied in above two columns        
        # Group the data by course & subject and get total-questions & unique-questions used for all course & subject
        self.df_QDCS = self.df_QDCS.groupby(['CourseName', 'SubjectName'], as_index = False).agg({'Unique_Questions': 'nunique', 'Total_Questions': 'count'})
        self.df_QDCS['QuestionsPerSession'] = self.df_QDCS['Total_Questions']/self.df_CSTA['TotalSession']
        
        # copy the practice session time data into a dataframe
        self.df0 = self.df_CSQE[['ExamSessionId', 'TotalTimeTaken']].copy() 
        self.df0 = self.df0.groupby(['ExamSessionId'], as_index=False)['TotalTimeTaken'].sum()  # Group the data by ExamSessionId
        self.df0['TotalTimeTaken'] = self.df0['TotalTimeTaken']/60.0   # to convert time into minutes
    
    def practice_session_time_histogram_range_split(self, plot_show = 'On'):
        # plot the histogram by splitting the range of data for better visualisation
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_histogram_range_split(self.df0['TotalTimeTaken'], "TotalTimeTaken(in minutes)", "Sessions", "Histogram of practice session time(in minutes)", 0, 10, 1, 10, 100, 5, plot_show, fname = './plots/Assignment_Usage/1.jpg')   # from helper.py
        
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def practice_session_time_histogram_logscale(self, plot_show = 'On'):
        # plot the histogram on log-scale for whole range of data for better visualisation
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_histogram_logscale(self.df0['TotalTimeTaken'], "TotalTimeTaken(in minutes)", "Sessions", "Histogram of practice session time(in minutes)", 0, 100, 5, plot_show, fname = './plots/Assignment_Usage/2.jpg')      # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def cwsw_practice_session_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df1 = self.df_CSTA.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='TotalSession')
        mn, mx = get_min_max(self.df_CSTA['TotalSession'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df1, mn, mx, 'YlGnBu', '.0f', "Distribution of practice sessions course-wise and subject-wise", plot_show, fname = './plots/Assignment_Usage/3.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    
    def cwsw_avg_practice_session_time_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df2 = self.df_CSTA.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='AvgSessionTime')
        mn, mx = get_min_max(self.df_CSTA['AvgSessionTime'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df2, mn, mx, 'YlGnBu', '.2f', "Average Practice session time(in minutes) course-wise subject-wise", plot_show, fname = './plots/Assignment_Usage/4.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def cwsw_questions_used_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df3 = self.df_QDCS.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='Total_Questions')
        mn, mx = get_min_max(self.df_QDCS['Total_Questions'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df3, mn, mx, 'YlGnBu', '.0f', "Number of questions used subject-wise and course-wise", plot_show, fname = './plots/Assignment_Usage/5.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def cwsw_unique_questions_used_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df4 = self.df_QDCS.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='Unique_Questions')
        mn, mx = get_min_max(self.df_QDCS['Unique_Questions'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df4, mn, mx, 'YlGnBu', '.0f', "Number of unique questions used subject-wise and course-wise", plot_show, fname = './plots/Assignment_Usage/6.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def cwsw_unique_users_heatmap(self, plot_show = 'On'):
        # copy the course, subject & user info into a seperate dataframe
        df_CSU = self.df_CSQE[['UserId', 'CourseName', 'SubjectName']].copy()
        # Group the data by course & subject and get unique-users for all course & subject
        df_CSU = df_CSU.groupby(['CourseName', 'SubjectName'], as_index = False).agg({'UserId': 'nunique'})
        df_CSU.rename(columns = {'UserId': 'Unique_Users'}, inplace = True) # rename the column to Unique_Users
        
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df5 = df_CSU.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='Unique_Users')
        mn, mx = get_min_max(df_CSU['Unique_Users'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df5, mn, mx, 'YlGnBu', '.0f', "Number of unique users subject-wise and course-wise", plot_show, fname = './plots/Assignment_Usage/7.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def cwsw_total_time_spent_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df6 = self.df_CSTA.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='TotalTimeTaken')
        mn, mx = get_min_max(self.df_CSTA['TotalTimeTaken'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df6, mn, mx, 'YlGnBu', '.1f', "Total Time Spent(in minutes) course-wise and subject-wise", plot_show, fname = './plots/Assignment_Usage/8.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def cwsw_questions_per_practice_session_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df7 = self.df_QDCS.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='QuestionsPerSession')
        mn, mx = get_min_max(self.df_QDCS['QuestionsPerSession'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df7, mn, mx, 'YlGnBu', '.1f', "Avg no. of questions per practice session subject-wise and course-wise", plot_show, fname = './plots/Assignment_Usage/9.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}



    
    
    
    
################### class containing all functions for Practice Session Usage ##################

class Practice_Session_Usage:
    def __init__(self, conn, start_date, end_date):
        self.conn = conn
        self.start_date = start_date
        self.end_date = end_date
        # Join all the tables containing data related to self-tests taken by users
        self.df_UserTest = read_usertest_table(conn, start_date, end_date) # from tableReader.py
        self.df_UserTest = self.df_UserTest.dropna(subset=['CompletedOn']) # drop rows with NaN TotalTimeTaken
        self.df_UserTest = self.df_UserTest.loc[self.df_UserTest['RoleId']==2]  # to consider only student data
        self.df_UserTest.reset_index(inplace = True)  # reset index
        self.df_UserTest = self.df_UserTest[((stats.zscore(self.df_UserTest['TimeTakenTillSubmission']))<4)] # Removing the outliers
        print(f"Length of data is: {len(self.df_UserTest)}")
        display(self.df_UserTest.head(5))
        
        # copy course, subject, time-taken and UerTestSessionIdinto a seperate dataframe
        self.dfw_UT = self.df_UserTest[['CourseName', 'SubjectName', 'TimeTakenTillSubmission', 'UserTestSessionId']].copy()
        # Group the data by course & subject and get total time for exams & total sessions for all course & subject
        self.df_CSTA_UT = self.dfw_UT.groupby(['CourseName', 'SubjectName'], as_index = False).agg({'TimeTakenTillSubmission': 'sum', 'UserTestSessionId': 'nunique'})
        self.df_CSTA_UT['TimeTakenTillSubmission'] = self.df_CSTA_UT['TimeTakenTillSubmission']/60.0    # to convert time into minutes
        self.df_CSTA_UT.rename(columns = {'UserTestSessionId': 'TotalSession'}, inplace = True)    # rename the column to TotalSession
        self.df_CSTA_UT['AvgSessionTime'] = self.df_CSTA_UT['TimeTakenTillSubmission']/self.df_CSTA_UT['TotalSession'] # obtain average session time
    
        # copy the course, subject & question info into a seperate dataframe
        self.df_QDCS_UT = self.df_UserTest[['QuestionId', 'CourseName', 'SubjectName']].copy()
        self.df_QDCS_UT['Unique_Questions'] = self.df_QDCS_UT['QuestionId'].copy() # create a column for unique-questions
        self.df_QDCS_UT['Total_Questions'] = self.df_QDCS_UT['QuestionId'].copy()  # create a column for total-questions
        self.df_QDCS_UT = self.df_QDCS_UT.drop(['QuestionId'], axis = 1)  # drop questionid column as required data is already copied in above two columns
        # Group the data by course & subject and get total-questions & unique-questions used for all course & subject
        self.df_QDCS_UT = self.df_QDCS_UT.groupby(['CourseName', 'SubjectName'], as_index = False).agg({'Unique_Questions': 'nunique', 'Total_Questions': 'count'})
        self.df_QDCS_UT['QuestionsPerSession'] = self.df_QDCS_UT['Total_Questions']/self.df_CSTA_UT['TotalSession']  
        
        # copy the practice session time data into a dataframe
        self.df0_UT = self.df_UserTest[['UserTestSessionId', 'TimeTakenTillSubmission']].copy()
        # Group the data by UserTestSessionId
        self.df0_UT = self.df0_UT.groupby(['UserTestSessionId'], as_index=False)['TimeTakenTillSubmission'].sum()
        self.df0_UT['TimeTakenTillSubmission'] = self.df0_UT['TimeTakenTillSubmission']/60.0   # to convert time into minutes
    
    def practice_session_time_histogram_range_split(self, plot_show = 'On'):
        # plot the histogram by splitting the range of data for better visualisation
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_histogram_range_split(self.df0_UT['TimeTakenTillSubmission'], "TimeTakenTillSubmission(in minutes)", "Sessions", "Histogram of practice session time(in minutes)", 0, 10, 1, 10, 100, 5, plot_show, fname = './plots/Practice_Session_Usage/1.jpg')  # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def practice_session_time_histogram_logscale(self, plot_show = 'On'):
        # plot the histogram on log-scale for whole range of data for better visualisation
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_histogram_logscale(self.df0_UT['TimeTakenTillSubmission'], "TimeTakenTillSubmission(in minutes)", "Sessions", "Histogram of practice session time(in minutes)", 0, 200, 5, plot_show, fname = './plots/Practice_Session_Usage/2.jpg')   # from helper.py 
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def cwsw_practice_session_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df1_UT = self.df_CSTA_UT.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='TotalSession')
        mn, mx = get_min_max(self.df_CSTA_UT['TotalSession'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df1_UT, mn, mx, 'YlGnBu', '.0f', "Distribution of practice sessions course-wise and subject-wise", plot_show, fname = './plots/Practice_Session_Usage/3.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def cwsw_avg_practice_session_time_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df2_UT = self.df_CSTA_UT.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='AvgSessionTime')
        mn, mx = get_min_max(self.df_CSTA_UT['AvgSessionTime'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df2_UT, mn, mx, 'YlGnBu', '.2f', "Average Practice session time(in minutes) course-wise subject-wise", plot_show, fname = './plots/Practice_Session_Usage/4.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def cwsw_questions_used_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df3_UT = self.df_QDCS_UT.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='Total_Questions')
        # plot the course-wise and subject-wise Heat Map
        mn, mx = get_min_max(self.df_QDCS_UT['Total_Questions'])
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df3_UT, mn, mx, 'YlGnBu', '.0f', "Number of questions used subject-wise and course-wise", plot_show, fname = './plots/Practice_Session_Usage/5.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def cwsw_unique_questions_used_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df4_UT = self.df_QDCS_UT.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='Unique_Questions')
        mn, mx = get_min_max(self.df_QDCS_UT['Unique_Questions'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df4_UT, mn, mx, 'YlGnBu', '.0f', "Number of unique questions used subject-wise and course-wise", plot_show, fname = './plots/Practice_Session_Usage/6.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def cwsw_unique_users_heatmap(self, plot_show = 'On'):
        # copy the course, subject & user info into a seperate dataframe
        df_CSU_UT = self.df_UserTest[['UserId', 'CourseName', 'SubjectName']].copy()
        # Group the data by course & subject and get unique-users for all co-urse & subject
        df_CSU_UT = df_CSU_UT.groupby(['CourseName', 'SubjectName'], as_index = False).agg({'UserId': 'nunique'})
        df_CSU_UT.rename(columns = {'UserId': 'Unique_Users'}, inplace = True)  # rename the column to Unique_Users
        
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df5_UT = df_CSU_UT.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='Unique_Users')
        mn, mx = get_min_max(df_CSU_UT['Unique_Users'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df5_UT, mn, mx, 'YlGnBu', '.0f', "Number of unique users subject-wise and course-wise", plot_show, fname = './plots/Practice_Session_Usage/7.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def cwsw_total_time_spent_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df6_UT = self.df_CSTA_UT.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='TimeTakenTillSubmission')
        mn, mx = get_min_max(self.df_CSTA_UT['TimeTakenTillSubmission'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df6_UT, mn, mx, 'YlGnBu', '.1f', "Total Time Spent(in minutes) course-wise and subject-wise", plot_show, fname = './plots/Practice_Session_Usage/8.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def cwsw_questions_per_practice_session_heatmap(self, plot_show = 'On'):
        # transform the data into the wide-form DataFrame needed by Seaborn to plot heatmap
        df7_UT = self.df_QDCS_UT.loc[:,:].reset_index().pivot(index='SubjectName', columns='CourseName', values='QuestionsPerSession')
        mn, mx = get_min_max(self.df_QDCS_UT['QuestionsPerSession'])
        # plot the course-wise and subject-wise Heat Map
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_heatmap(df7_UT, mn, mx, 'YlGnBu', '.1f', "Avg no. of questions per practice session subject-wise and course-wise", plot_show, fname = './plots/Practice_Session_Usage/9.jpg') # from helper.py
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}


    
    
    
    
               
################### class containing all functions for Institute Test Usage ##################        
        
class Institute_Test_Usage:
    def __init__(self, conn, start_date, end_date):
        self.conn = conn
        self.start_date = start_date
        self.end_date = end_date
        
        # Join all the tables containing data related to institute-tests taken by users
        self.df_CSQinsT = read_instest_table(conn, start_date, end_date) # from tableReader.py
        
        self.df_CSQinsT = self.df_CSQinsT.dropna(subset=['CompletedOn']) # drop rows with NaN TotalTimeTaken
        self.df_CSQinsT = self.df_CSQinsT.loc[self.df_CSQinsT['RoleId']==2]  # to consider only student data
        # self.df_CSQinsT = self.df_CSQinsT[((stats.zscore(self.df_CSQinsT['TimeTakenInSec']))<4)] # Removing the outliers
        self.df_CSQinsT.reset_index(inplace = True)  # reset index
        
        print(f"Length of data is: {len(self.df_CSQinsT)}")
        display(self.df_CSQinsT.head(5))
        
        # copy the institute-test time data into a dataframe
        self.df_1 = self.df_CSQinsT[['UserId', 'InstituteTestUserId', 'CourseName', 'SubjectName', 'AffiliationCodeId', 
                           'CenterCodeId', 'TimeTakenInSec', 'InstituteTestId']].copy()
        self.df_1.rename(columns = {'UserId': 'Users'}, inplace = True)  # rename UserId column to Users
        self.df_1.rename(columns = {'InstituteTestUserId': 'Tests'}, inplace = True) # rename InstituteTestUserId column to Tests
        self.df_1.rename(columns = {'InstituteTestId': 'insTests'}, inplace = True)  # rename InstituteTestId column to insTests
        
        # copy the data related to plot trend in a seperate dataframe
        self.df_2 = self.df_CSQinsT[['StartedOn', 'UserId', 'InstituteTestUserId', 'TimeTakenInSec', 'InstituteTestId']].copy()
        self.df_2.rename(columns = {'UserId': 'Users'}, inplace = True)  # rename UserId column to Users
        self.df_2.rename(columns = {'InstituteTestUserId': 'Tests'}, inplace = True)  # rename InstituteTestUserId column to Tests
        self.df_2.rename(columns = {'InstituteTestId': 'insTests'}, inplace = True)  # rename InstituteTestId column to insTests
        
        # Group the data by Course and get users, Tests, insTests, TimeTakenInSec corresponding to each courses
        self.df_C = self.df_1.groupby(['CourseName'], as_index = False).agg({'Users': 'nunique', 'Tests': 'nunique', 'insTests': 'nunique',
                                                                   'TimeTakenInSec': 'sum'})
        self.df_C['TestsPerUser'] = self.df_C['Tests']/self.df_C['Users']  # get Tests per user
        self.df_C['TimePerUser'] = self.df_C['TimeTakenInSec']/(self.df_C['Users']*60)  # get Time per user in minutes
        
        # Group the data by Subject and get users, Tests, insTests, TimeTakenInSec corresponding to each Subjects
        self.df_S = self.df_1.groupby(['SubjectName'], as_index = False).agg({'Users': 'nunique', 'Tests': 'nunique', 'insTests': 'nunique',
                                                                   'TimeTakenInSec': 'sum'})
        self.df_S['TestsPerUser'] = self.df_S['Tests']/self.df_S['Users']  # get Tests per user
        self.df_S['TimePerUser'] = self.df_S['TimeTakenInSec']/(self.df_S['Users']*60)  # get Time per user in minutes
        
        #Group the data by StartedOn dates with 1-day perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_D_ = self.df_2.groupby([pd.Grouper(key='StartedOn', freq='D')]).agg({'Users': 'nunique', 'Tests': 'nunique', 'insTests': 'nunique',
                                                                           'TimeTakenInSec': 'sum'})
        self.df_D_['TestsPerUser'] = self.df_D_['Tests']/self.df_D_['Users'] # to get the TestsPerUser
        self.df_D_['TimePerUser'] = self.df_D_['TimeTakenInSec']/(self.df_D_['Users']*60)  # to get the TimePerUser in minutes
        
        #Group the data by StartedOn dates with 1-week perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_W_ = self.df_2.groupby([pd.Grouper(key='StartedOn', freq='W')]).agg({'Users': 'nunique', 'Tests': 'nunique', 'insTests': 'nunique',
                                                                           'TimeTakenInSec': 'sum'})
        self.df_W_['TestsPerUser'] = self.df_W_['Tests']/self.df_W_['Users'] # to get the TestsPerUser
        self.df_W_['TimePerUser'] = self.df_W_['TimeTakenInSec']/(self.df_W_['Users']*60)  # to get the TimePerUser in minutes
        
        #Group the data by StartedOn dates with 1-month perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_M_ = self.df_2.groupby([pd.Grouper(key='StartedOn', freq='M')]).agg({'Users': 'nunique', 'Tests': 'nunique', 
                                                                           'insTests': 'nunique', 'TimeTakenInSec': 'sum'})
        self.df_M_['TestsPerUser'] = self.df_M_['Tests']/self.df_M_['Users']  # to get the TestsPerUser
        self.df_M_['TimePerUser'] = self.df_M_['TimeTakenInSec']/(self.df_M_['Users']*60)  # to get the TimePerUser in minutes
        
        #Group the data by StartedOn dates with 4-months perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_Q_ = self.df_2.groupby([pd.Grouper(key='StartedOn', freq='4M')]).agg({'Users': 'nunique', 'Tests': 'nunique', 
                                                                           'insTests': 'nunique', 'TimeTakenInSec': 'sum'})
        self.df_Q_['TestsPerUser'] = self.df_Q_['Tests']/self.df_Q_['Users']  # to get the TestsPerUser
        self.df_Q_['TimePerUser'] = self.df_Q_['TimeTakenInSec']/(self.df_Q_['Users']*60)  # to get the TimePerUser in minutes
        
        #Group the data by StartedOn dates with 1-year perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_Y_ = self.df_2.groupby([pd.Grouper(key='StartedOn', freq='Y')]).agg({'Users': 'nunique', 'Tests': 'nunique', 
                                                                           'insTests': 'nunique', 'TimeTakenInSec': 'sum'})
        self.df_Y_['TestsPerUser'] = self.df_Y_['Tests']/self.df_Y_['Users']  # to get the TestsPerUser
        self.df_Y_['TimePerUser'] = self.df_Y_['TimeTakenInSec']/(self.df_Y_['Users']*60)  # to get the TimePerUser in minutes
        
    def coursewise_analysis_1(self, plot_show = 'On'):
        # plot the bargraph for TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_C['TestsPerUser'], self.df_C['CourseName'], "CourseName", "TestsPerUser","Number of tests per user Vs Courses", plot_show, fname = './plots/Institute_Test_Usage/1.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def coursewise_analysis_2(self, plot_show = 'On'):    
        # plot the bargraph for Institute-Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_C['insTests'], self.df_C['CourseName'], "CourseName", "Institute-Tests","Number of tests Vs Courses", plot_show, fname = './plots/Institute_Test_Usage/2.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def coursewise_analysis_3(self, plot_show = 'On'):
        # plot the bargraph for TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_C['TimePerUser'], self.df_C['CourseName'], "CourseName", "TimePerUser", "Duration of tests per user Vs Courses", plot_show, fname = './plots/Institute_Test_Usage/3.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def subjectwise_analysis_1(self, plot_show = 'On'):
        # plot the bargraph for TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_S['TestsPerUser'], self.df_S['SubjectName'], "SubjectName", "TestsPerUser", "Number of tests per user Vs Subjects", plot_show, fname = './plots/Institute_Test_Usage/4.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def subjectwise_analysis_2(self, plot_show = 'On'):    
        # plot the bargraph for Institute-Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_S['insTests'], self.df_S['SubjectName'], "SubjectName", "Institute-Tests", "Number of tests Vs Subjects", plot_show, fname = './plots/Institute_Test_Usage/5.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def subjectwise_analysis_3(self, plot_show = 'On'):
        # plot the bargraph for TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_S['TimePerUser'], self.df_S['SubjectName'], "SubjectName", "TimePerUser", "Duration of tests per user Vs Subjects", plot_show, fname = './plots/Institute_Test_Usage/6.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def affiliationwise_analysis(self, plot_show = 'On'):
        # Group the data by Affiliation and get users, Tests, insTests, TimeTakenInSec corresponding to each Affiliations
        df_A = self.df_1.groupby(['AffiliationCodeId'], as_index = False).agg({'Users': 'nunique', 'Tests': 'nunique', 'insTests': 'nunique', 'TimeTakenInSec': 'sum'})
        df_A['TestsPerUser'] = df_A['Tests']/df_A['Users']  # get Tests per user
        df_A['TimePerUser'] = df_A['TimeTakenInSec']/(df_A['Users']*60)  # get Time per user in minutes
        
        #plot the histogram of number of Number of Tests by splitting range
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_histogram_range_split(df_A['insTests'], "Number of Tests", "Number of Affiliations", "Histogram of Number of Tests", 1, 10, 1, 10, 100, 5, plot_show, fname = './plots/Institute_Test_Usage/7.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
        
    def daily_trend_1(self, plot_show = 'On'):
        # plot the Daily Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_D_['TestsPerUser'], "Time", "TestsPerUser", "Daily Trend in TestsPerUser", plot_show, fname = './plots/Institute_Test_Usage/8.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def daily_trend_2(self, plot_show = 'On'):
        # plot the Daily Trend in Institute-Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_D_['insTests'], "Time", "Institute-Tests", "Daily Trend in Institute-Tests", plot_show, fname = './plots/Institute_Test_Usage/9.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def daily_trend_3(self, plot_show = 'On'):
        # plot the Daily Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_D_['TimePerUser'], "Time", "TimePerUser", "Daily Trend in TimePerUser", plot_show, fname = './plots/Institute_Test_Usage/10.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
        
    def weekly_trend_1(self, plot_show = 'On'):
        # plot the Weekly Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_W_['TestsPerUser'], "Time", "TestsPerUser", "Weekly Trend in TestsPerUser", plot_show, fname = './plots/Institute_Test_Usage/11.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def weekly_trend_2(self, plot_show = 'On'):
        # plot the Weekly Trend in Institute-Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_W_['insTests'], "Time", "Institute-Tests", "Weekly Trend in Institute-Tests", plot_show, fname = './plots/Institute_Test_Usage/12.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def weekly_trend_3(self, plot_show = 'On'):
        # plot the Weekly Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_W_['TimePerUser'], "Time", "TimePerUser", "Weekly Trend in TimePerUser", plot_show, fname = './plots/Institute_Test_Usage/13.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
        
    def monthly_trend_1(self, plot_show = 'On'):
        # plot the Monthly Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_M_['TestsPerUser'], "Time", "TestsPerUser", "Monthly Trend in TestsPerUser", plot_show, fname = './plots/Institute_Test_Usage/14.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def monthly_trend_2(self, plot_show = 'On'):
        # plot the Monthly Trend in Institute-Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_M_['insTests'], "Time", "Institute-Tests", "Monthly Trend in Institute-Tests", plot_show, fname = './plots/Institute_Test_Usage/15.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def monthly_trend_3(self, plot_show = 'On'):
        # plot the Monthly Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_M_['TimePerUser'], "Time", "TimePerUser", "Monthly Trend in TimePerUser", plot_show, fname = './plots/Institute_Test_Usage/16.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
        
    def quarterly_trend_1(self, plot_show = 'On'):
        # plot the Quarterly Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Q_['TestsPerUser'], "Time", "TestsPerUser", "Quarterly Trend in TestsPerUser", plot_show, fname = './plots/Institute_Test_Usage/17.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def quarterly_trend_2(self, plot_show = 'On'):
        # plot the Quarterly Trend in Institute-Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Q_['insTests'], "Time", "Institute-Tests", "Quarterly Trend in Institute-Tests", plot_show, fname = './plots/Institute_Test_Usage/18.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def quarterly_trend_3(self, plot_show = 'On'):
        # plot the Quarterly Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Q_['TimePerUser'], "Time", "TimePerUser", "Quarterly Trend in TimePerUser", plot_show, fname = './plots/Institute_Test_Usage/19.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    
    def yearly_trend_1(self, plot_show = 'On'):
        # plot the Yearly Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Y_['TestsPerUser'], "Time", "TestsPerUser", "Yearly Trend in TestsPerUser", plot_show, fname = './plots/Institute_Test_Usage/20.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def yearly_trend_2(self, plot_show = 'On'):
        # plot the Yearly Trend in Institute-Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Y_['insTests'], "Time", "Institute-Tests", "Yearly Trend in Institute-Tests", plot_show, fname = './plots/Institute_Test_Usage/21.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def yearly_trend_3(self, plot_show = 'On'):
        # plot the Yearly Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Y_['TimePerUser'], "Time", "TimePerUser", "Yearly Trend in TimePerUser", plot_show, fname = './plots/Institute_Test_Usage/22.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    


    
    
    
    
################### class containing all functions for Self Test Usage ##################        

class Self_Test_Usage:
    def __init__(self, conn, start_date, end_date):
        self.conn = conn
        self.start_date = start_date
        self.end_date = end_date
        
        # Join all the tables containing data related to institute-tests taken by users
        self.df_UserTest = read_usertest_table(conn, start_date, end_date) # from tableReader.py
        
        self.df_UserTest = self.df_UserTest.dropna(subset=['CompletedOn']) # drop rows with NaN TotalTimeTaken
        self.df_UserTest = self.df_UserTest.loc[self.df_UserTest['RoleId']==2]  # to consider only student data
        self.df_UserTest = self.df_UserTest[((stats.zscore(self.df_UserTest['TimeTakenTillSubmission']))<4)] # Removing the outliers
        self.df_UserTest.reset_index(inplace = True)  # reset index
        
        print(f"Length of data is: {len(self.df_UserTest)}")
        display(self.df_UserTest.head(5))
        
        # copy the institute-test time data into a dataframe
        self.df_1_UT = self.df_UserTest[['UserId', 'UserTestSessionId', 'CourseName', 'SubjectName', 'AffiliationCodeId', 
                           'CenterCodeId', 'TimeTakenTillSubmission']].copy()
        self.df_1_UT.rename(columns = {'UserId': 'Users'}, inplace = True)  # rename UserId column to Users
        self.df_1_UT.rename(columns = {'UserTestSessionId': 'Tests'}, inplace = True) # rename UserTestSessionId column to Tests
        
        # copy the data related to plot trend in a seperate dataframe
        self.df_2_UT = self.df_UserTest[['StartedOn', 'UserId', 'UserTestSessionId', 'TimeTakenTillSubmission']].copy()
        self.df_2_UT.rename(columns = {'UserId': 'Users'}, inplace = True)  # rename UserId column to Users
        self.df_2_UT.rename(columns = {'UserTestSessionId': 'Tests'}, inplace = True)  # rename UserTestSessionId column to Tests
        
        # Group the data by Course and get users, Tests, insTests, TimeTakenInSec corresponding to each courses
        self.df_C_UT = self.df_1_UT.groupby(['CourseName'], as_index = False).agg({'Users': 'nunique', 'Tests': 'nunique',
                                                                   'TimeTakenTillSubmission': 'sum'})
        self.df_C_UT['TestsPerUser'] = self.df_C_UT['Tests']/self.df_C_UT['Users']  # get Tests per user
        self.df_C_UT['TimePerUser'] = self.df_C_UT['TimeTakenTillSubmission']/(self.df_C_UT['Users']*60)  # get Time per user in minutes
        
        # Group the data by Subject and get users, Tests, insTests, TimeTakenInSec corresponding to each Subjects
        self.df_S_UT = self.df_1_UT.groupby(['SubjectName'], as_index = False).agg({'Users': 'nunique', 'Tests': 'nunique',
                                                                   'TimeTakenTillSubmission': 'sum'})
        self.df_S_UT['TestsPerUser'] = self.df_S_UT['Tests']/self.df_S_UT['Users']  # get Tests per user
        self.df_S_UT['TimePerUser'] = self.df_S_UT['TimeTakenTillSubmission']/(self.df_S_UT['Users']*60)  # get Time per user in minutes
        
        #Group the data by StartedOn dates with 1-day perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_D_UT = self.df_2_UT.groupby([pd.Grouper(key='StartedOn', freq='D')]).agg({'Users': 'nunique', 'Tests': 'nunique',
                                                                           'TimeTakenTillSubmission': 'sum'})
        self.df_D_UT['TestsPerUser'] = self.df_D_UT['Tests']/self.df_D_UT['Users'] # to get the TestsPerUser
        self.df_D_UT['TimePerUser'] = self.df_D_UT['TimeTakenTillSubmission']/(self.df_D_UT['Users']*60)  # to get the TimePerUser in minutes
        
        #Group the data by StartedOn dates with 1-week perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_W_UT = self.df_2_UT.groupby([pd.Grouper(key='StartedOn', freq='W')]).agg({'Users': 'nunique', 'Tests': 'nunique',
                                                                           'TimeTakenTillSubmission': 'sum'})
        self.df_W_UT['TestsPerUser'] = self.df_W_UT['Tests']/self.df_W_UT['Users'] # to get the TestsPerUser
        self.df_W_UT['TimePerUser'] = self.df_W_UT['TimeTakenTillSubmission']/(self.df_W_UT['Users']*60)  # to get the TimePerUser in minutes
        
        #Group the data by StartedOn dates with 1-month perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_M_UT = self.df_2_UT.groupby([pd.Grouper(key='StartedOn', freq='M')]).agg({'Users': 'nunique', 'Tests': 'nunique', 
                                                                           'TimeTakenTillSubmission': 'sum'})
        self.df_M_UT['TestsPerUser'] = self.df_M_UT['Tests']/self.df_M_UT['Users']  # to get the TestsPerUser
        self.df_M_UT['TimePerUser'] = self.df_M_UT['TimeTakenTillSubmission']/(self.df_M_UT['Users']*60)  # to get the TimePerUser in minutes
        
        #Group the data by StartedOn dates with 4-months perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_Q_UT = self.df_2_UT.groupby([pd.Grouper(key='StartedOn', freq='4M')]).agg({'Users': 'nunique', 'Tests': 'nunique', 
                                                                           'TimeTakenTillSubmission': 'sum'})
        self.df_Q_UT['TestsPerUser'] = self.df_Q_UT['Tests']/self.df_Q_UT['Users']  # to get the TestsPerUser
        self.df_Q_UT['TimePerUser'] = self.df_Q_UT['TimeTakenTillSubmission']/(self.df_Q_UT['Users']*60)  # to get the TimePerUser in minutes
        
        #Group the data by StartedOn dates with 1-year perid and get users, Tests, insTests, TimeTakenInSec corresponding to each period
        self.df_Y_UT = self.df_2_UT.groupby([pd.Grouper(key='StartedOn', freq='Y')]).agg({'Users': 'nunique', 'Tests': 'nunique', 
                                                                           'TimeTakenTillSubmission': 'sum'})
        self.df_Y_UT['TestsPerUser'] = self.df_Y_UT['Tests']/self.df_Y_UT['Users']  # to get the TestsPerUser
        self.df_Y_UT['TimePerUser'] = self.df_Y_UT['TimeTakenTillSubmission']/(self.df_Y_UT['Users']*60)  # to get the TimePerUser in minutes
        
    def coursewise_analysis_1(self, plot_show = 'On'):
        # plot the bargraph for TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_C_UT['TestsPerUser'], self.df_C_UT['CourseName'], "CourseName", "TestsPerUser", "Number of tests per user Vs Courses", plot_show, fname = './plots/Self_Test_Usage/1.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def coursewise_analysis_2(self, plot_show = 'On'):
        # plot the bargraph for Number of Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_C_UT['Tests'], self.df_C_UT['CourseName'], "CourseName", "Tests","Number of tests Vs Courses", plot_show, fname = './plots/Self_Test_Usage/2.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def coursewise_analysis_3(self, plot_show = 'On'):
        # plot the bargraph for TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_C_UT['TimePerUser'], self.df_C_UT['CourseName'], "CourseName", "TimePerUser", "Duration of tests per user Vs Courses", plot_show, fname = './plots/Self_Test_Usage/3.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def subjectwise_analysis_1(self, plot_show = 'On'):
        # plot the bargraph for TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_S_UT['TestsPerUser'], self.df_S_UT['SubjectName'], "SubjectName", "TestsPerUser", "Number of tests per user Vs Subjects", plot_show, fname = './plots/Self_Test_Usage/4.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def subjectwise_analysis_2(self, plot_show = 'On'):
        # plot the bargraph for Number of Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_S_UT['Tests'], self.df_S_UT['SubjectName'], "SubjectName", "Tests", "Number of tests Vs Subjects", plot_show, fname = './plots/Self_Test_Usage/5.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def subjectwise_analysis_3(self, plot_show = 'On'):
        # plot the bargraph for TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_S_UT['TimePerUser'], self.df_S_UT['SubjectName'], "SubjectName", "TimePerUser", "Duration of tests per user Vs Subjects", plot_show, fname = './plots/Self_Test_Usage/6.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def affiliationwise_analysis(self, plot_show = 'On'):
        # Group the data by Affiliation and get users, Tests, insTests, TimeTakenInSec corresponding to each Affiliations
        df_A_UT = self.df_1_UT.groupby(['AffiliationCodeId'], as_index = False).agg({'Users': 'nunique', 'Tests': 'nunique',
                                                                          'TimeTakenTillSubmission': 'sum'})
        df_A_UT['TestsPerUser'] = df_A_UT['Tests']/df_A_UT['Users']  # get Tests per user
        df_A_UT['TimePerUser'] = df_A_UT['TimeTakenTillSubmission']/(df_A_UT['Users']*60)  # get Time per user in minutes
        
        #plot the histogram of number of Number of Tests by splitting range
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_histogram_range_split(df_A_UT['Tests'], "Number of Tests", "Number of Affiliations", "Histogram of Number of Tests", 1, 10, 1, 10, 100, 5, plot_show, fname = './plots/Self_Test_Usage/7.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def daily_trend_1(self, plot_show = 'On'):
        # plot the Daily Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_D_UT['TestsPerUser'], "Time", "TestsPerUser", "Daily Trend in TestsPerUser", plot_show, fname = './plots/Self_Test_Usage/8.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def daily_trend_2(self, plot_show = 'On'):
        # plot the Daily Trend in Number of Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_D_UT['Tests'], "Time", "Tests", "Daily Trend in Tests", plot_show, fname = './plots/Self_Test_Usage/9.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def daily_trend_3(self, plot_show = 'On'):
        # plot the Daily Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_D_UT['TimePerUser'], "Time", "TimePerUser", "Daily Trend in TimePerUser", plot_show, fname = './plots/Self_Test_Usage/10.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def weekly_trend_1(self, plot_show = 'On'):
        # plot the Weekly Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_W_UT['TestsPerUser'], "Time", "TestsPerUser", "Weekly Trend in TestsPerUser", plot_show, fname = './plots/Self_Test_Usage/11.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def weekly_trend_2(self, plot_show = 'On'):
        # plot the Weekly Trend in Number of Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_W_UT['Tests'], "Time", "Tests", "Weekly Trend in Tests", plot_show, fname = './plots/Self_Test_Usage/12.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def weekly_trend_3(self, plot_show = 'On'):
        # plot the Weekly Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_W_UT['TimePerUser'], "Time", "TimePerUser", "Weekly Trend in TimePerUser", plot_show, fname = './plots/Self_Test_Usage/13.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def monthly_trend_1(self, plot_show = 'On'):
        # plot the Monthly Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_M_UT['TestsPerUser'], "Time", "TestsPerUser", "Monthly Trend in TestsPerUser", plot_show, fname = './plots/Self_Test_Usage/14.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def monthly_trend_2(self, plot_show = 'On'):
        # plot the Monthly Trend in Number of Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_M_UT['Tests'], "Time", "Tests", "Monthly Trend in Tests", plot_show, fname = './plots/Self_Test_Usage/15.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def monthly_trend_3(self, plot_show = 'On'):
        # plot the Monthly Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_M_UT['TimePerUser'], "Time", "TimePerUser", "Monthly Trend in TimePerUser", plot_show, fname = './plots/Self_Test_Usage/16.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def quarterly_trend_1(self, plot_show = 'On'):
        # plot the Quarterly Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Q_UT['TestsPerUser'], "Time", "TestsPerUser", "Quarterly Trend in TestsPerUser", plot_show, fname = './plots/Self_Test_Usage/17.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def quarterly_trend_2(self, plot_show = 'On'):
        # plot the Quarterly Trend in Number of Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Q_UT['Tests'], "Time", "Tests", "Quarterly Trend in Tests", plot_show, fname = './plots/Self_Test_Usage/18.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def quarterly_trend_3(self, plot_show = 'On'):
        # plot the Quarterly Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Q_UT['TimePerUser'], "Time", "TimePerUser", "Quarterly Trend in TimePerUser", plot_show, fname = './plots/Self_Test_Usage/19.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def yearly_trend_1(self, plot_show = 'On'):
        # plot the Yearly Trend in TestsPerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Y_UT['TestsPerUser'], "Time", "TestsPerUser", "Yearly Trend in TestsPerUser", plot_show, fname = './plots/Self_Test_Usage/20.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def yearly_trend_2(self, plot_show = 'On'):
        # plot the Yearly Trend in Number of Tests
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Y_UT['Tests'], "Time", "Tests", "Yearly Trend in Tests", plot_show, fname = './plots/Self_Test_Usage/21.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def yearly_trend_3(self, plot_show = 'On'):    
        # plot the Yearly Trend in TimePerUser
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Y_UT['TimePerUser'], "Time", "TimePerUser", "Yearly Trend in TimePerUser", plot_show, fname = './plots/Self_Test_Usage/22.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}

    
    
    
    


################### class containing all functions for Learn Usage ##################

class Learn_Usage:
    def __init__(self, conn, start_date, end_date):
        self.conn = conn
        self.start_date = start_date
        self.end_date = end_date
        
        # Join all the tables containing data related to Online-classes
        self.df_LU = read_onlineclass_table(conn, start_date, end_date) # from tableReader.py
        print(f"Length of data is: {len(self.df_LU)}")
        display(self.df_LU.head(5))
        
        # self.df_LU['StartTime'] = pd.to_datetime(self.df_LU['StartTime'])
        
        # copy the institute-test time data into a dataframe
        self.df_1_LU = self.df_LU[['OnlineClassId', 'CourseName', 'SubjectName', 'AffiliationId', 'Duration']].copy()
        self.df_1_LU.rename(columns = {'OnlineClassId': 'Classes'}, inplace = True) # rename OnlineClassId column to Classes
        
        # copy the data related to plot trend in a seperate dataframe
        self.df_2_LU = self.df_LU[['StartTime', 'OnlineClassId', 'Duration']].copy()
        self.df_2_LU.rename(columns = {'OnlineClassId': 'Classes'}, inplace = True)  # rename OnlineClassId column to Classes
        
        # Group the data by Course and get Classes & Duration corresponding to each courses
        self.df_C_LU = self.df_1_LU.groupby(['CourseName'], as_index = False).agg({'Classes': 'nunique', 'Duration': 'sum'})
        self.df_C_LU['TimePerClass'] = self.df_C_LU['Duration']/self.df_C_LU['Classes']  # to get time per class in minutes
        
        # Group the data by Subject and get Classes & Duration corresponding to each Subjects
        self.df_S_LU = self.df_1_LU.groupby(['SubjectName'], as_index = False).agg({'Classes': 'nunique', 'Duration': 'sum'})
        self.df_S_LU['TimePerClass'] = self.df_S_LU['Duration']/self.df_S_LU['Classes']  # to get time per class in minutes
        
        #Group the data by StartedOn dates with 1-day perid and get Classes & Duration corresponding to each period
        self.df_D_LU = self.df_2_LU.groupby([pd.Grouper(key='StartTime', freq='D')]).agg({'Classes': 'nunique', 'Duration': 'sum'})
        self.df_D_LU['TimePerClass'] = self.df_D_LU['Duration']/self.df_D_LU['Classes']  # to get the TimePerClass in minutes
        self.df_D_LU['TimePerClass'] = self.df_D_LU['TimePerClass'].fillna(-1)  # replace NaN by -1
        
        #Group the data by StartedOn dates with 1-week perid and get Classes & Duration corresponding to each period
        self.df_W_LU = self.df_2_LU.groupby([pd.Grouper(key='StartTime', freq='W')]).agg({'Classes': 'nunique', 'Duration': 'sum'})
        self.df_W_LU['TimePerClass'] = self.df_W_LU['Duration']/self.df_W_LU['Classes']  # to get the TimePerClass in minutes
        self.df_W_LU['TimePerClass'] = self.df_W_LU['TimePerClass'].fillna(-1)  # replace NaN by -1
        
        #Group the data by StartedOn dates with 1-month perid and get Classes & Duration corresponding to each period
        self.df_M_LU = self.df_2_LU.groupby([pd.Grouper(key='StartTime', freq='M')]).agg({'Classes': 'nunique', 'Duration': 'sum'})
        self.df_M_LU['TimePerClass'] = self.df_M_LU['Duration']/self.df_M_LU['Classes']  # to get the TimePerClass in minutes
        self.df_M_LU['TimePerClass'] = self.df_M_LU['TimePerClass'].fillna(-1)  # replace NaN by -1
        
        #Group the data by StartedOn dates with 4-months perid and get Classes & Duration corresponding to each period
        self.df_Q_LU = self.df_2_LU.groupby([pd.Grouper(key='StartTime', freq='Q')]).agg({'Classes': 'nunique', 'Duration': 'sum'})
        self.df_Q_LU['TimePerClass'] = self.df_Q_LU['Duration']/self.df_Q_LU['Classes']  # to get the TimePerClass in minutes
        self.df_Q_LU['TimePerClass'] = self.df_Q_LU['TimePerClass'].fillna(-1)  # replace NaN by -1
        
        #Group the data by StartedOn dates with 1-year perid and get Classes & Duration corresponding to each period
        self.df_Y_LU = self.df_2_LU.groupby([pd.Grouper(key='StartTime', freq='Y')]).agg({'Classes': 'nunique', 'Duration': 'sum'})
        self.df_Y_LU['TimePerClass'] = self.df_Y_LU['Duration']/self.df_Y_LU['Classes']  # to get the TimePerClass in minutes
        self.df_Y_LU['TimePerClass'] = self.df_Y_LU['TimePerClass'].fillna(-1)  # replace NaN by -1

    def coursewise_analysis_1(self, plot_show = 'On'):
        # plot the bargraph for Number of Online-Classes
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_C_LU['Classes'], self.df_C_LU['CourseName'], "CourseName", "Online-Classes", "Number of Online-Classes Vs Courses", plot_show, fname = './plots/Learn_Usage/1.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def coursewise_analysis_2(self, plot_show = 'On'):
        # plot the bargraph for Total-Class-Time
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_C_LU['Duration'], self.df_C_LU['CourseName'], "CourseName", "Total-Class-Time", "Total-Class-Time Vs Courses", plot_show, fname = './plots/Learn_Usage/2.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def coursewise_analysis_3(self, plot_show = 'On'):
        # plot the bargraph for TimePerClass
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_C_LU['TimePerClass'], self.df_C_LU['CourseName'], "CourseName", "TimePerClass", "Time-Per-Class Vs Courses", plot_show, fname = './plots/Learn_Usage/3.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def subjectwise_analysis_1(self, plot_show = 'On'):
        # plot the bargraph for Number of Online-Classes
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_S_LU['Classes'], self.df_S_LU['SubjectName'], "SubjectName", "Online-Classes", "Number of Online-Classes Vs Subjects", plot_show, fname = './plots/Learn_Usage/4.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def subjectwise_analysis_2(self, plot_show = 'On'):
        # plot the bargraph for Total-Class-Time
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_S_LU['Duration'], self.df_S_LU['SubjectName'], "SubjectName", "Total-Class-Time", "Total-Class-Time Vs Subjects", plot_show, fname = './plots/Learn_Usage/5.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def subjectwise_analysis_3(self, plot_show = 'On'):
        # plot the bargraph for TimePerClass
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_bargraph(self.df_S_LU['TimePerClass'], self.df_S_LU['SubjectName'], "SubjectName", "TimePerClass", "Time-Per-Class Vs Subjects", plot_show, fname = './plots/Learn_Usage/6.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def affiliationwise_analysis(self, plot_show = 'On'):
        # Group the data by Affiliation and get Classes & Duration corresponding to each Affiliations
        df_A_LU = self.df_1_LU.groupby(['AffiliationId'], as_index = False).agg({'Classes': 'nunique', 'Duration': 'sum'})
        df_A_LU['TimePerClass'] = df_A_LU['Duration']/df_A_LU['Classes']  # to get time per class in minutes
        
        #plot the histogram of number of Number of Classes by splitting range
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_histogram_range_split(df_A_LU['Classes'], "Number of Classes", "Number of Affiliations", "Histogram of Number of Classes", 1, 10, 1, 10, 150, 10, plot_show, fname = './plots/Learn_Usage/7.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    
        
    def daily_trend_1(self, plot_show = 'On'):
        # plot the Daily Trend in Number of Classes
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_D_LU['Classes'], "Time", "Classes", "Daily Trend in Number of Classes", plot_show, fname = './plots/Learn_Usage/8.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def daily_trend_2(self, plot_show = 'On'):
        # plot the Daily Trend in Duration
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_D_LU['Duration'], "Time", "Duration", "Daily Trend in Duration", plot_show, fname = './plots/Learn_Usage/9.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def daily_trend_3(self, plot_show = 'On'):
        # plot the Daily Trend in TimePerClass
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_D_LU['TimePerClass'], "Time", "TimePerClass", "Daily Trend in TimePerClass", plot_show, fname = './plots/Learn_Usage/10.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
    def weekly_trend_1(self, plot_show = 'On'):
        # plot the Weekly Trend in Number of Classes
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_W_LU['Classes'], "Time", "Classes", "Weekly Trend in Number of Classes", plot_show, fname = './plots/Learn_Usage/11.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def weekly_trend_2(self, plot_show = 'On'):
        # plot the Weekly Trend in Duration
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_W_LU['Duration'], "Time", "Duration", "Weekly Trend in Duration", plot_show, fname = './plots/Learn_Usage/12.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def weekly_trend_3(self, plot_show = 'On'):
        # plot the Weekly Trend in TimePerClass
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_W_LU['TimePerClass'], "Time", "TimePerClass", "Weekly Trend in TimePerClass", plot_show, fname = './plots/Learn_Usage/13.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def monthly_trend_1(self, plot_show = 'On'):
        # plot the Monthly Trend in Number of Classes
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_M_LU['Classes'], "Time", "Classes", "Monthly Trend in Number of Classes", plot_show, fname = './plots/Learn_Usage/14.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def monthly_trend_2(self, plot_show = 'On'):
        # plot the Monthly Trend in Duration
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_M_LU['Duration'], "Time", "Duration", "Monthly Trend in Duration", plot_show, fname = './plots/Learn_Usage/15.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def monthly_trend_3(self, plot_show = 'On'):
        # plot the Monthly Trend in TimePerClass
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_M_LU['TimePerClass'], "Time", "TimePerClass", "Monthly Trend in TimePerClass", plot_show, fname = './plots/Learn_Usage/16.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def quarterly_trend_1(self, plot_show = 'On'):
        # plot the Quarterly Trend in Number of Classes
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Q_LU['Classes'], "Time", "Classes", "Quarterly Trend in Number of Classes", plot_show, fname = './plots/Learn_Usage/17.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def quarterly_trend_2(self, plot_show = 'On'):
        # plot the Quarterly Trend in Duration
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Q_LU['Duration'], "Time", "Duration", "Quarterly Trend in Duration", plot_show, fname = './plots/Learn_Usage/18.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def quarterly_trend_3(self, plot_show = 'On'):
        # plot the Quarterly Trend in TimePerClass
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Q_LU['TimePerClass'], "Time", "TimePerClass", "Quarterly Trend in TimePerClass", plot_show, fname = './plots/Learn_Usage/19.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    
    def yearly_trend_1(self, plot_show = 'On'):
        # plot the Yearly Trend in Number of Classes
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Y_LU['Classes'], "Time", "Classes", "Yearly Trend in Number of Classes", plot_show, fname = './plots/Learn_Usage/20.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def yearly_trend_2(self, plot_show = 'On'):
        # plot the Yearly Trend in Duration
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Y_LU['Duration'], "Time", "Duration", "Yearly Trend in Duration", plot_show, fname = './plots/Learn_Usage/21.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
    def yearly_trend_3(self, plot_show = 'On'):
        # plot the Yearly Trend in TimePerClass
        base64PNG, base64SVG, plotlyData, plotlyLayout = plot_trend(self.df_Y_LU['TimePerClass'], "Time", "TimePerClass", "Yearly Trend in TimePerClass", plot_show, fname = './plots/Learn_Usage/22.jpg')
        return {"base64PNG": base64PNG, 
                "base64SVG": base64SVG, 
                "plotlyData": plotlyData, 
                "plotlyLayout": plotlyLayout}
        
        
