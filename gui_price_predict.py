import tkinter as tk
from tkinter import BOTH, E, END, HORIZONTAL, LEFT, NE, RIGHT, VERTICAL, W, Menu, ttk
from tkcalendar import *
from databaseorganistor import DB
import datetime
import matplotlib.pyplot as plt
from model import Model_pre
import pandas as pd

from matplotlib.pyplot import grid, plot, text

class Gui():
    def __init__(self,win, database = "./cars_selling_mod.csv"):
        self.win = win
        self.autoDB = DB(database)
        
        """Window setup"""
        win.geometry("880x680")
        win.resizable(0, 0)
        win.title("AutoStatsCreator - Price prediction")
        
        menubar = tk.Menu(win)
        win.config(menu=menubar)
        file_menu = Menu(menubar)        
        menubar.add_cascade(label = "Help", menu = file_menu)
        # file_menu.add_command(label='About',command = self.help)
        self.prepareGui(win)
        
    def prepareGui(self,win):
        
        ###  Frames
        vehTypeFrame =  tk.Frame(self.win)
        modelFrame = tk.Frame(self.win)
        brandFrame = tk.Frame(self.win)
        optFrame = tk.Frame(self.win)
        datesFrame = tk.Frame(self.win)
        
        priceFrame = tk.Frame(datesFrame)
        prodYearFrame = tk.Frame(datesFrame)
        powerPSFrame = tk.Frame(datesFrame)
        kmStandFrame = tk.Frame(datesFrame)
        dataCreatedFrame = tk.Frame(datesFrame)
        
        buttonFrame = tk.Frame(self.win)
        
        ### Brand
        self.BrandListBox = tk.Listbox(brandFrame,selectmode='multiple',exportselection = False)
        for el in sorted(self.autoDB.createListFromColumn('brand')): self.BrandListBox.insert(END, el)
        brandScrollBar = tk.Scrollbar(brandFrame)
        brandScrollBar.pack(side = RIGHT, fill = BOTH)
        self.BrandListBox.pack(fill = BOTH, side = LEFT)
        self.BrandListBox.config(yscrollcommand = brandScrollBar.set)
        brandScrollBar.config(command = self.BrandListBox.yview)
        brandFrame.grid(row = 1, column = 0)
        tk.Label(text="Choose brand").grid(row = 0, column = 0)
        
        ### Model
        self.modelListBox = tk.Listbox(modelFrame,selectmode='multiple',exportselection = False)
        for el in sorted(self.autoDB.createListFromColumn('model')): self.modelListBox.insert(END, el)
        modelScrollBar = tk.Scrollbar(modelFrame)
        modelScrollBar.pack(side=RIGHT, fill=BOTH)
        self.modelListBox.pack(fill = BOTH, side = LEFT)
        self.modelListBox.config(yscrollcommand = modelScrollBar.set)
        modelScrollBar.config(command = self.modelListBox.yview)
        modelFrame.grid(row = 1, column = 1)
        tk.Label(text = "Choose model").grid(row = 0, column = 1,ipady=5)
        
        ### vehType
        self.vehTypeListBox = tk.Listbox(vehTypeFrame, selectmode = 'multiple',exportselection = False)
        for el in sorted(self.autoDB.createListFromColumn('vehicleType')): self.vehTypeListBox.insert(END, el)
        vehTypeScrollBar = tk.Scrollbar(vehTypeFrame)
        vehTypeScrollBar.pack(side = RIGHT, fill = BOTH)
        self.vehTypeListBox.pack(fill = BOTH, side = LEFT)
        self.vehTypeListBox.config(yscrollcommand = vehTypeScrollBar.set)
        vehTypeScrollBar.config(command = self.vehTypeListBox.yview)
        vehTypeFrame.grid(row = 1, column = 2)
        tk.Label(text="Choose vehType").grid(row = 0, column = 2,ipady=5)

        ### GearBox
        
        tk.Label(optFrame, text = " Choose gearbox:").pack(side='top')
        self.gearBoxComboBox = ttk.Combobox(optFrame, values=sorted(self.autoDB.createListFromColumn('gearbox')))
        self.gearBoxComboBox.pack(side = 'top')
        self.gearBoxComboBox.current(1)
        
        ### fuelType
        tk.Label(optFrame, text = " Choose fuel type:").pack(side = 'top')
        self.fuelTypeComboBox = ttk.Combobox(optFrame, values=sorted(self.autoDB.createListFromColumn('fuelType')))
        self.fuelTypeComboBox.pack(side = 'top')
        self.fuelTypeComboBox.current(1)
        
        ### kmStand
        tk.Label(kmStandFrame, text = "km stand").grid(column = 0, row = 0)
        self.kmStandEntry = tk.Entry(kmStandFrame)
        self.kmStandEntry.insert(-1, '0')
        self.kmStandEntry.grid(column = 0, row = 1)

        
        ### Production Year
        tk.Label(prodYearFrame, text = "Production year:").grid(column = 0, row = 0)
        self.prodYearComboBox = ttk.Combobox(prodYearFrame, values = list(range(1900, 2023, 1)))
        self.prodYearComboBox.current(0)
        self.prodYearComboBox.grid(column = 0, row = 1)
        
        ### Power PS
        tk.Label(powerPSFrame, text = "Horse Power").grid(column = 0, row = 0)
        self.powerPSEntry = tk.Entry(powerPSFrame)
        self.powerPSEntry.insert(-1, '0')
        self.powerPSEntry.grid(column = 0, row = 1)


        ### frame placing
        optFrame.grid(row = 1, column = 3, ipady = 5)
        priceFrame.pack(side = 'top')
        kmStandFrame.pack(side = 'top')
        powerPSFrame.pack(side = 'top')
        prodYearFrame.pack(side = 'top')
        datesFrame.grid(row = 1, column = 4, ipady = 5)
        dataCreatedFrame.pack(side = 'top')
        buttonFrame.grid(row = 0, column = 4)
        
        tk.Button(buttonFrame, text = "Check price", command = lambda: self.getFilter()).grid(row = 0, column = 0,ipadx = 10)
        tk.Button(buttonFrame,text="Reset",command=lambda: self.cleanTable()).grid(row=0, column = 1,ipadx = 10)
        tk.Button(buttonFrame, text='Complete categories', command = lambda: self.autoDB.complCatFunc()).grid(row=0, column = 2,ipadx = 10)
        tk.Button(self.win, text='Check models', command = lambda: self.filterModelsByBrand()).grid(row=0, column = 3)
        
    
    def filterModelsByBrand(self):
        """getting available Models for selected brand"""
        self.getBrand()
        self.modelListBox.delete(0,END)
        self.getModelsDB = self.autoDB.current_db[self.autoDB.current_db['brand'].isin(self.filterBrand)]
        for el in sorted(self.getModelsDB['model'].unique().tolist()): self.modelListBox.insert(END, el)
                
    def filterAutos(self):
        """filtering datas based on values from filters"""
        self.autosDBF = self.autoDB.current_db
        self.autosDBF = self.autosDBF[(self.autosDBF.brand.isin(self.filterBrand))
                            & (self.autosDBF.model.isin(self.filterModel))
                            & (self.autosDBF.yearOfRegistration >= self.prodYearFilter - 1) 
                                & (self.autosDBF.yearOfRegistration <= self.prodYearFilter + 1)]
                
        if len(dbf_try := self.autosDBF[self.autosDBF.vehicleType.isin(self.filterVehType)]) >= 100:
            self.autosDBF = dbf_try
        if len(dbf_try := self.autosDBF[self.autosDBF.gearbox == self.gearboxFilter]) >= 100:
            self.autosDBF = dbf_try
        if len(dbf_try := self.autosDBF[self.autosDBF.fuelType == self.fuelTypeFilter]) >= 100:
            self.autosDBF = dbf_try
        
    def getModel(self):
        """getting current sellection of Models or all available Models"""
        self.filterModel = []
        if len(self.modelListBox.curselection()) !=0 :
            for i in self.modelListBox.curselection(): self.filterModel.append(self.modelListBox.get(i))
        else: self.filterModel = self.autoDB.createListFromColumn('model')
    
    def getBrand(self):
        """getting current sellection of Brands or all available Brands"""
        self.filterBrand= []
        if len(self.BrandListBox.curselection()) !=0 :
            for i in self.BrandListBox.curselection(): self.filterBrand.append(self.BrandListBox.get(i))
        else: self.filterBrand = self.autoDB.createListFromColumn('brand')
        
    def getVehType(self):
        """getting current sellection of Vehicle Type or all available types"""
        self.filterVehType = []
        if len(self.vehTypeListBox.curselection()) !=0 :
            for i in self.vehTypeListBox.curselection(): self.filterVehType.append(self.vehTypeListBox.get(i))
        else: self.filterVehType = self.autoDB.createListFromColumn('vehicleType')
        
    def getFilter(self):
        """getting current selection and filtering data"""
        self.getBrand()
        self.getVehType()
        self.getModel()
        self.getParams()
        self.filterAutos()
        print(self.filterBrand, self.filterModel, self.filterVehType, self.gearboxFilter, self.fuelTypeFilter
              , self.kmStandFilter, self.prodYearFilter, self.powerPSFilter)
        self.make_prediction()
    
    def getParams(self):
        """getting Gearbox, Fuel Type, km Stand, Year of production from GUI"""
        self.gearboxFilter = self.gearBoxComboBox.get()
        self.fuelTypeFilter = self.fuelTypeComboBox.get()
        self.kmStandFilter = int(self.kmStandEntry.get())
        self.powerPSFilter = int(self.powerPSEntry.get())

        self.prodYearFilter = int(self.prodYearComboBox.get())

    def transform_series(self):
        data_to_predict = {self.filterBrand[0]:[1], self.filterModel[0]:[1], self.filterVehType[0]:[1], self.gearboxFilter:[1]
                           , self.fuelTypeFilter:[1], float(self.prodYearFilter):[1],"powerPS": [int(self.powerPSFilter)]
                           , 'kilometer':[int(self.kmStandFilter)]}
        
        data_to_predict = pd.DataFrame.from_dict(data_to_predict)
        trans = Model_pre
        Model_pre.transform_c_powerPS(trans, data_to_predict)
        Model_pre.transform_c_kilometer(trans, data_to_predict)
        return data_to_predict.drop(columns=["powerPS","kilometer"])

        
    def make_prediction(self):
        #dbooo = "./cars_selling.csv"
        current_dbooo = self.autosDBF
        print("*************************")
        #print(current_dbooo.describe())
        #print(current_dbooo.info())

        #current_dbooo = current_dbooo[:100000]
        self.predicton_model = Model_pre(current_dbooo)
        self.predicton_model.prepare_datebase()
        self.predict_from_filter()

    def predict_from_filter(self):
        
        self.predicton_model.t_db = self.predicton_model.t_db.append(self.transform_series(), ignore_index=True)
        to_predict = self.predicton_model.t_db.tail(1).fillna(0).drop(columns = ["price"])
        
        
        self.predicton_model.predict_by_best_model(to_predict=to_predict)
        self.predicton_model.show_sampler()
        print(self.predicton_model.y_test.describe())

        self.predicton_model.t_db.to_excel("output.xlsx")  

        #print(self.predicton_model.t_db.columns.tolist())
        #print(self.predicton_model.reg.predict(_db))

              
    def statsFiltersAdv(self):
        ### count autos by Brand
        newDBFStatsBrand = self.autosDBF[['brand']].copy().dropna()
        newDBFStatsBrand['index1'] = newDBFStatsBrand.index
        newDBFStatsBrand = newDBFStatsBrand.groupby(['brand']).nunique()   
        newDBFStatsBrand.drop(newDBFStatsBrand[newDBFStatsBrand.index1 == 0 ].index, inplace= True)
        #print(str(newDBFStatsBrand))
        
        ### count autos by Model
        newDBFStatsModel = self.autosDBF[['model']].copy().dropna()
        newDBFStatsModel['index1'] = newDBFStatsModel.index
        newDBFStatsModel = newDBFStatsModel.groupby(['model']).nunique()   
        newDBFStatsModel.drop(newDBFStatsModel[newDBFStatsModel.index1 == 0 ].index, inplace= True)
        #print(str(newDBFStatsModel))
        
        ### count autos by vehicleType
        newDBFStatsVehType = self.autosDBF[['vehicleType']].copy().dropna()
        newDBFStatsVehType['index1'] = newDBFStatsVehType.index
        newDBFStatsVehType = newDBFStatsVehType.groupby(['vehicleType']).nunique()   
        newDBFStatsVehType.drop(newDBFStatsVehType[newDBFStatsVehType.index1 == 0 ].index, inplace= True)
        #print(str(newDBFStatsVehType))
        
        
        
#database = "./cars_selling_sh.csv"

#current_db = databaseorganistor.DB(database)

win = tk.Tk()
ourGui = Gui(win)
win.mainloop()

#406
