#! /usr/bin/python -tt

import json

from .Base import KlAkBase
from .Params import KlAkParamsEncoder


class KlAkTestMigrationData (KlAkBase):
    def __init__(self, server, instance = ''):
        self.server = server
        self.instance = instance

    def TestExportGroup(self, wstrDstDir, lGroup):
        data = {'wstrDstDir': wstrDstDir, 'lGroup': lGroup}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestExportGroup'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestImportGroup(self, wstrSrcDir, lGroup, bIsIdempotent):
        data = {'wstrSrcDir': wstrSrcDir, 'lGroup': lGroup, 'bIsIdempotent': bIsIdempotent}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestImportGroup'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def TestExportDeviceQueries(self, wstrDstDir):
        data = {'wstrDstDir': wstrDstDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestExportDeviceQueries'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestImportDeviceQueries(self, wstrSrcDir):
        data = {'wstrSrcDir': wstrSrcDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestImportDeviceQueries'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestExportCommonTasks(self, wstrDstDir, wstrTaskPrefix):
        data = {'wstrDstDir': wstrDstDir, 'wstrTaskPrefix': wstrTaskPrefix}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestExportCommonTasks'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestImportCommonTasks(self, wstrSrcDir):
        data = {'wstrSrcDir': wstrSrcDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestImportCommonTasks'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestExportCommonReports(self, wstrDstDir, wstrReportsPrefix):
        data = {'wstrDstDir': wstrDstDir, 'wstrReportsPrefix': wstrReportsPrefix}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestExportCommonReports'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestImportCommonReports(self, wstrSrcDir):
        data = {'wstrSrcDir': wstrSrcDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestImportCommonReports'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestExportCustomCategories(self, wstrDstDir, wstrNameFilter):
        data = {'wstrDstDir': wstrDstDir, 'wstrNameFilter': wstrNameFilter}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestExportCustomCategories'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestImportCustomCategories(self, wstrSrcDir):
        data = {'wstrSrcDir': wstrSrcDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestImportCustomCategories'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def TestExportUnassignedTags(self, wstrDstDir):
        data = {'wstrDstDir': wstrDstDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestExportUnassignedTags'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestImportUnassignedTags(self, wstrSrcDir):
        data = {'wstrSrcDir': wstrSrcDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestImportUnassignedTags'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestExportUserVisits(self, wstrDstDir, pExportedHostNames):
        data = {'wstrDstDir': wstrDstDir, 'pExportedHostNames': pExportedHostNames}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestExportUserVisits'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestImportUserVisits(self, wstrSrcDir):
        data = {'wstrSrcDir': wstrSrcDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestImportUserVisits'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestExportNotificationSettings(self, wstrDstDir):
        data = {'wstrDstDir': wstrDstDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestExportNotificationSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestImportNotificationSettings(self, wstrSrcDir):
        data = {'wstrSrcDir': wstrSrcDir}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestImportNotificationSettings'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestVerifyImportedHostAttributes(self, wstrDisplayNamePart):
        data = {'wstrDisplayNamePart': wstrDisplayNamePart}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestVerifyImportedHostAttributes'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def TestCreateEmptyMetadata(self, wstrGroupsFolder):
        data = {'wstrGroupsFolder': wstrGroupsFolder}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestCreateEmptyMetadata'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def TestCreateUserVisits(self, wstrHostName):
        data = {'wstrHostName': wstrHostName}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestCreateUserVisits'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestCleanupUserVisits(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestCleanupUserVisits'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestGetUserVisits(self):
        data = {}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestGetUserVisits'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def TestExportDevKey(self, wstrDstDir, lGroup, wstrPassword):
        data = {'wstrDstDir': wstrDstDir, 'lGroup': lGroup, 'wstrPassword': wstrPassword}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestExportDevKey'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text, retval = False)

    def TestImportDevKey(self, wstrSrcDir, lGroup, wstrPassword):
        data = {'wstrSrcDir': wstrSrcDir, 'lGroup': lGroup, 'wstrPassword': wstrPassword}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.TestImportDevKey'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

    def GetEntitiesFromArchiveForRealDataTest(self, wstrArchiveName):
        data = {'wstrArchiveName': wstrArchiveName}
        response = self.server.session.post(url = self.server.Call((lambda: self.instance + '.' if self.instance != None and self.instance != '' else '')() + 'TestMigrationData.GetEntitiesFromArchiveForRealDataTest'), headers = KlAkBase.common_headers, data = json.dumps(data, cls = KlAkParamsEncoder))
        return self.ParseResponse(response.status_code, response.text)

