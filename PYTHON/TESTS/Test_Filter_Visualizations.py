# -*- coding: utf-8 -*-

"""
    Test_Filter_Visualizations - Creates a dashboard to view DARWIN filters
                                 retrieved via _Get_Filtered_DARWINs_()
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 07, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

import os
os.chdir('<INSERT-ROOT-DIRECTORY-PATH-HERE>')

from API.InfoAPI.DWX_Info_API import DWX_Info_API
from MINIONS.dwx_graphics_helpers import DWX_Graphics_Helpers

class Test_Filter_Visualizations():
    
    def __init__(self):
    
        self._api = DWX_Info_API()
        self._dataset = None
        self._graphics = DWX_Graphics_Helpers()
    
    ##########################################################################  
    
    """
    Excerpt from https://blog.darwinex.com/identify-overfit-trading-strategies/:
    
        Typically, three combinations of scores for the above attributes 
        demonstrate consistent performance between backtests and live trading 
        (when accompanied by High Ex, High Mc, High Rs scores):
            
        1) Low Cp | High Os/Cs | High Pf | High R-
        2) Moderate Cp | High La | High Pf
        3) High Pf | Very High R+/R- or Dc | Moderate La

    """
    
    def _run_(self,
              _filters={
                    'Return/Drawdown Default':
                        [['drawdown',-10,0,'6m'],
                         ['return',5,100,'1m']],
                    'Ds > 75': [['d-score',75,100,'actual']], 
                    'Pf > 9.5': [['Pf',9.5,10,'actual']],
                    'R+ > 9.5': [['R+',9.5,10,'actual']],
                    'Os > 9.5': [['Os',9.5,10,'actual']],
                    'Cp<3 | Os>7 | Cs>7 | Pf>7 | R->7 | Ex>7 | Mc>7 | Rs>7': 
                        [['Sc',0,2.99,'actual'],
                         ['Os',7.01,10,'actual'],
                         ['Cs',7.01,10,'actual'],
                         ['Pf',7.01,10,'actual'],
                         ['R-',7.01,10,'actual'],
                         ['Ex',7.01,10,'actual'],
                         ['Rs',7.01,10,'actual'],
                         ['Mc',7.01,10,'actual']],
                    '4<Cp<6 | La>9 | Pf>9 | Ex>7 | Mc>7 | Rs>7':
                        [['Sc',4.01,5.99,'actual'],
                         ['La',9.01,10,'actual'],
                         ['Pf',9.01,10,'actual'],
                         ['Ex',7.01,10,'actual'],
                         ['Rs',7.01,10,'actual'],
                         ['Mc',7.01,10,'actual']]
                    }):
        
        if self._dataset is None:
            
            # 1) Get filtered DARWINs
            _filtered_darwins = {_name: self._api._Get_Filtered_DARWINS_(
                                                    _filters=_filter) \
                                                    .productName \
                                                    .unique() \
                                                    .tolist()
                                for _name, _filter in _filters.items()}
            
            # 2) Get DARWIN Quotes for all filtered DARWINs, regardless of filter.
            _darwins = []
            
            for _filter in _filtered_darwins.values():
                _darwins = _darwins + _filter
            
            _quotes = self._api._Get_Historical_Quotes_( \
                    _symbols= list(set(_darwins)))
            
            # 3) Create dict of go.Scatter lists (for each filter)
            _scatter_dict = {_name: self._graphics._generate_scatter_list_(
                                _quotes[_filtered_darwins[_name]])
                            
                            for _name in _filtered_darwins.keys()}
            
            # 4) Create stacked list of Scatter objects for updatemenus later.
            #    We'll use this to enable disable traces on a Plotly chart.
            _scatter_stack = []
            
            for _name, _scatter_list in _scatter_dict.items():
                print(f'[INFO] Filter "{_name}" has {len(_scatter_list)} DARWINs')
                _scatter_stack = _scatter_stack + _scatter_list
            
            # 5) Create default (disabled) updatemenus toggle list
            # _updatemenus_toggle = [False for i in range(len(_scatter_stack))]
            
            ##################################################################
            # Return list for Plotly toggle
            def _enable_filter_(_name, _stack_length):
                
                # Get index of _name in _scatter_dict
                _index = list(_scatter_dict.keys()).index(_name)
                
                # Get size of scatter list for this _name
                _size = len(_scatter_dict[_name])
                
                # Create toggle list
                _ret = []
                
                if _index == 0:
                    _ret = [True for i in range(0, _size, 1)] + \
                           [False for i in range(_size, _stack_length, 1)]
                else:
                    # Toggle everything before _index as False
                    for _i in range(0, _index, 1):
                        _ret = _ret + [False for _x in range(
                                                        len(_scatter_dict[
                                                            list(_scatter_dict.keys())[_i]]))]
                
                    # Now toggle True for this _index
                    _ret = _ret + [True for _i in range(len(_scatter_dict[_name]))]
                    
                    # Now toggle False for everything after this _index
                    _ret = _ret + [False for _i in range(len(_ret), _stack_length, 1)]
                
                return _ret
            ##################################################################
            
            # Test
            # return _enable_filter_(list(_scatter_dict.keys())[1], len(_scatter_stack))
        
            # 6) Create updatemenus object for Plotly
            _updatemenus = list([
                    dict(#type="buttons",
                         active=-1,
                         buttons=list([
                            dict(label = _name,
                                 method = 'update', # update
                                 args = [{'visible': _enable_filter_(_name, len(_scatter_stack))},
                                         {'title': _name}])
        
                         for _name in _scatter_dict.keys()]),
                    )
                ])
        
            # Save data in memory
            self._dataset = _scatter_stack
        
        # Plot
        self._graphics._plotly_multi_scatter_(_data=self._dataset,
                                              _title='DARWIN Filter Visualizer v1.0',
                                              _updatemenus=_updatemenus,
                                              _dir_prefix='MISC/')
        
