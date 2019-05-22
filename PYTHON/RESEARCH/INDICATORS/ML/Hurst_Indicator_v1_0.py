# -*- coding: utf-8 -*-

"""
    Hurst_Indicator - Subclass of DWX_Indicator implementing the Hurst Exponent
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: May 21, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

import os
os.chdir('<INSERT-PATH-TO-PROJECT-DIR-HERE>')

from RESEARCH.INDICATORS.DWX_Indicator import DWX_Indicator

from hurst import compute_Hc
import numpy as np

class Hurst_Indicator(DWX_Indicator):
    
    def __init__(self, **kwargs):
        
        super(Hurst_Indicator, self).__init__(**kwargs)
        
        # Defaults
        if self._algo is None:
            self._algo = compute_Hc
        
        # Run
        if self._data is None:
            print('[ERROR] No data provided.')
        
    ##########################################################################
    
    def _calculate_(self):
        
        _h = [np.nan for i in range(0, self._data.shape[0], 1)]
        
        for i in range(self._params[0], self._data.shape[0], 1):
            _h[i] = self._algo(np.log(self._data[(i-self._params[0]):(i-1)]), 
                          kind=self._params[1],
                          simplified=self._params[2])[0]
        
        return _h
        
    ##########################################################################
    
