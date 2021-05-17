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

st.title('Analysis of World Covid-19 Vaccination Progress')
st.text("")
st.text("")
st.image("logo.jfif")
st.markdown("---")
sidebar = st.sidebar
sidebar.title('Analysis of World Covid-19 Vaccination Progress')


def viewDataset():
    st.header('Data Used in Project')
    datasets = ['Country Data', 'Manufacturers Data']
    selData = st.selectbox(options=datasets, label='Select Dataset to View')
    if selData == datasets[0]:
        dataframe = analysis_cnt.getDataframe()
        showDetails(dataframe)
    elif selData == datasets[1]:
        dataframe = analysis_mnf.getDataframe()
        showDetails(dataframe)


def showDetails(dataframe):
    with st.spinner("Loading Data..."):
        st.dataframe(dataframe[:5000])

        st.markdown('---')
        cols = st.beta_columns(4)
        cols[0].markdown("### No. of Rows :")
        cols[1].markdown(f"# {dataframe.shape[0]}")
        cols[2].markdown("### No. of Columns :")
        cols[3].markdown(f"# {dataframe.shape[1]}")
        st.markdown('---')

        st.header('Summary')
        st.dataframe(dataframe.describe())
        st.markdown('---')

        types = {'object': 'Categorical',
                 'int64': 'Numerical', 'float64': 'Numerical'}
        types = list(map(lambda t: types[str(t)], dataframe.dtypes))
        st.header('Dataset Columns')
        for col, t in zip(dataframe.columns, types):
            st.markdown(f"### {col}")
            cols = st.beta_columns(4)
            cols[0].markdown('#### Unique Values :')
            cols[1].markdown(f"# {dataframe[col].unique().size}")
            cols[2].markdown('#### Type :')
            cols[3].markdown(f"## {t}")


def analyseManufacturers():

    st.header('Vaccine Manufacturers Total Count')

    data = analysis_mnf.getMnfCount()
    st.plotly_chart(plotBar(data, "Pfizer is the most popular Vaccine Manufacturer",
                            "No. of Vaccinations", "Manufacturer"))

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

    st.header('Increase in Vaccine Manufacturing over time')
    st.image('plotImages/man_line.png')


def countrywiseAnalysis():

    st.header('Overall Total Vaccinations')
    data = analysis_cnt.getCountryVaccinations()
    st.plotly_chart(plotBarh(data.head(20), 'Top 20 countries with most Vaccinations',
                             'Country Name', 'No. of Vaccinations'))

    st.text("")
    st.plotly_chart(plotChloropeth(data, 'Total Vaccination in world countries',
                                   'Country Name', 'No. of Vaccinations'))
    st.markdown("---")

    st.header('Total People Vaccinated')
    data = analysis_cnt.getPeopleVaccinated()
    st.plotly_chart(plotBarh(data.head(20), 'Top 20 Countries with Most People Vaccinated',
                             'Country Name', 'No. of Vaccinations'))

    st.text("")
    st.plotly_chart(plotChloropeth(
        data, 'Total people Vaccinated in world countries', 'Country Name', 'No. of Vaccinations'))
    st.markdown("---")

    st.header('Total Fully Vaccinated People')
    data = analysis_cnt.getPeopleFullyVaccinated()
    st.plotly_chart(plotBarh(data.head(20), 'Top 20 Countries with Most Fully Vaccinated People',
                             'Country Name', 'No. of Vaccinations'))

    st.text("")
    st.plotly_chart(plotChloropeth(
        data, 'Total people fully Vaccinated in world countries', 'Country Name', 'No. of Vaccinations'))
    st.markdown("---")

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
    titlesList = [report.title for report in reports]
    selReport = st.selectbox(options=titlesList, label="Select Report")

    reportToView = sess.query(Report).filter_by(title=selReport).first()

    markdown = f"""
        ## {reportToView.title}
        ### {reportToView.desc}
        
    """

    st.markdown(markdown)


sidebar.header('Choose Your Option')
options = ['View Dataset', 'Analyse Manufacturers',
           'Analyse Country', 'View Report']
choice = sidebar.selectbox(options=options, label="Choose Action")

with st.spinner("Please Wait for Some Time..."):
    analysis_mnf = Analyse("datasets\manufacturer.csv")
    analysis_cnt = Analyse("datasets\country.csv")

    if choice == options[0]:
        viewDataset()
    if choice == options[1]:
        analyseManufacturers()
    elif choice == options[2]:
        countrywiseAnalysis()
