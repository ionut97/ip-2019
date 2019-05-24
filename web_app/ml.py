import pickle

class ModelManager(object):
    def __init__(self):
        print("Loading model")

        self.model = pickle.load(open("ML/model.pkl", "rb"))
        self.dataset = pickle.load(open("ML/dataset.pkl", "rb"))
        self.matrix = pickle.load(open("ML/matrix.pkl", "rb"))

    def getMakes(self):
        makes = []

        for index, row in self.dataset.iterrows():
            if row['Make'] not in makes:
                makes.append(row['Make'])
        return makes

    def getModels(self, make):
        models = []

        for index, row in self.dataset.iterrows():
            if (row['Make'] == make and row['Model'] not in models):
                models.append(row['Model'])

        return models


    def estimatePrice(self, make, carmodel, year, mileage):
        index_X = 0

        for index, row in self.dataset.iterrows():
            if (row['Make'] == make and row['Model'] == carmodel):
                index_X = index

        variable = self.matrix[index_X]
        variable[-1] = mileage
        variable[-2] = year
        variable2 = []
        variable2.append(variable)
        variable2.append(variable)
        return int(self.model.predict(variable2)[0])
