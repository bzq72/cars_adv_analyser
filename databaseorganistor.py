from cmath import nan
import pandas as pd
import datetime
import numpy
from tkinter import messagebox



class DB:
      
    def __init__(self, db):
        self.load_db(db)
        
    def with_warning_message(func):
        def wrapper(self):
            if (messagebox.askokcancel("Warning!", "Function will take couple minutes \nDo you want to proceed?")) == True:
                func(self)
            else: return
        return wrapper
    
    def str_var(self):
        """initalization varables used in completing categories"""
        self.diesel_type_by_motor = ['tdi','diesel']
        self.benzin_type_by_motor = ['t','tfsi','benzin','1.8t']
        self.lpg_type_by_motor = ['lpg',]
        self.brands = []
        self.audi_models = ['a1','a2','a3','a4','a5','a6','a8','q3','q5','q7','tt']
        #self.brands = ['audi','bmw','vw']
        
    def load_db (self,db):
        """loading and transforming database"""
        self.current_db = pd.read_csv(db, encoding='latin1')
        try: 
            self.current_db['lastSeen'] = self.current_db['lastSeen;;;;;;;;']
            self.current_db.drop(columns="lastSeen;;;;;;;;")
        except:
            pass
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
    
    def complete_cat_fueltype(self):
        """completing column fueltype by data in adv title"""
        print("completing column fuel type")
        i=0
        for k, el in enumerate(self.current_db['name']):
            row = self.current_db.iloc[k]
            if str(row['fuelType']).lower() in ['nan', 'na']:
                for word in str(row['name']).lower().split("_"):
                    if word in self.lpg_type_by_motor: 
                        self.current_db._set_value(k,'fuelType','lpg')
                        i+=1
                        continue
                    elif  word in self.benzin_type_by_motor: 
                        self.current_db._set_value(k,'fuelType','benzin')
                        i+=1
                        continue
                    elif word in self.diesel_type_by_motor: 
                        self.current_db._set_value(k,'fuelType','diesel')
                        i+=1
                        continue
        print(f"completed fuel type in {i} adverts ")


    def complete_model(self):
        """completing audi models by data in adv title"""
        print("completing audi models")
        i=0
        for k, el in enumerate(self.current_db['name']):
            row = self.current_db.iloc[k]
            if str(row['model']).lower() in ['nan', 'na']:
                for i, word in enumerate(str(row['name']).lower().split("_")):
                    if word in self.audi_models:
                        self.current_db._set_value(k,'model',word)
                        i+=1   
                        continue
        print(f"completed audi models in {i} adverts ")

    def complete_gearbox(self):
        """completing column gearbox by data in adv title"""
        print("completing column gearbox")
        i=0
        for k,el in enumerate(self.current_db['name']):
            row = self.current_db.iloc[k]
            if str(row['gearbox']).lower() in ['nan','na']:
                for word in str(row['name']).lower().split("_"):
                    if word in ['automatik',]:
                        self.current_db._set_value(k, 'gearbox','automatik')
                        i+=1
                        continue
                    elif word == 'manuell':
                        self.current_db._set_value(k, 'gearbox','manuell')
                        i+=1
                        continue
        print(f"completed gearboxes in {i} adverts ")
        
    def create_list_from_column(self,column_name):
        return self.current_db[str(column_name)].unique().tolist()    
    
    @with_warning_message
    def compl_cat_func(self):
        """completing columns by data in adv title"""
        print("completing columns by data in adv title")
        self.str_var()
        self.complete_cat_fueltype()
        self.complete_model()
        self.complete_gearbox()
        
        """        
database = "./cars_selling.csv"

current_db = DB(database)

#urrent_db.compl_cat_func()

current_db.show()
"""
#90
