from genericpath import exists
import tkinter as tk
from tkinter import BOTH, E, END, HORIZONTAL, LEFT, NE, RIGHT, VERTICAL, W, Menu, ttk
from tkcalendar import *
from databaseorganistor import DB
import datetime
import matplotlib.pyplot as plt
from model import Model_pre
import pandas as pd

from matplotlib.pyplot import grid, plot, text
from gui_base import gui_base
from tkinter import messagebox


class price_predictor(gui_base):
    def prepare_gui(self):
        self.prepare_frames()
        self.prepare_brand_frame()
        self.prepare_buttons()
        self.prepare_fueltype_frame()
        self.prepare_vehtype_frame()
        self.prepare_gearbox_frame()
        self.prepare_km_stand_frame()
        self.prepare_model_frame()
        self.prepare_prod_year_frame()
        self.prepare_price_frame()
        self.prepare_power_ps_frame()
        self.placing_frame()
        
    def prepare_frames(self):
        self.veh_type_main_frame =  tk.Frame(self.main_frame)
        self.veh_type_frame =  tk.Frame(self.veh_type_main_frame)
        self.model_main_frame = tk.Frame(self.main_frame)
        self.model_frame = tk.Frame(self.model_main_frame)
        self.brand_main_frame = tk.Frame(self.main_frame)
        self.brand_frame = tk.Frame(self.brand_main_frame)
        self.opt_frame = tk.Frame(self.main_frame)
        self.dates_frame = tk.Frame(self.main_frame)
        self.price_frame = tk.Frame(self.dates_frame)
        self.prod_year_frame = tk.Frame(self.dates_frame)
        self.km_stand_frame = tk.Frame(self.dates_frame)
        self.date_created_frame = tk.Frame(self.dates_frame)
        self.button_frame = tk.Frame(self.main_frame)
        self.pred_frame = tk.Frame(self.main_frame)
        self.power_ps_frame = tk.Frame(self.dates_frame)

        
    def prepare_km_stand_frame(self):
        tk.Label(self.km_stand_frame, text = "Actual km stand").grid(column = 0, row = 0)
        self.km_stand_entry = tk.Entry(self.km_stand_frame)
        self.km_stand_entry.insert(-1, '150000')
        self.km_stand_entry.grid(column = 0, row = 1)

        
    def prepare_prod_year_frame(self):
        tk.Label(self.prod_year_frame, text = "Production year:").grid(column = 0, row = 0)
        self.prod_year_combobox = ttk.Combobox(self.prod_year_frame, values = list(range(1900, 2023, 1)))
        self.prod_year_combobox.current(100)
        self.prod_year_combobox.grid(column = 0, row = 1)
        
    def prepare_power_ps_frame(self):
        tk.Label(self.power_ps_frame, text = "Horse Power").grid(column = 0, row = 0)
        self.power_ps_entry = tk.Entry(self.power_ps_frame)
        self.power_ps_entry.insert(-1, '100')
        self.power_ps_entry.grid(column = 0, row = 1)

    def placing_frame(self):
        self.opt_frame.grid(row = 1, column = 3, ipady = 5)
        self.km_stand_frame.pack(side = 'top')
        self.pred_frame.grid(row = 2, column = 2)
        self.power_ps_frame.pack(side = 'top')
        self.prod_year_frame.pack(side = 'top')
        self.dates_frame.grid(row = 1, column = 4, ipady = 5)
        self.button_frame.grid(row = 0, column = 4)
        
        
    def price_pred_frame(self):
        tk.Label(self.pred_frame, text = "Your car is worth: ").grid(column = 0, row = 0)
        tk.Label(self.pred_frame, text = f" Euro" ).grid(column = 0, row = 1)
        
    def prepare_buttons(self):
        tk.Button(self.button_frame, text = "Check price", command = lambda: self.get_filter()).grid(row = 0, column = 0)
        tk.Button(self.button_frame, text='Complete missing data', command = self.auto_DB.compl_cat_func).grid(row=0, column = 1)
        tk.Button(self.main_frame, text='Check models', command = lambda: self.filter_models_by_brand()).grid(row=0, column = 1)
                
    def filter_autos(self):
        """filtering datas based on values from filters"""
        self.autos_DBF = self.auto_DB.current_db
        self.autos_DBF = self.autos_DBF[(self.autos_DBF.brand.isin(self.filter_brand))
                            & (self.autos_DBF.model.isin(self.filter_model))
                            & (self.autos_DBF.yearOfRegistration >= self.prod_year_filter - 2) 
                                & (self.autos_DBF.yearOfRegistration <= self.prod_year_filter + 2)]
                
        if len(dbf_try := self.autos_DBF[self.autos_DBF.gearbox == self.gearbox_filter]) >= 100:
            self.autos_DBF = dbf_try
        if len(dbf_try := self.autos_DBF[self.autos_DBF.fuelType == self.fuel_type_filter]) >= 100:
            self.autos_DBF = dbf_try
        if len(dbf_try := self.autos_DBF[self.autos_DBF.vehicleType.isin(self.filter_veh_type)]) >= 100:
            self.autos_DBF = dbf_try
        
    def get_filter(self):
        """getting current selection and filtering data"""
        super().get_filter()
        if ((len(self.filter_brand)!=1) or (len(self.filter_veh_type)!=1) or (len(self.filter_model)!=1)):
            messagebox.showerror("Error", "Please choose one varaible for each category")
            return
            
        self.make_prediction()
    
    def get_params(self):
        """getting Gearbox, Fuel Type, km Stand, Year of production from GUI"""
        self.gearbox_filter = self.gearbox_combobox.get()
        self.fuel_type_filter = self.fuel_type_combobox.get()
        self.km_stand_filter = int(self.km_stand_entry.get())
        self.power_ps_filter = int(self.power_ps_entry.get())
        self.prod_year_filter = int(self.prod_year_combobox.get())
        

    def transform_series(self):
        data_to_predict = {self.filter_brand[0]:[1], self.filter_model[0]:[1], self.filter_veh_type[0]:[1], self.gearbox_filter:[1]
                           , self.fuel_type_filter:[1], float(self.prod_year_filter):[1],"powerPS": [int(self.power_ps_filter)]
                           , 'kilometer':[int(self.km_stand_filter)], 'nein':1}
        
        data_to_predict = pd.DataFrame.from_dict(data_to_predict)
        trans = Model_pre
        Model_pre.transform_c_powerPS(trans, data_to_predict)
        Model_pre.transform_c_kilometer(trans, data_to_predict)
        return data_to_predict.drop(columns=["powerPS","kilometer"])

        
    def make_prediction(self):
        current_dbooo = self.autos_DBF
        self.predicton_model = Model_pre(current_dbooo)
        self.predicton_model.prepare_datebase()
        self.predict_from_filter()

    def predict_from_filter(self):
        
        self.predicton_model.t_db = self.predicton_model.t_db.append(self.transform_series(), ignore_index=True)
        to_predict = self.predicton_model.t_db.tail(1).fillna(0).drop(columns = ["price"])
        
        pred_price = int(self.predicton_model.predict_by_best_model(to_predict=to_predict)[0])
        self.predicton_model.show_sampler()
        print(self.predicton_model.y_test.describe())
        
        self.pred_frame.destroy()
        self.pred_frame = tk.Frame(self.main_frame)
        tk.Label(self.pred_frame, text = "Your car is worth: ").pack(side = 'top')
        tk.Label(self.pred_frame, text = f"{pred_price} Euro" ).pack(side = 'top')
        tk.Label(self.pred_frame, text = "Cars similar to yours are worth:").pack(side = 'top')
        tk.Label(self.pred_frame, text = f"min.: {int(self.predicton_model.y.min())} Euro" ).pack(side = 'top')
        tk.Label(self.pred_frame, text = f"max.: {int(self.predicton_model.y.max())} Euro" ).pack(side = 'top')
        tk.Label(self.pred_frame, text = f"mean: {int(self.predicton_model.y.mean())} Euro" ).pack(side = 'top')
        tk.Label(self.pred_frame, text = f"median: {int(self.predicton_model.y.median())} Euro" ).pack(side = 'top')

        self.pred_frame.grid(row = 2, column = 2)
        
        self.predicton_model.t_db.to_excel("output.xlsx")  

        #print(self.predicton_model.t_db.columns.tolist())
        #print(self.predicton_model.reg.predict(_db))

              
    def statsFiltersAdv(self):
        ### count autos by Brand
        newDBFStatsBrand = self.autos_DBF[['brand']].copy().dropna()
        newDBFStatsBrand['index1'] = newDBFStatsBrand.index
        newDBFStatsBrand = newDBFStatsBrand.groupby(['brand']).nunique()   
        newDBFStatsBrand.drop(newDBFStatsBrand[newDBFStatsBrand.index1 == 0 ].index, inplace= True)
        #print(str(newDBFStatsBrand))
        
        ### count autos by Model
        newDBFStatsModel = self.autos_DBF[['model']].copy().dropna()
        newDBFStatsModel['index1'] = newDBFStatsModel.index
        newDBFStatsModel = newDBFStatsModel.groupby(['model']).nunique()   
        newDBFStatsModel.drop(newDBFStatsModel[newDBFStatsModel.index1 == 0 ].index, inplace= True)
        #print(str(newDBFStatsModel))
        
        ### count autos by vehicleType
        newDBFStatsVehType = self.autos_DBF[['vehicleType']].copy().dropna()
        newDBFStatsVehType['index1'] = newDBFStatsVehType.index
        newDBFStatsVehType = newDBFStatsVehType.groupby(['vehicleType']).nunique()   
        newDBFStatsVehType.drop(newDBFStatsVehType[newDBFStatsVehType.index1 == 0 ].index, inplace= True)
        #print(str(newDBFStatsVehType))
        
        
        
#database = "./cars_selling_sh.csv"

#current_db = databaseorganistor.DB(database)

"""win = tk.Tk()
ourGui = price_predictor(win)
win.mainloop()"""

#406
