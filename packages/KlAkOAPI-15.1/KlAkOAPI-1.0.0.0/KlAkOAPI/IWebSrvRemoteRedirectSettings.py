#! /usr/bin/python -tt

import json

from .Base import KlAkBase
from .Params import KlAkParamsEncoder


class KlAkIWebSrvRemoteRedirectSettings (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def SetWebSrvRemoteRedirectSettings(self, wstrHostId, pSettings):
        data = {'wstrHostId': wstrHostId, 'pSettings': pSettings}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteRedirectSettings.SetWebSrvRemoteRedirectSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetWebSrvRemoteRedirectSettings(self, wstrHostId):
        data = {'wstrHostId': wstrHostId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteRedirectSettings.GetWebSrvRemoteRedirectSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

