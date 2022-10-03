from cmath import nan
import pandas as pd
import datetime
import numpy

class DB:
      
    def __init__(self, db):
        self.load_db(db)
        self.diesel_type_by_motor = ['tdi','diesel']
        self.benzin_type_by_motor = ['t','tfsi','benzin','1.8t']
        self.lpg_type_by_motor = ['lpg',]
        self.brands = []
        self.audi_models = ['a1','a2','a3','a4','a5','a6','a7','a8','q3','q5','q7','tt']
        #self.brands = ['audi','bmw','vw']

    def load_db (self,db):
        self.current_db = pd.read_csv(db, encoding='latin1')
        self.current_db = self.current_db[self.current_db.lastSeen.notnull()]
        self.current_db['lastSeen'] = pd.to_datetime(self.current_db['lastSeen']
                                                    ,format="%Y-%m-%d %H:%M:%S", errors = 'coerce')
        self.current_db['dateCrawled'] = pd.to_datetime(self.current_db['dateCrawled']
                                                    ,format="%Y-%m-%d %H:%M:%S", errors = 'coerce')
        self.current_db['dateCreated'] = pd.to_datetime(self.current_db['dateCreated']
                                                    ,format="%Y-%m-%d %H:%M:%S", errors = 'coerce')

        self.current_db[['model','notRepairedDamage','seller','gearbox','vehicleType','fuelType','brand']] = self.current_db[['model','notRepairedDamage','seller','gearbox','vehicleType','fuelType','brand']].fillna(str('nan')).astype('category')
        
    def show(self):
        #print(self.current_db.info(memory_usage='deep'))
        pass 
    
    def complete_cat_fuel_type(self):
        for k, el in enumerate(self.current_db['name']):
            row = self.current_db.iloc[k]
            if str(row['fuelType']).lower() in ['nan', 'na']:
                for word in str(row['name']).lower().split("_"):
                    if word in self.lpg_type_by_motor: self.current_db._set_value(k,'fuelType','lpg')
                    elif  word in self.benzin_type_by_motor: self.current_db._set_value(k,'fuelType','benzin')
                    elif word in self.diesel_type_by_motor: self.current_db._set_value(k,'fuelType','diesel')

    def complete_model(self):
        for k, el in enumerate(self.current_db['name']):
            row = self.current_db.iloc[k]
            if str(row['model']).lower() in ['nan', 'na']:
                for i, word in enumerate(str(row['name']).lower().split("_")):
                    if word in self.audi_models:
                        self.current_db._set_value(k,'model',word)   

    def complete_gearbox(self):
        for k,el in enumerate(self.current_db['name']):
            row = self.current_db.iloc[k]
            if str(row['gearbox']).lower() in ['nan','na']:
                for word in str(row['name']).lower().split("_"):
                    if word in ['automatik',]:
                        self.current_db._set_value(k, 'gearbox','automatik')
                    elif word == 'manuell':
                        self.current_db._set_value(k, 'gearbox','manuell')
        
    def create_list_from_column(self,columnName):
        return self.current_db[str(columnName)].unique().tolist()    
    
    def compl_cat_func(self):
        current_db.complete_cat_fuel_type()
        current_db.complete_model()
        current_db.complete_gearbox()
        print("bangla")

                
database = "./cars_selling_sh.csv"

current_db = DB(database)
current_db.complete_cat_fuel_type()
current_db.complete_model()
current_db.complete_gearbox()
current_db.show()

#90
