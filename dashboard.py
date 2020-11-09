# -*- coding: utf-8 -*-
"""Dashboard.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FuIeTz3F8jwnRtzYKiSIJdxuES90c5Ij
"""

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go 

import pandas as pd
import requests
import json
from pandas.io.json import json_normalize

import streamlit as st

import altair as alt

def main(): 
  st.markdown("<h1 style='text-align: center; color: #4d0a00;'><strong><u>Covid-19 Indonesia Dashboard</u></strong></h1>", unsafe_allow_html=True)
  st.sidebar.markdown("<h1 style='text-align: center; color: #aaccee;'><strong><u>Covid-19 Dashboard</u></strong></h1>", unsafe_allow_html=True)
  st.markdown("This Web App is a live Covid-19 Indonesia Dashboard which access Data sourced from BNPB Indonesia with url: https://opendata.arcgis.com/datasets/685be21cd0034247b5ceeac996d947fe_0.geojson", unsafe_allow_html=True)

  api_bnpb = "https://opendata.arcgis.com/datasets/685be21cd0034247b5ceeac996d947fe_0.geojson" #initialization of url json
  request = requests.get(api_bnpb)
  data = request.json()
  df = pd.json_normalize(data,'features', sep = "_")
  df.drop(columns = ['type', 'geometry','properties_Object_ID', 'properties_CFR_Harian','properties_RI_Harian','properties_FID','properties_ObjectId'], inplace = True)
  df.rename(columns = {'properties_Provinsi': 'state','properties_Tanggal':'date','properties_Kasus_Terkonfirmasi_Akumulatif': 'Total_Terkonfirmasi', 'properties_Penambahan_Harian_Kasus_Terkonf' : 'Terkonfirmasi_Harian',
                     'properties_Kasus_Sembuh_Akumulatif': 'Total_Sembuh', 'properties_Penambahan_Harian_Kasus_Sembuh': 'Sembuh_Harian', 'properties_Kasus_Meninggal_Akumulatif':'Total_MeninggalDunia','properties_Penambahan_Harian_Kasus_Meningg':'MeninggalDunia_Harian','properties_Kasus_Aktif_Akumulatif':'Total_Aktif' }, inplace=True)
  df.drop(df[df.state=="Indonesia"].index, inplace=True)

  
  st.write(df)
  
  temp = df.groupby(['state'])['Total_Terkonfirmasi', 'Total_MeninggalDunia', 'Total_Sembuh', 'Total_Aktif'].sum().reset_index()
  temp.style.background_gradient(cmap='Pastel1')
 
  full_latest = df.groupby(['state'])['Total_Terkonfirmasi', 'Total_MeninggalDunia', 'Total_Sembuh', 'Total_Aktif'].max().sort_values(by='Total_Terkonfirmasi',ascending=False).reset_index()
  Top10kasus_terkonfirmasi = full_latest.sort_values(by='Total_Terkonfirmasi', ascending=False).head(10)
  Top10kasus_sembuh = full_latest.sort_values(by='Total_Sembuh', ascending=False).head(10)
  Top10kasus_meninggaldunia = full_latest.sort_values(by='Total_MeninggalDunia', ascending=False).head(10)
  Top10kasus_aktif = full_latest.sort_values(by='Total_Aktif', ascending=False).head(10)

  Total_Terkonfirmasi_fix = full_latest['Total_Terkonfirmasi'].sum()
  Total_Sembuh_fix = full_latest['Total_Sembuh'].sum()
  Total_MeninggalDunia_fix = full_latest['Total_MeninggalDunia'].sum()
  Total_Aktif_fix = full_latest['Total_Aktif'].sum()

  st.write('Total Confirmed Cases From Indonesia - ',Total_Terkonfirmasi_fix)
  st.write('Total Death Cases From Indonesia - ',Total_MeninggalDunia_fix)
  st.write('Total Recovered Cases From Indonesia - ',Total_Sembuh_fix)
  st.write('Total Active Cases From Indonesia - ',Total_Aktif_fix)

  st.sidebar.subheader('Analysis through Heat Maps')
  select = st.sidebar.selectbox('Choose Heat Map Type',['Confirmed Cases','Recovered Cases','Active Cases','Death Cases'],key='1')
  if not st.sidebar.checkbox("Hide Map",True):
    if select == "Confirmed Cases": 
      fig = px.choropleth(df, geojson='https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson', 
                          locations='state', 
                          color='Total_Terkonfirmasi', 
                          color_continuous_scale='Reds', 
                          featureidkey='properties.state', 
                          animation_frame='date', 
                          range_color=(0, max(df['Total_Terkonfirmasi'])), 
                          title='Provinces of Indonesia on Confirmed Cases'
                          )
      fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
      fig.update_geos(fitbounds="locations", visible=False)
      st.plotly_chart(fig)

    elif select == "Recovered Cases":
      fig1 = px.choropleth(df, geojson='https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson', 
                           locations='state', 
                           color='Total_Sembuh', 
                           color_continuous_scale='Reds', 
                           featureidkey='properties.state', 
                           animation_frame='date', 
                           range_color=(0, max(df['Total_Sembuh'])),
                           title='Provinces of Indonesia on Recovered Cases'
                           )
      fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
      fig1.update_geos(fitbounds="locations", visible=False)
      st.plotly_chart(fig1)

    elif select == "Active Cases":
      fig11 = px.choropleth(df, geojson='https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson', 
                            locations='state', 
                            color='Total_Aktif', 
                            color_continuous_scale='Reds', 
                            featureidkey='properties.state', 
                            animation_frame='date', 
                            range_color=(0, max(df['Total_Aktif'])),
                            title='Provinces of Indonesia on Active Cases'
                            )
      fig11.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
      fig11.update_geos(fitbounds="locations", visible=False)
      st.plotly_chart(fig11)

    else:
      fig12 = px.choropleth(df, geojson='https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson', 
                            locations='state', 
                            color='Total_MeninggalDunia', 
                            color_continuous_scale='Reds', 
                            featureidkey='properties.state', 
                            animation_frame='date', 
                            range_color=(0, max(df['Total_MeninggalDunia'])),
                            title='Provinces of Indonesia on Death Cases'
                            )
      fig12.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
      fig12.update_geos(fitbounds="locations", visible=False)
      st.plotly_chart(fig12)

  st.sidebar.subheader('Analysis through Bar Chart')
  select = st.sidebar.selectbox('Choose Bar Chart',['Confirmed Cases','Recovered Cases','Active Cases','Deaths Cases'],key='2')
  if not st.sidebar.checkbox("Hide Bar Chart",True):
    if select == "Confirmed Cases": 
      fig2 = px.bar(Top10kasus_terkonfirmasi, x=Top10kasus_terkonfirmasi['state'], y=Top10kasus_terkonfirmasi['Total_Terkonfirmasi'],
              hover_name=Top10kasus_terkonfirmasi['state'],
              color=Top10kasus_terkonfirmasi['Total_Terkonfirmasi'], text=Top10kasus_terkonfirmasi['Total_Terkonfirmasi'], height=400)
      fig2.update_traces(texttemplate='%{text:}', textposition='outside')
      fig2.update_layout(
        title={
        'text': "Top 10 Provinces of Indonesia on Confirmed Cases",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
      # Set the visibility ON
      fig2.update_xaxes(title='Provinsi', visible=True, showticklabels=True)
      # Set the visibility OFF
      fig2.update_yaxes(title='Total', visible=True, showticklabels=True)
      st.plotly_chart(fig2)

    elif select == "Recovered Cases":
      fig21 = px.bar(Top10kasus_sembuh, x=Top10kasus_sembuh['state'], y=Top10kasus_sembuh['Total_Sembuh'],
              hover_name=Top10kasus_sembuh['state'],
              color=Top10kasus_sembuh['Total_Sembuh'], text=Top10kasus_sembuh['Total_Sembuh'], height=400)
      fig21.update_traces(texttemplate='%{text:}', textposition='outside')
      fig21.update_layout(
        title={
        'text': "Top 10 Provinces of Indonesia on Recovered Cases",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
      # Set the visibility ON
      fig21.update_xaxes(title='Provinsi', visible=True, showticklabels=True)
      # Set the visibility OFF
      fig21.update_yaxes(title='Total', visible=True, showticklabels=True)
      st.plotly_chart(fig21)
            
    elif select == "Active Cases":
      fig22 = px.bar(Top10kasus_aktif, x=Top10kasus_aktif['state'], y=Top10kasus_aktif['Total_Aktif'],
              hover_name=Top10kasus_aktif['state'],
              color=Top10kasus_aktif['Total_Aktif'], text=Top10kasus_aktif['Total_Aktif'], height=400)
      fig22.update_traces(texttemplate='%{text:}', textposition='outside')
      fig22.update_layout(
        title={
        'text': "Top 10 Provinces of Indonesia on Active Cases",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
      # Set the visibility ON
      fig22.update_xaxes(title='Provinsi', visible=True, showticklabels=True)
      # Set the visibility OFF
      fig22.update_yaxes(title='Total', visible=True, showticklabels=True)
      st.plotly_chart(fig22)

    else:
      fig23 = px.bar(Top10kasus_meninggaldunia, x=Top10kasus_meninggaldunia['state'], y=Top10kasus_meninggaldunia['Total_MeninggalDunia'],
              hover_name=Top10kasus_meninggaldunia['state'],
              color=Top10kasus_meninggaldunia['Total_MeninggalDunia'], text=Top10kasus_meninggaldunia['Total_MeninggalDunia'], height=400)
      fig23.update_traces(texttemplate='%{text:}', textposition='outside')
      fig23.update_layout(
        title={
        'text': "Top 10 Provinces of Indonesia on Death Cases",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
      # Set the visibility ON
      fig23.update_xaxes(title='Provinsi', visible=True, showticklabels=True)
      # Set the visibility OFF
      fig23.update_yaxes(title='Total', visible=True, showticklabels=True)
      st.plotly_chart(fig23)

  st.sidebar.subheader('Analysis through Pie Chart')
  select = st.sidebar.selectbox('Choose Pie Chart',['Confirmed Cases','Recovered Cases','Active Cases','Deaths Cases'],key='2')
  if not st.sidebar.checkbox("Hide Pie Chart",True):
    if select == "Confirmed Cases": 
      fig3 = go.Figure(data=[go.Pie(labels=Top10kasus_terkonfirmasi['state'], values=Top10kasus_terkonfirmasi['Total_Terkonfirmasi'],
                               insidetextorientation='radial',
                               pull=[0.1, 0, 0, 0, 0, 0])])
      fig3.update_traces(textinfo='percent+label')  
      st.plotly_chart(fig3)

    elif select == "Recovered Cases":
      fig31 = go.Figure(data=[go.Pie(labels=Top10kasus_sembuh['state'], values=Top10kasus_sembuh['Total_Sembuh'],
                               insidetextorientation='radial',
                               pull=[0.1, 0, 0, 0, 0, 0])])
      fig31.update_traces(textinfo='percent+label')  
      st.plotly_chart(fig31)

    elif select == "Active Cases":
      fig32 = go.Figure(data=[go.Pie(labels=Top10kasus_aktif['state'], values=Top10kasus_aktif['Total_Aktif'],
                               insidetextorientation='radial',
                               pull=[0.1, 0, 0, 0, 0, 0])])
      fig32.update_traces(textinfo='percent+label')  
      st.plotly_chart(fig32)

    else:
      fig33 = go.Figure(data=[go.Pie(labels=Top10kasus_meninggaldunia['state'], values=Top10kasus_meninggaldunia['Total_MeninggalDunia'],
                               insidetextorientation='radial',
                               pull=[0.1, 0, 0, 0, 0, 0])])
      fig33.update_traces(textinfo='percent+label')  
      st.plotly_chart(fig33)
  
  st.sidebar.subheader('Analysis through Bubble Chart')
  select = st.sidebar.selectbox(Choose Tree Maps',['Confirmed Cases'],key='2')
  if not st.sidebar.checkbox("Hide Bubble Chart",True):
    Top10kasus_terkonfirmasi['Recovered_Rate'] = Top10kasus_terkonfirmasi['Total_Sembuh'] / Top10kasus_terkonfirmasi['Total_Terkonfirmasi']
    Top10kasus_terkonfirmasi['Death_Rate'] = Top10kasus_terkonfirmasi['Total_MeninggalDunia'] / Top10kasus_terkonfirmasi['Total_Terkonfirmasi']
    Top10kasus_terkonfirmasi.index = Top10kasus_terkonfirmasi.index
    fig4 = px.scatter(Top10kasus_terkonfirmasi, x='Recovered_Rate', y='Death_Rate',
                  color='state', size='Total_Terkonfirmasi', hover_name='state',
                  size_max=30)
    st.plotly_chart(fig4)
    
  
  st.sidebar.subheader('Analysis through Tree Maps')
  select = st.sidebar.selectbox('Choose Tree Maps',['Confirmed Cases','Recovered Cases','Active Cases','Deaths Cases'],key='2')
  if not st.sidebar.checkbox("Hide Tree Maps",True):
    if select == "Confirmed Cases": 
      fig4 = px.treemap(Top10kasus_terkonfirmasi.sort_values(by='Total_Terkonfirmasi', ascending=False).reset_index(drop=True), 
                 path=["state"], values="Total_Terkonfirmasi", height=700,
                 title='Top 10 Provinces of Indonesia on Confirmed Case',
                 color_discrete_sequence = px.colors.qualitative.Prism)
      fig4.data[0].textinfo = 'label+text+value'
      fig4.update_layout(margin=dict(t=80,l=0,r=0,b=0)) 
      st.plotly_chart(fig4)

    elif select == "Recovered Cases":
      fig41 = px.treemap(Top10kasus_sembuh.sort_values(by='Total_Sembuh', ascending=False).reset_index(drop=True), 
                 path=["state"], values="Total_Sembuh", height=700,
                 title='Top 10 Provinces of Indonesia on Recovered Case',
                 color_discrete_sequence = px.colors.qualitative.Prism)
      fig41.data[0].textinfo = 'label+text+value'
      fig41.update_layout(margin=dict(t=80,l=0,r=0,b=0)) 
      st.plotly_chart(fig41)
    
    elif select == "Active Cases":
      fig42 = px.treemap(Top10kasus_aktif.sort_values(by='Total_Aktif', ascending=False).reset_index(drop=True), 
                 path=["state"], values="Total_Aktif", height=700,
                 title='Top 10 Provinces of Indonesia on Active Case',
                 color_discrete_sequence = px.colors.qualitative.Prism)
      fig42.data[0].textinfo = 'label+text+value'
      fig42.update_layout(margin=dict(t=80,l=0,r=0,b=0)) 
      st.plotly_chart(fig42)

    else:
      fig43 = px.treemap(Top10kasus_meninggaldunia.sort_values(by='Total_MeninggalDunia', ascending=False).reset_index(drop=True), 
                 path=["state"], values="Total_MeninggalDunia", height=700,
                 title='Top 10 Provinces of Indonesia on Death Case',
                 color_discrete_sequence = px.colors.qualitative.Prism)
      fig43.data[0].textinfo = 'label+text+value'
      fig43.update_layout(margin=dict(t=80,l=0,r=0,b=0)) 
      st.plotly_chart(fig43)


  st.sidebar.subheader('Analysis through Scatter Plot')
  select = st.sidebar.selectbox('Choose Scatter Plot',['Confirmed Cases','Recovered Cases','Active Cases','Deaths Cases'],key='2')
  if not st.sidebar.checkbox("Hide Scatter Plots",True):
    if select == "Confirmed Cases": 
      fig5 = px.scatter(Top10kasus_terkonfirmasi, x='state', y='Total_Terkonfirmasi')
      st.plotly_chart(fig5)

    elif select == "Recovered Cases":
      fig51 = px.scatter(Top10kasus_sembuh, x='state', y='Total_Sembuh')
      st.plotly_chart(fig51)

    elif select == "Active Cases":
      fig52 = px.scatter(Top10kasus_aktif, x='state', y='Total_Aktif')
      st.plotly_chart(fig52)

    else:
      fig53 = px.scatter(Top10kasus_meninggaldunia, x='state', y='Total_MeninggalDunia')
      st.plotly_chart(fig53)
  
  subset_data = df
  Province_name_input = st.multiselect('state', df.groupby('state').count().reset_index()['state'].tolist())
  # by country name
  if len(Province_name_input) > 0:
      subset_data = df[df['state'].isin(Province_name_input)]
  
  st.sidebar.subheader('Comparision of infection growth with Analysis through Line Chart')
  select = st.sidebar.selectbox('Choose Line Chart',['Confirmed Cases','Recovered Cases','Active Cases','Deaths Cases'],key='2')
  if not st.sidebar.checkbox("Hide Line Chart",True):
    if select == "Confirmed Cases": 
      total_cases_graph=alt.Chart(subset_data).transform_filter(
        alt.datum.Total_Terkonfirmasi > 0  
      ).mark_line().encode(
        x=alt.X('date', type='nominal', title='Date'),
        y=alt.Y('sum(Total_Terkonfirmasi):Q',  title='Confirmed cases'),
        color='state',
        tooltip = 'sum(Total_Terkonfirmasi)',
      ).properties(
        width=1500,
        height=600
      ).configure_axis(
        labelFontSize=17,
        titleFontSize=20
      )
      st.altair_chart(total_cases_graph)

    elif select == "Recovered Cases":
      total_cases_graph1  =alt.Chart(subset_data).transform_filter(
        alt.datum.Total_Sembuh > 0  
      ).mark_line().encode(
        x=alt.X('date', type='nominal', title='Date'),
        y=alt.Y('sum(Total_Sembuh):Q',  title='Recovered cases'),
        color='state',
        tooltip = 'sum(Total_Sembuh)',
      ).properties(
        width=1500,
        height=600
      ).configure_axis(
        labelFontSize=17,
        titleFontSize=20
      )
      st.altair_chart(total_cases_graph1)
    
    elif select == "Active Cases":
      total_cases_graph2  =alt.Chart(subset_data).transform_filter(
        alt.datum.Total_Aktif > 0  
      ).mark_line().encode(
        x=alt.X('date', type='nominal', title='Date'),
        y=alt.Y('sum(Total_Aktif):Q',  title='Active cases'),
        color='state',
        tooltip = 'sum(Total_Aktif)',
      ).properties(
        width=1500,
        height=600
      ).configure_axis(
        labelFontSize=17,
        titleFontSize=20
      )
      st.altair_chart(total_cases_graph2)

    else:
      total_cases_graph3  =alt.Chart(subset_data).transform_filter(
        alt.datum.Total_MeninggalDunia > 0  
      ).mark_line().encode(
        x=alt.X('date', type='nominal', title='Date'),
        y=alt.Y('sum(Total_MeninggalDunia):Q',  title='Death cases'),
        color='state',
        tooltip = 'sum(Total_MeninggalDunia)',
      ).properties(
        width=1500,
        height=600
      ).configure_axis(
        labelFontSize=17,
        titleFontSize=20
      )
      st.altair_chart(total_cases_graph3)


if __name__ == '__main__':
    main()
    
    st.markdown("For issues Contact - nadyaasafitri@gmail.com")

