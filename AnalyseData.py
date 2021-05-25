import pandas as pd


class Analyse:

    def __init__(self, path):
        self.df = pd.read_csv(path)
        # self.df = self.df[:1000]
        if path == 'datasets\country.csv':
            self.df["Total_vaccinations(count)"] = self.df.groupby(
                "country").total_vaccinations.tail(1)
            self.df["People_vaccinated(count)"] = self.df.groupby(
                "country").people_vaccinated.tail(1)
            self.df["People_fully_vaccinated(count)"] = self.df.groupby(
                "country").people_fully_vaccinated.tail(1)
            self.df["Total_vaccinations(count)_per_hundred"] = self.df.groupby(
                "country").total_vaccinations_per_hundred.tail(1)
            self.df["People_vaccinated(count)_per_hundred"] = self.df.groupby(
                "country").people_vaccinated_per_hundred.tail(1)
            self.df["People_fully_vaccinated(count)_per_hundred"] = self.df.groupby(
                "country").people_fully_vaccinated_per_hundred.tail(1)
        # self.cleanData()

    def getDataframe(self):
        return self.df

    def cleanData(self):
        self.df.drop(columns=[self.df.columns[0]], inplace=True)

    def getCategories(self):
        return self.df.groupby('Category').count().sort_values('App')['App'][::-1]

    def getMnfCount(self):
        return self.df.groupby('vaccine').count()['location']

    def getTopVaccPerHundred(self):
        return self.df.groupby('country').mean().sort_values('total_vaccinations_per_hundred', ascending=False)['total_vaccinations_per_hundred'][:100]

    def TimelineManufact(self):
        return

    def getCountryData(self, iso):
        return self.df.loc[(self.df['iso_code'] == iso)]

    def get_vac_data(self, location):
        return self.df[self.df['location'] == location]

    def getCountryVaccinations(self):
        return self.df.groupby("country")["Total_vaccinations(count)"].mean().sort_values(ascending=False)

    def getPeopleVaccinated(self):
        return self.df.groupby("country")["People_vaccinated(count)"].mean().sort_values(ascending=False)

    def getPeopleFullyVaccinated(self):
        return self.df.groupby("country")["People_fully_vaccinated(count)"].mean().sort_values(ascending=False)


    def getCountryVaccinations_100(self):
        return self.df.groupby("country")["Total_vaccinations(count)_per_hundred"].mean().sort_values(ascending=False)

    def getPeopleVaccinated_100(self):
        return self.df.groupby("country")["People_vaccinated(count)_per_hundred"].mean().sort_values(ascending=False)

    def getPeopleFullyVaccinated_100(self):
        return self.df.groupby("country")["People_fully_vaccinated(count)_per_hundred"].mean().sort_values(ascending=False)


    def getCountryVaccinations_vaccine(self, vaccine):
        return self.df[self.df['vaccines'] == vaccine].groupby("country")["Total_vaccinations(count)"].mean().sort_values(ascending=False)

    def getPeopleVaccinated_vaccine(self, vaccine):
        return self.df[self.df['vaccines'] == vaccine].groupby("country")["People_vaccinated(count)"].mean().sort_values(ascending=False)

    def getPeopleFullyVaccinated_vaccine(self, vaccine):
        return self.df[self.df['vaccines'] == vaccine].groupby("country")["People_fully_vaccinated(count)"].mean().sort_values(ascending=False)

    def getVaccines(self):
        return self.df.vaccines.unique()