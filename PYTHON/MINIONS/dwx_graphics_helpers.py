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
    
    ##########################################################################
    
    def _generate_scatter_list_(self, _df):
        return [go.Scatter(
                        x = _df.index,
                        y = _df[_darwin],
                        name = _darwin) 
                    for _darwin in _df.columns]
    
    ##########################################################################
    
    def _plotly_multi_scatter_(self, 
                                  _data=None,
                                  _updatemenus=None,
                                  _title=None,
                                  _legend=None,
                                  _dir_prefix='../MISC/',
                                  _x_title='Date / Time',
                                  _y_title='Quote'):
        
        # Setup Layout
        _layout = go.Layout(
            title=_title,
            showlegend=_legend,
            updatemenus=_updatemenus,
            xaxis=dict(                
                title=_x_title,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#ffffff'
                )
            ),
            yaxis=dict(
                title=_y_title,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#ffffff'
                )
            ),
            hoverlabel = dict(namelength = -1),
            images=[dict(
                #source="https://d139oolcsxoepg.cloudfront.net/2_108_0/images/logos/darwinex/logo-darwinex.svg",
                source="https://avatars2.githubusercontent.com/u/26509507?s=460&v=4",
                xref="paper", yref="paper",
                x=1.04, y=0.99,
                sizex=0.105, sizey=0.105,
                xanchor="left", yanchor="bottom"
              )]
        )
            
        fig = go.Figure(data=_data, layout=_layout)
        po.plot(fig, filename=_dir_prefix + f'{_title.replace(" ", "-")}.html')
    
    ##########################################################################
        
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
            
            _data = self._generate_scatter_list_(_df)
            
            """
            _data = [go.Scatter(
                        x = _df.index,
                        y = _df[_darwin],
                        name = _darwin) 
                    for _darwin in _df.columns]
            """
            
            
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
        
