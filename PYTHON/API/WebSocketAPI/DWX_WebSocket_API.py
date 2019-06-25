# -*- coding: utf-8 -*-
"""
    DWX WebSocket API - Subclass of DWX_API for Quotes Streaming
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 25, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

import os
os.chdir('<INSERT-ROOT-PROJECT-DIRECTORY-HERE>')

from API.dwx_api import DWX_API
import websockets, json, asyncio

class DWX_WebSocket_API(DWX_API):
    
    def __init__(self,
                 _api_url='ws://api.darwinex.com/quotewebsocket/1.0.0',
                 _api_name='',
                 _version=0.0):
        
        super(DWX_WebSocket_API, self).__init__(_api_url, _api_name, _version)
        
        # Set to WebSocket URL
        self._url = _api_url
        
        # If false, stop polling data from websocket
        self._active = True
        self._websocket = None
        
    ##########################################################################
    
    async def subscribe(self, _symbols=['DWZ.4.7','DWC.4.20','LVS.4.20','SYO.4.24','YZZ.4.20']):
        
        async with websockets.connect(self._url, 
                                      extra_headers=self._auth_headers) as websocket:

           # Subscribe to symbols
           await websocket.send(json.dumps({ 'op': 'subscribe', 'productNames' :_symbols}))
           
           # If _active is True, process data received.
           while self._active:
               
               _ret = await websocket.recv()
               
               # Insert your Quote handling logic here
               print(_ret)

    ##########################################################################
		
    def run(self, _symbols=['DWZ.4.7','DWC.4.20','LVS.4.20','SYO.4.24','YZZ.4.20']):
        
        self.event_loop = asyncio.get_event_loop()
        
        try:
            self.event_loop.run_until_complete(self.subscribe(_symbols))
            
        except RuntimeError as re:
            print(re)
    
    ##########################################################################
    
    def stop(self):
        """
        Stop and close loop
        """
        self.event_loop.stop()
        
    ##########################################################################
