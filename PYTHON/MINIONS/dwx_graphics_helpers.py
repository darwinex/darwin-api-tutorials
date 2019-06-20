# -*- coding: utf-8 -*-
"""
    DWX Graphics - Helper Class
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 20, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""
import plotly.offline as po
import plotly.graph_objs as go
import matplotlib.ticker as ticker

class DWX_Graphics_Helpers():
    
    def __init__(self):
        pass
    
    ##########################################################################
        
    def _mpl_plot_axis_(self, _plt, _ax, _df, _darwin, 
                          _x_title, _y_title, _line_color,
                          _line_width, _tail_max,
                          _bgcolor, _tfont):
        
        # Matplotlib y-axis formatter
        @ticker.FuncFormatter
        def major_formatter(x, pos):
            return "%.2f" % x
        
        _ax.cla()
        _ax.set_title(_darwin, **_tfont)
        _ax.set_facecolor(_bgcolor)
            
        _ax.ticklabel_format(useOffset=False)
        _ax.yaxis.set_major_formatter(major_formatter)
        _ax.yaxis.set_major_formatter(major_formatter)

        _ax.set_xticklabels([])
        _ax.set_xlabel(_x_title, **_tfont)
        _ax.set_ylabel(_y_title, **_tfont)
        
        _ax.set_ylim(bottom=_df[_darwin].tail(_tail_max).min() - 0.01,
                                              top=_df[_darwin].tail(_tail_max).max() + 0.01)
                
        _ax.plot(_df.tail(_tail_max).index, 
                  _df[_darwin].tail(100).values,
                  color=_line_color,
                  linewidth=_line_width)
                  #marker='.')
        
        _ax.grid(linestyle='-', linewidth='0.5', color='grey')
        
        _plt.tight_layout() 
        _plt.pause(0.01)
        
    
    ##########################################################################
    
    def _generate_scatter_single_(self, _df, _name):
        return go.Scatter(
                        x = _df.index,
                        y = _df,
                        name = _name)
        
    def _generate_scatter_list_(self, _df):
        
        return [self._generate_scatter_single_(
                        _df = _df[_darwin],
                        _name = _darwin
                    ) for _darwin in _df.columns]
        
        """
        return [go.Scatter(
                        x = _df.index,
                        y = _df[_darwin],
                        name = _darwin) 
                    for _darwin in _df.columns]
        """
        
    ##########################################################################
    
    
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
                        _name='',
                        _x_title='Date / Time', 
                        _y_title='Quote', 
                        _main_title='DWX_Info_API: def _Get_Quotes_() Example',
                        _annotations=[],
                        _plot_only=False):
        
        if _df is not None:
            
            _data = self._generate_scatter_list_(_df)
            
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
        
        if _plot_only:
            po.iplot(fig)
        else:
            # Set output filename and plot
            if _custom_filename != '':
                po.plot(fig, filename=_dir_prefix + _custom_filename)
            else:
                po.plot(fig, filename=_dir_prefix + _main_title + '.html')
        
    ##########################################################################
    
    def _plotly_scatter_y2(self, 
                           _custom_filename='',
                           _t1_data=None, _t2_data=None,
                           _x1=None, _y1=None, _x1_title=None, 
                           _y1_range=None, _y1_title=None,_x2=None, 
                           _y2=None, _x2_title=None, _y2_range=None, 
                           _y2_title=None, _main_title=None,
                           _annotations=[]):
        
        if _t1_data is None or _t2_data is None:
            print('[ÈRROR] You must provide lists of Scatter objects to proceed.')
            return None
        
        _data = _t1_data + _t2_data
        
        _layout = go.Layout(
                
            title=_main_title,
            xaxis=dict(
                title=_x1_title,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
             
            yaxis=dict(
                title=_y1_title,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
                # overlaying='y',
                # side='left'
            ),
                
            yaxis2=dict(
                title=_y2_title,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                overlaying='y',
                #range=_y2_range,
                side='right'
            ),
            hoverlabel = dict(namelength = -1),
            annotations=_annotations
        )
                
        fig = go.Figure(data=_data, layout=_layout)
        
        if _custom_filename != '':
            po.plot(fig, filename=_custom_filename)
        else:
            po.plot(fig, filename=_main_title + '.html')
            
        #po.plot(_fig, filename=self._reports_dir_prefix + _main_title + '.html')
        
    #########################################################################
