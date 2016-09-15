# JRM Launcher - Launch JanRyuMon without the need of Internet Explorer and ActiveX
# Copyright (C) Mino <mino@minomino.org>

# This file is part of JRM Launcher.

# JRM Launcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# JRM Launcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with JRM Launcher. If not, see <http://www.gnu.org/licenses/>.

import urllib.parse
import urllib.request
import urllib.error
import html.parser
import http.cookiejar
import sys

from jrm.NcKeygen import NcKeygen

class JrmSession():
    
    def __init__(self, ukey):
        # Info
        self.jrm_url = "http://janryumon.plaync.jp/"
        self.jrm_login_url = "https://www.ncsoft.jp/login/ajax/loginProc"
        self.ukey = ukey
        
        # Feed
        self.cookies = http.cookiejar.CookieJar(http.cookiejar.DefaultCookiePolicy())
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
    
    def login(self, username, password):
        
        params = urllib.parse.urlencode({"returl": self.jrm_url, "login": 1, "UKEY": self.ukey,
                                          "account": username, "password": password}).encode("utf-8")
        request = urllib.request.Request(self.jrm_login_url, params,
                                         {"Referer": self.jrm_url,
                                          "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"})
        
        try:
            self.opener.open(request)
            for cookie in self.cookies:
                if cookie.name == "GPSESSIONID" and cookie.value != '""':
                    self.session_id = cookie.value
                    return True
            return False
        except urllib.error.HTTPError as e:
            return False

