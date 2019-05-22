# -*- coding: utf-8 -*-

"""
    DWX_Indicator - Indicator base class
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: May 21, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

class DWX_Indicator(object):
    
    def __init__(self, 
                 _name,_data,
                 _algo, _params):
        
        self._name = _name
        self._data = _data
        self._algo = _algo
        self._params = _params
        
    def _calculate_(self):
        
        return self._algo(self._params)