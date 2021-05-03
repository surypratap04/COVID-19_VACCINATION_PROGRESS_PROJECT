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
    pass

def analyseManufacturers():

    st.header('Vaccine Manufacturers Total Count')

    data = analysis_mnf.getMnfCount()
    st.plotly_chart(plotBar(data, "Total Count of Vaccine Manufacturers", "No. of Vaccinations", "Manufacturer"))

    st.header('Timeline of Manufacturer Vaccinations')
    iso_6 = ['CHN','IND','USA','IDN','PAK','BRA']
    dfs = []
    for i in iso_6:
        dfs.append(analysis_cnt.getCountryData(i))
    sel_con = st.selectbox(options = ['India', 'United States', 'China', 'Indonasia'], label="Select Country")
    vac_Ind = analysis_mnf.get_vac_data(sel_con)
    st.dataframe(analysis_mnf.get_vac_data(sel_con))
    st.plotly_chart(plotLine(vac_Ind, 'date', 'total_vaccinations', 'vaccine',  'title'))

    st.header('Vacinnation in Countries')
    st.plotly_chart(plotScatter(dfs, ['date'], ['daily_vaccinations'], 6, iso_6, 'title', 'xlabel', 'ylabel'))

def countrywiseAnalysis():
    st.header('Vaccine Manufacturers per hundred')

    data = analysis_mnf.getTopVaccPerHundred()
    st.plotly_chart(plotBar(data, "Total Count of Vaccine Manufacturers", "No. of Vaccinations", "Manufacturer"))


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
options = [ 'View Database', 'Analyse Manufacturers','Analyse Country', 'View Report' ]
choice = sidebar.selectbox( options = options, label="Choose Action" )

if choice == options[0]:
    viewDataset()
if choice == options[1]:
    analyseManufacturers()
elif choice == options[2]:
    countrywiseAnalysis()