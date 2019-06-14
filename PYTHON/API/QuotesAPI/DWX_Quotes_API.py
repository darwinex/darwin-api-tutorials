# -*- coding: utf-8 -*-
"""
    DWX Quotes API - Subclass of DWX_API for Quotes Streaming
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 14, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""
import os
os.chdir('<INSERT-PROJECT-ROOT-DIR-HERE>')

from MINIONS.dwx_graphics_helpers import DWX_Graphics_Helpers
from API.dwx_api import DWX_API

from matplotlib import pyplot as plt
from requests import Session
import pandas as pd
import numpy as np

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 500)

class DWX_Quotes_API(DWX_API):
    
    def __init__(self, 
                 _api_url='https://api.darwinex.com',
                 _api_name='quotes',
                 _version=1.0):
        
        super(DWX_Quotes_API, self).__init__(_api_url, _api_name, _version)
        self._graphics = DWX_Graphics_Helpers()
        
        # Note: Pass _json=False and _stream=True to self._Call_API_() to 
        # receive request object instead of JSON text output.
    
    ##########################################################################
    
    def _stream_quotes_(self, 
                        _endpoint='/quotes',
                        _symbols=['THA.4.12','LVS.4.20']):
        
        # Create session for streaming quotes
        _s = Session()
        
        # Construct DARWIN list for sending to the endpoint
        _data = "{\"productNames\": [ \"" + "\",\"".join(_symbols) + "\" ]}"
        
        # Retreive Request object for session
        _ret = self._Call_API_(_endpoint,
                               _type='POST',                               
                               _data=_data, 
                               _json=False,
                               _stream=True)
                
        # Send the request
        _resp = _s.send(_ret.prepare(), stream=True, verify=True)
        
        # Yield output
        for _l in _resp.iter_lines():
            if _l:
                yield _l

    ##########################################################################
    
    def _process_stream_(self, 
                         _symbols=['DWZ.4.7','DWC.4.20','LVS.4.20','SYO.4.24','YZZ.4.20'],
                         _plot=True):
       
        # Create empty dataframe
        self._df = pd.DataFrame(columns=_symbols)
        
        # Create graphing objects if _plot==True
        if _plot:
            
            # Create fig, ax
            if len(_symbols) > 1:
                _fig, _ax = plt.subplots(nrows=1, ncols=len(_symbols), figsize=(20,4))
            else:
                _fig, _ax = plt.subplots(figsize=(10,6))        
            
        # for line in self.streaming(symbols=_symbols):
        for _ret in self._stream_quotes_(_symbols=_symbols):
        
            # Parse string to dict
            _stream = eval(_ret)
        
            # Extract values of interest.
            _darwin = _stream['productName']
            _quote = _stream['quote']
            _timestamp = _stream['timestamp']
            
            # Add to DataFrame
            _quotes = [np.nan for x in range(self._df.shape[1])]
            _quotes[_symbols.index(_darwin)] = _quote
            _row = pd.Series(index=_symbols,
                             data=_quotes,
                             name=_timestamp)
            
            self._df = self._df.append(_row)
            self._df.fillna(method='ffill', inplace=True)
            self._df.fillna(method='bfill', inplace=True)
            
            if _plot == False:
                print(_stream)
            else:
                # Axis to pass
                if len(_symbols) > 1:
                    _axp = _ax[_symbols.index(_darwin)]
                else:
                    _axp = _ax
                    
                # Call plotter function from self._graphics
                self._graphics._mpl_plot_axis_(
                        plt, 
                        _axp,
                        #_ax[_symbols.index(_darwin)], 
                        self._df,
                        _darwin,
                        'Last 100 ticks',
                        'Quote',
                        '#00fa9a',
                        0.5,
                        100,
                        '#07335B',
                        {'fontname':'Courier New'})
              
    ##########################################################################
