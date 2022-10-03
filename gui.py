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
        self.auto_DB = DB(database)
        
        """Window setup"""
        win.geometry("880x680")
        win.resizable(0, 0)
        win.title("Cars Adv Scroller")
        
        menubar = tk.Menu(win)
        win.config(menu=menubar)
        file_menu = Menu(menubar)        
        menubar.add_cascade(label = "Help", menu = file_menu)
        # file_menu.add_command(label='About',command = self.help)
        self.prepare_gui(win)
        
    def prepare_gui(self,win):
        
        ###  Frames
        veh_type_frame =  tk.Frame(self.win)
        model_frame = tk.Frame(self.win)
        brand_frame = tk.Frame(self.win)
        opt_frame = tk.Frame(self.win)
        dates_frame = tk.Frame(self.win)
        
        price_frame = tk.Frame(dates_frame)
        prod_year_frame = tk.Frame(dates_frame)
        km_stand_frame = tk.Frame(dates_frame)
        date_created_frame = tk.Frame(dates_frame)
        
        button_frame = tk.Frame(self.win)
        
        ### Brand
        self.brand_listbox = tk.Listbox(brand_frame,selectmode='multiple',exportselection = False)
        for el in sorted(self.auto_DB.create_list_from_column('brand')): self.brand_listbox.insert(END, el)
        brand_scrollbar = tk.Scrollbar(brand_frame)
        brand_scrollbar.pack(side = RIGHT, fill = BOTH)
        self.brand_listbox.pack(fill = BOTH, side = LEFT)
        self.brand_listbox.config(yscrollcommand = brand_scrollbar.set)
        brand_scrollbar.config(command = self.brand_listbox.yview)
        brand_frame.grid(row = 1, column = 0)
        tk.Label(text="Choose brand").grid(row = 0, column = 0)
        
        ### Model
        self.model_listbox = tk.Listbox(model_frame,selectmode='multiple',exportselection = False)
        for el in sorted(self.auto_DB.create_list_from_column('model')): self.model_listbox.insert(END, el)
        model_scrollbar = tk.Scrollbar(model_frame)
        model_scrollbar.pack(side=RIGHT, fill=BOTH)
        self.model_listbox.pack(fill = BOTH, side = LEFT)
        self.model_listbox.config(yscrollcommand = model_scrollbar.set)
        model_scrollbar.config(command = self.model_listbox.yview)
        model_frame.grid(row = 1, column = 1)
        tk.Label(text = "Choose model").grid(row = 0, column = 1,ipady=5)
        
        ### vehType
        self.veh_type_listbox = tk.Listbox(veh_type_frame, selectmode = 'multiple',exportselection = False)
        for el in sorted(self.auto_DB.create_list_from_column('vehicleType')): self.veh_type_listbox.insert(END, el)
        veh_type_scrollbar = tk.Scrollbar(veh_type_frame)
        veh_type_scrollbar.pack(side = RIGHT, fill = BOTH)
        self.veh_type_listbox.pack(fill = BOTH, side = LEFT)
        self.veh_type_listbox.config(yscrollcommand = veh_type_scrollbar.set)
        veh_type_scrollbar.config(command = self.veh_type_listbox.yview)
        veh_type_frame.grid(row = 1, column = 2)
        tk.Label(text="Choose vehType").grid(row = 0, column = 2,ipady=5)

        ### GearBox
        
        tk.Label(opt_frame, text = " Choose gearbox:").pack(side='top')
        self.gearbox_combobox = ttk.Combobox(opt_frame, values=sorted(self.auto_DB.create_list_from_column('gearbox')))
        self.gearbox_combobox.pack(side = 'top')
        self.gearbox_combobox.current(1)
        
        ### fuelType
        tk.Label(opt_frame, text = " Choose fuel type:").pack(side = 'top')
        self.fuel_type_combobox = ttk.Combobox(opt_frame, values=sorted(self.auto_DB.create_list_from_column('fuelType')))
        self.fuel_type_combobox.pack(side = 'top')
        self.fuel_type_combobox.current(1)
        
        ### seller
        tk.Label(opt_frame, text = " Choose seller:").pack(side = 'top')
        self.seller_combobox = ttk.Combobox(opt_frame, values = sorted(self.auto_DB.create_list_from_column('seller')))
        self.seller_combobox.pack(side = 'top')
        self.seller_combobox.current(1)
        
        ### nRepDamaged
        tk.Label(opt_frame, text = "Not demaged?").pack(side = 'top')
        self.n_rep_damaged_combobox = ttk.Combobox(opt_frame, values=sorted(self.auto_DB.create_list_from_column('notRepairedDamage')))
        self.n_rep_damaged_combobox.pack(side = 'top')
        self.n_rep_damaged_combobox.current(0)
        
        ### Price
        tk.Label(price_frame, text = "Lowest price").grid(column = 0, row = 0)
        tk.Label(price_frame,text = "Highest price").grid(column = 1, row = 0)
        self.price_low_entry = tk.Entry(price_frame)
        self.price_low_entry.insert(-1, '0')
        self.price_low_entry.grid(column = 0, row = 1)
        self.price_hi_entry = tk.Entry(price_frame)
        self.price_hi_entry.insert(-1, '90000')
        self.price_hi_entry.grid(column = 1, row = 1)
        
        ### kmStand
        tk.Label(km_stand_frame, text = "Min. km stand").grid(column = 0, row = 0)
        tk.Label(km_stand_frame,text = "Max. km stand").grid(column = 1, row = 0)
        self.km_stand_low_entry = tk.Entry(km_stand_frame)
        self.km_stand_low_entry.insert(-1, '0')
        self.km_stand_low_entry.grid(column = 0, row = 1)
        self.km_stand_hi_entry = tk.Entry(km_stand_frame)
        self.km_stand_hi_entry.insert(-1, '1000000')
        self.km_stand_hi_entry.grid(column = 1, row = 1)
        
        ### Production Year
        tk.Label(prod_year_frame, text = "Production year from:").grid(column = 0, row = 0)
        tk.Label(prod_year_frame,text = "Production year to:").grid(column = 1, row = 0)
        self.prod_year_low_combobox = ttk.Combobox(prod_year_frame, values = list(range(1900, 2023, 1)))
        self.prod_year_low_combobox.current(0)
        self.prod_year_low_combobox.grid(column = 0, row = 1)
        self.prod_year_hi_combobox = ttk.Combobox(prod_year_frame, values=list(range(1900, 2023, 1)))
        self.prod_year_hi_combobox.current('end')
        self.prod_year_hi_combobox.grid(column = 1, row = 1)
        
        ### Advert creation date
        tk.Label(date_created_frame, text="Created date from:").grid(column = 0, row = 0)
        tk.Label(date_created_frame,text="Created date to:").grid(column = 1,row = 0)
        self.date_created_low_entry=DateEntry(date_created_frame, dateformat = 3, width = 12, background = 'darkblue',
                            foreground = 'white', borderwidth = 4, year = 2000, month = 1, day = 1)
        self.date_created_low_entry.grid(row = 1, column = 0, sticky = 'ew')
        self.date_created_hi_entry=DateEntry(date_created_frame, dateformat = 3, width = 12, background = 'darkblue',
                            foreground = 'white', borderwidth = 4, Calendar = 2022)
        self.date_created_hi_entry.grid(row = 1, column = 1, sticky = 'ew')
        
        ### frame placing
        opt_frame.grid(row = 1, column = 3, ipady = 5)
        price_frame.pack(side = 'top')
        km_stand_frame.pack(side = 'top')
        prod_year_frame.pack(side = 'top')
        dates_frame.grid(row = 1, column = 4, ipady = 5)
        date_created_frame.pack(side = 'top')
        button_frame.grid(row = 0, column = 4)
        
        ### table
        results_frame = tk.Frame(self.win)
        self.results = ttk.Treeview(results_frame)
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
        results_frame.grid(row = 2, column = 0,columnspan = 5)
        
        tk.Button(button_frame, text = "Filtr", command = lambda: self.get_filter()).grid(row = 0, column = 0,ipadx = 10)
        tk.Button(button_frame,text="Reset",command=lambda: self.clean_table()).grid(row=0, column = 1,ipadx = 10)
        tk.Button(button_frame, text='Complete categories', command = lambda: self.auto_DB.compl_cat_func()).grid(row=0, column = 2,ipadx = 10)
        tk.Button(self.win, text='Check models', command = lambda: self.filter_models_by_brand()).grid(row=0, column = 3)
        
        self.prepare_chart_frame()
    
    def filter_models_by_brand(self):
        self.get_brand()
        self.model_listbox.delete(0,END)
        self.get_models_DB = self.auto_DB.current_db[self.auto_DB.current_db['brand'].isin(self.filter_brand)]
        for el in sorted(self.get_models_DB['model'].unique().tolist()): self.model_listbox.insert(END, el)
                
    def filter_autos(self):
        self.autos_DBF = self.auto_DB.current_db
        self.autos_DBF = self.autos_DBF[(self.autos_DBF.brand.isin(self.filter_brand))
                            & (self.autos_DBF.model.isin(self.filter_model))
                            & (self.autos_DBF.vehicleType.isin(self.filter_veh_type))
                            & (self.autos_DBF.gearbox == self.gearbox_filter)
                            & (self.autos_DBF.fuelType == self.fuel_type_filter)
                            & (self.autos_DBF.seller == self.seller_filter)
                            & (self.autos_DBF.notRepairedDamage == self.n_rep_damaged_filter)
                            & (self.autos_DBF.price >= self.low_price_filter)
                                & (self.autos_DBF.price <= self.high_price_filter)
                            & (self.autos_DBF.kilometer >= self.low_km_stand_filter) 
                                & (self.autos_DBF.kilometer <= self.high_km_stand_filter)
                            & (self.autos_DBF.yearOfRegistration >= self.low_prod_year_filter)
                                & (self.autos_DBF.yearOfRegistration <= self.high_prod_year_filter)
                            & (self.autos_DBF.dateCreated >= self.date_created_low_filter)
                                & (self.autos_DBF.dateCreated <= self.date_created_high_filter)]
        
        for k,el in enumerate(self.autos_DBF['name']):
            filtered_autos = self.autos_DBF.iloc[k]
            self.results.insert('', tk.END,
                values=(filtered_autos['brand'],filtered_autos['model'],filtered_autos['vehicleType'],
                filtered_autos['gearbox'],filtered_autos['fuelType'], filtered_autos['seller'], 
                filtered_autos['notRepairedDamage'], filtered_autos['price'], filtered_autos['kilometer'],
                filtered_autos['yearOfRegistration'], filtered_autos['dateCreated']))
            
        self.stats_filters_adv()


    def clean_table(self):
        self.make_chart()
        for row in self.results.get_children(): self.results.delete(row)
        
            
    def get_model(self):
        self.filter_model = []
        if len(self.model_listbox.curselection()) !=0 :
            for i in self.model_listbox.curselection(): self.filter_model.append(self.model_listbox.get(i))
        else: self.filter_model = self.auto_DB.create_list_from_column('model')
    
    def get_brand(self):
        self.filter_brand= []
        if len(self.brand_listbox.curselection()) !=0 :
            for i in self.brand_listbox.curselection(): self.filter_brand.append(self.brand_listbox.get(i))
        else: self.filter_brand = self.auto_DB.create_list_from_column('brand')
        
    def get_veh_type(self):
        self.filter_veh_type = []
        if len(self.veh_type_listbox.curselection()) !=0 :
            for i in self.veh_type_listbox.curselection(): self.filter_veh_type.append(self.veh_type_listbox.get(i))
        else: self.filter_veh_type = self.auto_DB.create_list_from_column('vehicleType')
        
    def get_filter(self):
        self.get_brand()
        self.get_veh_type()
        self.get_model()
        self.get_params()
        self.filter_autos()
    
    def get_params(self):
        self.gearbox_filter = self.gearbox_combobox.get()
        self.fuel_type_filter = self.fuel_type_combobox.get()
        self.seller_filter = self.seller_combobox.get()
        self.n_rep_damaged_filter = self.n_rep_damaged_combobox.get()
        self.low_price_filter = int(self.price_low_entry.get())
        self.high_price_filter = int(self.price_hi_entry.get())
        self.low_km_stand_filter = int(self.km_stand_low_entry.get())
        self.high_km_stand_filter = int(self.km_stand_hi_entry.get())
        self.low_prod_year_filter = int(self.prod_year_low_combobox.get())
        self.high_prod_year_filter = int(self.prod_year_hi_combobox.get())
        self.date_created_low_filter = self.date_created_low_entry.get()
        self.date_created_low_filter = datetime.datetime.strptime(str(self.date_created_low_filter),'%d.%m.%Y')
        self.date_created_high_filter = self.date_created_hi_entry.get()        
        self.date_created_high_filter = datetime.datetime.strptime(str(self.date_created_high_filter),'%d.%m.%Y')

    def make_chart(self):
        self.chart_DF = self.autos_DBF[['yearOfRegistration', 'price']]
        print(len(self.chart_DF['price']))
        outplot  = self.chart_DF.plot.hexbin(x = 'yearOfRegistration', y = 'price', gridsize = 25 )
        plt.show()
        print("typppppppppp")
        model = Model_pre(self.autos_DBF)
        model.make_profile()
        print(type(self.autos_DBF))
    
    def prepare_chart_frame(self):
        chart_frame =tk.Frame(self.win)
        cha_gen_label = tk.Label(chart_frame, text = 'Choose options for chart:',pady= 10)
        ch_X_axis_label = tk.Label(chart_frame, text = 'Choose X-axis:')
        ch_Y_axis_label = tk.Label(chart_frame, text = 'Choose Y-axis:')
        ch_chart_type_label = tk.Label(chart_frame, text= 'Choose chart type:')
        self.ch_X_axis_combobox = ttk.Combobox(chart_frame, values=['brand', 'model', 'vehicle_type', 'gearbox', 'fuelType',
                              'seller', 'nRepDamaged', 'price', 'kmStand', 'year', 'createData'])
        self.ch_Y_axis_combobox = ttk.Combobox(chart_frame, values=['brand', 'model', 'vehicle_type', 'gearbox', 'fuelType',
                              'seller', 'nRepDamaged', 'price', 'kmStand', 'year', 'createData'])       
        self.ch_chart_type_combobox = ttk.Combobox(chart_frame, values=['bar','hist','box','kde','area','scatter','hexbin','pie'])
        self.gen_chart_button = tk.Button(chart_frame,text="Generete chart", command= lambda: self.generete_chart() )
        cha_gen_label.pack(side = 'top')
        ch_X_axis_label.pack(side = 'top')
        self.ch_X_axis_combobox.pack(side = 'top')
        ch_Y_axis_label.pack(side = 'top')
        self.ch_Y_axis_combobox.pack(side = 'top')
        ch_chart_type_label.pack(side = 'top')
        self.ch_chart_type_combobox.pack(side = 'top')
        self.gen_chart_button.pack(side = 'top')
        chart_frame.grid(row = 3, column = 3)
    
    def generete_chart(self):
        x_axis, y_axis = str(self.ch_X_axis_combobox.get()), str(self.chYAxisComboBox.get())
        match self.chChartTypeComboBox.get():
            case "bar":
                self.chart_DF = self.autos_DBF[[x_axis, y_axis]]
                self.chart_DF.set_index(x_axis,inplace=True)
                print(self.chart_DF.info)
                self.chart_DF.plot.bar()
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
    
    def stats_filters_adv(self):
        ### count autos by Brand
        newDBFStatsBrand = self.autos_DBF[['brand']].copy().dropna()
        newDBFStatsBrand['index1'] = newDBFStatsBrand.index
        newDBFStatsBrand = newDBFStatsBrand.groupby(['brand']).nunique()   
        newDBFStatsBrand.drop(newDBFStatsBrand[newDBFStatsBrand.index1 == 0 ].index, inplace= True)
        print(str(newDBFStatsBrand))
        
        ### count autos by Model
        newDBFStatsModel = self.autos_DBF[['model']].copy().dropna()
        newDBFStatsModel['index1'] = newDBFStatsModel.index
        newDBFStatsModel = newDBFStatsModel.groupby(['model']).nunique()   
        newDBFStatsModel.drop(newDBFStatsModel[newDBFStatsModel.index1 == 0 ].index, inplace= True)
        print(str(newDBFStatsModel))
        
        ### count autos by vehicleType
        newDBFStatsVehType = self.autos_DBF[['vehicleType']].copy().dropna()
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
