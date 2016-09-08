# -*- coding: utf-8 -*-
"""
Spyder Editor


"""

import quandl
import seaborn 

"""This sets the Quandl API Key"""

quandl.ApiConfig.api_key="Your API KEY"
rigs=quandl.get("BKRHUGHES/RIGS_BY_STATE_TOTALUS_LAND")
oil=quandl.get("CHRIS/CME_CL1")
oil.High.plot()
rigs.plot()