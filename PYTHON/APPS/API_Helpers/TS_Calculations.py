# -*- coding: utf-8 -*-
"""
    TS_Calculations.py - Helper methods for miscellaneous calculations
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: July 25, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

import os
os.chdir('<INSERT-PROJECT-ROOT-DIR-HERE>')

import random
import numpy as np

##############################################################################

# Function that avoids zero division error.
def safe_divide(n, d):
    
    ret = 0.0
    
    try:
        ret = float(n) / d
    except ZeroDivisionError:
        ret = 0.0
    
    return ret

##############################################################################
    
# Calculate portfolio rets (assets in columns, index as timestamps)
def calculate_portfolio_returns(_df, cumulative=True):
    
    # _df = None 
    
    if cumulative is True:
        _df = (1 + _df.fillna(method='bfill').pct_change()\
        .apply(lambda x: safe_divide(sum(x.values), \
                                     len(np.nonzero(x.values)[0])), axis=1)).cumprod() - 1
    else:
        _df = _df.fillna(method='bfill').pct_change()\
        .apply(lambda x: safe_divide(sum(x.values), len(np.nonzero(x.values)[0])), axis=1)
        
    return(_df.fillna(method='bfill').to_frame())
    
##############################################################################
