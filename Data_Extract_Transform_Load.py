                               # Data Collection and Transformation
# Required Packages
import pandas as pd
import numpy as np
import sqlalchemy as sql
import git 
import os 
import json
import psycopg2

class Phonepe_pulse:
    
     def data_collection(self):
          git.Repo.clone_from('https://github.com/PhonePe/pulse.git','phonepe_pulse_data')
          return 1
     
     def data_transformation(self):

                                # Aggregated transactions

          # PATH OF AGGREAGATED TRANSACTION MENTIONED BELOW

          path = "phonepe_pulse_data/data/aggregated/transaction/country/india/state/"

          Agg_state_Name_list = os.listdir(path)

          Full_Data={'state':[], 'year':[],'quater':[],'agg_transaction_type':[], 'agg_transaction_count':[], 'agg_transaction_amount':[]} # DATA CONTAINER  for DATAFRAME

          for i in Agg_state_Name_list:  
               path_i = path+i+'/'
               path_year = os.listdir(path_i)
               for year in path_year:       
                    path_year_file = path_i+year
                    year_files = os.listdir(path_year_file)
                    for file_ in year_files: 
                         file_path = path_year_file+'/'+file_
                         data_file = open(file_path,'r')
                         Data = json.load(data_file)
                         for z in Data['data']["transactionData"]:
                              Name = z['name']
                              count = z["paymentInstruments"][0]["count"]
                              amount = z["paymentInstruments"][0]["amount"]
                              Full_Data['agg_transaction_type'].append(Name)
                              Full_Data['agg_transaction_count'].append(count)
                              Full_Data['agg_transaction_amount'].append(amount)
                              Full_Data['state'].append(i)
                              Full_Data['year'].append(year)
                              Full_Data['quater'].append(int(file_.strip('.json')))

          agg_transaction_df = pd.DataFrame(Full_Data)
          # print(agg_transaction_df.columns)
                                  
                                  # Aggregated user
               
          # PATH OF AGGREAGATED USER MENTIONED BELOW

          PATH  = 'phonepe_pulse_data/data/aggregated/user/country/india/state'

          agg_users_state_names = os.listdir(path)
          
          user_data = {'state':[], 'year':[],'quater':[],'registered_users': [] ,"agg_users_appopens":[], 'agg_users_brand' :[] , 'agg_users_count':[],'agg_users_percentage':[]}


          for i in agg_users_state_names: 
               agg_state_path = PATH+'/'+i+'/'
               agg_states_years = os.listdir(agg_state_path)  
               for year in agg_states_years:
                    file_path = agg_state_path+year+'/'
                    year_files = os.listdir(file_path)
                    for j in year_files:
                         f=file_path+j
                         data = open(f,'r')
                         file_ = json.load(data)
                         # ----------Data fill condition-------
                         if file_["data"]['usersByDevice'] is not None:
                              for z in file_["data"]['usersByDevice']:
                                   Name = i
                                   Year = year
                                   Q = int(j.strip('.json'))
                                   ru = file_['data']['aggregated']['registeredUsers']
                                   ao = file_['data']['aggregated']['appOpens']
                                   brand = z['brand']
                                   count = z['count']
                                   percentage = z["percentage"]
                                   user_data["state"].append(Name)
                                   user_data['year'].append(Year)
                                   user_data['quater'].append(Q)
                                   user_data['registered_users'].append(ru)
                                   user_data["agg_users_appopens"].append(ao)
                                   user_data['agg_users_brand'].append(brand)
                                   user_data['agg_users_count'].append(count)
                                   user_data['agg_users_percentage'].append(percentage)
                         else:
                              Name = i
                              Year = year
                              Q = int(j.strip('.json'))
                              ru = file_['data']['aggregated']['registeredUsers']
                              ao = file_['data']['aggregated']['appOpens']

                              user_data["state"].append(Name)
                              user_data['year'].append(Year)
                              user_data['quater'].append(Q)
                              user_data['registered_users'].append(ru)
                              user_data["agg_users_appopens"].append(ao)
                              user_data['agg_users_brand'].append('Not Mentioned')
                              user_data['agg_users_count'].append(0)
                              user_data['agg_users_percentage'].append(0)

          agg_user_df = pd.DataFrame(user_data)
          # print(agg_user_df.columns)

                                     # MAP TRANSACTION

          # PATH OF MAP TRANSACTION MENTIONED BELOW
          
          path = 'phonepe_pulse_data/data/map/transaction/hover/country/india/state'

          map_state_names = os.listdir(path)

          Map_Data = {'state':[],'year':[],'quater':[],'map_transaction_district':[],'map_transaction_type':[],'map_transaction_count':[],'map_transaction_amount':[]}

          for i in map_state_names:
               map_state_path   = path + '/' + i + '/'
               map_states_years = os.listdir(map_state_path)
               for year in map_states_years:
                    file_path  = map_state_path + year + '/'
                    year_files = os.listdir(file_path)
               for j in year_files:
                    f = file_path + j
                    data = open(f,'r')
                    file_ = json.load(data)
                    for z in file_['data']["hoverDataList"]:
                         state_name =  i
                         Year = year
                         Q = int(j.strip('.json'))
                         dist_name = z['name']
                         type_  = z['metric'][0]['type'] if z['metric'][0]['type'] else "Not Mentioned"
                         count  = z['metric'][0]['count'] if z['metric'][0]['count'] else 0
                         amount = z['metric'][0]['amount'] if z['metric'][0]['amount'] else 0
                         Map_Data['state'].append(state_name)
                         Map_Data['map_transaction_district'].append(dist_name)
                         Map_Data['map_transaction_type'].append(type_)
                         Map_Data['map_transaction_count'].append(count)
                         Map_Data['map_transaction_amount'].append(amount)
                         Map_Data['year'].append(Year)
                         Map_Data['quater'].append(Q)

          Map_df = pd.DataFrame(Map_Data)
          # print(Map_df.columns)

                                 # MAP USER 

          # PATH OF MAP USER  MENTIONED BELOW
          
          path = 'phonepe_pulse_data/data/map/user/hover/country/india/state'
          map_state_names = os.listdir(path)
          Map_Data = {'state':[],'year':[],'quater':[],'map_user_district':[],'map_registered_users':[],'map_appopens':[]}

          for i in map_state_names:
               map_state_path   = path + '/' + i + '/'
               map_states_years = os.listdir(map_state_path)
          for year in map_states_years:
               file_path  = map_state_path + year + '/'
               year_files = os.listdir(file_path)
          for j in year_files:
               f = file_path + j
               data = open(f,'r')
               file_ = json.load(data)
               for z in file_['data']["hoverData"]:
                    state_name = i
                    Year = year
                    q = int(j.strip('.json'))
                    Map_User_District = z
                    Map_Registered_Users = file_['data']["hoverData"][z]['registeredUsers']
                    Map_appopens = file_['data']["hoverData"][z]['appOpens']

                    Map_Data['state'].append(state_name)
                    Map_Data['year'].append(Year)
                    Map_Data['quater'].append(q)
                    Map_Data['map_user_district'].append(Map_User_District)
                    Map_Data['map_registered_users'].append(Map_Registered_Users)
                    Map_Data['map_appopens'].append(Map_appopens)


          Map_User_df = pd.DataFrame(Map_Data)
          # print(Map_User_df.columns)


                                  #   TOP TRANSACTION DISTRICT AND STATE

          # PATH OF TOP TRANSACTION  MENTIONED BELOW

          path = 'phonepe_pulse_data/data/top/transaction/country/india/state'

          top_states_names = os.listdir(path)

          Top_data = {'state':[],'year':[],'quater':[],'top_transaction_district':[],'top_transaction_type':[],'top_transaction_count':[],'top_transaction_amount':[]}


          for i in top_states_names:
               top_state_path   = path + '/' + i + '/'
               top_states_years = os.listdir(top_state_path)
          for year in top_states_years:
               file_path  = top_state_path + year + '/'
               year_files = os.listdir(file_path)
          for j in year_files:
               f = file_path + j
               data = open(f,'r')
               file_ = json.load(data)
               for z in range(len(file_['data']["districts"])):
                    state_name = i
                    Year = year
                    q = int(j.strip('.json'))
                    Top_Transaction_District = file_['data']["districts"][z]["entityName"]
                    Top_Transaction_Type = file_['data']["districts"][z]["metric"]["type"]
                    Top_Transaction_Count = file_['data']["districts"][z]["metric"]["count"]
                    Top_Transaction_Amount = file_['data']["districts"][z]["metric"][ "amount"]
                    Top_data['state'].append(state_name)
                    Top_data['year'].append(Year)
                    Top_data['quater'].append(q)
                    Top_data['top_transaction_district'].append(Top_Transaction_District )
                    Top_data['top_transaction_type'].append(Top_Transaction_Type)
                    Top_data['top_transaction_count'].append(Top_Transaction_Count)
                    Top_data['top_transaction_amount'].append(Top_Transaction_Amount)
          
          Top_transaction_df_dist = pd.DataFrame(Top_data)
          # print(Top_transaction_df_dist.columns)


                              #   TOP TRANSACTION PINCODES
          
          Top_pincode_data = {'state':[],'year':[],'quater':[],'top_transaction_pincode':[],'top_transaction_type':[],'top_transaction_count':[],'top_transaction_amount':[]}

          for i in top_states_names:
               top_state_path   = path + '/' + i + '/'
               top_states_years = os.listdir(top_state_path)
          for year in top_states_years:
               file_path  = top_state_path + year + '/'
               year_files = os.listdir(file_path)
               for j in year_files:
                    f = file_path + j
                    data = open(f,'r')
                    file_ = json.load(data)
                    for z in range(len(file_['data']["pincodes"])):
                         state_name = i
                         Year = year
                         q = int(j.strip('.json'))
                         Top_Transaction_Pincode = file_['data']["pincodes"][z]["entityName"]
                         Top_Transaction_Type = file_['data']["pincodes"][z]["metric"]["type"]
                         Top_Transaction_Count = file_['data']["pincodes"][z]["metric"]["count"]
                         Top_Transaction_Amount = file_['data']["pincodes"][z]["metric"][ "amount"]
                         Top_pincode_data ['state'].append(state_name)
                         Top_pincode_data ['year'].append(Year)
                         Top_pincode_data ['quater'].append(q)
                         Top_pincode_data ['top_transaction_pincode'].append(Top_Transaction_Pincode)
                         Top_pincode_data ['top_transaction_type'].append(Top_Transaction_Type)
                         Top_pincode_data ['top_transaction_count'].append(Top_Transaction_Count)
                         Top_pincode_data ['top_transaction_amount'].append(Top_Transaction_Amount)

          Top_pincode_data_df = pd.DataFrame(Top_pincode_data)
          # print(Top_pincode_data_df.columns)


                                                # TOP USER 
          
          # PATH OF TOP USER   MENTIONED BELOW

          path = 'phonepe_pulse_data/data/top/user/country/india/state'

          top_states_names = os.listdir(path)

          Top_data = {'state':[],'year':[],'quater':[],'top_user_district':[],'top_registered_users':[]}

          for i in top_states_names:
               top_state_path   = path + '/' + i + '/'
               top_states_years = os.listdir(top_state_path)
               for year in top_states_years:
                    file_path  = top_state_path + year + '/'
                    year_files = os.listdir(file_path)
                    for j in year_files:
                         f = file_path + j
                         data = open(f,'r')
                         file_ = json.load(data)
                         for z in range(len(file_['data']["districts"])):
                              state_name = i
                              Year = year
                              q = int(j.strip('.json'))
                              Top_User_District = file_['data']["districts"][z]["name"]
                              TopUser_Registered_users = file_['data']["districts"][z]["registeredUsers"]
                              Top_data['state'].append(state_name)
                              Top_data['year'].append(Year)
                              Top_data['quater'].append(q)
                              Top_data['top_user_district'].append(Top_User_District)
                              Top_data['top_registered_users'].append(TopUser_Registered_users)

          Top_User_District_data = pd.DataFrame(Top_data)
          # print(Top_User_District_data.columns)

                                #    TOP USER PINCODES

          Top_data = {'state':[],'year':[],'quater':[],'top_user_pincode':[],'top_registered_users':[]}

          for i in top_states_names:
               top_state_path   = path + '/' + i + '/'
               top_states_years = os.listdir(top_state_path)
               for year in top_states_years:
                    file_path  = top_state_path + year + '/'
                    year_files = os.listdir(file_path)
               for j in year_files:
                    f = file_path + j
                    data = open(f,'r')
                    file_ = json.load(data)
                    for z in range(len(file_['data']["pincodes"])):
                         state_name = i
                         Year = year
                         q = int(j.strip('.json'))
                         Top_User_Pincode = file_['data']["pincodes"][z]["name"]
                         TopUser_Registered_users = file_['data']["pincodes"][z]["registeredUsers"]
                         Top_data['state'].append(state_name)
                         Top_data['year'].append(Year)
                         Top_data['quater'].append(q)
                         Top_data['top_user_pincode'].append(Top_User_Pincode)
                         Top_data['top_registered_users'].append(TopUser_Registered_users) 

          Top_Users_Pincode_data  = pd.DataFrame(Top_data)
          # print(Top_Users_Pincode_data.columns)

          df_names = [agg_transaction_df , agg_user_df,Map_df,Map_User_df,Top_transaction_df_dist,Top_pincode_data_df ,Top_User_District_data, Top_Users_Pincode_data]
          return df_names
     
     def data_load(self,df_names):

          DATABASE_URL = "postgresql://postgres:root@localhost:5432/phonepe_pulse"
          engine = sql.create_engine(DATABASE_URL)
          table_name = ['aggregated_transaction','aggregated_user','map_transaction','map_user','top_transaction_district_state','top_transaction_pincode','top_user_district','top_user_pincode']
          for i in range(len(table_name)):
                    df_names[i].to_csv(table_name[i]+'.csv')
                    df_names[i].to_sql(name=table_name[i], con=engine, if_exists='replace', index=False)
               
          return "Data Extraction Transformation And Load Process Successfully Done !!!"

# OBJECT CREATION FOR  Phonepe_pulse CLASS :   

object = Phonepe_pulse()
object.data_collection()
df_names = object.data_transformation()
ack = object.data_load(df_names)
print(ack)

# Note : Run this file one time for etl process otherwise you will face error while cloning the github repo.

                              # Process Done 

