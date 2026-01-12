#! /usr/bin/python -tt

import json

from .Base import KlAkBase
from .Params import KlAkParamsEncoder


class KlAkFileManager (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def SaveFile(self, wstrFileId, wstrTempFileId):
        data = {'wstrFileId': wstrFileId, 'wstrTempFileId': wstrTempFileId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'FileManager.SaveFile'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def SetFileAttributes(self, wstrFileId, pParams):
        data = {'wstrFileId': wstrFileId, 'pParams': pParams}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'FileManager.SetFileAttributes'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def DeleteFile(self, wstrFileId):
        data = {'wstrFileId': wstrFileId}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'FileManager.DeleteFile'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def GetFiles(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'FileManager.GetFiles'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def GetFileData(self, wstrFileId, lBuffOffset, lBuffSize):
        data = {'wstrFileId': wstrFileId, 'lBuffOffset': lBuffOffset, 'lBuffSize': lBuffSize}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'FileManager.GetFileData'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

