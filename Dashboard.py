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
                               options=['Intro','View Data Source','Transaction Type Analysis',"User Brand Analysis","SDP Analysis",'Time-based Analysis','Insights'],
                               icons = ['mic-fill',"database-fill",'coin','person-circle','geo-alt-fill','hourglass-split','clipboard-data-fill'],
                               menu_icon='alexa',
                               default_index=0,
                           )

#__________________________________________________________________________________________________________________________________________________________________________________________---

                                     #________________________________________Condition_____________________________________#


if selected == "Transaction Type Analysis":

        col1, col2 ,col3 , col4 , col5 ,col6= st.columns([6,7,8,8,7,7])

        st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)


        # FILTERS


        # 1) state

        cursor.execute('select distinct(state) from public.map_transaction order by state desc')
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
        col6.write("")
        with col6.expander(":violet[FILTER]"):
            year = st.select_slider(':violet[CHOOSE YEAR]', options=y_values)
        with col6.expander(':violet[FILTER]'):
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
            st.metric(label="", value=f"{round(((total_transaction_count[0]/100000)/10),2)}M",
                        delta=total_transaction_count[0])

        #_________________________________________________________________________________________________________________________________________________________________

        # Metrics 2 : Total Transaction Amount


        query_2 = f"select sum(map_transaction_amount) from public.map_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by state"
        cursor.execute(query_2)
        total_transaction_amount = [int(i[0]) for i in cursor.fetchall()]
        with col3.expander(":violet[Transaction Amount]"):
            st.metric(label="", value=f"{round(((total_transaction_amount[0]/100000)/10),2)}M",
                    delta=total_transaction_amount[0])

        #__________________________________________________________________________________________________________________________________________________________________

        # Metrics 3 : Avg Transaction count

        query_1 = f"select avg(map_transaction_amount) from public.map_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by state"
        cursor.execute(query_1)
        total_transaction_count = [int(i[0]) for i in cursor.fetchall()]
        with col4.expander(":violet[Average Amount]"):
           st.metric(label="", value=f"{round(((total_transaction_count[0]/100000)/10),2)}M",
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
#_______________________________________________________________________________________________________________________________________________________________________________________________

elif selected == "User Brand Analysis":


    col1, col2, col3,col5 = st.columns([7, 7, 7,6])

    st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)

                                                                             #__________FILTERS___________#

    # 1) Year
    cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
    y_values = [i[0] for i in cursor.fetchall()]

    # 2) Quater
    cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
    q_values = [i[0] for i in cursor.fetchall()]
    with col5.expander(":violet[FILTER]"):
        year = st.select_slider(':violet[CHOOSE YEAR]', options=y_values)
        q = st.select_slider(':violet[CHOOSE QUATER]', options=q_values)


    # 3) State
    cursor.execute('select distinct(state) from public.map_transaction order by state desc')
    state_names = [i[0] for i in cursor.fetchall()]  # State Names



    # 4) Brand

    cursor.execute(f"select distinct(agg_users_brand) from public.aggregated_user where agg_users_brand!='Not Mentioned' order by agg_users_brand  ")
    y_values = [i[0] for i in cursor.fetchall()]

    with col5.expander(":violet[FILTER]"):
        state_selected = st.selectbox(':violet[CHOOSE STATE]', state_names)
        st.write("")
        st.write("")

#_____________________________________________________________________________________________________________________________________________________________________________

                                    #_____________________________METRICS______________________#

    # State Name

    with col1.expander(":violet[STATE]"):
        st.write("")
        st.write("")
        st.subheader(state_selected)
        st.write("")


    # metrics 1: Total User Registered:

    query_5 = f"select sum(registered_users) from public.aggregated_user where state = '{state_selected}'  and year = '{year}'   and quater = {q} group by state;"

    cursor.execute(query_5)

    total_reg_user = [i[0] for i in cursor.fetchall()]

    with col2.expander(":violet[Total (RU)  Year-Wise]"):
      st.metric('',f'{math.ceil((total_reg_user[0]/100000)/10)}M', delta=int(total_reg_user[0]))


    #_____________________________________________________________________________________________________________________________________________________________________

    # Metrices 2 : Appopens

    query_6 = f"select  sum(agg_users_appopens) from public.aggregated_user where state = '{state_selected}' and year = '{year}'  and quater = {q} group by state"
    cursor.execute(query_6)

    total_app_opens = [i[0] for i in cursor.fetchall()]

    with col3.expander(':violet[USER APPOPENS (Y)]'):
      st.metric('',f'{math.ceil((total_app_opens[0]/100000)/10)}M' , delta=int(total_app_opens[0]))

    st.write("")
    st.write("")
    st.write("")

   #______________________________________________________________________________________________________________________________________________________________________________

                                                                                        #_______CHARTS_______#


    col1,col2,col3,col4,col5 = st.columns([3,7,2,7,3])
    with col2.expander(":violet[FILTER]"):
        option = st.selectbox(":violet[Choose Option]", ['App Opens', 'Registered Users'])
    with col4.expander(':violet[FILTER]'):
        brand = st.selectbox(':violet[CHOOSE BRAND]', options=y_values)
    st.write("")
    st.write("")

    col1,col2 ,col3= st.columns([8,8,8])

    # 1 ) Quater  and appopens and RU in (filter year , state , year )

    if option == "Registered Users":
        query = f"select quater , sum(registered_users) from public.aggregated_user where year = '{year}' and agg_users_brand = '{brand}' and state = '{state_selected}'group by quater order by quater asc"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['Quater','Registered Users'])
        fig = px.bar(df, x="Quater", y="Registered Users")
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
        with col1.expander(f"{brand} brand in {state_selected} {option} Over The Quaters {year} "):
             st.plotly_chart(fig, theme=None, use_container_width=True)

    elif option == "App Opens":
        query = f"select quater , sum(agg_users_appopens) from public.aggregated_user where year = '2021' and agg_users_brand = 'Vivo' and state = 'tamil-nadu' group by quater order by quater asc"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['Quater','App Opens'])
        pie = px.pie(df, names='Quater', values='App Opens', hole=0.7,
                     color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                              '#CA8DE1'])  # change color

        pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6",
                          textposition='outside')

        with col1.expander(f"{brand} brand in {state_selected} {option} Over The Quaters of {year}"):
             st.plotly_chart(pie, theme=None, use_container_width=True)

    #______________________________________________________________________________________________________________________________________________________________________

    # 2) brand in RU /AP  over the year

    if option == "Registered Users":
        query = f"select year , sum(registered_users) from public.aggregated_user where  agg_users_brand = '{brand}' and state = '{state_selected}' group by year order by year  asc"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['Year','Registered Users'])
        fig = px.line(df, x="Year", y="Registered Users",markers='D')
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
        with col2.expander(f"{brand} brand in {state_selected} {option} Over The Years "):
             st.plotly_chart(fig, theme=None, use_container_width=True)

    elif option == "App Opens":
        query = f"select year , sum(agg_users_appopens) from public.aggregated_user where  agg_users_brand = 'Vivo' and state = 'tamil-nadu' group by year order by year  asc"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['Year','App Opens'])
        fig = px.line(df, x="Year", y="App Opens", markers='D')
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

        with col2.expander(f"{brand} brand in {state_selected} {option} Over The Year"):
             st.plotly_chart(fig, theme=None, use_container_width=True)



    # 3) State - wise Brand Engagement of Ao/Ru
    if option == "Registered Users":
        query = f"select state , sum(registered_users) as val from public.aggregated_user where year = '{year}' and quater = {q} and agg_users_brand = '{brand}' group by state order by val desc limit 10;"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['State','Registered Users'])

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
        with col3.expander(f"{brand} Brand {option} Over The Year {year} In India States "):
            st.plotly_chart(fig, theme=None, use_container_width=True)
    elif option == 'App Opens':

        query = f"select state , sum(agg_users_appopens) as val from public.aggregated_user where year = '{year}' and quater = {q} and agg_users_brand = '{brand}' group by state order by val desc limit 10;"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['State', 'App opens'])

        fig = px.bar(df, x="State", y="App opens")
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
        with col3.expander(f"{brand} Brand {option} Over The Year {year} In India States "):
            st.plotly_chart(fig, theme=None, use_container_width=True)
    st.write("")
    st.write('')
    st.write("")
    st.write('')
    st.write("")
    st.write('')
   #_____________________________________________________________________________________________________________________________________________________________
    col1,col2,col3 = st.columns([30,100,1])
    col2.header(":violet[Top 10 Brands By Registered Users in State]")
    st.write("")

    # 4) Top 10 brand in each state

    col1, col2, col3 = st.columns([1, 100, 1])
    query = f"select agg_users_brand , sum(agg_users_count) as val  from public.aggregated_user where year = '{year}' and quater = {q} and state = '{state_selected}' group by agg_users_brand order by val desc limit 10"
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
    with col2.expander(f"Top 10 Brands By Registered Users In  {state_selected} In The Year  {year} And {q}th Quater  "):
        st.plotly_chart(fig, theme=None, use_container_width=True)

#____________________________________________________________________________________________________

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

        pie = px.pie(df, names='Names', values='value', labels={'Names': 'State Type', 'value': 'Transaction Amount'},
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
                     labels={'Names': 'Pincode Type', 'value': 'Transaction Amount'},
                     color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
        pie.update_traces(textposition='outside')

        with col3.expander("TOP 10 PINCODES :orange[Vs]  OTHER PINCODES"):
            st.plotly_chart(pie, theme=None, use_container_width=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
    #_______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


                                                               #___________________Top 10 DP In State By Transaction Amount_______________#

        col1,col2,col3 = st.columns([2,8,1])


        col2.title(':violet[Top 10 DP In State By Transaction Amount]')
        st.write("")
        st.write("")

    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                          #___________FILTERS_______________#

        col1, col2, col3 ,col4, col5 = st.columns([5,5, 5,5,5])

    #_____________________________________________________________________________________________________________________________________________________
    # 1) State
        query="select distinct(state) from public.top_transaction_district_state order by state desc"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        with col1.expander(":violet[FILTER]"):
            state_selected =  st.selectbox(":violet[PICK STATE]",res)

    # 2) Districts and Pincodes

        with col2.expander(":violet[Filter]"):
            vary = st.selectbox(':violet[PICK OPTION]',['District','Pincode'])

    # 3) Amount and Count

        with col3.expander(":violet[Filter]"):
            Choice = st.selectbox(':violet[PICK CHOICE]', ['Amount', 'Count'])

    # 4) Year and Quater

        # 1) Year
        cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        with col4.expander(":violet[Filter]"):
            year = st.select_slider(":violet[Choose Year]", options=y_values)
            st.write("")
            q = st.select_slider(':violet[Choose Quater]', options=q_values)
        st.write("")
        st.write('')

    # 5) Top / Bottom 10

        with col5.expander(":violet[Filter]"):
            order = st.selectbox(":violet[Choose Order]",['desc','asc'])

#____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                           #_____CONDITION METRICS_____#
        col1,col2,col3  = st.columns([1,100,1])

        if vary == "District":
                 if Choice == "Amount":
                     query_1 = f"select top_transaction_district , sum(top_transaction_amount) as val from public.top_transaction_district_state where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_transaction_district order by val {order} limit 10;"
                     cursor.execute(query_1)
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

                 elif Choice == "Count":
                     query_1 = f"select top_transaction_district , sum(top_transaction_count) as val from public.top_transaction_district_state where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_transaction_district order by val {order} limit 10;"
                     cursor.execute(query_1)
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
                     with col2.expander("Top 10 District By Transaction Count"):
                         st.plotly_chart(fig, theme=None, use_container_width=True)





        elif vary == "Pincode":
                if Choice == "Amount":
                    query_pin = f"select top_transaction_pincode , sum(top_transaction_amount) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_transaction_pincode order by val {order} limit 10;"
                    cursor.execute(query_pin)
                    res = [i for i in cursor.fetchall()]
                    df = pd.DataFrame(res,columns=["Pincode","Transaction Amount"])
                    pie = px.pie(df, names='Pincode', values="Transaction Amount", hole=0.7,
                                 color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
                    pie.update_traces(textposition='outside')

                    pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                      hoverlabel_font_color="#F500E6")


                    with col2.expander("Top 10 Pincode By Transaction Amount"):
                        st.plotly_chart(pie, theme=None, use_container_width=True)

                elif Choice == "Count":
                    query_pin = f"select top_transaction_pincode , sum(top_transaction_count) as val from public.top_transaction_pincode where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_transaction_pincode order by val {order} limit 10;"
                    cursor.execute(query_pin)
                    res = [i for i in cursor.fetchall()]
                    df = pd.DataFrame(res, columns=["Pincode", "Transaction Count"])
                    pie = px.pie(df, names='Pincode', values="Transaction Count", hole=0.7,
                                 color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
                    pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                      hoverlabel_font_color="#F500E6")
                    pie.update_traces(textposition='outside')

                    with col2.expander("Top 10 Pincode By Transaction Count"):
                        st.plotly_chart(pie, theme=None, use_container_width=True)



    elif selected_1 == "User":


        #_________________________________________________________________________________________________________________________________________________________________

                                                                                              #____State Registered Users Analysis____#
        # info :
        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[State Registered Users Analysis]')
        st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)
        # __________________________________________________________________________________________________________________________________________________________________

                                                                                               # ____________FILTERS___________#

        col1, col3, col4, col5 ,col6 = st.columns([8,  8, 8, 8,6])

        # 1) Year
        cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        # 3) State
        cursor.execute('select distinct(state) from public.top_user_district order by state desc')
        state_names = [i[0] for i in cursor.fetchall()]  # State Names

        with col4.expander(":violet[FILTER]"):
            st.write("")
            state_selected = st.selectbox(':violet[CHOOSE STATE]', state_names)
            # st.write("")
            # st.write("")

        with col5.expander(":violet[FILTER]"):
            st.write("")
            year = st.select_slider(':violet[CHOOSE YEAR]', options=y_values)

            q = st.select_slider(':violet[CHOOSE QUATER]', options=q_values)

        with col6.expander(':violet[FILTER]'):
            st.write("")
            order = st.selectbox(":violet[CHOOSE ORDER]", ['Top', 'Bottom'])

    #_____________________________________________________________________________________________________________________________________________________________________________

                                                                    # ________________METRICS__________________#

    # 1) Metric  : Top State By RU

        query = f"select state , sum(top_registered_users) as val from public.top_user_district where year= '{year}' and quater= {q} group by state order by val desc limit 1;"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        cursor.execute(query)
        res1 = [i[1] for i in cursor.fetchall()]
        with col1.expander(":violet[Top State By Registered Users]"):
            # st.write("")
            st.metric("", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")

    # ________________________________________________________________________________________________________________________________________________________________________________________

    # 2) Metric  : Current State By RU

        Query_1 = f"select state , sum(top_registered_users) as val from public.top_user_district where year= '{year}' and quater= {q} and state = '{state_selected}' group by state order by val desc limit 1;"
        cursor.execute(Query_1)
        res = [i[0] for i in cursor.fetchall()]  # Name
        cursor.execute(Query_1)
        res1 = [i[1] for i in cursor.fetchall()]  # Count
        with col3.expander(":violet[Current State By Registered Users]"):
            st.metric("", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")

    #_______________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                    # ___________CHARTS___________#

        col1, col2,col3 = st.columns([1, 100,1])

    # _____________________________________________________________________________________________________________________________________________________________________________

    # 1) Bar : Top/Bottom  1o States By (RU)

        if order == 'Bottom':
            query = f"select state , sum(top_registered_users) as val from public.top_user_district where year= '{year}' and quater= {q} group by state order by val asc limit 10;"
            cursor.execute(query)
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
            with col2.expander("Bottom 10 State By Registered Users"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif order == "Top":
            query = f"select state , sum(top_registered_users) as val from public.top_user_district where year= '{year}' and quater= {q} group by state order by val desc limit 10;"
            cursor.execute(query)
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
            with col2.expander("Top 10 State By Registered Users"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

# ____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                         # _______DISTRICTS-WISE ANALYSIS___________#

            # info :
        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[District Registered Users Analysis]')
        col2.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)


    # ___________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                         # __________FILTERS____________#\

        col1, col3, col4, col5,col6 = st.columns([9,  8, 7, 7,6])

        # 1) Year
        cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        # 3) State
        cursor.execute(
            'select distinct(top_transaction_district) from public.top_transaction_district_state order by top_transaction_district;')
        dist_names = [i[0] for i in cursor.fetchall()]  # dist Names


        with col4.expander(":violet[FILTER]"):
            st.write("")
            # st.write("")
            dist_selected = st.selectbox(':violet[CHOOSE DISTRICT]', dist_names)
        with col5.expander(":violet[FILTER]"):
            st.write("")
            year = st.select_slider(':violet[YEAR]', options=y_values)
            st.write("")
            q = st.select_slider(':violet[QUATER]', options=q_values)
        with col6.expander(":violet[FILTER]"):
            st.write("")
            order = st.selectbox(":violet[ORDER]", ['Top', 'Bottom'])

        # _________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                  # _____________METRICS___________#

        # 1) Metric  : Top District By Amount
        query = f"select top_user_district , sum(top_registered_users) as val from  public.top_user_district where year= '{year}' and quater= {q} group by top_user_district order by val desc limit 1;"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        cursor.execute(query)
        res1 = [i[1] for i in cursor.fetchall()]
        with col1.expander(":violet[Top District By Registered Users]"):
            st.metric("", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")

        # ______________________________________________________________________________________________________________________________________________________________________________________________

        # 3) Metric  : Current State By RU

        Query_1 = f"select top_user_district , sum(top_registered_users) as val from  public.top_user_district where year= '{year}' and quater= {q} and top_user_district = '{dist_selected}' group by top_user_district order by val desc limit 1;"

        cursor.execute(Query_1)
        res = [i[0] for i in cursor.fetchall()]  # Name

        cursor.execute(Query_1)
        res1 = [i[1] for i in cursor.fetchall()]  # Count
        with col3.expander(":violet[Current District By Registered Users]"):
            st.metric("", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")

        # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                         # ___________CHARTS___________#

        col1, col2 ,col3= st.columns([1,100 ,1])

        #_____________________________________________________________________________________________________________________________________________________________________________

        # 1) Bar : Top/Bottom  1o districts By RU

        if order == 'Bottom':
            query = f"select top_user_district , sum(top_registered_users) as val from public.top_user_district where year= '{year}' and quater= {q} group by top_user_district order by val  limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['District', 'Registered Users'])
            fig = px.bar(df, x="District", y="Registered Users")
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
            with col2.expander("Bottom 10 District By Registered Users"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif order == "Top":
            query = f"select top_user_district , sum(top_registered_users) as val from public.top_user_district where year= '2022' and quater= 1 group by top_user_district order by val desc limit 10;"
            cursor.execute(query)
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
            with col2.expander("Top 10 District By Registered Users"):
                st.plotly_chart(fig, theme=None, use_container_width=True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        # ____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                # ________PINCODE TRANSACTION ANALYSIS___________#

        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[Pincode Registers Users Analysis]')

        st.write("")
        st.write("")

        # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                 # _____________FILTER_____________________#

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

        # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                                       # ____________CHARTS____________#

        col1, col2 ,col3= st.columns([1,100,1])

        # 1)  Top 10 Pincode By Transaction Amount

        if order == "Top":
            query_pin = f"select top_user_pincode , sum(top_registered_users) as val from public.top_user_pincode where year = '{year}' and quater = {q} group by  top_user_pincode order by val desc limit 10;"
            cursor.execute(query_pin)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Pincode', 'Registered Users'])
            pie = px.pie(df, names='Pincode', values='Registered Users', hole=0.7,
                         color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                                  '#CA8DE1'])  # change color
            pie.update_traces(textposition='outside')
            with col2.expander("Top 10 Pincode By Registered Users"):
                st.plotly_chart(pie, theme=None, use_container_width=True)

        elif order == "Bottom":
            query_pin = f"select top_user_pincode , sum(top_registered_users) as val from public.top_user_pincode where year = '{year}' and quater = {q} group by  top_user_pincode order by val  limit 10;"
            cursor.execute(query_pin)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Pincode', 'Registered Users'])
            pie = px.pie(df, names='Pincode', values='Registered Users', hole=0.7,
                         color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                                  '#CA8DE1'])  # change color
            pie.update_traces(textposition='outside')
            with col2.expander("Bottom 10 Pincode By Registered Users"):
                st.plotly_chart(pie, theme=None, use_container_width=True)




        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                   # _____________SDP Registered User  Concentration________________________#

        col1, col2, col3, = st.columns([2, 10, 1])

        col2.title(':violet[SDP   Registered UserConcentration Analysis]')

        st.write("")
        st.write("")

        # ___________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                # _______________FILTERS___________________#

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

        with col2.expander(":violet[FILTER]"):
            st.write("")
            q = st.select_slider(':violet[Pick QUATER]', options=q_values)


        # __________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                      # __________CHARTS_______________#

        col1, col2, col3 = st.columns([7, 7, 7])

                                                                                                       # _________State_Level__________#

        querys_top = f"select sum(top_registered_users) as val from public.top_user_district where year = '{year}' and quater = {q}  group by state order by val desc limit 10;"
        cursor.execute(querys_top)
        res = [i for i in cursor.fetchall()]
        df_1 = pd.DataFrame(res, columns=['Amount Top'])

        querys_bottom = f"select  sum(top_registered_users) as val from public.top_user_district where year = '{year}' and quater ={q} and state not in (select state  from  public.top_user_district where year = '{year}' and quater ={q}  group by state order by  sum(top_registered_users) desc limit 10) group by state order by val desc ;"

        cursor.execute(querys_bottom)
        res = [i for i in cursor.fetchall()]
        df_2 = pd.DataFrame(res, columns=['Amount Bottom'])

        state_last = {"Names": [], 'value': []}
        state_last['Names'].append("Top 10 States")
        state_last['Names'].append("Other States")

        state_last['value'].append(int(sum(df_1['Amount Top'])))
        state_last['value'].append(int(sum(df_2['Amount Bottom'])))

        df = pd.DataFrame(state_last)

        pie = px.pie(df, names='Names', values='value', labels={'Names': 'State Type', 'value': 'Registered Users'},
                     hole=0.7,
                     color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
        pie.update_traces(textposition='outside')

        with col1.expander("TOP 10 STATES :orange[Vs]  OTHER STATES"):
            st.plotly_chart(pie, theme=None, use_container_width=True)

        # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                       # ______________Districts Level__________#

        # Metrics 3 : District Transaction Concentration :

        query_top = f"select  sum(top_registered_users) as val from public.top_user_district where year = '{year}' and quater = {q}  group by top_user_district order by val desc limit 10"
        cursor.execute(query_top)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Top'])
        last = {'Names': [], 'value': []}
        last['Names'].append("Top 10 Districts")
        last['value'].append(int(sum(df['Amount Top'])))

        query_bottom = f"select  sum(top_registered_users)  from public.top_user_district where year = '{year}' and quater ={q} and top_user_district not in (select top_user_district  from public.top_user_district where year = '{year}' and quater ={q} group by top_user_district  order by sum(top_registered_users) desc limit 10) group by top_user_district  order by sum(top_registered_users) desc ;"
        cursor.execute(query_bottom)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Bottom'])

        last['Names'].append("Other Districts")
        last['value'].append(int(sum(df['Amount Bottom'])))

        df = pd.DataFrame(last)  # '#a7269e', '#d450b0', '#eb8adb',
        pie = px.pie(df, names='Names', values='value', hole=0.7,
                     labels={'Names': 'District Type', 'value': 'Registered Users'},
                     color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
        pie.update_traces(textposition='outside')

        with col2.expander("TOP 10 DISTRICTS :orange[Vs]  OTHER DISTRICTS"):
            st.plotly_chart(pie, theme=None, use_container_width=True)

        # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                 #_____________PINCODE_____________#

        query_top = f"select sum(top_registered_users) as val  from public.top_user_pincode where year = '{year}' and quater = {q} group by top_user_pincode order by val desc limit 10"
        cursor.execute(query_top)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Top'])
        last = {'Names': [], 'value': []}
        last['Names'].append("Top 10 Pincodes")
        last['value'].append(int(sum(df['Amount Top'])))

        query_bottom = f"select  sum(top_registered_users)  from  public.top_user_pincode where year = '{year}' and quater ={q} and top_user_pincode not in (select top_user_pincode  from public.top_user_pincode where year = '{year}' and quater ={q} group by top_user_pincode  order by sum(top_registered_users) desc limit 10) group by top_user_pincode order by sum(top_registered_users) desc;"
        cursor.execute(query_bottom)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Bottom'])

        last['Names'].append("Other Pincodes")
        last['value'].append(int(sum(df['Amount Bottom'])))

        df = pd.DataFrame(last)
        pie = px.pie(df, names='Names', values='value', hole=0.7,
                     labels={'Names': 'Pincode Type', 'value': 'Registered Userst'},
                     color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
        pie.update_traces(textposition='outside')

        with col3.expander("TOP 10 PINCODES :orange[Vs]  OTHER PINCODES"):
            st.plotly_chart(pie, theme=None, use_container_width=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        # _______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                 # ___________________Top 10 DP In State By Transaction Amount_______________#

        col1, col2, col3 = st.columns([2, 8, 1])

        col2.title(':violet[Top 10 DP In State By Registered User]')
        st.write("")
        st.write("")

        # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                                                        # ___________FILTERS_______________#

        col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5])

        # ________________________________________________________________________________________________________________________________________________________________________________________
        # 1) State

        query = "select distinct(state) from public.top_transaction_district_state order by state desc"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        with col1.expander(":violet[FILTER]"):
            st.write("")

            state_selected = st.selectbox(":violet[PICK STATE]", res)

        # 2) Districts and Pincodes

        with col2.expander(":violet[Filter]"):
            st.write("")
            vary = st.selectbox(':violet[PICK OPTION]', ['District', 'Pincode'])



        # 1) Year
        cursor.execute('select distinct(year) from public.top_user_pincode order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from public.aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        with col4.expander(":violet[Filter]"):
            year = st.select_slider(":violet[Choose Year]", options=y_values)

        with col3.expander(":violet[FILTER]"):
            q = st.select_slider(':violet[Choose Quater]', options=q_values)
        st.write("")
        st.write('')

        # 5) Top / Bottom 10

        with col5.expander(":violet[Filter]"):
            st.write("")
            order = st.selectbox(":violet[Choose Order]", ['desc', 'asc'])

        # ____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                           # _____CONDITION METRICS_____#
        col1, col2, col3 = st.columns([1, 100, 1])

        if vary == "District":

                query_1 = f"select top_user_district , sum(top_registered_users) as val from public.top_user_district where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_user_district order by val {order} limit 10;"
                cursor.execute(query_1)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['District', 'Registered Users'])
                fig = px.bar(df, x="District", y="Registered Users")
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
                with col2.expander("Top 10 District By Registered User"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)





        elif vary == "Pincode":

                query_pin = f"select top_user_pincode , sum(top_registered_users) as val from public.top_user_pincode where year = '{year}' and quater = {q} and state = '{state_selected}' group by top_user_pincode order by val {order}  limit 10;"
                cursor.execute(query_pin)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=["Pincode", "Registered Users"])
                pie = px.pie(df, names='Pincode', values="Registered Users", hole=0.7,
                             color_discrete_sequence=['#a7269e', '#FFFFFF'])  # change color
                pie.update_traces(textposition='outside')

                pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#F500E6")

                with col2.expander("Top 10 Pincode By Registered Users"):
                    st.plotly_chart(pie, theme=None, use_container_width=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

elif selected == 'View Data Source':


    selected = option_menu(
               menu_title="Phonepe Pulse",
               options=['Aggregated Transaction', 'Aggregated User', 'Map Transaction', "Map User",
                        "Top trnasaction District And State", "Top Transaction Pincode",
                        "Top user District And State", 'Top User Pincode'],
               icons=['table', 'table', 'table', 'table', 'table', 'table', 'table', 'table'],
               menu_icon='database-fill-check',
               default_index=0,
           )

    if selected == "Aggregated Transaction":
        query_1 = "select * from public.aggregated_transaction"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df  = pd.DataFrame(res,columns =['state',	'year',	'quater',	'agg_transaction_type',	'agg_transaction_count'	,'agg_transaction_amount'])
        st.dataframe(df)

    elif selected =="Aggregated User":
        query_1 = "select * from public.aggregated_user"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state',	'year',	'quater',	'registered_users',	'agg_users_appopens',	'agg_users_brand','agg_users_count',	'agg_users_percentage'])
        st.dataframe(df)


    elif selected =="Map Transaction":
        query_1 = "select * from public.map_transaction"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state'	,'year'	,'quater'	,'map_transaction_district',	'map_transaction_type','	map_transaction_count','map_transaction_amount'])
        st.dataframe(df)

    elif selected =="Map User":
        query_1 = "select * from public.map_user"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state'	,'year'	,'quater'	,'map_user_district'	,'map_registered_users'	,'map_appopens'])
        st.dataframe(df)

    elif selected =="Top trnasaction District And State":
        query_1 = "select * from public.top_transaction_district_state"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state',	"year",	'quater',	'top_transaction_district',	'top_transaction_type','top_transaction_count',	'top_transaction_amount'])
        st.dataframe(df)

    elif selected =="Top Transaction Pincode":
        query_1 = "select * from public.top_transaction_pincode"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state'	,'year',	'quater'	,'top_transaction_pincode','top_transaction_type',	'top_transaction_count','top_transaction_amount'])
        st.dataframe(df)

    elif selected =="Top user District And State":
        query_1 = "select * from public.top_user_district"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state',	'year',	'quater',	'top_user_district',	'top_registered_users'])
        st.dataframe(df)

    elif selected =="Top User Pincode":
        query_1 = "select * from public.top_user_pincode"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state',	'year','quater'	,'top_user_pincode','top_registered_users'])
        st.dataframe(df)

#____________________________________________________________________________________________________________________________________________________________________________________________________
elif selected == "":
    pass
