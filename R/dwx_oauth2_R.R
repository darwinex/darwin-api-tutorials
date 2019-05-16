# dwx_oauth2_R.R
# --
# @author: Darwinex Labs (www.darwinex.com)

# Last Updated: May 16, 2019

# Copyright (c) 2017-2019, Darwinex. All rights reserved.

# Licensed under the BSD 3-Clause License, you may not use this file except 
# in compliance with the License. 

# You may obtain a copy of the License at:    
# https://opensource.org/licenses/BSD-3-Clause

library(httr)

get_tokens <- function(username = "", password = "",
		       client_id = "", client_secret = "",
		       scope = "openid",
		       token_url = "https://api.darwinex.com/token",
		       grant_type = "password")
{
	secret <- base64enc::base64encode(charToRaw(paste0(client_id, ":", client_secret)))

	req <- httr::POST(token_url,
			  httr::add_headers(
					    "Authorization" = paste("Basic", secret),
					    "Content-Type" = "application/x-www-form-urlencoded;charset=UTF-8"
					    ),
			  body = paste0("grant_type=", grant_type,
					"&username=", username,
					"&password=", password,
					"&scope=", scope)
			  )

	httr::stop_for_status(req, "Authenticating with Darwinex..")
	tokens <- httr::content(req)

	return(tokens)
}
