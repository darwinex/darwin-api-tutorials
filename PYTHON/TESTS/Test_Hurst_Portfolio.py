# -*- coding: utf-8 -*-

"""
    Test_Hurst_Portfolio - Implements Hurst_Indicator functionality
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

from RESEARCH.INDICATORS.ML.Hurst_Indicator_v1_0 import Hurst_Indicator
from API.InfoAPI.DWX_Info_API import DWX_Info_API

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Test_Hurst_Portfolio():
    
    def __init__(self):
        self._api = DWX_Info_API()
        self._ds = {}
    
    ##########################################################################    
    
    def _run_(self, 
              _darwins=['NTI','ZVQ'],
              _thresholds=(0.30,0.70),
              _plot=False):
        
        if len(self._ds.keys()) == 0:
            
            for _darwin in _darwins:
            
                print('[INFO] Processing DARWIN ${} ..'.format(_darwin))
                _quotes = self._api._Get_Historical_Quotes_(_symbols=[_darwin], 
                                                            _plot_title='')
            
                _quotes['hurst'] = Hurst_Indicator(_name='Hurst',
                                                    _data=_quotes[_darwin].values,
                                                    _algo=None,
                                                    _params=[101,'price',True])._calculate_()
                
                # Geometric Random Walk
                _quotes['state'] = 0
                
                # Trending
                _quotes['state'] = np.where(_quotes['hurst'] > _thresholds[1], 
                                             1, 
                                             _quotes['state'])
                
                # Mean Reverting
                _quotes['state'] = np.where(_quotes['hurst'] < _thresholds[0], 
                                             -1, 
                                             _quotes['state'])
                
                self._ds[_darwin] = _quotes
        
                # Plot results
                if _plot:
                    self._plot_results_(_darwin=_darwin,
                                        _hurst_thresholds=_thresholds)
        
        print('\n.. DONE!')
        
    ##########################################################################
    
    def _plot_results_(self, _darwin='NTI',
                       _hurst_thresholds=(0.3,0.7)):
        
        plt.style.use('ggplot')
        
        # Setup plot figure dimensions
        plt.figure(figsize=(16,10))
        
        # Plot rolling Hurst
        plt.subplot(2,2,1)
        self._ds[_darwin]['hurst'].plot(color='blue')
        plt.xlabel('Date / Time')
        plt.ylabel('Hurst Exponent')
        
        # Thresholds
        plt.axhline(_hurst_thresholds[0],color='g')
        plt.axhline(_hurst_thresholds[1],color='r')
        
        plt.subplot(2,2,2)
        self._ds[_darwin][_darwin].plot(color='green')
        plt.xlabel('Date / Time')
        plt.ylabel('Quote')

        # State        
        plt.subplot(2,2,3)
        self._ds[_darwin]['state'].plot(color='black')
        plt.xlabel('Date / Time')
        plt.ylabel('State')
        
        # Rolling 21-day volatility
        plt.subplot(2,2,4)
        plt.plot(self._ds[_darwin][_darwin].pct_change().rolling(21).std(), color='red')
        plt.xlabel('Date / Time')
        plt.ylabel('Rolling 21-day Volatility')
        
    ##########################################################################
    
if __name__ == '__main__':
    
    # List of DARWINs
    _darwins = ['NTI','KVL', 'ERQ']
    
    # Initialize test
    _test = Test_Hurst_Portfolio()
    
    # Run indicator on all DARWINs and plot results
    _test._run_(_darwins=_darwins,
                _thresholds=(0.3,0.7),
                _plot=True)
    
