#! /usr/bin/python -tt

import json

from .Base import KlAkBase
from .Params import KlAkParamsEncoder


class KlAkCertUtils (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def GetCertificateAttributes(self, pCertificateFileChunk):
        data = {'pCertificateFileChunk': pCertificateFileChunk}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.GetCertificateAttributes'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def GenerateSelfSignedCertificate(self, pParams):
        data = {'pParams': pParams}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.GenerateSelfSignedCertificate'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def Certificate2Params(self, pCert, pwchPassword):
        data = {'pCert': pCert, 'pwchPassword': pwchPassword}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.Certificate2Params'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def CreateCSR(self, companyName, organizationName, organizationUnit, countryName, regionName, cityName):
        data = {'companyName': companyName, 'organizationName': organizationName, 'organizationUnit': organizationUnit, 'countryName': countryName, 'regionName': regionName, 'cityName': cityName}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.CreateCSR'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def IsEncrypted(self, cert):
        data = {'cert': cert}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.IsEncrypted'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def ConvertPKCS12ToPEM(self, cert, pwchPassword):
        data = {'cert': cert, 'pwchPassword': pwchPassword}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.ConvertPKCS12ToPEM'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def EncryptPEM(self, pemCert, pwchPassword):
        data = {'pemCert': pemCert, 'pwchPassword': pwchPassword}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.EncryptPEM'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def GeneratePassword(self, length, isUserFriendly):
        data = {'length': length, 'isUserFriendly': isUserFriendly}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.GeneratePassword'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def CheckKeypair(self, pCert, pPrivate):
        data = {'pCert': pCert, 'pPrivate': pPrivate}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.CheckKeypair'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def MakePKCS12(self, pCert, pPrivate, wstrPrivatePassKey, wstrFriendlyName, wstrPassKey):
        data = {'pCert': pCert, 'pPrivate': pPrivate, 'wstrPrivatePassKey': wstrPrivatePassKey, 'wstrFriendlyName': wstrFriendlyName, 'wstrPassKey': wstrPassKey}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'CertUtils.MakePKCS12'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

