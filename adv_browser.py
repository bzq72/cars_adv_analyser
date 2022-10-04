from gui_base import gui_base

class Browser(gui_base):
    def prepare_gui(self):
        """preparing gui"""
        self.prepare_frames()
        self.prepare_brand_frame()
        self.prepare_buttons()
        self.prepare_creation_frame()
        self.prepare_fueltype_frame()
        self.prepare_vehtype_frame()
        self.prepare_gearbox_frame()
        self.prepare_km_stand_frame()
        self.prepare_model_frame()
        self.prepare_n_rep_damaged_frame()
        self.prepare_price_frame()
        self.prepare_prod_year_frame()
        self.prepare_seller_frame()
        self.placing_frame()
        self.adv_browser()   
        
    def get_filter(self):
        """getting current selection and filtering data"""
        self.clean_table()
        super().get_filter()
        