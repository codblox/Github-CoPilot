# Code to convert replace .PR from a string to p 

string1 = "EPR.PRC"
string2 = string1.replace("PR", "p")

#compare two pandas series for common values

import pandas as pd
import numpy as np

series1 = pd.Series([1,2,3,4,5,6,7,8,9,10])
series2 = pd.Series([1,2,3,4,5,6,7,8,9,10])

series1.isin(series2) 