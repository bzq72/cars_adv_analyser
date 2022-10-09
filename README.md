# Cars adv analyser
Program to browser cars adverts with option to predict car value. Main purpose of project is sharping programming skills and getting practical knowledge of working with data, predictions models and simple GUI.

### Method used:
- 	 Predictive Modelling
- 	 Data processing 
- 	 Inferential Statistics
- 	 Graphic User Interface
- 	 and more


### Technologies:
- 	 Python
- 	 Pandas, NumPy
- 	 scikit-learn
- 	 tkinter

## Installation

From link below download .RAR package and then run Cars_Adv_Analyser.exe. That's all!

https://www.dropbox.com/s/4zx3h7cghwaczc3/Cars_Adv_Analyser.rar?dl=0

## Project background:
First idea was creating simple adverts browser based on Tkinter library. As a database was used JSON from german website with cars adverts from 2016. During cleaning and preprocessing with Pandas library, appeared thought to completed blank/Nan values using information from advert name.  After completed this stage, project was abandoned.

After few weeks and learning more about machine learning, project has been given new lease of life. Idea was simple: based on knowledge about price and details from cars adverts, predict price of users car. To reach this goal, it was necessary to build regression models, transform database and more.

Currently, project is fully operational. 

Next ideas:
- 	complete help and menu;
- 	accelerate action;
- 	shorter code;
- 	 transfer program to website;
- 	 get actual adverts.


## User manual:
Program allowed user to browser cars adverts (browser window) and predict value of car (predictor window). 
Both windows are divided on few sections which are a little differ):
- 	 Navigation buttons:
	 - 	 "Open adverts browser" - switch to browser window
	 - 	 "Open price predictor" - switch to predictor window
- 	 Functions buttons - include buttons for void functions
- 	 Options choose frame - include widgets for setting cars features
- 	 Results frame - include results of user work

![This is an image](https://i.postimg.cc/hjjHSMmf/Frames.jpg)

### Browser window

*Functions buttons:*
- 	"Check models" - before using this button user have to select brand from brand frame. His function is showing available models in model frame for selected brands.
- 	"Filtr" - filtering adverts based on selected features and showing them in results frame.
- 	"Reset" - reset "Options choose frame" and "Result frame"
- 	"Complete missing data" - searching information about gearbox,  models, fuel type in advert description and with them fill up missing data.

*Options choose frame* - showing available cars features for filtering data.

*Results frame - showing filtered adverts


### Predictor window

In comparison with "Browser window" we can find few differences:
- "Check price" button - based on selected features, car price is estimating and showed in "Result frame":
- "Result frame" - include information about estimated value of user car and statistic about similar cars price: min, max, mean, median.

![This is an image](https://i.postimg.cc/GmmNPqMz/predi.jpg)



## Project review:

Project is divided on 5 classes:
- 	 DB - include: loading database from JSON format, changing columns types, data precleaning, completing functions;
- 	 Gui_Base - parent class for Browser and Price_Predictor, include main function for GUI organisation, abstractfunctions, warning decorator, getting parameters from filter and filtering;
- 	 Browser - include selecting items from parent class
- 	 Price_Predictor - include selecting items from parent class, modifications  of some parent functions, handling Model_Pre class;
- 	 Model_Pre - include price prediction functions by few regression models and preparing dataframe for their use.
	
	
### Selected programs features description:

#### Price prediction:
Data for car prediction are sourced from main database by filtering similar cars features. Filters are setted by user. There are also extra filters to unselect extremal variables value. Selected advert must have same brand and model, production year has 2 years deviation. If we have more than 100 filtered adverts, we are using sequentially: gearbox, fuel type, vehicle type filter, until amount of adverts is above 100. Next columns powerPS, kilometr stand, production year are transforming to boolean columns. PowerPS, kilometr stand are dividing to ranges. Production year columns are divided for each year boolean columns. We are not in possession information about models generations, if we take a look on price-production year chart we see stepped line, that js why we are treating this variable as categorical one. Afterwards set is divided to train and test one. 
For most accurate price estimating, prediction is made by few regression models: linear regression, lasso regression, ridge regression, AdaBoost regression, Random Forrest regressor, K-nearest Neighbours Regression. To predict price is chosen, this one with best r^2 score.

#### Completing categories:
Mostly website users during creating their cars selling adverts aren't filling all of avaiable features. However, they put a lot of infromation in adverts title or description e.g.: "VW_PASSAT_1.9_TDI_131_PS_LEDER", "BMW_530d_touring_Vollausstattung_NAVI", "Opel_meriva_1.6_16_v_lpg__z16xe_no_OPC". With such information and knowledge what we are searching, we can try to fill up missing values.
Program has a static variables signed for some categories (gearbox, fuel type, model (for now only audi models)). In adverts names we are searching this static variables for missing values in columns. If found, information is assigned.












