# -*- coding: utf-8 -*-
"""
    DWX_Info_API.py - DARWIN Info API (Subclass of DWX_API)
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: May 29, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

import os, time
os.chdir('<INSERT-PATH-TO-PROJECT-DIR-HERE>')

from MINIONS.dwx_graphics_helpers import DWX_Graphics_Helpers
from API.dwx_api import DWX_API

import pandas as pd
import numpy as np

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 500)

class DWX_Info_API(DWX_API):
    
    def __init__(self):
        super(DWX_Info_API, self).__init__()
        self._graphics = DWX_Graphics_Helpers()
        
    #########################################################    
    # Function: Get Quotes for all DARWINs in list _symbols #
    #########################################################

    def _Get_Historical_Quotes_(self, _symbols=['THA.4.12','LVS.4.20'], 
                               _start='', #_start=pd.to_datetime('today') - pd.to_timedelta(240, 'D'),
                               _end='', #_end=pd.to_datetime('today'),
                               _endpoint='/products/{}/history/quotes',
                               _plot_title='DWX_Info_API: def _Get_Quotes_() Example',
                               _delay=0.01):
        
        if isinstance(_symbols, list):
            
            _dict = {}
            _count = 1
            
            for darwin in _symbols:
                
                print('\n[DarwinInfoAPI] Processing {} / {}: ${}'.format(_count, len(_symbols), darwin))
                
                try:
                    
                    # If dates provided, attach query parameters to endpoint
                    if _start not in ['', np.nan]:
                        
                        _ep = _endpoint.format(darwin) + '?start={}&end={}'.format(
                                        int(_start.timestamp())*1000, 
                                        int(_end.timestamp())*1000)
                    
                    else:
                        _ep = _endpoint.format(darwin)
                    
                    # Construct DataFrame from returned JSON
                    _dict[darwin] = pd.DataFrame(data=self._Call_API_(_ep, 'GET', ''))
                            
                    # Assign column names
                    _dict[darwin].columns = ['timestamp', darwin]
                    
                    # Convert ms timestamp to datetime
                    _dict[darwin].timestamp = pd.to_datetime(_dict[darwin].timestamp, unit='ms')
                    
                    # Crop to data before today's date
                    _dict[darwin] = _dict[darwin][_dict[darwin].timestamp.dt.date < pd.to_datetime('today').date()]
                    
                    # Set index to timestamp
                    _dict[darwin] = _dict[darwin].set_index('timestamp')
                    
                    # Sleep
                    if _delay > 0:
                        time.sleep(_delay)
                    
                except Exception as ex:
                    
                    print('[ERROR] Something went wrong while looking up ${}'.format(darwin))
                    _exstr = "Exception Type {0}. Args:\n{1!r}"
                    _msg = _exstr.format(type(ex).__name__, ex.args)
                    print(_msg)
                    continue
                
                # Update counter
                _count += 1
                    
            _retdf = pd.concat([_df for _df in _dict.values() if isinstance(_df, pd.DataFrame)], axis=1)
            _retdf.columns = _symbols
            
            if _plot_title != '':
                self._graphics._plotly_dataframe_scatter_(_custom_filename='example_quotes.html', 
                                                          _dir_prefix='MISC/', 
                                                          _df=_retdf,
                                                          _x_title='EOD Timestamp',
                                                          _y_title='DARWIN Quote',
                                                          _main_title=_plot_title)
            
            return _retdf
            
        else:
            print('[ERROR] Please specify symbols as Python list []')    
        
                     
    ######################################################################### 
    
    def _Get_Historical_Scores_(self, 
                                _symbols=['THA.4.12','LVS.4.20'], 
                                _endpoint='/products/{}/history/badges',
                                _plot_title='DWX_Info_API: def _Get_Historical_Scores_() Example',
                                _delay=0.01):
        
        if isinstance(_symbols, list):
            
            _dict = {}
            _count = 1
            
            # Badges dict for later use
            _badge_cols = ['eod_ts','Dp','Ex','Mc','Rs', 
                            'Ra','Os','Cs','Rp','Rm',
                            'Dc','La','Pf','Cp','Ds',
                            'fcal_ts','lcal_ts']
            
            for darwin in _symbols:
                
                print('\n[DarwinInfoAPI] Processing {} / {}: ${}'.format(_count, len(_symbols), darwin))
                
                try:
            
                    # Construct DataFrame from returned JSON
                    _dict[darwin] = self._Call_API_(_endpoint.format(darwin), 'GET', '')
                          
                    _dict[darwin] = [_dict[darwin][i][:2] + [x for x in _dict[darwin][i][2]] + _dict[darwin][i][-2:] for i in range(len(_dict[darwin]))]
                    
                    
                    _dict[darwin] = pd.DataFrame(data=_dict[darwin], index=[_dict[darwin][i][0] for i in range(len(_dict[darwin]))])
        
                    # Assign column names
                    _dict[darwin].columns = _badge_cols
                    
                    # Convert ms timestamp to datetime
                    _dict[darwin].eod_ts = pd.to_datetime(_dict[darwin].eod_ts, unit='ms')
                    _dict[darwin].fcal_ts = pd.to_datetime(_dict[darwin].fcal_ts, unit='ms')
                    _dict[darwin].lcal_ts = pd.to_datetime(_dict[darwin].lcal_ts, unit='ms')
                    
                    # Set index to eod_ts
                    _dict[darwin] = _dict[darwin].set_index('eod_ts')
                    
                    # Sleep
                    if _delay > 0:
                        time.sleep(_delay)
                    
                except Exception as ex:
                    
                    print('[ERROR] Something went wrong while looking up ${}'.format(darwin))
                    _exstr = "Exception Type {0}. Args:\n{1!r}"
                    _msg = _exstr.format(type(ex).__name__, ex.args)
                    print(_msg)
                    continue
                
                # Update counter
                _count += 1
                
            # If only one symbol provided, plot scores via Plotly
            if len(_symbols) == 1:
                
                if _plot_title != '':
                    self._graphics._plotly_dataframe_scatter_(_custom_filename='example_scores.html', 
                                                              _dir_prefix='MISC/', 
                                                              _df=_dict[_symbols[0]].drop(['fcal_ts','lcal_ts','Ds','Dp'], axis=1).loc[:, ],
                                                              _x_title='EOD Timestamp',
                                                              _y_title='Score / Investment Attribute',
                                                              _main_title=_plot_title)
                
            return _dict
        
        else:
            print('[ERROR] Please specify symbols as Python list []')    
    
    #########################################################################
    
    def _Get_DARWIN_Universe_(self, 
                          _status='ALL',
                          _endpoint='/products{}',
                          _query_string='?status={}&page={}&per_page={}',
                          _page=0,
                          _perPage=50,
                          _iterate=True,
                          _delay=0.01):
    
        # Get first batch
        try:
            print('[DarwinInfoAPI] Getting first {} DARWINs..'.format(_perPage))
            _darwins = self._Call_API_(_endpoint \
                                      .format(_query_string \
                                              .format(_status, _page, _perPage)), 
                                              _type='GET',
                                              _data='')
            
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
            return None
            
        if _iterate:
            
            # Calculate number of pages
            _pages = int(_darwins['totalPages'])
            
            # Keep 'content' list of DARWINs, discard everything else
            _darwins = _darwins['content']
            
            print('[API] {} pages of {} DARWINs each found.. iterating, stand by! :muscle:\n'
                  .format(_pages, _perPage))
            
            # Iterate
            for i in range(_page + 1, _pages):
                
                print('\r[DarwinInfoAPI] Getting page {} of {}'.format(i+1, _pages), end='', flush=True)
                
                try:
                    _darwins = _darwins + self._Call_API_(_endpoint \
                                              .format(_query_string \
                                                      .format(_status, i, _perPage)), 
                                                      _type='GET',
                                                      _data='')['content']
                    
                    # Sleep until next time
                    if _delay > 0:
                        time.sleep(_delay)
                    
                except Exception as ex:
                    _exstr = "Exception Type {0}. Args:\n{1!r}"
                    _msg = _exstr.format(type(ex).__name__, ex.args)
                    print(_msg)
                    continue
                
        # Return dict
        return pd.DataFrame(_darwins)
        
    ######################################################################### 
