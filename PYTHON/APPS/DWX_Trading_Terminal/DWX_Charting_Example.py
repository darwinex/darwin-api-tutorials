# -*- coding: utf-8 -*-
"""
    DWX_Charting_Example.py - Example application that demonstrates how to
                              create DARWIN charting functionality.
    
    Important Notes:
    --
    Portfolio calculations are missing:
        1) transaction costs, 
        2) performance fees, 
        3) divergence
    etc.
        
    Future updates will iteratively improve upon this code whilst adding
    more functionality.
    
    Credits: This project using py-quantmod to render charts:
    https://github.com/jackluo/py-quantmod
    
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: July 25, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

import os, pickle
os.chdir('<INSERT-PROJECT-ROOT-DIR-HERE>')

import dash
import dash_core_components as core
import dash_html_components as html
from dash.dependencies import Input, Output
import quantmod as qm
import pandas as pd

from API.InfoAPI.DWX_Info_API import DWX_Info_API
from APPS.API_Helpers.TS_Calculations import calculate_portfolio_returns

class DWX_Charting_Example():
    
    def __init__(self):
    
        # Constants
        self.darwin_db = 'APPS/DWX_Trading_Terminal/DATA/darwin_db.pkl'
        self.indi_db = 'APPS/DWX_Trading_Terminal/DATA/talib_indicator_db.dict.pkl'
        
        # APIs
        self.info_api = DWX_Info_API()
        
        # Load DARWIN Tickers via PICKLE or API
        try:
            print(f'[KERNEL] Reading DARWINS DB from {self.darwin_db}')
            self.darwins_df = pd.read_pickle(self.darwin_db)
        except FileNotFoundError as e:
            print(e)
            self.darwins_df = self.info_api._Get_DARWIN_Universe_()
            
            print(f'[KERNEL] Writing DARWINS DB to {self.darwin_db}')
            self.darwins_df.to_pickle(self.darwin_db)

        print('\n[INFO] Preparing to launch terminal..')

        ###################
        # Create Controls #
        ###################
                
        # DARWIN Tickers Dropdown Menu
        self.indicator_desc = pickle.load(open(self.indi_db, 'rb'))
        
        self.darwins = [dict(label=str(symbol), value=str(symbol))
                   for symbol in self.darwins_df[self.darwins_df\
                                                 .status\
                                                 .isin(['ACTIVE','DELETED'])]\
                                                 .productName]
        
        # Technical Indicators Dropdown Menu
        self.indicators = dir(qm.ta)[9:-4]
        self.indicators = [dict(label=str(indicator[4:]) 
                                        + ' (' 
                                        + self.indicator_desc[indicator[4:]]
                                        + ')', 
                                value=str(indicator))
                     for indicator in self.indicators]

    # Launch Dash Application
    def _launch_(self, port=4003):
        
        # Create layout
        app = dash.Dash(__name__, external_stylesheets = [])
        
        # Layout
        app.layout = html.Div(
            [
                html.Div(
                    [
                        html.H2('DARWIN Trading Terminal - v1.0.1 (Building Blocks)',
                                style={'padding-top': '15px'}),
                                
                        html.Span(
                            core.Dropdown(
                                id='darwins',
                                multi=True,
                                options=self.darwins,
                                value='PLF',
                            ),
                            style={
                                'width': '510px',
                                'display': 'inline-block',
                                'text-align': 'left',
                                'color': '#07335B'
                            },
                        ),
                        html.Span(
                            core.Dropdown(
                                id='indicators',
                                options=self.indicators,
                                multi=True,
                                value=[],
                            ),
                            style={
                                'width': '510px',
                                'display': 'inline-block',
                                'text-align': 'left',
                                'color': '#07335B'
                            },
                        ),
                    ]
                ),
                html.Div(
                    [html.Label('Enter Indicator Parameters Here:'), 
                     core.Input(id='params')],
                    id='parameter-controls',
                    style={'display': 'none'}
                ),
                core.Graph(id='chart')
            ],
            style={
                'width': '1024px',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'text-align': 'center',
                'font-family': 'overpass',
                'background-color': '#07335B',
                'color': '#FFFFFF'
            }
        )
        
        ######################################################################
        
        # DECORATOR
        @app.callback(Output('parameter-controls', 'style'), [Input('indicators', 'value')])
        
        # WRAPPED FUNCTION
        def display_control(multi):
            if not multi:
                return {'display': 'none'}
            else:
                return {'display': 'inline-block'}
        
        ######################################################################
                
        # DECORATOR
        @app.callback(Output('chart', 'figure'), [Input('darwins', 'value'),
                                                   Input('indicators', 'value'),
                                                   Input('params', 'value')])
        # WRAPPED FUNCTION
        def update_chart(darwins, indicators, params):
            
            print(darwins)
            
            # Get Quantmod Chart
            ch = self.get_darwin_dataset(darwins)
            
            # Get functions
            if params:
                params = params.replace('(', '').replace(')', '').split(';')
                params = [args.strip() for args in params]
                for function, args in zip(indicators, params):
                    if args:
                        args = args.split(',')
                        newargs = []
                        for arg in args:
                            try:
                                arg = int(arg)
                            except:
                                try:
                                    arg = float(arg)
                                except:
                                    pass
                            newargs.append(arg)
        
                        print(newargs)
                        getattr(qm, function)(ch, *newargs)
                    else:
                        getattr(qm, function)(ch)
            else:
                for function in indicators:
                    getattr(qm, function)(ch)
        
            # Return plot as figure
            fig = ch.to_figure(type='line', width=1024, theme='dark')
            
            # Adjust fillcolor
            fig['data'][0]['fillcolor'] = '#07335B'
            
            return fig
        
        # RUN APP
        app.run_server(debug=True, use_reloader=False, port=port)
        
    ######################################################################
        
    # Helper Function: Get DARWIN Dataset
    def get_darwin_dataset(self, assets, cumulative=True, rebase=False):
    	    
        # Type checks for mandatorily used arguments
        if isinstance(assets, str):
            _symbols = [assets]
        elif isinstance(assets, list):
            _symbols = [a for a in assets]
        else:
            raise TypeError("Invalid DARWIN symbols array '{0}'. "
                            "It should be a list of strings.".format(assets))
    
        # Get Quotes
        _portfolio = self.info_api._Get_Historical_Quotes_(_symbols=_symbols)
        
        # Rebase to common dates
        if rebase:
            _portfolio.dropna(inplace=True)
        
        # Calculate cumulative portfolio returns
        _portfolio = calculate_portfolio_returns(_portfolio, cumulative=cumulative)
        
        # symbols now contains a dataframe of Quotes by asset, one column per.
        
        # symbols.columns will have a different source later on after calculating
        # the portfolio
        _portfolio.columns = ['Close']
        
        return qm.Chart(_portfolio)
            

# In[]:
# Main

"""
if __name__ == '__main__':
    
    dwx = DWX_Charting_Example()
    dwx._launch_(port=4003)
"""
