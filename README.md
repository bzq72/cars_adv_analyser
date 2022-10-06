Cars adv analyser

Program to browser cars adverts with option to predict car value. Main purpose of project is sharping programming skills and getting practical knowledge of working with data, predictions models and simple GUI.
Method used:

    Predictive Modeling
    Data processing
    Inferential Statistics
    Graphic User Interface
    and more

Technologies:

    Python
    Pandas, NumPy
    scikit-learn
    tkinter

Project background:

First idea was creating simple adverts browser based on Tkinter library. As a database was used JSON from german website with cars adverts from 2016. During cleaning and preprocessing with Pandas library, appeared thought to completed blank/Nan values using informations from advert name. After completed this stage, project was abandoned.

After few weeks and learning more about machine learning, project has been given new lease of life. Idea was simple: based on knowlegde about price and details from cars adverts, predict price of users car. To reach this goal, it was necessary to build regression models, transform database and more.

Currently project is fully operational.

Next ideas:

    complete help and manu;
    accelerate action;
    shorter code;
    transfer program to website;
    get actual adverts.

Project description:
User manual:

Program allowed user to browser cars adverts (browser window) and predtict value of car (predictor window).
Both windows are devided on few section which are a little differ):

    Navigation buttons:
        “Open adverts browser” - switch to browser window
        “Open price predictor” - switch to predictor window
    Functions buttons - include buttons for void functions
    Options choose frame - include widgets for setting cars features
    Results frame - include results of user work

Browser window

Funtions buttons:

    “Check models” - before using this button user have to select brand from brand frame. His function is showing available models in model frame for selected brands.
    “Filtr” - filtering adverts based on selected features and showing them in results frame.
    “Reset” - reset “Options choose frame” and “Result frame”
    “Complete missing data” - searching information about gearbox, models, fuel type in advert description and with them fill up missing data.

Options choose frame - showing available cars features for fiktering data.

Results frame - showing filtered adverts
Predictor window

In comparison with “Browser window” we can fine few differences:

    “Check prize” button - based on selected features, car price is estimating and showed in “Result frame”:
    “Result frame” - include informations about estimated value of user car and statistic about similar cars price: min, max, mean, median.
