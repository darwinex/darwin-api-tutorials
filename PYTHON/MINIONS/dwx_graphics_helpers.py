# -*- coding: utf-8 -*-
"""
    DWX Graphics - Helper Class
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: May 16, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

import plotly.offline as po
import plotly.graph_objs as go

class DWX_Graphics_Helpers():
    
    def __init__(self):
        pass
    
    # Single Series Scatter Chart
    def _plotly_dataframe_scatter_(self, 
                        _custom_filename='',
                        _dir_prefix='../MISC/',
                        _df=None, 
                        _x=None, 
                        _y=None,
                        _name='',
                        _x_title='Date / Time', 
                        _y_title='Quote', 
                        _main_title='DWX_Info_API: def _Get_Quotes_() Example',
                        _annotations=[]):
        
        if _df is not None:
            _data = [go.Scatter(
                        x = _df.index,
                        y = _df[_darwin],
                        name = _darwin) 
                    for _darwin in _df.columns]
            
        else:
            print('[ERROR] Can\'t plot thin air I\'m afraid... :)')
            return None
    
        # Setup Layout
        _layout = go.Layout(
            title=_main_title,
            xaxis=dict(
                title=_x_title,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title=_y_title,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            hoverlabel = dict(namelength = -1),
            annotations=_annotations
        )
                
        # Create figure
        fig = go.Figure(data=_data, layout=_layout)
        
        # Set output filename and plot
        if _custom_filename != '':
            po.plot(fig, filename=_dir_prefix + _custom_filename)
        else:
            po.plot(fig, filename=_dir_prefix + _main_title + '.html')
        
