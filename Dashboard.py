# Required Library

import  streamlit as st

import streamlit_option_menu

from streamlit_option_menu import *

import numpy as np

import pandas as pd

import psycopg2 as pg2

import matplotlib.pyplot as plt

from  plotly.subplots import make_subplots

import plotly_express as px

import plotly.graph_objects as go

from streamlit_vertical_slider import vertical_slider

import math
#____________________________________________________________________________________________________________________________________________________________________________

# POSTGRESQL CONNECTIVITY

praveen = pg2.connect(host='localhost', user='postgres', password='root', database='phonepe_pulse')
cursor = praveen.cursor()

#_____________________________________________________________________________________________________________________________________________________________________________

# PAGE CONFIGURATION

st.set_page_config(page_title='Phonepe Project By Praveen',layout="wide" )

#______________________________________________________________________________________________________________________________________________________________________________

                                                                    # PROGRAMS INITIATED

with st.sidebar:     # Navbar


    selected = option_menu(
                               menu_title="Phonepe Pulse",
                               options=['Intro','Transaction Type Analysis',"User Brand Analysis","SDP Analysis",'Time-based Analysis',],
                               icons = ['mic-fill','coin','person-circle','geo-alt-fill','hourglass-split'],
                               menu_icon='alexa',
                               default_index=0,
                           )

#_______________________________________________________________________________________________________________________________________________________________________________

                               #________________________________________Condition_____________________________________#


if selected == "Transaction Type Analysis":

        col1, col2 ,col3 , col4 , col5 ,col6= st.columns([6,7,8,8,7,5])

        st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)


        # FILTERS


        # 1) state

        cursor.execute('select distinct(state) from public.map_transaction')
        state_names = [i[0] for i in cursor.fetchall()]  # State Names
        with col5.expander(':violet[FILTER]'):

             state_selected = st.selectbox(':violet[CHOOSE STATE]', state_names)
             st.write("")


        # 2) year

        cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]


        # 3) Quater

        cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]


        # Year , Quater Combined
        with col6.expander(":violet[FILTER]"):
            year = st.select_slider(':violet[CHOOSE YEAR]', options=y_values)


        col6.write("")
        col6.write("")
        with col6.expander(":violet[FILTER]"):
            q = st.select_slider(':violet[CHOOSE QUATER]', options=q_values)



        # State Name

        with col1.expander(":violet[State]"):
            st.write("")
            st.subheader(state_selected)
            st.write("")

            st.markdown("<style>div.block-container{padding-top:4rem;}</style>", unsafe_allow_html=True)



#______________________________________________________________________________________________________________________________________________________________________________


                                                                      #__________METRICS __________#

        # Metrics 1 : Total Transaction Count

        query_1 = f"select sum(map_transaction_count) from public.map_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by state"
        cursor.execute(query_1)
        total_transaction_count = [int(i[0]) for i in cursor.fetchall()]
        with col2.expander(":violet[Transaction count]"):
            st.metric(label="", value=total_transaction_count[0],
                        delta=total_transaction_count[0]/100)

        #_________________________________________________________________________________________________________________________________________________________________

        # Metrics 2 : Total Transaction Amount


        query_2 = f"select sum(map_transaction_amount) from public.map_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by state"
        cursor.execute(query_2)
        total_transaction_amount = [int(i[0]) for i in cursor.fetchall()]
        with col3.expander(":violet[Transaction Amount]"):
            st.metric(label="", value=total_transaction_amount[0],
                    delta=total_transaction_amount[0]/100)

        #__________________________________________________________________________________________________________________________________________________________________

        # Metrics 3 : Avg Transaction count

        query_1 = f"select avg(map_transaction_amount) from public.map_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by state"
        cursor.execute(query_1)
        total_transaction_count = [int(i[0]) for i in cursor.fetchall()]
        with col4.expander(":violet[Average Amount]"):
           st.metric(label="", value=total_transaction_count[0],
                    delta=total_transaction_count[0]/100)

#___________________________________________________________________________________________________________________________________________________________________

                                                                      #____________CHARTS___________#


        c1,c2,c3 = st.columns([4,8,2])

        c2.title(":violet[Transaction Type Analysis]")  # Title
        c2.write("")
        c2.write("")

        #______________________________________________________________________________________________________________________________________________________________________

        col1 , col2 = st.columns([10,10])

        # PIE Chart : Total Transaction Type By Count

        # Pie 1 : Total Transaction Type By Count

        query_3 = f"select  agg_transaction_type , sum(agg_transaction_count)as Total_Transaction from public.aggregated_transaction where year = {year} and quater = {q} and state = '{state_selected}' group by agg_transaction_type;"
        cursor.execute(query_3)
        total_transaction_type_by_amount = [i for i in cursor.fetchall()]
        df = pd.DataFrame(total_transaction_type_by_amount, columns=['Transaction Type',"Transaction Count"])
        pie = px.pie(df, names='Transaction Type', values='Transaction Count', hole=0.6,color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb','#CA8DE1' ])   # change color
        pie.update_traces(textposition='outside')
        pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        with col1.expander("Total Transaction Count By Transaction Type"):

             st.plotly_chart(pie, theme=None, use_container_width=True)


        #______________________________________________________________________________________________________________________________________________________________________



        # Pie 2 : Total Transaction Type By Amount

        query_3 = f"select  agg_transaction_type , sum(agg_transaction_amount)as Total_Transaction from public.aggregated_transaction where year = {year} and quater = {q} and state = '{state_selected}' group by agg_transaction_type;"
        cursor.execute(query_3)
        total_transaction_type_by_amount = [i for i in cursor.fetchall()]
        df = pd.DataFrame(total_transaction_type_by_amount, columns=['Transaction Type',"Transaction Amount"])
        pie = px.pie(df, names='Transaction Type', values='Transaction Amount', hole=0.6,color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb','#CA8DE1' ])   # change color
        pie.update_traces(textposition='outside')
        pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        with col2.expander("Total Transaction Amount By Transaction Type"):

             st.plotly_chart(pie, theme=None, use_container_width=True)
#_______________________________________________________________________________________________________________________________________________________________________________

elif selected == "User Brand Analysis":

    col1, col2, col3, col4  = st.columns([7, 7, 7, 7])
    st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)

                                                                             #__________FILTERS___________#

    # 1) Year
    cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
    y_values = [i[0] for i in cursor.fetchall()]

    # 2) Quater
    cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
    q_values = [i[0] for i in cursor.fetchall()]
    with col4.expander(":violet[FILTER]"):
        year = st.select_slider(':violet[CHOOSE YEAR]', options=y_values)
        q = st.select_slider(':violet[CHOOSE QUATER]', options=q_values)
    col4.write("")

    # 3) State
    cursor.execute('select distinct(state) from public.map_transaction order by state desc')
    state_names = [i[0] for i in cursor.fetchall()]  # State Names
    with col4.expander(":violet[FILTER]"):
        state_selected = st.selectbox(':violet[CHOOSE STATE]', state_names)

    col4.write("")


    # 4) Brand

    cursor.execute(f"select distinct(agg_users_brand) from public.aggregated_user where agg_users_brand!='Not Mentioned' order by agg_users_brand  ")
    y_values = [i[0] for i in cursor.fetchall()]
    with col4.expander(":violet[FILTER]"):
        brand = st.selectbox(':violet[CHOOSE BRAND]', options=y_values)
        st.write("")

#_____________________________________________________________________________________________________________________________________________________________________________

                                    #_____________________________METRICS______________________#

    # State Name

    with col1.expander(":violet[STATE]"):
        st.write("")
        st.write("")
        st.write("")
        st.subheader(state_selected)
        col1.write("")




    # metrics 1: Total User Registered:

    query_5 = f"select sum(registered_users) from public.aggregated_user where state = '{state_selected}'  and year = '{year}' group by state;"

    cursor.execute(query_5)

    total_reg_user = [i[0] for i in cursor.fetchall()]

    with col2.expander(":violet[Total (RU)  Year-Wise]"):
          st.metric('', int(total_reg_user[0]), delta=int(total_reg_user[0]))





    #_____________________________________________________________________________________________________________________________________________________________________

    # Metrices 2 : Appopens

    query_6 = f"select  sum(agg_users_appopens) from public.aggregated_user where state = '{state_selected}' and year = '{year}' group by state"
    cursor.execute(query_6)

    total_app_opens = [i[0] for i in cursor.fetchall()]

    with col3.expander(':violet[USER APPOPENS (Y)]'):
      st.metric('', int(total_app_opens[0]), delta=int(total_app_opens[0]))

    #________________________________________________________________________________________________________________________________________________________________________

      # metrics 3: Total User Registered:

    query_5 = f"select sum(registered_users) from public.aggregated_user where state = '{state_selected}' and quater = {q} and year = '{year}' group by state;"

    cursor.execute(query_5)

    total_reg_user = [i[0] for i in cursor.fetchall()]

    with col2.expander(":violet[Total (RU) Quater-Wise]"):
          st.metric('', int(total_reg_user[0]), delta=int(total_reg_user[0]))

    #__________________________________________________________________________________________________________________________________________________________________________
    # Metrices 4 : Appopens (q)

    query_6 = f"select  sum(agg_users_appopens) from public.aggregated_user where state = '{state_selected}' and quater = {q} and year = '{year}' group by state"
    cursor.execute(query_6)
    total_app_opens = [i[0] for i in cursor.fetchall()]
    with col3.expander(':violet[USER APPOPENS (Q)]'):
      st.metric('', int(total_app_opens[0]), delta=int(total_app_opens[0]))

   #___________________________________________________________________________________________________________________________________________________________________________

    # Metrics 5 : Total User Registered till now

      query_5 = f"select sum(registered_users) from public.aggregated_user ;"
      cursor.execute(query_5)
      total_reg_user = [i[0] for i in cursor.fetchall()]
      with col1.expander(":violet[Total (RU) Till Date (2022)]"):
          st.metric('', int(total_reg_user[0]), delta=int(total_reg_user[0]))
          col1.write("")



    #____________________________________________________________________________________________________________________________________________________________________________

      # Metrices 4 : Appopens (q)

    query_6 = f"select  sum(agg_users_appopens) from public.aggregated_user;"
    cursor.execute(query_6)
    total_app_opens = [i[0] for i in cursor.fetchall()]
    with col1.expander(':violet[Total Appopens Till Date (2022)]'):
          st.metric('', int(total_app_opens[0]), delta=int(total_app_opens[0]))

    #_____________________________________________________________________________________________________________________________________________________________________________

    c1,c2,c3 = st.columns([4,8,2])
    c2.title(":violet[Brand Analysis In State-Wise]")
    c2.write("")
    c2.write('')
   #______________________________________________________________________________________________________________________________________________________________________________

                                                                                        #_______CHARTS_______#

    # 1) Top 10 Brand By State Registered Users

    col1,col2 = st.columns([7,7])

    query=f"select agg_users_brand,sum(agg_users_count) as val from public.aggregated_user where year = '{year}'  and quater = {q} and state = '{state_selected}' group by agg_users_brand order by val desc limit 10;"
    cursor.execute(query)
    res = [i for i in cursor.fetchall()]
    df = pd.DataFrame(res,columns=['Brand','Registered Users'])
    fig = px.bar(df, x="Brand", y="Registered Users")
    fig.update_layout(title_x=1)
    fig.update_layout(
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        xaxis_title_font=dict(color='#a7269e'),
        yaxis_title_font=dict(color='#a7269e')
    )
    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                      hoverlabel_font_color="#F500E6")
    fig.update_traces(marker_color='#d450b0')
    with col1.expander("Top 10 Brand Registered Users By State"):
         st.plotly_chart(fig, theme=None, use_container_width=True)

    #______________________________________________________________________________________________________________________________________________________________________________

    # 2) Top 10 States By brand

    query_1 = f"select state,sum(agg_users_count) as val from public.aggregated_user where year = '{year}'  and quater = {q} and agg_users_brand = '{brand}' group by state order by val desc limit 10;"

    cursor.execute(query_1)
    res = [i for i in cursor.fetchall()]
    df = pd.DataFrame(res, columns=['State', 'Registered Users'])
    fig = px.bar(df, x="State", y="Registered Users")
    fig.update_layout(title_x=1)
    fig.update_layout(
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        xaxis_title_font=dict(color='#a7269e'),
        yaxis_title_font=dict(color='#a7269e')
    )
    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                      hoverlabel_font_color="#F500E6")
    fig.update_traces(marker_color='#d450b0')
    with col2.expander("Top 10 States Registered Users By Brand"):
        st.plotly_chart(fig, theme=None, use_container_width=True)
#____________________________________________________________________________________________________________________________________________________________

elif selected == "SDP Analysis":

    with st.sidebar:
        selected_1 = option_menu(
            menu_title="",
            options=['Choose Option', 'Transaction', "User"],
            icons=['', 'coin', 'person-circle'],
            default_index=0,
        )

    if selected_1 == 'Transaction':

        # info :
        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[State Transactions Analysis]')
        col2.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

    #_____________________________________________________________________________________________________________________________

                                                     #____________FILTERS___________#

    col1,col2,col3,col4,col5 = st.columns([7,7,7,7,7])

    # 1) Year
    cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
    y_values = [i[0] for i in cursor.fetchall()]

    # 2) Quater
    cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
    q_values = [i[0] for i in cursor.fetchall()]


    # 3) State
    cursor.execute('select distinct(state) from public.map_transaction order by state desc')
    state_names = [i[0] for i in cursor.fetchall()]  # State Names

    col5.write("")
    with col5.expander(":violet[FILTER]"):
        st.write("")
        state_selected = st.selectbox(':violet[CHOOSE STATE]', state_names)
    with col5.expander(":violet[FILTER]"):
        st.write("")
        year = st.select_slider(':violet[CHOOSE YEAR]', options=y_values)
        st.write("")
        q = st.select_slider(':violet[CHOOSE QUATER]', options=q_values)
        st.write("")
        order = st.selectbox(":violet[CHOOSE ORDER]",['Top','Bottom'])


    #_________________________________________________________________________________________________________________________________

                                                      #________________METRICS__________________#

    # 1) Metric  : Top State By Amount
    query = f"select state , sum(top_transaction_amount) as val from public.top_transaction_district_state  where year= '{year}' and quater= {q} group by state order by val desc limit 1;"
    cursor.execute(query)
    res = [i[0] for i in cursor.fetchall()]
    cursor.execute(query)
    res1=[i[1] for i in cursor.fetchall()]
    with col1.expander(":violet[Top State By Amount]"):
        st.metric("",value=res[0],delta=math.ceil(res1[0]))

    #________________________________________________________________________________________________________________________________________________________________________________________

    # 2) Metric  : Top State By Count

    Query = f"select state , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val desc limit 1;"
    cursor.execute(Query)
    res = [i[0] for i in cursor.fetchall()]    # Name
    cursor.execute(Query)
    res1 = [i[1] for i in cursor.fetchall()]   # Count
    with col2.expander(":violet[Top State By Count]"):
        st.metric("", value=res[0], delta=math.ceil(res1[0]))

    #______________________________________________________________________________________________________________________________________________________________________________________________

    # 3) Metric  : Current State By Amount

    Query_1 = f"select state , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater = {q} and state = '{state_selected}' group by state;"

    cursor.execute(Query_1)
    res = [i[0] for i in cursor.fetchall()]  # Name
    cursor.execute(Query_1)
    res1 = [i[1] for i in cursor.fetchall()]  # Count
    with col3.expander(":violet[Current State By Amount]"):
        st.metric("", value=res[0], delta=math.ceil(res1[0]))

    #_______________________________________________________________________________________________________________________________________________________________________________________________________

    # 4) Metric  : Current State By Count

        Query_1 = f"select state , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater = {q} and state = '{state_selected}' group by state;"

        cursor.execute(Query_1)
        res = [i[0] for i in cursor.fetchall()]  # Name
        cursor.execute(Query_1)
        res1 = [i[1] for i in cursor.fetchall()]  # Count
        with col4.expander(":violet[Current State By Count]"):
            st.metric("", value=res[0], delta=math.ceil(res1[0]))

    #____________________________________________________________________________________________________________________________________________________________________________________________________


                                                                                  #___________CHARTS___________#

    col1,col2 = st.columns([7,7])

    #_____________________________________________________________________________________________________________________________________________________________________________

    # 1) Bar : Top/Bottom  1o States By Count

    if order == 'Bottom':
        query=f"select state , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val asc limit 10;"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['State', 'Transaction Count'])
        fig = px.bar(df, x="State", y="Transaction Count")
        fig.update_layout(title_x=1)
        fig.update_layout(
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            xaxis_title_font=dict(color='#a7269e'),
            yaxis_title_font=dict(color='#a7269e')
        )
        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        fig.update_traces(marker_color='#d450b0')
        with col1.expander("Bottom 10 State By Transaction Count"):
            st.plotly_chart(fig, theme=None, use_container_width=True)

    elif order == "Top":
            query = f"select state , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val desc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State', 'Transaction Count'])
            fig = px.bar(df, x="State", y="Transaction Count")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                xaxis_title_font=dict(color='#a7269e'),
                yaxis_title_font=dict(color='#a7269e')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col1.expander("Top 10 State By Transaction Count"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

    #____________________________________________________________________________________________________________________________________________________________________________________________________

    # 1) Bar : Top/Bottom  1o States By Count

    if order == 'Bottom':
        query=f"select state , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val asc limit 10;"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['State', 'Transaction Amount'])
        fig = px.bar(df, x="State", y="Transaction Amount")
        fig.update_layout(title_x=1)
        fig.update_layout(
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            xaxis_title_font=dict(color='#a7269e'),
            yaxis_title_font=dict(color='#a7269e')
        )
        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        fig.update_traces(marker_color='#d450b0')
        with col2.expander("Bottom 10 State By Transaction Amount"):
            st.plotly_chart(fig, theme=None, use_container_width=True)

    elif order == "Top":
            query = f"select state , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by state order by val desc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State', 'Transaction Amount'])
            fig = px.bar(df, x="State", y="Transaction Amount")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                xaxis_title_font=dict(color='#a7269e'),
                yaxis_title_font=dict(color='#a7269e')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col2.expander("Top 10 State By Transaction Amount"):
                st.plotly_chart(fig, theme=None, use_container_width=True)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")


#_____________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                              #_______DISTRICTS-WISE ANALYSIS___________#

    # info :
    col1, col2, col3, = st.columns([4, 10, 1])
    col2.title(':violet[District Transactions Analysis]')
    col2.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

    #___________________________________________________________________________________________________________________________________________________________________________________________________

                                                                     #__________FILTERS____________#\

    col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])


    # 1) Year
    cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
    y_values = [i[0] for i in cursor.fetchall()]

    # 2) Quater
    cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
    q_values = [i[0] for i in cursor.fetchall()]

    # 3) State
    cursor.execute('select distinct(top_transaction_district) from public.top_transaction_district_state order by top_transaction_district;')
    dist_names = [i[0] for i in cursor.fetchall()]  # dist Names

    col5.write("")
    with col5.expander(":violet[FILTER]"):
        st.write("")
        dist_selected = st.selectbox(':violet[CHOOSE DISTRICT]', dist_names)
    with col5.expander(":violet[FILTER]"):
        st.write("")
        year = st.select_slider(':violet[YEAR]', options=y_values)
        st.write("")
        q = st.select_slider(':violet[QUATER]', options=q_values)
        st.write("")
        order = st.selectbox(":violet[ORDER]", ['Top', 'Bottom'])

    #_________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                      #_____________METRICS___________#

    # 1) Metric  : Top District By Amount
    query = f"select top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state  where year= '{year}' and quater= {q} group by top_transaction_district order by val desc limit 1;"
    cursor.execute(query)
    res = [i[0] for i in cursor.fetchall()]
    cursor.execute(query)
    res1 = [i[1] for i in cursor.fetchall()]
    with col1.expander(":violet[Top District By Amount]"):
        st.metric("", value=res[0], delta=math.ceil(res1[0]))

    # ________________________________________________________________________________________________________________________________________________________________________________________

    # 2) Metric  : Top district  By Count

    Query = f"select top_transaction_district , sum(top_transaction_count) as val from public.top_transaction_district_state  where year= '{year}' and quater= {q} group by top_transaction_district order by val desc limit 1;"
    cursor.execute(Query)
    res = [i[0] for i in cursor.fetchall()]  # Name
    cursor.execute(Query)
    res1 = [i[1] for i in cursor.fetchall()]  # Count
    with col2.expander(":violet[Top State By Count]"):
        st.metric("", value=res[0], delta=math.ceil(res1[0]))

    # ______________________________________________________________________________________________________________________________________________________________________________________________

    # 3) Metric  : Current State By Amount

    Query_1 = f"select  top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state  where year= '{year}' and quater = {q} and  top_transaction_district = '{dist_selected}' group by  top_transaction_district;"

    cursor.execute(Query_1)
    res = [i[0] for i in cursor.fetchall()]  # Name

    cursor.execute(Query_1)
    res1 = [i[1] for i in cursor.fetchall()]  # Count
    with col3.expander(":violet[Current District By Amount]"):
        st.metric("", value=res[0], delta=math.ceil(res1[0]))

    # _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

    # # 4) Metric  : Current State By Count

    Query_1 = f"select  top_transaction_district , sum(top_transaction_count) as val from public.top_transaction_district_state  where year= '{year}' and quater = {q} and  top_transaction_district = '{dist_selected}' group by  top_transaction_district;"

    cursor.execute(Query_1)
    res = [i[0] for i in cursor.fetchall()]  # Name
    cursor.execute(Query_1)
    res1 = [i[1] for i in cursor.fetchall()]  # Count
    with col4.expander(":violet[Current State By Count]"):
        st.metric("", value=res[0], delta=math.ceil(res1[0]))

    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________



                                                                                  #___________CHARTS___________#

    col1,col2 = st.columns([7,7])

    #_____________________________________________________________________________________________________________________________________________________________________________

    # 1) Bar : Top/Bottom  1o districts By Count

    if order == 'Bottom':
        query=f"select top_transaction_district , sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by top_transaction_district order by val asc limit 10;"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['District', 'Transaction Count'])
        fig = px.bar(df, x="District", y="Transaction Count")
        fig.update_layout(title_x=1)
        fig.update_layout(
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            xaxis_title_font=dict(color='#a7269e'),
            yaxis_title_font=dict(color='#a7269e')
        )
        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        fig.update_traces(marker_color='#d450b0')
        with col1.expander("Bottom 10 District By Transaction Count"):
            st.plotly_chart(fig, theme=None, use_container_width=True)

    elif order == "Top":
            query = f"select top_transaction_district, sum(top_transaction_count) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by top_transaction_district order by val desc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State', 'Transaction Count'])
            fig = px.bar(df, x="State", y="Transaction Count")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                xaxis_title_font=dict(color='#a7269e'),
                yaxis_title_font=dict(color='#a7269e')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col1.expander("Top 10 District By Transaction Count"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

    #____________________________________________________________________________________________________________________________________________________________________________________________________

    # 2) Bar : Top/Bottom  1o districts By amount

    if order == 'Bottom':
        query=f"select top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by top_transaction_district  order by val asc limit 10;"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['District', 'Transaction Amount'])
        fig = px.bar(df, x="District", y="Transaction Amount")
        fig.update_layout(title_x=1)
        fig.update_layout(
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            xaxis_title_font=dict(color='#a7269e'),
            yaxis_title_font=dict(color='#a7269e')
        )
        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        fig.update_traces(marker_color='#d450b0')
        with col2.expander("Bottom 10 Districts By Transaction Amount"):
            st.plotly_chart(fig, theme=None, use_container_width=True)

    elif order == "Top":
            query = f"select top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state where year= '{year}' and quater= {q} group by top_transaction_district order by val desc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['District', 'Transaction Amount'])
            fig = px.bar(df, x="District", y="Transaction Amount")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                xaxis_title_font=dict(color='#a7269e'),
                yaxis_title_font=dict(color='#a7269e')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col2.expander("Top 10 District By Transaction Amount"):
                st.plotly_chart(fig, theme=None, use_container_width=True)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                  # ________PINCODE TRANSACTION ANALYSIS___________#


    col1, col2, col3, = st.columns([4, 10, 1])
    col2.title(':violet[Pincode Transactions Analysis]')

    st.write("")
    st.write("")

    #______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                    #_____________FILTER_____________________#

    col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

    # 1) Year
    cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
    y_values = [i[0] for i in cursor.fetchall()]

    # 2) Quater
    cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
    q_values = [i[0] for i in cursor.fetchall()]

    with col4.expander(":violet[FILTER]"):
        st.write("")
        year = st.select_slider(':violet[SELECT YEAR]', options=y_values)
        st.write("")
        q = st.select_slider(':violet[SELECT QUATER]', options=q_values)
    with col2.expander(":violet[FILTER]"):

        st.write("")
        order = st.selectbox(":violet[SELECT ORDER]", ['Top', 'Bottom'])

   #______________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                          #____________CHARTS____________#


    col1,col2 = st.columns([7,7])


     # 1)  Top 10 Pincode By Transaction Amount


    if order == "Top":
        query_pin = f"select top_transaction_pincode , sum(top_transaction_amount) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} group by  top_transaction_pincode order by val desc limit 10;"
        cursor.execute(query_pin)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Pincode', 'Transaction Amount'])
        pie = px.pie(df, names='Pincode', values='Transaction Amount', hole=0.7,
                     color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                              '#CA8DE1'])  # change color
        pie.update_traces(textposition='outside')
        with col1.expander("Top 10 Pincode By Transaction Amount"):
             st.plotly_chart(pie, theme=None, use_container_width=True)

    elif order == "Bottom":
        query_pin = f"select top_transaction_pincode , sum(top_transaction_amount) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} group by  top_transaction_pincode order by val asc limit 10;"
        cursor.execute(query_pin)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Pincode', 'Transaction Amount'])
        pie = px.pie(df, names='Pincode', values='Transaction Amount', hole=0.7,
                     color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                              '#CA8DE1'])  # change color
        pie.update_traces(textposition='outside')
        with col1.expander("Bottom 10 Pincode By Transaction Amount"):
           st.plotly_chart(pie, theme=None, use_container_width=True)


    #_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________

    # 2) Top 10 Pincode By Transaction Count

    if order == 'Top':
        query_pin_1 = f"select top_transaction_pincode , sum(top_transaction_count) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} group by  top_transaction_pincode order by val desc limit 10;"
        cursor.execute(query_pin_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Pincode', 'Transaction Count'])
        pie = px.pie(df, names='Pincode', values='Transaction Count', hole=0.7,
                     color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                              '#CA8DE1'])  # change color
        pie.update_traces(textposition='outside')
        with col2.expander("Top 10 Pincode By Transaction Count"):
             st.plotly_chart(pie, theme=None, use_container_width=True)

    if order == 'Bottom':
        query_pin_1 = f"select top_transaction_pincode , sum(top_transaction_count) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} group by  top_transaction_pincode order by val asc limit 10;"
        cursor.execute(query_pin_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Pincode', 'Transaction Count'])
        pie = px.pie(df, names='Pincode', values='Transaction Count', hole=0.7,
                     color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                              '#CA8DE1'])  # change color
        pie.update_traces(textposition='outside')
        with col2.expander("Bottom 10 Pincode By Transaction Count"):
              st.plotly_chart(pie, theme=None, use_container_width=True)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


                                                                     #_____________SDP Transaction Amount Concentration________________________#

    col1, col2, col3, = st.columns([2, 10, 1])

    col2.title(':violet[SDP Transaction Amount Concentration Analysis]')

    st.write("")
    st.write("")

    #___________________________________________________________________________________________________________________________________________________________________________________________________________________________________


                                                                                    #_______________FILTERS___________________#

    col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

    # 1) Year
    cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
    y_values = [i[0] for i in cursor.fetchall()]

    # 2) Quater
    cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
    q_values = [i[0] for i in cursor.fetchall()]

    with col4.expander(":violet[FILTER]"):
        st.write("")
        year = st.select_slider(':violet[Pick YEAR]', options=y_values)
        st.write("")
    with col2.expander(":violet[FILTER]"):
        q = st.select_slider(':violet[Pick QUATER]', options=q_values)

    # with col2.expander(":violet[FILTER]"):
    #     st.write("")
    #     order = st.selectbox(":violet[ ORDER]", ['Top', 'Bottom'])

   #__________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                  #__________CHARTS_______________#


    col1,col2,col3 = st.columns([7,7,7])

                                                                                                                #_________State_Level__________#

    querys_top = f"select sum(top_transaction_amount) as val from public.top_transaction_district_state where year = '{year}' and quater = {q}  group by state order by val desc limit 10;"
    cursor.execute(querys_top)
    res = [i for i in cursor.fetchall()]
    df_1 = pd.DataFrame(res, columns=['Amount Top'])

    querys_bottom = f"select  sum(top_transaction_amount) as val from public.top_transaction_district_state where year = '{year}' and quater ={q} and state not in (select state  from public.top_transaction_district_state where year = '{year}' and quater ={q}  group by state order by  sum(top_transaction_amount) desc limit 10) group by state order by val desc ;"

    cursor.execute(querys_bottom)
    res = [i for i in cursor.fetchall()]
    df_2 = pd.DataFrame(res, columns=['Amount Bottom'])

    state_last = {"Names": [], 'value': []}
    state_last['Names'].append("Top 10 States")
    state_last['Names'].append("Other States")

    state_last['value'].append(int(sum(df_1['Amount Top'])))
    state_last['value'].append(int(sum(df_2['Amount Bottom'])))

    df = pd.DataFrame(state_last)

    pie = px.pie(df, names='Names', values='value', labels={'Names': 'District Type', 'value': 'Transaction Amount'},
                 hole=0.7,
                 color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
    pie.update_traces(textposition='outside')

    with col1.expander("TOP 10 STATES :orange[Vs]  OTHER STATES"):
        st.plotly_chart(pie, theme=None, use_container_width=True)

    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                          #______________Districts Level__________#

        # Metrics 3 : District Transaction Concentration :

    query_top = f"select sum(top_transaction_amount) as val  from public.top_transaction_district_state where year = '{year}' and quater = {q} group by top_transaction_district order by val desc limit 10;"
    cursor.execute(query_top)
    res = [i for i in cursor.fetchall()]
    df = pd.DataFrame(res, columns=['Amount Top'])
    last = {'Names': [], 'value': []}
    last['Names'].append("Top 10 Districts")
    last['value'].append(int(sum(df['Amount Top'])))

    query_bottom = f"select  sum(top_transaction_amount)  from public.top_transaction_district_state where year = '{year}' and quater ={q} and top_transaction_district not in (select top_transaction_district   from public.top_transaction_district_state where year = '{year}' and quater ={q}  group by top_transaction_district order by sum(top_transaction_amount) desc limit 10) group by top_transaction_district order by sum(top_transaction_amount) desc ;"
    cursor.execute(query_bottom)
    res = [i for i in cursor.fetchall()]
    df = pd.DataFrame(res, columns=['Amount Bottom'])


    last['Names'].append("Other Districts")
    last['value'].append(int(sum(df['Amount Bottom'])))

    df = pd.DataFrame(last)  # '#a7269e', '#d450b0', '#eb8adb',
    pie = px.pie(df, names='Names', values='value', hole=0.7,
                 labels={'Names': 'District Type', 'value': 'Transaction Amount'},
                 color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
    pie.update_traces(textposition='outside')

    with col2.expander("TOP 10 DISTRICTS :orange[Vs]  OTHER DISTRICTS"):
          st.plotly_chart(pie, theme=None, use_container_width=True)

    #______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                               #____________PINCODE_____________#

    query_top = f"select sum(top_transaction_amount) as val  from public.top_transaction_pincode where year = '{year}' and quater = {q} group by top_transaction_pincode order by val desc limit 10;"
    cursor.execute(query_top)
    res = [i for i in cursor.fetchall()]
    df = pd.DataFrame(res, columns=['Amount Top'])
    last = {'Names': [], 'value': []}
    last['Names'].append("Top 10 Pincodes")
    last['value'].append(int(sum(df['Amount Top'])))

    query_bottom = f"select  sum(top_transaction_amount)  from public.top_transaction_pincode where year = '{year}' and quater ={q} and top_transaction_pincode not in (select top_transaction_pincode   from public.top_transaction_pincode where year = '{year}' and quater ={q} group by top_transaction_pincode  order by sum(top_transaction_amount) desc limit 10) group by top_transaction_pincode order by sum(top_transaction_amount) ;"
    cursor.execute(query_bottom)
    res = [i for i in cursor.fetchall()]
    df = pd.DataFrame(res, columns=['Amount Bottom'])

    last['Names'].append("Other Pincodes")
    last['value'].append(int(sum(df['Amount Bottom'])))

    df = pd.DataFrame(last)
    pie = px.pie(df, names='Names', values='value', hole=0.7,
                 labels={'Names': 'District Type', 'value': 'Transaction Amount'},
                 color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
    pie.update_traces(textposition='outside')

    with col3.expander("TOP 10 PINCODES :orange[Vs]  OTHER PINCODES"):
        st.plotly_chart(pie, theme=None, use_container_width=True)

#_______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________








