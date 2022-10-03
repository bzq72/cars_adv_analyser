import tkinter as tk
from tkinter import BOTH, E, END, HORIZONTAL, LEFT, NE, RIGHT, VERTICAL, W, Menu, ttk
from tkcalendar import *
from databaseorganistor import DB
import datetime
import matplotlib.pyplot as plt
from model import Model_pre

from matplotlib.pyplot import grid, plot, text

class Gui():
    def __init__(self,win, database = "./cars_selling_mod.csv"):
        self.win = win
        self.autoDB = DB(database)
        
        """Window setup"""
        win.geometry("880x680")
        win.resizable(0, 0)
        win.title("AutoStatsCreator")
        
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
        
        ### seller
        tk.Label(optFrame, text = " Choose seller:").pack(side = 'top')
        self.sellerComboBox = ttk.Combobox(optFrame, values = sorted(self.autoDB.createListFromColumn('seller')))
        self.sellerComboBox.pack(side = 'top')
        self.sellerComboBox.current(1)
        
        ### nRepDamaged
        tk.Label(optFrame, text = "Not demaged?").pack(side = 'top')
        self.nRepDamagedComboBox = ttk.Combobox(optFrame, values=sorted(self.autoDB.createListFromColumn('notRepairedDamage')))
        self.nRepDamagedComboBox.pack(side = 'top')
        self.nRepDamagedComboBox.current(0)
        
        ### Price
        tk.Label(priceFrame, text = "Lowest price").grid(column = 0, row = 0)
        tk.Label(priceFrame,text = "Highest price").grid(column = 1, row = 0)
        self.priceLowEntry = tk.Entry(priceFrame)
        self.priceLowEntry.insert(-1, '0')
        self.priceLowEntry.grid(column = 0, row = 1)
        self.priceHiEntry = tk.Entry(priceFrame)
        self.priceHiEntry.insert(-1, '90000')
        self.priceHiEntry.grid(column = 1, row = 1)
        
        ### kmStand
        tk.Label(kmStandFrame, text = "Min. km stand").grid(column = 0, row = 0)
        tk.Label(kmStandFrame,text = "Max. km stand").grid(column = 1, row = 0)
        self.kmStandLowEntry = tk.Entry(kmStandFrame)
        self.kmStandLowEntry.insert(-1, '0')
        self.kmStandLowEntry.grid(column = 0, row = 1)
        self.kmStandHiEntry = tk.Entry(kmStandFrame)
        self.kmStandHiEntry.insert(-1, '1000000')
        self.kmStandHiEntry.grid(column = 1, row = 1)
        
        ### Production Year
        tk.Label(prodYearFrame, text = "Production year from:").grid(column = 0, row = 0)
        tk.Label(prodYearFrame,text = "Production year to:").grid(column = 1, row = 0)
        self.prodYearLowComboBox = ttk.Combobox(prodYearFrame, values = list(range(1900, 2023, 1)))
        self.prodYearLowComboBox.current(0)
        self.prodYearLowComboBox.grid(column = 0, row = 1)
        self.prodYearHighComboBox = ttk.Combobox(prodYearFrame, values=list(range(1900, 2023, 1)))
        self.prodYearHighComboBox.current('end')
        self.prodYearHighComboBox.grid(column = 1, row = 1)
        
        ### Advert creation date
        tk.Label(dataCreatedFrame, text="Created date from:").grid(column = 0, row = 0)
        tk.Label(dataCreatedFrame,text="Created date to:").grid(column = 1,row = 0)
        self.dateCreatedLowEntry=DateEntry(dataCreatedFrame, dateformat = 3, width = 12, background = 'darkblue',
                            foreground = 'white', borderwidth = 4, year = 2000, month = 1, day = 1)
        self.dateCreatedLowEntry.grid(row = 1, column = 0, sticky = 'ew')
        self.dateCreatedHighEntry=DateEntry(dataCreatedFrame, dateformat = 3, width = 12, background = 'darkblue',
                            foreground = 'white', borderwidth = 4, Calendar = 2022)
        self.dateCreatedHighEntry.grid(row = 1, column = 1, sticky = 'ew')
        
        ### frame placing
        optFrame.grid(row = 1, column = 3, ipady = 5)
        priceFrame.pack(side = 'top')
        kmStandFrame.pack(side = 'top')
        prodYearFrame.pack(side = 'top')
        datesFrame.grid(row = 1, column = 4, ipady = 5)
        dataCreatedFrame.pack(side = 'top')
        buttonFrame.grid(row = 0, column = 4)
        
        ### table
        resultsFrame = tk.Frame(self.win)
        self.results = ttk.Treeview(resultsFrame)
        self.results['columns'] = ('brand', 'model', 'vehicle_type', 'gearbox', 'fuelType',
                              'seller', 'nRepDamaged', 'price', 'kmStand', 'year', 'createData')
        self.results.column("#0", width=0,  stretch='no')
        self.results.column("brand", anchor='center', width=80)
        self.results.column("model", anchor='center',width=80)
        self.results.column("vehicle_type", anchor='center',width=80)
        self.results.column("gearbox", anchor='center',width=80)
        self.results.column("fuelType", anchor='center',width=80)
        self.results.column("seller", anchor='center',width=80)
        self.results.column("nRepDamaged", anchor = 'center',width=80)
        self.results.column("price", anchor = 'center',width=80)
        self.results.column("kmStand", anchor = 'center',width=80)
        self.results.column("year", anchor = 'center',width=80)
        self.results.column("createData", anchor = 'center',width=80)

        self.results.heading("#0",text="",anchor='center')
        self.results.heading("brand",text="Brand",anchor='center')
        self.results.heading("model",text="Model",anchor='center')
        self.results.heading("vehicle_type",text="Vehicle type",anchor='center')
        self.results.heading("gearbox",text="Gearbox",anchor='center')
        self.results.heading("fuelType",text="Fuel Type",anchor='center')
        self.results.heading("seller",text="Seller",anchor='center')
        self.results.heading("nRepDamaged",text="Dameged",anchor='center')
        self.results.heading("price",text="Price",anchor='center')
        self.results.heading("kmStand",text="km stand",anchor='center')
        self.results.heading("year",text="Prod data",anchor='center')
        self.results.heading("createData",text="Offer created",anchor='center')
        
        self.results.grid(row = 0, column = 0)
        resultsFrame.grid(row = 2, column = 0,columnspan = 5)
        
        tk.Button(buttonFrame, text = "Filtr", command = lambda: self.getFilter()).grid(row = 0, column = 0,ipadx = 10)
        tk.Button(buttonFrame,text="Reset",command=lambda: self.cleanTable()).grid(row=0, column = 1,ipadx = 10)
        tk.Button(buttonFrame, text='Complete categories', command = lambda: self.autoDB.complCatFunc()).grid(row=0, column = 2,ipadx = 10)
        tk.Button(self.win, text='Check models', command = lambda: self.filterModelsByBrand()).grid(row=0, column = 3)
        
        self.prepareChartFrame()
    
    def filterModelsByBrand(self):
        self.getBrand()
        self.modelListBox.delete(0,END)
        self.getModelsDB = self.autoDB.current_db[self.autoDB.current_db['brand'].isin(self.filterBrand)]
        for el in sorted(self.getModelsDB['model'].unique().tolist()): self.modelListBox.insert(END, el)
                
    def filterAutos(self):
        self.autosDBF = self.autoDB.current_db
        self.autosDBF = self.autosDBF[(self.autosDBF.brand.isin(self.filterBrand))
                            & (self.autosDBF.model.isin(self.filterModel))
                            & (self.autosDBF.vehicleType.isin(self.filterVehType))
                            & (self.autosDBF.gearbox == self.gearboxFilter)
                            & (self.autosDBF.fuelType == self.fuelTypeFilter)
                            & (self.autosDBF.seller == self.sellerFilter)
                            & (self.autosDBF.notRepairedDamage == self.nRepDamagedFilter)
                            & (self.autosDBF.price >= self.lowPriceFilter)
                                & (self.autosDBF.price <= self.highPriceFilter)
                            & (self.autosDBF.kilometer >= self.lowKmStandFilter) 
                                & (self.autosDBF.kilometer <= self.highKmStandFilter)
                            & (self.autosDBF.yearOfRegistration >= self.lowProdYearFilter) 
                                & (self.autosDBF.yearOfRegistration <= self.highProdYearFilter)
                            & (self.autosDBF.dateCreated >= self.dateCreatedLowFilter)
                                & (self.autosDBF.dateCreated <= self.dateCreatedHighFilter)]
        
        for k,el in enumerate(self.autosDBF['name']):
            filteredAutos = self.autosDBF.iloc[k]
            self.results.insert('', tk.END,
                values=(filteredAutos['brand'],filteredAutos['model'],filteredAutos['vehicleType'],
                filteredAutos['gearbox'],filteredAutos['fuelType'], filteredAutos['seller'], 
                filteredAutos['notRepairedDamage'], filteredAutos['price'], filteredAutos['kilometer'],
                filteredAutos['yearOfRegistration'], filteredAutos['dateCreated']))
            
        self.statsFiltersAdv()


    def cleanTable(self):
        self.makeChart()
        for row in self.results.get_children(): self.results.delete(row)
        
            
    def getModel(self):
        self.filterModel = []
        if len(self.modelListBox.curselection()) !=0 :
            for i in self.modelListBox.curselection(): self.filterModel.append(self.modelListBox.get(i))
        else: self.filterModel = self.autoDB.createListFromColumn('model')
    
    def getBrand(self):
        self.filterBrand= []
        if len(self.BrandListBox.curselection()) !=0 :
            for i in self.BrandListBox.curselection(): self.filterBrand.append(self.BrandListBox.get(i))
        else: self.filterBrand = self.autoDB.createListFromColumn('brand')
        
    def getVehType(self):
        self.filterVehType = []
        if len(self.vehTypeListBox.curselection()) !=0 :
            for i in self.vehTypeListBox.curselection(): self.filterVehType.append(self.vehTypeListBox.get(i))
        else: self.filterVehType = self.autoDB.createListFromColumn('vehicleType')
        
    def getFilter(self):
        self.getBrand()
        self.getVehType()
        self.getModel()
        self.getParams()
        self.filterAutos()
    
    def getParams(self):
        self.gearboxFilter = self.gearBoxComboBox.get()
        self.fuelTypeFilter = self.fuelTypeComboBox.get()
        self.sellerFilter = self.sellerComboBox.get()
        self.nRepDamagedFilter = self.nRepDamagedComboBox.get()
        self.lowPriceFilter = int(self.priceLowEntry.get())
        self.highPriceFilter = int(self.priceHiEntry.get())
        self.lowKmStandFilter = int(self.kmStandLowEntry.get())
        self.highKmStandFilter = int(self.kmStandHiEntry.get())
        self.lowProdYearFilter = int(self.prodYearLowComboBox.get())
        self.highProdYearFilter = int(self.prodYearHighComboBox.get())
        self.dateCreatedLowFilter = self.dateCreatedLowEntry.get()
        self.dateCreatedLowFilter = datetime.datetime.strptime(str(self.dateCreatedLowFilter),'%d.%m.%Y')
        self.dateCreatedHighFilter = self.dateCreatedHighEntry.get()        
        self.dateCreatedHighFilter = datetime.datetime.strptime(str(self.dateCreatedHighFilter),'%d.%m.%Y')

    def makeChart(self):
        self.chartDF = self.autosDBF[['yearOfRegistration', 'price']]
        print(len(self.chartDF['price']))
        outplot  = self.chartDF.plot.hexbin(x = 'yearOfRegistration', y = 'price', gridsize = 25 )
        plt.show()
        print("typppppppppp")
        model = Model_pre(self.autosDBF)
        model.make_profile()
        print(type(self.autosDBF))
    
    def prepareChartFrame(self):
        chartFrame =tk.Frame(self.win)
        chaGenLabel = tk.Label(chartFrame, text = 'Choose options for chart:',pady= 10)
        chXAxisLabel = tk.Label(chartFrame, text = 'Choose X-axis:')
        chYAxisLabel = tk.Label(chartFrame, text = 'Choose Y-axis:')
        chChartTypeLabel = tk.Label(chartFrame, text= 'Choose chart type:')
        self.chXAxisComboBox = ttk.Combobox(chartFrame, values=['brand', 'model', 'vehicle_type', 'gearbox', 'fuelType',
                              'seller', 'nRepDamaged', 'price', 'kmStand', 'year', 'createData'])
        self.chYAxisComboBox = ttk.Combobox(chartFrame, values=['brand', 'model', 'vehicle_type', 'gearbox', 'fuelType',
                              'seller', 'nRepDamaged', 'price', 'kmStand', 'year', 'createData'])       
        self.chChartTypeComboBox = ttk.Combobox(chartFrame, values=['bar','hist','box','kde','area','scatter','hexbin','pie'])
        self.genChartButton = tk.Button(chartFrame,text="Generete chart", command= lambda: self.genereteChart() )
        chaGenLabel.pack(side = 'top')
        chXAxisLabel.pack(side = 'top')
        self.chXAxisComboBox.pack(side = 'top')
        chYAxisLabel.pack(side = 'top')
        self.chYAxisComboBox.pack(side = 'top')
        chChartTypeLabel.pack(side = 'top')
        self.chChartTypeComboBox.pack(side = 'top')
        self.genChartButton.pack(side = 'top')
        chartFrame.grid(row = 3, column = 3)
    
    def genereteChart(self):
        xAxis, yAxis = str(self.chXAxisComboBox.get()), str(self.chYAxisComboBox.get())
        match self.chChartTypeComboBox.get():
            case "bar":
                self.chartDF = self.autosDBF[[xAxis, yAxis]]
                self.chartDF.set_index(xAxis,inplace=True)
                print(self.chartDF.info)
                self.chartDF.plot.bar()
                print('bar')
            case 'hist':
                pass
            case 'box':
                pass
            case'kde':
                pass
            case 'area':
                pass
            case 'scatter':
                pass
            case 'hexbin':
                pass
            case 'pie':
                pass
            
        plt.show()
    
    def statsFiltersAdv(self):
        ### count autos by Brand
        newDBFStatsBrand = self.autosDBF[['brand']].copy().dropna()
        newDBFStatsBrand['index1'] = newDBFStatsBrand.index
        newDBFStatsBrand = newDBFStatsBrand.groupby(['brand']).nunique()   
        newDBFStatsBrand.drop(newDBFStatsBrand[newDBFStatsBrand.index1 == 0 ].index, inplace= True)
        print(str(newDBFStatsBrand))
        
        ### count autos by Model
        newDBFStatsModel = self.autosDBF[['model']].copy().dropna()
        newDBFStatsModel['index1'] = newDBFStatsModel.index
        newDBFStatsModel = newDBFStatsModel.groupby(['model']).nunique()   
        newDBFStatsModel.drop(newDBFStatsModel[newDBFStatsModel.index1 == 0 ].index, inplace= True)
        print(str(newDBFStatsModel))
        
        ### count autos by vehicleType
        newDBFStatsVehType = self.autosDBF[['vehicleType']].copy().dropna()
        newDBFStatsVehType['index1'] = newDBFStatsVehType.index
        newDBFStatsVehType = newDBFStatsVehType.groupby(['vehicleType']).nunique()   
        newDBFStatsVehType.drop(newDBFStatsVehType[newDBFStatsVehType.index1 == 0 ].index, inplace= True)
        print(str(newDBFStatsVehType))
        
        
        
#database = "./cars_selling_sh.csv"

#current_db = databaseorganistor.DB(database)

win = tk.Tk()
ourGui = Gui(win)
win.mainloop()

#406
