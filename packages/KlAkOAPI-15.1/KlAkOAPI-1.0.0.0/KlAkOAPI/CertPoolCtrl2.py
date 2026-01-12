#! /usr/bin/python -tt

import json

from .Base import KlAkBase
from .Params import KlAkParamsEncoder


class KlAkCertPoolCtrl2 (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetCertificateInfoDetails(self, nVServerId, nFunction):
        data = {'nVServerId': nVServerId, 'nFunction': nFunction}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertPoolCtrl2.GetCertificateInfoDetails'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

