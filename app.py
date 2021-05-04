import streamlit as st

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from database import Report
from visualization import *
from AnalyseData import Analyse

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

analysis_mnf = Analyse("datasets\manufacturer.csv")
analysis_cnt = Analyse("datasets\country.csv")

st.title('Analysis of World Covid-19 Vaccination Progress')
sidebar = st.sidebar

def viewForm():

    st.plotly_chart(plot())

    title = st.text_input("Report Title")
    desc = st.text_area('Report Description')
    btn = st.button("Submit")

    if btn:
        report1 = Report(title = title, desc = desc, data = "")
        sess.add(report1)
        sess.commit()
        st.success('Report Saved')

def viewDataset():
    st.header('Datasets used in this Analysis')
    datasets = ['Country Data', 'Manufacturers Data']
    selData = st.selectbox(options= datasets, label= 'Select Dataset to View')
    if selData == datasets[0]:
        st.dataframe(analysis_cnt.getDataframe())
    elif selData == datasets[1]:
        st.dataframe(analysis_mnf.getDataframe())

def analyseManufacturers():

    st.header('Vaccine Manufacturers Total Count')

    data = analysis_mnf.getMnfCount()
    st.plotly_chart(plotBar(data, "Total Count of Vaccine Manufacturers", "No. of Vaccinations", "Manufacturer"))

    # st.header('Timeline of Manufacturer Vaccinations')
    # iso_6 = ['CHN','IND','USA','IDN','PAK','BRA']
    # dfs = []
    # for i in iso_6:
    #     dfs.append(analysis_cnt.getCountryData(i))
    #     iso_6 = ['CHN','IND','USA','IDN','PAK','BRA']

    # sel_con = st.selectbox(options = ['India', 'United States', 'China', 'Indonasia'], label="Select Country")
    # vac_Ind = analysis_mnf.get_vac_data(sel_con)
    # st.dataframe(analysis_mnf.getDataframe())
    # st.plotly_chart(plotLine(vac_Ind, 'date', 'total_vaccinations', 'vaccine',  'title'))

    # st.header('Vacinnation in Countries')
    # st.plotly_chart(plotScatter(dfs, ['date'], ['daily_vaccinations'], 6, iso_6, 'title', 'xlabel', 'ylabel'))

    st.header('Popular Vaccine Manufacturers')
    st.image('plotImages/man_line.png')


def countrywiseAnalysis():

    st.header('Daily Vaccinations in Countries')
    st.image('plotImages/daily_vacc_line.png')

    st.header('Fully Vaccinated Peoples in Countries')
    st.image('plotImages/fully_vacc_line.png')

    st.header('No. of Vaccinated People in Countries')
    st.image('plotImages/people_vacc_line.png')

    st.header('Total Vaccinations done in Countries')
    st.image('plotImages/total_vacc_line.png')

    st.header('Vaccination done per 100 in Countries')
    st.image('plotImages/total_per100_line.png')


def viewReport():
    reports = sess.query(Report).all()
    titlesList = [ report.title for report in reports ]
    selReport = st.selectbox(options = titlesList, label="Select Report")
    
    reportToView = sess.query(Report).filter_by(title = selReport).first()

    markdown = f"""
        ## {reportToView.title}
        ### {reportToView.desc}
        
    """

    st.markdown(markdown)

sidebar.header('Choose Your Option')
options = [ 'View Dataset', 'Analyse Manufacturers','Analyse Country', 'View Report' ]
choice = sidebar.selectbox( options = options, label="Choose Action" )

if choice == options[0]:
    viewDataset()
if choice == options[1]:
    analyseManufacturers()
elif choice == options[2]:
    countrywiseAnalysis()