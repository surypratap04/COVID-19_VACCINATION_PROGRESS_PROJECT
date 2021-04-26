import streamlit as st

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from database import Report
from visualization import plot, plotBar
from AnalyseData import Analyse

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

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

    analysis_mnf = Analyse("datasets\manufacturer.csv")
    data = analysis_mnf.getMnfCount()
    st.plotly_chart(plotBar(data, "Total Count of Vaccine Manufacturers", "No. of Vaccinations", "Manufacturer"))

def countrywiseAnalysis():
    st.header('Vaccine Manufacturers per hundred')

    analysis_mnf = Analyse("datasets\country.csv")
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
options = [ 'View Database', 'Analyse','Analyse Country', 'View Report' ]
choice = sidebar.selectbox( options = options, label="Choose Action" )

if choice == options[0]:
    viewDataset()
if choice == options[1]:
    analyseManufacturers()
elif choice == options[2]:
    countrywiseAnalysis()