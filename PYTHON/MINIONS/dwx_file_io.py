# -*- coding: utf-8 -*-
"""
    DWX File I/O - Helper Functions
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: May 16, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

def load_config(_filename=''):
    return {_key: _value for _key, _value in (l.replace('\n','').split('=') for l in open(_filename))}
