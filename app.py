import streamlit as st

from sqlalchemy.orm import seesionmaker
from sqlalchemy import create_engine
import pandas as pd
from database import Report

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

st.title('Analysis of covid 19 vaccination progress')
sidebar = st.sidebar()

def viewform():
    title = st.text_input("Report Title")
    desc = st.text_area('Report description')
    btn =st.button("sumbit")
    if btn:
        report1 = Report(Title = title, desc = desc, date = "")
        sess.add(report1)
        sess.commit()
        st.success('Report Saved')

sidebar.header('choose your option')
options = ['view database','Analyse','view report']
sidebar.selectbox(options = options, label="Choose Action")

if choice == options[1]:
    viewform()
    
    