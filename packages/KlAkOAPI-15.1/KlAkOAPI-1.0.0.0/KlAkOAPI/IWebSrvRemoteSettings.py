#! /usr/bin/python -tt

import json

from .Base import KlAkBase
from .Params import KlAkParamsEncoder


class KlAkIWebSrvRemoteSettings (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetCertificateInfo(self, wstrHostId):
        data = {'wstrHostId': wstrHostId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.GetCertificateInfo'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def SetCustomCertificate(self, wstrHostId, pCertData):
        data = {'wstrHostId': wstrHostId, 'pCertData': pCertData}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.SetCustomCertificate'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetCustomPkgHttpFqdn(self, wstrHostId):
        data = {'wstrHostId': wstrHostId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.GetCustomPkgHttpFqdn'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def SetCustomPkgHttpFqdn(self, wstrHostId, wsFqdn):
        data = {'wstrHostId': wstrHostId, 'wsFqdn': wsFqdn}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'IWebSrvRemoteSettings.SetCustomPkgHttpFqdn'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

