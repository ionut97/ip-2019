import pickle
#loading a model from a file called model.pkl
model = pickle.load(open("model.pkl","rb"))

dataset = pickle.load(open("dataset.pkl","rb"))


#aceste 2 functii vor fi utile pentru frontend --------------------------------
def getMakes():
    #returneaza o lista cu marcile masinilor din model pentru frontend
    makes = []
    
    for index,row in dataset.iterrows():
        if row['Make'] not in makes:
            makes.append(row['Make'])
    
    return makes


def getModels(make):
    #make e un string, adica e un element 
    #din lista furnizata de functia de mai sus

    models = []
    
    for index,row in dataset.iterrows():
        if(row['Make'] == make and row['Model'] not in models):
            models.append(row['Model'])
    
    return models

print(getModels('Audi'))
#------------------------------------------------------------------------------


X = pickle.load(open("X.pkl","rb"))
#functie pentru endpoint-ul in care vom face prezicerea primind ca parametrii
#marca, modelul(furnizate de functiile de mai sus), anul si km

def estimatePrice(make,carmodel,year,mileage):
    
    index_X = 0
    
    for index,row in dataset.iterrows():
        if(row['Make'] == make and row['Model'] == carmodel):
            index_X = index
    
    variable = X[index_X]
    variable[-1] = mileage
    variable[-2] = year
    variable2 = []
    variable2.append(variable)
    variable2.append(variable)
    return model.predict(variable2)

#functia asta va rezulta o lista cu 2 elemente, ambele sunt identice
#motivul este ca pentru metoda predict a modelului aveam nevoie de o matrice
#iar, eu am creat o matrice cu 2 linii care reprezinta de 2 ori datele despre masina


print(estimatePrice('Audi','A3Sedan',2015,25000))


















