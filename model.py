import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from tkinter import messagebox

class Model_Pre:
    def __init__(self, db):
        self.db = db
    
    def make_profile(self):
        """creating raport of DB"""
        #profile = ProfileReport(self.db)
        #profile.to_notebook_iframe()

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
        new_columns = ["under_50_PS", "under_75_PS","under_100_PS","under_125_PS","under_150_PS","under_175_PS","under_200_PS","under_250_PS","under_300_PS"
                       ,"under_400_PS","above_400_PS"]
        for column in new_columns: date_base[column] = 0 
        for k in date_base.index:
            row =date_base.iloc[k]
            if int(row["powerPS"]) < 50: date_base._set_value(k, "under_50_PS", 1)
            if int(row["powerPS"]) < 75: date_base._set_value(k, "under_75_PS", 1)
            if int(row["powerPS"]) < 100: date_base._set_value(k, "under_100_PS", 1)
            if int(row["powerPS"]) < 125: date_base._set_value(k, "under_125_PS", 1)
            if int(row["powerPS"]) < 150: date_base._set_value(k, "under_150_PS", 1)
            if int(row["powerPS"]) < 175: date_base._set_value(k, "under_175_PS", 1)
            if int(row["powerPS"]) < 200: date_base._set_value(k, "under_200_PS", 1)
            if int(row["powerPS"]) < 250: date_base._set_value(k, "under_250_PS", 1)
            if int(row["powerPS"]) < 300: date_base._set_value(k, "under_300_PS", 1)
            if int(row["powerPS"]) < 400: date_base._set_value(k, "under_400_PS", 1)
            if int(row["powerPS"]) >= 400: date_base._set_value(k, "above_400_PS", 1)
      
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
        self.db = self.db.drop(columns=['seller','offerType','nrOfPictures','dateCrawled','name', 'dateCrawled', 'dateCreated'
                                        ,'monthOfRegistration','dateCreated','postalCode','abtest'])
        try: self.db = self.db.drop(columns=[ 'lastSeen;;;;;;;;'])
        except: pass
        try: self.db = self.db.drop(columns=[ 'lastSeen'])
        except: pass
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
        """static filter"""
        #self.db  = self.db[self.db.brand == "audi"]
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
        pass

        self.db = self.db.dropna()
        
    def scale_variables(self):
        """scaling variables from DB with mean = 0 and std = 1"""
        Sc = StandardScaler()
        Sc.fit(self.x_train)
        self.x_train = Sc.transform(self.x_train)
        Sc.fit(self.x_test)
        self.x_test = Sc.transform(self.x_test)

        
    def devide_set(self):
        """deviding db to train and test sets"""
        x = self.t_db.drop(columns=['price'])
        self.y = self.t_db['price']
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, self.y, test_size=0.2, random_state=666)

    def linear_regression(self, skip_train = False, to_predict = None):
        """making prediction by linear regression"""
        if not skip_train:
            self.li_r = LinearRegression().fit(self.x_train, self.y_train)
            y_pred = self.li_r.predict(self.x_test)
            r2 = r2_score(self.y_test, y_pred)
        if  to_predict is not None: 
            try: return self.li_r.predict(to_predict)
            except: return [0]
        return {self.linear_regression:r2}
        
    def lasso_regression(self, skip_train = False, to_predict = None):
        """making prediction by lasso regression"""
        if not skip_train:
            self.la_r = Lasso (normalize = True).fit(self.x_train, self.y_train)
            y_pred = self.la_r.predict(self.x_test)
            r2 = r2_score(self.y_test, y_pred)
        if to_predict is not None: 
            try: return self.la_r.predict(to_predict)
            except: return [0]

        return {self.lasso_regression:r2}

    def ridge_regression(self, skip_train = False, to_predict = None):
        """making prediction by ridge regression"""
        if not skip_train:
            self.ri_r = Ridge(normalize = True).fit(self.x_train, self.y_train)
            y_pred = self.ri_r.predict(self.x_test)
            r2 = r2_score(self.y_test, y_pred)
        if to_predict is not None: 
            try: return self.ri_r.predict(to_predict)
            except: return [0]
        return {self.ridge_regression:r2}

    def adaboost_regressor(self, skip_train = False, to_predict = None):
        """making prediction by AdaBoost regression"""
        if not skip_train:
            self.ab_r = AdaBoostRegressor(n_estimators =1000).fit(self.x_train, self.y_train)
            y_pred = self.ab_r.predict(self.x_test)
            r2 = r2_score(self.y_test, y_pred)
        if to_predict is not None: 
            try: return self.ab_r.predict(to_predict)
            except: return [0]
        return {self.adaboost_regressor:r2}

    def random_forrest_regressor(self, skip_train = False, to_predict = None):
        """making prediction by Random Forrest regressor"""
        if not skip_train:
            self.rf_r = AdaBoostRegressor(n_estimators =1000).fit(self.x_train, self.y_train)
            y_pred = self.rf_r.predict(self.x_test)
            r2 = r2_score(self.y_test, y_pred)
        if to_predict is not None: 
            try: return self.rf_r.predict(to_predict)
            except: return [0]
        return {self.random_forrest_regressor:r2}

    def k_neighbors_regressor(self, skip_train = False, to_predict = None):
        """making prediction by KNearest regressor"""
        if not skip_train:
            self.kn_r = KNeighborsRegressor().fit(self.x_train, self.y_train)
            y_pred =  self.kn_r.predict(self.x_test)
            r2 = r2_score(self.y_test, y_pred)
        if to_predict is not None: 
            try: return self.kn_r.predict(to_predict)
            except: return [0]
        return {self.k_neighbors_regressor:r2}
    
    def check_all_models(self):
        """collecting models accurency"""
        scores = {}
        list = [self.linear_regression(), self.adaboost_regressor(), self.lasso_regression(), self.ridge_regression(), self.random_forrest_regressor(), self.k_neighbors_regressor()] 
        for reg in list: scores.update(reg)
        return scores

    def choose_model(self):
        """choosing best model"""
        return max(self.check_all_models(), key=self.check_all_models().get)

    def predict_by_best_model(self, to_predict):
        """predicting value by best model"""
        return self.choose_model()(skip_train = True, to_predict = to_predict)

    def to_predict():
        pass
    
    def prepare_datebase(self):
        """preparing db"""
        self.clean_table()
        self.filter()
        self.transformer()
        try: self.devide_set()
        except: 
            messagebox.showerror("Error", "The is not enought similar cars to yours \nChange filters and try again")
        #self.scale_variables()
    
    def predict_price(self, to_predict):
        """predicting price"""
        self.prepare_datebase()
        self.predict_by_best_model(to_predict=to_predict)
    
    def show_sampler(self):
        """showing samples""" 
        print(self.y_test[0:10])
        
        
        
"""
dbooo = "./cars_selling.csv"
current_dbooo = pd.read_csv(dbooo, encoding='latin1')
#current_dbooo = current_dbooo[:100000]
test_obj = Model_Pre(current_dbooo)
test_obj.clean_table()
test_obj.filter()
test_obj.transformer()
test_obj.devide_set()
#test_obj.scale_variables()
test_obj.choose_model()
test_obj.show_sampler()
#test_obj.predict_by_best_model()
"""

















#test_obj.make_model() juz z tego nie korzystamy 
#print(test_obj.db())

#test_obj.t_db.to_excel("output.xlsx")  


#new_row = {"audi":1,  'manuell':1  ,'kombi':1  ,'nein':1   ,'a4':1  ,'benzin':1  ,'is_above_50k':1  ,'110_120_PS':1  ,2012.0:1}
#test_obj.t_db = test_obj.t_db.append(new_row, ignore_index=True)
#print(_db := test_obj.t_db.tail(1).fillna(0).drop(columns = ["price"]))
#print(_db)
#print(test_obj.t_db.columns.tolist())
##test = test_obj.t_db[99:100].drop(columns = ["price"])
#new_row = test_obj.t_db.tail(1).drop(columns = ["price"])


#print(test.loc[:, (test != 0).any(axis=0)])
#print(test_obj.reg.predict(test))
#print(test_obj.reg.predict(_db))

#test_obj.t_db.to_excel("output.xlsx")  


