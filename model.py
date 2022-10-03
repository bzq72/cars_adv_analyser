from pandas_profiling import ProfileReport
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score
from sklearn.linear_model import LinearRegression
import numpy as np


class Model_pre:
    def __init__(self, db):
        self.db = db
    
    def make_profile(self):
        profile = ProfileReport(self.db)
        profile.to_notebook_iframe()

    def transform_c_year(self):
        """transforming column yearOfRegistration to boolean/categorical columns"""
        print("transform_c_year processing...")
        new_columns = self.t_db["yearOfRegistration"].unique()
        for column in new_columns:  self.t_db[column] = 0 
        for k in self.t_db.index:
            row =self.t_db.iloc[k] 
            self.t_db._set_value(k,row["yearOfRegistration"], 1)

    def transform_c_cat(self):
        """transforming columns brand, model, gearbox, vehicleType, notRepairedDamage, fuelType to boolean/categorical columns"""
        print("transform_c_cat processing...")
        self.db.reset_index(drop=True, inplace=True)
        self.t_db = self.db
        #self.t_db = self.db[column ="price","yearOfRegistration","powerPS","brand","model","gearbox","vehicleType","notRepairedDamage","fuelType"]
        brand_columns = self.t_db["brand"].unique() #volkswagen' 'skoda' 'bmw' 'peugeot' 'mazda' 'nissan' 'renault' 'ford'
                                                # 'mercedes_benz' 'honda' 'mini' 'smart' 'audi' 'subaru' 'mitsubishi'
                                                # 'hyundai' 'opel' 'alfa_romeo' 'seat' 'lancia' 'porsche' 'citroen'
                                                # 'toyota' 'kia' 'fiat' 'chevrolet' 'dacia' 'suzuki' 'chrysler' 'volvo'
                                                # 'jaguar' 'rover' 'jeep' 'saab' 'land_rover' 'lada' 'daihatsu' 'daewoo']
        gearbox_columns = self.t_db["gearbox"].unique() # 'manuell' 'automatik'
        new_columns = np.append(brand_columns, gearbox_columns)
        vehicle_type_columns = self.t_db["vehicleType"].unique() # 'kleinwagen' 'limousine' 'cabrio' 'kombi' 'suv' 'bus' 'coupe' 'andere'
        new_columns = np.append(new_columns, vehicle_type_columns)
        not_rep_dam_columns = self.t_db["notRepairedDamage"].unique() # 'nein' 'ja'
        new_columns = np.append(new_columns, not_rep_dam_columns)
        model_columns = self.t_db["model"].unique() # a lot
        new_columns = np.append(new_columns, model_columns)
        fuel_type_columns = self.t_db["fuelType"].unique() # 'benzin' 'diesel' 'lpg' 'andere' 'hybrid' 'cng' 'elektro'
        new_columns = np.append(new_columns, fuel_type_columns)
        for column in new_columns:  self.t_db[column] = 0 
        for k in self.t_db.index:
            row =self.t_db.iloc[k] 
            self.t_db._set_value(k,row["brand"], 1)
            self.t_db._set_value(k,row["gearbox"], 1)
            self.t_db._set_value(k,row["vehicleType"], 1)
            self.t_db._set_value(k,row["notRepairedDamage"], 1)
            self.t_db._set_value(k,row["fuelType"], 1)
            self.t_db._set_value(k,row["model"], 1)
            if k % 1000 == 0: print("k= ", k)
            
    def transform_c_kilometer(self,date_base):
        """transforming column kilometer to boolean/categorical columns"""
        print("transform_c_kilometer processing...")
        new_columns = ["is_above_150k", "is_above_100k","is_above_50k","is_under_50k"]
        for column in new_columns:  date_base[column] = 0 

        for k in date_base.index:
            if k % 1000 == 0: print("k= ", k)
            row = date_base.iloc[k]
            if int(row["kilometer"]) < 50000:
               date_base._set_value(k, "is_under_50k", 1)
            elif int(row["kilometer"]) >= 150000:
                date_base._set_value(k, "is_above_50k", 1)
                date_base._set_value(k, "is_above_100k", 1)
                date_base._set_value(k, "is_above_150k", 1)
            elif int(row["kilometer"]) >= 100000:
                    date_base._set_value(k, "is_above_100k", 1)
                    date_base._set_value(k, "is_above_50k", 1)
            elif int(row["kilometer"]) >= 50000:
                    date_base._set_value(k, "is_above_50k", 1)
            else: 
                breakpoint()
                pass        


    def transform_c_powerPS(self,date_base): #powerPS
        """transforming column powerPS to boolean/categorical columns"""

        print("transform_c_powerPS processing...")
        new_columns = ["under_50_PS", "50_75_PS","75_90_PS","90_100_PS","100_110_PS","110_120_PS","120_130_PS","130_140_PS","140_150_PS"
                       ,"150_160_PS","160_170_PS","170_180_PS","180_190_PS","190_200_PS","200_225_PS","225_250_PS","250_275_PS"
                       , "275_300_PS","275_300_PS","300_350_PS","350_400_PS","above_400_PS"]
        
        for column in new_columns: date_base[column] = 0 
        for k in date_base.index:
            row =date_base.iloc[k]
            if int(row["powerPS"]) < 50: 
                date_base._set_value(k, "under_50_PS", 1)
            elif (int(row["powerPS"]) >= 50) & (int(row["powerPS"]) < 75): 
                date_base._set_value(k, "50_75_PS", 1)
            elif (int(row["powerPS"]) >= 75) & (int(row["powerPS"]) < 90): 
                date_base._set_value(k, "75_90_PS", 1)
            elif (int(row["powerPS"]) >= 90) & (int(row["powerPS"]) < 100): 
                date_base._set_value(k, "90_100_PS", 1)
            elif (int(row["powerPS"]) >= 100) & (int(row["powerPS"]) < 110): 
                date_base._set_value(k, "100_110_PS", 1)
            elif (int(row["powerPS"]) >= 110) & (int(row["powerPS"]) < 120): 
                date_base._set_value(k, "110_120_PS", 1)
            elif (int(row["powerPS"]) >= 120) & (int(row["powerPS"]) < 130): 
                date_base._set_value(k, "120_130_PS", 1)
            elif (int(row["powerPS"]) >= 130) & (int(row["powerPS"]) < 140): 
                date_base._set_value(k, "130_140_PS", 1)
            elif (int(row["powerPS"]) >= 140) & (int(row["powerPS"]) < 150): 
                date_base._set_value(k, "140_150_PS", 1)
            elif (int(row["powerPS"]) >= 150) & (int(row["powerPS"]) < 160): 
                date_base._set_value(k, "150_160_PS", 1)
            elif (int(row["powerPS"]) >= 160) & (int(row["powerPS"]) < 170): 
                date_base._set_value(k, "160_170_PS", 1)
            elif (int(row["powerPS"]) >= 170) & (int(row["powerPS"]) < 180): 
                date_base._set_value(k, "170_180_PS", 1)
            elif (int(row["powerPS"]) >= 180) & (int(row["powerPS"]) < 190): 
                date_base._set_value(k, "180_190_PS", 1)
            elif (int(row["powerPS"]) >= 190) & (int(row["powerPS"]) < 200): 
                date_base._set_value(k, "190_200_PS", 1)
            elif (int(row["powerPS"]) >= 200) & (int(row["powerPS"]) < 225): 
                date_base._set_value(k, "200_225_PS", 1)
            elif (int(row["powerPS"]) >= 225) & (int(row["powerPS"]) < 250): 
                date_base._set_value(k, "225_250_PS", 1)
            elif (int(row["powerPS"]) >= 250) & (int(row["powerPS"]) < 275): 
                date_base._set_value(k, "250_275_PS", 1)
            elif (int(row["powerPS"]) >= 275) & (int(row["powerPS"]) < 300): 
                date_base._set_value(k, "275_300_PS", 1)
            elif (int(row["powerPS"]) >= 300) & (int(row["powerPS"]) < 350): 
                date_base._set_value(k, "300_350_PS", 1)
            elif (int(row["powerPS"]) >= 350) & (int(row["powerPS"]) < 400): date_base._set_value(k, "350_400_PS", 1)
            elif int(row["powerPS"]) >= 400: date_base._set_value(k, "above_400_PS", 1)
            else: 
                breakpoint()
                pass        


    def transformer(self):
        """transforming columns to more appropriate"""
        self.clean_price()
        self.transform_c_cat()
        self.transform_c_kilometer(self.t_db)
        self.transform_c_powerPS(self.t_db)
        self.transform_c_year()
        self.t_db = self.t_db.drop(columns=["brand","powerPS","yearOfRegistration",'gearbox','fuelType','vehicleType','notRepairedDamage','kilometer','model'])

    
    def clean_table(self):
        """cleaning Datas from invalid, extreme values and not needed columns"""
        self.db = self.db.drop(columns=['seller','offerType','nrOfPictures','dateCrawled','name','lastSeen;;;;;;;;'
                                        ,'monthOfRegistration','dateCreated','postalCode','abtest'])
        self.db = self.db.dropna()
        self.clean_powerPS()
        self.clean_price()
        self.clean_produce_year()
        
    def clean_price(self):
        """cleaning price column from invalid or extreme values"""
        self.db["price"] = pd.to_numeric(self.db["price"], errors="coerce")
        self.db  = self.db[(self.db.price > 500) & (self.db.price < 100000)]

    def clean_produce_year(self):
        """cleaning yearOfRegistration column from invalid or extreme values"""
        self.db["yearOfRegistration"] = pd.to_numeric(self.db["yearOfRegistration"],errors="coerce")      
        self.db  = self.db[self.db.yearOfRegistration > 1980]

    def clean_powerPS(self):  
        """cleaning powerPS column from invalid or extreme values"""
        self.db["powerPS"] = pd.to_numeric(self.db["powerPS"],errors="coerce")
        self.db  = self.db[(self.db.powerPS > 60) & (self.db.powerPS < 400)]
        
    def filter(self):
        self.db  = self.db[self.db.brand == "audi"]
        #volkswagen' 'skoda' 'bmw' 'peugeot' 'mazda' 'nissan' 'renault' 'ford'
                                                # 'mercedes_benz' 'honda' 'mini' 'smart' 'audi' 'subaru' 'mitsubishi'
                                                # 'hyundai' 'opel' 'alfa_romeo' 'seat' 'lancia' 'porsche' 'citroen'
                                                # 'toyota' 'kia' 'fiat' 'chevrolet' 'dacia' 'suzuki' 'chrysler' 'volvo'
                                                # 'jaguar' 'rover' 'jeep' 'saab' 'land_rover' 'lada' 'daihatsu' 'daewoo']
                                                
        #self.db  = self.db[self.db.brand == "volkswagen "]
        #self.db  = self.db[self.db.model == "a4"]
        #self.db  = self.db[self.db.gearbox == "automatik"]
        #self.db  = self.db[self.db.fuelType == "benzin"]
        #self.db  = self.db[self.db.vehicleType == "kombi"]

        #self.db  = self.db[(self.db.yearOfRegistration > 2004) & (self.db.yearOfRegistration < 2008)]
        #self.db  = self.db[(self.db.powerPS > 109) & (self.db.powerPS < 151)]
        #self.db  = self.db[(self.db.kilometer > 90000) & (self.db.kilometer < 150000)]


        
        self.db = self.db.dropna()

    def linear_regression(self):
        x = self.t_db.drop(columns=['price'])
        y = self.t_db['price']
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=666)
        self.reg = LinearRegression().fit(X_train, y_train,)

        
    def make_model(self):
        print("make model processing...")
        x = self.t_db.drop(columns=['price'])
        y = self.t_db['price']
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=666)
        """ classifier = SVC()
        print("Fitting classifier")
        classifier.fit(X_train, y_train)
        print("Predicting Y ")
        y_predicted = classifier.predict(X_test)
        print(y_test,y_predicted)
        print("Calculating Accuracy...")
        print('Accuracy: ', accuracy_score(y_test, y_predicted))
        print("Calculating F1...")
        print('F1: ', f1_score(y_test, y_predicted, average='macro'))
        print(classifier.coef0)
        print(X_test[20:25])
        print(classifier.predict(X_test[20:25]))"""
        
        self.reg = LinearRegression().fit(X_train, y_train,)
        
        print("score ", self.reg.score(X_train, y_train))
        print("coef", self.reg.coef_)
        
        print(y_test[0:10])
        print(self.reg.predict(X_test[0:10]))
        print(X_test[0:10])
        

dbooo = "./cars_selling.csv"
current_dbooo = pd.read_csv(dbooo, encoding='latin1')
current_dbooo = current_dbooo[:1000]
test_obj = Model_pre(current_dbooo)
test_obj.clean_table()
test_obj.filter()
#current_dbooo = pd.read_excel("output3.xlsx")
test_obj.transformer()
test_obj.make_model()
#print(test_obj.db())

#test_obj.t_db.to_excel("output.xlsx")  


new_row = {"audi":1,  'manuell':1  ,'kombi':1  ,'nein':1   ,'a4':1  ,'benzin':1  ,'is_above_50k':1  ,'110_120_PS':1  ,2012.0:1}
test_obj.t_db = test_obj.t_db.append(new_row, ignore_index=True)
print(_db := test_obj.t_db.tail(1).fillna(0).drop(columns = ["price"]))
print(_db)
print(test_obj.t_db.columns.tolist())
test = test_obj.t_db[99:100].drop(columns = ["price"])
new_row = test_obj.t_db.tail(1).drop(columns = ["price"])


#print(test.loc[:, (test != 0).any(axis=0)])
#print(test_obj.reg.predict(test))
#print(test_obj.reg.predict(_db))

#test_obj.t_db.to_excel("output.xlsx")  


