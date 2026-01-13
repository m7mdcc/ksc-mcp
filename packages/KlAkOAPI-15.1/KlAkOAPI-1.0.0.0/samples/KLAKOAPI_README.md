# KlAkOAPI - Kaspersky Security Center Open API Python Wrapper

**A comprehensive Python wrapper library for interacting with Kaspersky Security Center (KSC) server via KSC Open API**

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Core Concepts](#core-concepts)
- [Common Operations](#common-operations)
- [API Modules](#api-modules)
- [Code Samples](#code-samples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

---

## Overview

KlAkOAPI is a Python library that provides a high-level wrapper around Kaspersky Security Center's Open API. It enables administrators and developers to automate tasks, manage devices, generate reports, and interact with KSC infrastructure programmatically.

### Key Capabilities

- **Device Management**: Find, group, and manage network devices
- **Task Automation**: Create, schedule, and monitor tasks
- **Reporting**: Generate and download reports in various formats
- **Statistics**: Query system statistics and create charts
- **License Management**: Monitor and manage license keys
- **Group Operations**: Manage device groups and hierarchies
- **Server Hierarchy**: Work with primary-secondary server configurations
- **Gateway Connections**: Connect to network agents and slave servers
- **Tag Management**: Apply and manage tags on hosts for organization
- **Update Agents**: Configure and manage update agent assignments
- **User Management**: Create internal users and manage permissions
- **Incident Management**: Find and manage security incidents
- **Mobile Devices**: Manage mobile devices and enrollment packages
- **Network Operations**: Upload/execute files, download network lists
- **AD Integration**: Sync with Active Directory structure
- **Notifications**: Configure email and notification settings
- **Application Control**: Manage application categories and file categorization
- **IP Subnets**: Configure IP subnet scanning ranges
- **Virtual Servers**: Manage and monitor virtual server instances

---

## Features

- **Multiple Authentication Methods**: Basic Auth, NTLM, and Gateway connections
- **Asynchronous Operations**: Handle long-running tasks with state checking
- **Chunk-based Data Retrieval**: Efficiently process large datasets
- **Virtual Server Support**: Connect to specific virtual servers
- **Cross-platform**: Works on Windows and Linux
- **Rich Parameter Handling**: Advanced parameter composition and parsing

---

## Installation

### Prerequisites

- Python 3.6+
- Kaspersky Security Center installed (version 15.x+)
- Network connectivity to KSC server
- Valid KSC user account with appropriate permissions

### Install from Package

```bash
pip install KlAkOAPI
```

### Install from Source

```bash
# Navigate to the package directory
cd packages/KlAkOAPI-15.1/KlAkOAPI-1.0.0.0

# Install the package
python setup.py install
```

---

## Quick Start

### Basic Connection Example

```python
from KlAkOAPI.AdmServer import KlAkAdmServer
import socket

# Server connection details
server_address = socket.getfqdn()  # or 'ksc.example.com'
server_port = 13299
server_url = f'https://{server_address}:{server_port}'

# For Windows - use NTLM authentication
username = None
password = None

# For Linux - use basic authentication
# username = 'klakoapi_test'
# password = 'your_password'

# SSL certificate verification
SSLVerifyCert = r'C:\ProgramData\KasperskyLab\adminkit\1093\cert\klserver.cer'

# Create server connection
server = KlAkAdmServer.Create(server_url, username, password, verify=SSLVerifyCert)

if server.connected:
    print("Successfully connected to KSC server!")
else:
    print("Connection failed!")
```

### List All Groups

```python
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.ChunkAccessor import KlAkChunkAccessor

# Create host group object
hostGroup = KlAkHostGroup(server)

# Get root group ID
rootGroupId = hostGroup.GroupIdGroups().RetVal()

# Find all groups
result = hostGroup.FindGroups(
    '',
    vecFieldsToReturn=['id', 'name', 'grp_full_name'],
    vecFieldsToOrder=[],
    pParams={},
    lMaxLifeTime=100
)

print(f"Found {result.RetVal()} groups")
```

---

## Authentication

### 1. Basic Authentication

```python
from KlAkOAPI.AdmServer import KlAkAdmServer

server = KlAkAdmServer.Create(
    server_url,
    username='admin_user',
    password='secure_password',
    verify='/path/to/certificate.cer'
)
```

### 2. NTLM Authentication (Windows)

```python
server = KlAkAdmServer.CreateNTLM(
    server_url,
    verify='/path/to/certificate.cer'
)
```

### 3. Virtual Server Connection

```python
server = KlAkAdmServer.Create(
    server_url,
    username='admin_user',
    password='secure_password',
    verify='/path/to/certificate.cer',
    vserver='VirtualServerName'  # Connect to specific virtual server
)
```

### 4. Gateway Connection to Network Agent

```python
from KlAkOAPI.CgwHelper import KlAkCgwHelper
from KlAkOAPI.GatewayConnection import KlAkGatewayConnection
from KlAkOAPI.Params import KlAkParams, paramParams

# Step 1: Get nagent location
cgwHelper = KlAkCgwHelper(server)
nagentLocation = cgwHelper.GetNagentLocation(wsHostName).RetVal()

# Step 2: Build locations list
arrLocation = [paramParams(nagentLocation)]

# Step 3: Prepare gateway connection
gatewayConnection = KlAkGatewayConnection(server)
response = gatewayConnection.PrepareGatewayConnection(arrLocation)
token = response.OutPar('wstrAuthKey')

# Step 4: Connect via gateway
nagent = KlAkAdmServer.CreateGateway(server_url, token, verify=False)
```

---

## Core Concepts

### KlAkParams - Parameter Container

The `KlAkParams` class is the fundamental data structure used throughout KlAkOAPI for passing parameters to API methods.

```python
from KlAkOAPI.Params import KlAkParams, KlAkArray, paramInt, paramString

# Create params from dictionary
params = KlAkParams({
    'name': 'TestGroup',
    'parentId': 0
})

# Add parameters individually
params = KlAkParams()
params.AddString('name', 'TestGroup')
params.AddInt('parentId', 0)
params.AddBool('enabled', True)
params.AddDateTime('creationDate', datetime.datetime.now())

# Nested parameters
params.AddParams('nested', {'key': 'value'})

# Arrays
params.AddArray('items', [paramInt(1), paramInt(2), paramInt(3)])

# Access values
name = params['name']
nested_value = params.GetValue('nested')['key']
```

### Asynchronous Actions

Many operations in KSC are asynchronous. Use `KlAkAsyncActionStateChecker` to monitor their progress.

```python
from KlAkOAPI.AsyncActionStateChecker import KlAkAsyncActionStateChecker
from KlAkOAPI.Base import MillisecondsToSeconds

# Start async operation
result = hostGroup.RemoveGroup(nGroupId, nFlags=1)
actionGuid = result.OutPar('strActionGuid')

# Monitor completion
checker = KlAkAsyncActionStateChecker(server)
while True:
    state = checker.CheckActionState(actionGuid)

    if state.OutPar('bFinalized'):
        if state.OutPar('bSuccededFinalized'):
            print("Operation completed successfully!")
        else:
            errorData = KlAkParams(state.OutPar('pStateData'))
            print(f"Error: {errorData['GNRL_EA_DESCRIPTION']}")
        break
    else:
        # Wait for suggested delay
        delay = MillisecondsToSeconds(state.OutPar('lNextCheckDelay'))
        time.sleep(delay)
```

### Chunk-based Iteration

For large result sets, use chunked iteration for efficient data retrieval.

```python
from KlAkOAPI.ChunkAccessor import KlAkChunkAccessor

# Initial search returns an accessor
result = hostGroup.FindGroups('', ['id', 'name'], [], {}, 100)
strAccessor = result.OutPar('strAccessor')

# Iterate through chunks
chunkAccessor = KlAkChunkAccessor(server)
totalItems = chunkAccessor.GetItemsCount(strAccessor).RetVal()

start = 0
chunkSize = 100

while start < totalItems:
    chunk = chunkAccessor.GetItemsChunk(strAccessor, start, chunkSize)
    items = chunk.OutPar('pChunk')['KLCSP_ITERATOR_ARRAY']

    for item in items:
        print(f"Group: {item['name']} (ID: {item['id']})")

    start += chunkSize
```

---

## Common Operations

### Device Management

#### Find Devices

```python
from KlAkOAPI.HostGroup import KlAkHostGroup

hostGroup = KlAkHostGroup(server)

# Find hosts by FQDN
result = hostGroup.FindHosts(
    '(KLHST_WKS_FQDN="workstation.example.com")',
    ['KLHST_WKS_HOSTNAME', 'KLHST_WKS_DN', 'name'],
    [],
    {'KLGRP_FIND_FROM_CUR_VS_ONLY': True},
    100
)

strAccessor = result.OutPar('strAccessor')
chunkAccessor = KlAkChunkAccessor(server)
# ... process chunks as shown above
```

#### Move Hosts to Group

```python
# Find hosts to move
hosts_to_move = ['host1.example.com', 'host2.example.com']
target_group_id = 123  # ID of target group

# Move hosts
hostGroup.MoveHostsToGroup(hosts_to_move, target_group_id)
```

### Group Management

#### Create Group

```python
# Add subgroup to root (Managed devices)
rootId = hostGroup.GroupIdGroups().RetVal()

newGroupId = hostGroup.AddGroup({
    'name': 'New Subgroup',
    'parentId': rootId
}).RetVal()

print(f"Created group with ID: {newGroupId}")
```

#### Search Groups with Filters

```python
# Groups with name matching pattern
result = hostGroup.FindGroups(
    '(name="Test*")',
    ['id', 'name', 'grp_full_name'],
    [],
    {},
    100
)

# Groups with critical devices
result = hostGroup.FindGroups(
    '(KLGRP_CHLDHST_CNT_CRT >= 1)',
    ['id', 'name', 'KLGRP_CHLDHST_CNT_CRT'],
    [],
    {},
    100
)

# Large groups (100+ devices)
result = hostGroup.FindGroups(
    '(KLGRP_CHLDHST_CNT >= 100)',
    ['id', 'name', 'KLGRP_CHLDHST_CNT'],
    [],
    {},
    100
)

# Groups created after specific date
result = hostGroup.FindGroups(
    '(creationDate>"2024-01-01T00:00:00Z")',
    ['id', 'name', 'creationDate'],
    [],
    {},
    100
)
```

#### Delete Group

```python
# Remove group (asynchronous)
result = hostGroup.RemoveGroup(nGroupId, nFlags=1)
actionGuid = result.OutPar('strActionGuid')

# Monitor completion with AsyncActionStateChecker
# ...
```

### Task Management

#### Create Group Task

```python
from KlAkOAPI.Tasks import KlAkTasks
from KlAkOAPI.Params import KlAkParams

tasks = KlAkTasks(server)

# Create a "Show Message" task
taskParams = KlAkParams({
    'TASKID_COMPONENT_NAME': '86',
    'TASKID_PRODUCT_NAME': '1103',
    'TASKID_VERSION': '1.0.0.0',
    'TASK_NAME': 'KLNAG_TASK_SHOW_MSG'
})

taskParams.AddParams('TASK_ADDITIONAL_PARAMS', {
    'KLNAG_MSG_TEXT': 'Hello from KlAkOAPI!'
})

taskParams.AddInt('TASKSCH_TYPE', 0)  # Manual schedule

taskParams.AddParams('TASK_INFO_PARAMS', {
    'DisplayName': 'My Test Task',
    'PRTS_TASK_GROUPID': rootGroupId,
    'klprts-TaskScheduleSubtype': 256
})

taskId = tasks.AddTask(taskParams).RetVal()
print(f"Created task with ID: {taskId}")
```

#### Run Task and Monitor

```python
from KlAkOAPI.EventProcessing import KlAkEventProcessing

# Start task
tasks.RunTask(taskId)

# Monitor task state
eventProcessing = KlAkEventProcessing(server)
fields = KlAkArray(['event_type', 'task_new_state', 'rise_time'])
sort = KlAkArray([{'Name': 'rise_time', 'Asc': False}])
filter = KlAkParams({'event_type': 'KLPRCI_TaskState'})

history = tasks.GetTaskHistory(taskId, fields, sort, '', filter)
iteratorId = history.OutPar('strIteratorId')

# Process events
recordCount = eventProcessing.GetRecordCount(iteratorId).RetVal()
events = eventProcessing.GetRecordRange(iteratorId, 0, recordCount)

for event in events.OutPar('pParamsEvents')['KLEVP_EVENT_RANGE_ARRAY']:
    print(f"Event: {event['task_new_state']} at {event['rise_time']}")

eventProcessing.ReleaseIterator(iteratorId)
```

### Report Generation

```python
from KlAkOAPI.ReportManager import KlAkReportManager

reportManager = KlAkReportManager(server)

# List available reports
reports = reportManager.EnumReports().RetVal()
for report in reports:
    print(f"Report ID {report['RPT_ID']}: {report['RPT_DN']}")

# Generate report (HTML format)
options = KlAkParams({})
options.AddInt('KLRPT_MAX_RECORDS_DETAILS', 3000)
options.AddInt('KLRPT_TARGET_TYPE', 0)
options.AddInt('KLRPT_XML_TARGET_TYPE', 0)  # 0=HTML, 1=XLS, 2=PDF
options.AddBool('KLRPT_PDF_LANDSCAPE', True)

products = KlAkParams({
    'KLRPT_PROD_NAME': '1093',
    'KLRPT_PROD_NAME_LOC': 'Administration server',
    'KLRPT_PROD_VER': '1.0.0.0'
})

options.AddArray('KLRPT_LOC_PRODUCTS', [paramParams(products)])

# Execute report asynchronously
reportId = 1  # ID of report to generate
requestId = reportManager.ExecuteReportAsync(reportId, options).OutPar('strRequestId')

# Monitor completion
# ... use AsyncActionStateChecker

# Download result
server.DownloadFile(reportFile, 'local_report.html')
```

### Statistics and Charts

```python
# Request statistics
query = KlAkParams({})
query.AddParams('KLSTS_Administration', {})
query.AddParams('KLSTS_Deployment', {})
query.AddParams('KLSTS_Protection', {})
query.AddParams('KLSTS_Updates', {})

requestId = reportManager.RequestStatisticsData(query).OutPar('strRequestId')

# Get results
resultData = reportManager.GetStatisticsData(requestId).OutPar('pResultData')

# Parse deployment status
if 'KLSTS_Deployment' in resultData:
    status = resultData['KLSTS_Deployment']
    print(f"Deployment Status: {status['KLSTS_Par_Status']}")
    print(f"Hosts with AV: {status['KLSTS_Par_Dpl_HostsWithAVP']}")
    print(f"Total hosts in groups: {status['KLSTS_Par_Dpl_HostsInGroups']}")
```

### License Management

```python
from KlAkOAPI.LicenseKeys import KlAkLicenseKeys

licenses = KlAkLicenseKeys(server)

# Enumerate licenses
fields = [
    'KLLIC_APP_ID', 'KLLIC_SERIAL', 'KLLIC_PROD_NAME',
    'KLLIC_LIMIT_DATE', 'KLLIC_KEY_TYPE', 'KLLIC_LIC_COUNT'
]

chunkAccessor = licenses.EnumKeys(fields, [], {}, lTimeoutSec=3600)
iterator = chunkAccessor.OutPar('wstrIterator')

# Process licenses
# ... use GroupSyncIterator to iterate

keyCount = chunkAccessor.OutPar('lKeyCount')
print(f"Found {keyCount} license keys")
```

### Tag Management

```python
from KlAkOAPI.ListTags import KlAkListTags

tagsControl = KlAkListTags(server, 'HostsTags')

# Enumerate all tags
allTags = tagsControl.GetAllTags(None).RetVal()
for tag in allTags:
    print(f"Tag: {tag}")

# Add a new tag
tagsControl.AddTag('Production', {})

# Rename tag
tagsControl.RenameTag('Production', 'ProductionServers', {})

# Set tags on hosts
hostIds = ['host1_id', 'host2_id']
tagsArrayItem = KlAkParams({
    'KLTAGS_VALUE': 'ProductionServers',
    'KLTAGS_SET': True
})

hostsArrayItem = KlAkParams({
    'KLTAGS_ITEM_ID': hostIds[0],
    'KLTAGS_TAGS': [paramParams(tagsArrayItem)]
})

tagsControl.SetTags([paramParams(hostsArrayItem)], {'KLTAGS_FULL_REPLACE': False})

# Delete tag
tagsControl.DeleteTags2(['OldTag'], {})
```

### User Management

```python
from KlAkOAPI.SecurityPolicy import KlAkSecurityPolicy
from KlAkOAPI.DataProtectionApi import KlAkDataProtectionApi
from KlAkOAPI.Params import dateTimeToStr, paramBinary

# Protect password
dataProtection = KlAkDataProtectionApi(server)
protectedPassword = dataProtection.ProtectUtf16StringGlobally("SecurePassword123!").RetVal()

# Add internal user
users = KlAkSecurityPolicy(server)
userName = "api_user_" + dateTimeToStr(datetime.datetime.now()).replace("-", "_").replace(":", "_")

userId = users.AddUser({
    "KLSPL_USER_NAME": userName,
    "KLSPL_USER_FULL_NAME": "API User",
    "KLSPL_USER_PWD_ENCRYPTED": paramBinary(protectedPassword)
}).RetVal()

print(f"Created user {userName} with ID: {userId}")
```

### Update Agent Management

```python
from KlAkOAPI.UaControl import KlAkUaControl
from KlAkOAPI.Params import KlAkParams, paramLong

uaControl = KlAkUaControl(server)

# Disable automatic assignment
if uaControl.GetAssignUasAutomatically().RetVal():
    uaControl.SetAssignUasAutomatically(False)

# Register host as update agent
hostId = 'target_host_hostname'
groupId = rootGroupId

uaInfo = KlAkParams({})
uaInfo.Add('UaHostId', hostId)

uaScope = KlAkParams({
    'ScopeGroups': [paramParams({
        'ScopeId': paramLong(groupId),
        'ScopeName': 'Main Group Scope'
    })]
})

uaInfo.AddParams('UaScope', uaScope)
uaControl.RegisterUpdateAgent(uaInfo)
```

### Incident Management

```python
# Find incidents
hostGroup = KlAkHostGroup(server)

# Find handled incidents
strAccessor = hostGroup.FindIncidents(
    'KLINCDT_IS_HANDLED=1',
    ['KLINCDT_ID', 'KLINCDT_SEVERITY', 'KLINCDT_ADDED',
     'KLINCDT_BODY', 'KLINCDT_IS_HANDLED', 'KLHST_WKS_HOSTNAME'],
    [],
    lMaxLifeTime=3600
).OutPar('strAccessor')

chunkAccessor = KlAkChunkAccessor(server)
recordsCount = chunkAccessor.GetItemsCount(strAccessor).RetVal()

print(f"Found {recordsCount} incidents")

chunk = chunkAccessor.GetItemsChunk(strAccessor, 0, recordsCount)
for incident in chunk.OutPar('pChunk')['KLCSP_ITERATOR_ARRAY']:
    print(f"Incident ID: {incident['KLINCDT_ID']}")
    print(f"  Severity: {incident['KLINCDT_SEVERITY']}")
    print(f"  Body: {incident['KLINCDT_BODY']}")
    print(f"  Host: {incident['KLHST_WKS_HOSTNAME']}")
```

### Mobile Device Management

```python
from KlAkOAPI.UserDevicesApi import KlAkUserDevicesApi
from KlAkOAPI.SrvView import KlAkSrvView

userDevicesApi = KlAkUserDevicesApi(server)

# Get user's devices
devices = userDevicesApi.GetDevices(userId).RetVal()
for device in devices:
    print(f"Device ID: {device['KLMDM_DEVICE_ID']}")
    print(f"  Model: {device['KLMDM_DEVICE_MODEL']}")
    print(f"  OS: {device['KLMDM_DEVICE_OS']}")
    print(f"  Friendly Name: {device['KLMDM_DEVICE_FRIENDLY_NAME']}")
    if 'KLMDM_DEVICE_MDM_PROTOCOL' in device:
        print(f"  MDM Protocol: {device['KLMDM_DEVICE_MDM_PROTOCOL']}")

# Get enrollment packages
packages = userDevicesApi.GetEnrollmentPackages(userId).RetVal()
for package in packages:
    print(f"Package ID: {package['KLMDM_ENR_PKG_ID']}")
    print(f"  Protocol: {package['KLMDM_ENR_PKG_MDM_PROTOCOLS']}")
    print(f"  State: {package['KLMDM_ENR_PKG_STATE']}")
    print(f"  URL: {package['KLMDM_ENR_PKG_UNIFIED_URL']}")
```

### IP Subnet Configuration

```python
from KlAkOAPI.ScanDiapasons import KlAkScanDiapasons
import socket

scanDiapasons = KlAkScanDiapasons(server)

# Create IP subnet from CIDR notation
# Example: 192.168.1.0/24
network = "192.168.1.0"
maskBits = 24

mask = socket.htonl((0xffffffff << (32 - maskBits)) & 0xffffffff)
ip = int.from_bytes(socket.inet_aton(network), byteorder='little') & mask

params = KlAkParams({})
params.AddString('KLDPNS_DN', 'MySubnet')
params.AddArray('KLDPNS_ILS', [paramParams({
    'KLDPNS_IL_ISSUBNET': True,
    'KLDPNS_IL_MASKORLOW': paramInt(mask),
    'KLDPNS_IL_SUBNETORHI': paramInt(ip)
})])
params.AddInt('KLDPNS_LF', 3600*8)  # Lifetime
params.AddBool('KLDPNS_ScanEnabled', True)  # Enable scanning

subnetId = scanDiapasons.AddDiapason(params).RetVal()
print(f"Created subnet with ID: {subnetId}")
```

### Application Categories

```python
from KlAkOAPI.FileCategorizer2 import KlAkFileCategorizer2

# Create an application deny list category
expression = KlAkParams({
    'ex_type': 3,  # MD5 hash
    'str': 'e4d909c290d0fb1ca068ffaddf22cbd0',
    'str_op': 0
})

category = KlAkParams({
    'name': 'BlockedApplications',
    'CategoryType': 0,  # 0 = deny list
    'inclusions': [expression]
})

categoryId = KlAkFileCategorizer2(server).CreateCategory(category).RetVal()
print(f"Created category with ID: {categoryId}")
```

### Email Notifications

```python
import KlAkOAPI.IWebUsersSrv
import uuid

# Create email with HTML body and QR code
options = KlAkParams({
    'MailRecipients': ['admin@example.com'],
    'MailSubject': 'Security Alert Report',
    'MailBodyType': 'html'
})

# Add HTML body
htmlBody = '''
<h2>Security Report</h2>
<ul>
    <li>Critical incidents: 5</li>
    <li>Warning incidents: 12</li>
    <li>Info incidents: 23</li>
</ul>
'''
options.AddString('MailBody', htmlBody)

# Add QR code image (base64 encoded PNG)
qrCode = KlAkParams({})
qrCode.AddBinary('QrCodePicture', base64EncodedPngData)
qrCode.AddString('QrCodePictureName', 'security_qr.png')

options.AddArray('QrCodes', [qrCode])

# Send email
KlAkOAPI.IWebUsersSrv.KlAkIWebUsersSrv(server).SendEmail(
    options,
    str(uuid.uuid4())
)
```

### Virtual Server Statistics

```python
# Get virtual server statistics
hostGroup = KlAkHostGroup(server)

stats = hostGroup.GetInstanceStatistics([
    'KLSRV_ST_VIRT_SERVER_COUNT',
    'KLSRV_ST_TOTAL_HOSTS_COUNT',
    'KLSRV_ST_VIRT_SERVERS_DETAILS'
]).RetVal()

print(f"Virtual Servers: {stats['KLSRV_ST_VIRT_SERVER_COUNT']}")
print(f"Total Hosts: {stats['KLSRV_ST_TOTAL_HOSTS_COUNT']}")

# Virtual server details
for vserver in stats['KLSRV_ST_VIRT_SERVERS_DETAILS']:
    print(f"\nVirtual Server: {vserver['KLSRV_ST_VIRT_SERVER_NAME']}")
    print(f"  ID: {vserver['KLSRV_ST_VIRT_SERVER_ID']}")
    if 'KLSRV_ST_VSERVER_HOST_COUNT' in vserver:
        print(f"  Hosts: {vserver['KLSRV_ST_VSERVER_HOST_COUNT']}")
    if 'KLSRV_ST_VSERVER_IOSMDM_DEV_COUNT' in vserver:
        print(f"  iOS Devices: {vserver['KLSRV_ST_VSERVER_IOSMDM_DEV_COUNT']}")
```

### Host Settings Operations

```python
# Dump host settings
hostId = 'target_host_hostname'

# Get all settings section names
sections = hostGroup.SS_GetNames(
    hostId,
    'SS_SETTINGS',
    '1103',  # Product code
    '1.0.0.0'  # Version
).RetVal()

print("Host Settings:")
for section in sections:
    print(f"\n[{section}]")
    settings = hostGroup.SS_Read(
        hostId,
        'SS_SETTINGS',
        '1103',
        '1.0.0.0',
        section
    ).RetVal()
    print(settings)
```

---

## API Modules

### Core Modules

| Module | Description |
|--------|-------------|
| `KlAkAdmServer` | Main server connection and configuration |
| `KlAkParams` | Parameter container for API calls |
| `KlAkArray` | Array handling for parameters |
| `KlAkBase` | Base utilities and helpers |

### Device Management

| Module | Description |
|--------|-------------|
| `KlAkHostGroup` | Manage device groups and hierarchies |
| `KlAkSrvView` | Server views and iterators |
| `KlAkHostTasks` | Host-specific task management |
| `KlAkNagHstCtl` | Network Agent host control |

### Task Management

| Module | Description |
|--------|-------------|
| `KlAkTasks` | Group task creation and management |
| `KlAkTask` | Individual task operations |

### Reporting

| Module | Description |
|--------|-------------|
| `KlAkReportManager` | Report generation and statistics |
| `KlAkEventProcessing` | Event processing and history |

### Server Management

| Module | Description |
|--------|-------------|
| `KlAkServerHierarchy` | Primary-secondary server hierarchy |
| `KlAkVServers` | Virtual server management |
| `KlAkLicenseKeys` | License key management |

### User Management & Security

| Module | Description |
|--------|-------------|
| `KlAkSecurityPolicy` | Security policy and user management |
| `KlAkDataProtectionApi` | Data protection and password encryption |
| `KlAkSrvView` | User enumeration and lookups |

### Tagging & Organization

| Module | Description |
|--------|-------------|
| `KlAkListTags` | Tag management for hosts |

### Update Management

| Module | Description |
|--------|-------------|
| `KlAkUaControl` | Update Agent control and assignment |

### Network & Scanning

| Module | Description |
|--------|-------------|
| `KlAkScanDiapasons` | IP subnet scanning configuration |
| `KlAkAdHosts` | Active Directory host integration |

### Mobile Device Management

| Module | Description |
|--------|-------------|
| `KlAkUserDevicesApi` | Mobile device and enrollment management |
| `KlAkNagNetworkListApi` | Network list file management |

### Application Control

| Module | Description |
|--------|-------------|
| `KlAkFileCategorizer2` | File categorization and application categories |

### Notifications

| Module | Description |
|--------|-------------|
| `KlAkEventNotificationProperties` | Notification settings |
| `KlAkIWebUsersSrv` | Email notification services |

### Utility Modules

| Module | Description |
|--------|-------------|
| `KlAkChunkAccessor` | Chunk-based data retrieval |
| `KlAkAsyncActionStateChecker` | Monitor async operations |
| `KlAkCgwHelper` | Gateway connection helper |
| `KlAkGatewayConnection` | Gateway connection management |
| `KlAkGroupSyncIterator` | Group-based iteration |

### Advanced Operations

| Module | Description |
|--------|-------------|
| `KlAkNagRdu` | Remote file operations on agents |
| `KlAkNagHstCtl` | Network Agent host control via gateway |

---

## Code Samples

### Complete: Find and Move Devices

```python
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.ChunkAccessor import KlAkChunkAccessor
from KlAkOAPI.Params import KlAkParams

# Connect to server
server = KlAkAdmServer.Create(
    'https://ksc.example.com:13299',
    username='admin',
    password='password',
    verify=False  # Disable SSL verification for testing
)

hostGroup = KlAkHostGroup(server)

# Find hosts with specific criteria
result = hostGroup.FindHosts(
    '(KLHST_WKS_FQDN="*.example.com")',
    ['KLHST_WKS_HOSTNAME', 'KLHST_WKS_DN'],
    [],
    {'KLGRP_FIND_FROM_CUR_VS_ONLY': True},
    100
)

strAccessor = result.OutPar('strAccessor')
chunkAccessor = KlAkChunkAccessor(server)
items_count = chunkAccessor.GetItemsCount(strAccessor).RetVal()

hosts_to_move = []
chunk = chunkAccessor.GetItemsChunk(strAccessor, 0, items_count)

for host in KlAkParams(chunk.OutPar('pChunk'))['KLCSP_ITERATOR_ARRAY']:
    hosts_to_move.append(host['KLHST_WKS_HOSTNAME'])
    print(f"Found: {host['KLHST_WKS_DN']}")

# Move hosts to target group
if hosts_to_move:
    target_group = 123
    hostGroup.MoveHostsToGroup(hosts_to_move, target_group)
    print(f"Moved {len(hosts_to_move)} hosts to group {target_group}")
```

### Complete: Upload and Execute File on Remote Host

```python
from KlAkOAPI.NagRdu import KlAkNagRdu
from KlAkOAPI.AsyncActionStateChecker import KlAkAsyncActionStateChecker
import time

# Connect to nagent via gateway (see Gateway Connection section)
nagent = ...  # gateway connection

nagRdu = KlAkNagRdu(nagent)

# Upload file
upload_url = nagRdu.GetUrlToUploadFileToHost().RetVal()
nagent.UploadFile(upload_url, 'local_script.zip')

# Execute file
actionGuid = nagRdu.ExecuteFileAsync(upload_url, 'script.bat', '').RetVal()

# Monitor execution
checker = KlAkAsyncActionStateChecker(nagent)
while True:
    state = checker.CheckActionState(actionGuid)
    if state.OutPar('bFinalized'):
        if state.OutPar('bSuccededFinalized'):
            print("Execution completed successfully!")
            # Download results
            resultUrl = nagRdu.GetUrlToDownloadFileFromHost(
                state.OutPar('pStateData')['LastActionResult']
            ).RetVal()
            nagent.DownloadFile(resultUrl, 'results.zip')
        break
    time.sleep(1)
```

### Complete: Create Statistics Chart

```python
import base64
import uuid
from KlAkOAPI.Params import KlAkParams, KlAkArray, paramParams

reportManager = KlAkReportManager(server)

# Request deployment statistics
dashUuid = str(uuid.uuid4())
query = KlAkParams({
    'KLPPT_DASHBOARD': {
        dashUuid: {
            'KLRPT_DSH_TYPE': 31,  # Deployment status
            'id': rootGroupId
        }
    }
})

requestId = reportManager.RequestStatisticsData(query).OutPar('strRequestId')
# Wait for completion...

# Get results
result = reportManager.GetStatisticsData(requestId).OutPar('pResultData')
dashData = result['KLPPT_DASHBOARD'][dashUuid]

# Create chart
chartData = KlAkParams({
    'data': [
        dashData['nOkCount'],
        dashData['nWrnCount'],
        dashData['nCrtCount']
    ],
    'name': 'Deployment Status'
})

chartParams = KlAkParams({})
chartParams.AddArray('KLRPT_CHART_DATA', [paramParams(chartData)])
chartParams.AddString('KLRPT_CHART_DATA_DESC', 'Deployment Status')
chartParams.AddArray('KLRPT_CHART_SERIES', [
    'OK', 'Warning', 'Critical'
])
chartParams.AddBool('KLRPT_CHART_PIE', True)

# Generate PNG
pngResult = reportManager.CreateChartPNG(chartParams, {
    'RPT_CHART_WIDTH': 800,
    'RPT_CHART_HEIGHT': 600
})

# Save chart
with open('deployment_chart.png', 'wb') as f:
    f.write(base64.b64decode(pngResult.OutPar('pPngData')))
```

---

## Error Handling

### Try-Except Pattern

```python
from KlAkOAPI.Error import KlAkError, KlAkResponseError

try:
    result = hostGroup.RemoveGroup(nGroupId, nFlags=1)
    # Process result...
except KlAkResponseError as e:
    print(f"API Error: {e}")
    print(f"Error code: {e.error_code}")
    print(f"Description: {e.description}")
except KlAkError as e:
    print(f"General KlAkOAPI Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Check Return Values

```python
# Check operation success
result = hostGroup.AddGroup({'name': 'Test', 'parentId': rootId})
if result.RetVal() is None:
    print("Failed to create group")
else:
    groupId = result.RetVal()
    print(f"Created group with ID: {groupId}")
```

### Validate Connection

```python
server = KlAkAdmServer.Create(server_url, username, password)

if not server.connected:
    print("Failed to connect to KSC server")
    # Handle connection failure
    exit(1)
```

---

## Best Practices

### 1. Connection Management

```python
# Use context managers where possible
# Always check connection state before operations
if server.connected:
    # Perform operations
    pass

# Close connection when done
# (Note: KlAkAdmServer handles cleanup automatically)
```

### 2. SSL Certificate Handling

```python
# Production: Always verify SSL certificates
server = KlAkAdmServer.Create(
    server_url,
    username,
    password,
    verify=r'C:\ProgramData\KasperskyLab\adminkit\1093\cert\klserver.cer'
)

# Testing: Can disable verification
server = KlAkAdmServer.Create(
    server_url,
    username,
    password,
    verify=False
)
```

### 3. Asynchronous Operations

```python
# Always monitor async operations to completion
# Don't assume immediate success

actionGuid = someAsyncOperation().OutPar('strActionGuid')

checker = KlAkAsyncActionStateChecker(server)
maxRetries = 60  # Prevent infinite loops

for _ in range(maxRetries):
    state = checker.CheckActionState(actionGuid)
    if state.OutPar('bFinalized'):
        break
    time.sleep(1)
else:
    print("Operation timed out")
```

### 4. Large Dataset Handling

```python
# Use chunked iteration for large result sets
# Process data in chunks rather than loading all at once

chunkSize = 100
start = 0

while start < totalItems:
    chunk = chunkAccessor.GetItemsChunk(strAccessor, start, chunkSize)
    # Process chunk...
    start += chunkSize
```

### 5. Parameter Construction

```python
# Use KlAkParams for complex structures
# Provides type safety and proper serialization

params = KlAkParams()
params.AddString('name', 'value')
params.AddInt('count', 42)
params.AddParams('nested', {'key': 'value'})

# Better than: params = {'name': 'value', 'count': 42}
```

### 6. Error Recovery

```python
# Implement retry logic for transient failures
# Check specific error codes for appropriate action

maxRetries = 3
for attempt in range(maxRetries):
    try:
        result = server.SomeOperation()
        break
    except KlAkResponseError as e:
        if e.error_code == 0x7FF10001:  # Specific error
            if attempt < maxRetries - 1:
                time.sleep(5)
                continue
        raise
```

### 7. Resource Cleanup

```python
# Always release iterators when done
try:
    iteratorId = someApi.ResetIterator(...)
    # Process data...
finally:
    if 'iteratorId' in locals():
        someApi.ReleaseIterator(iteratorId)
```

---

## Additional Resources

### Official Documentation

- KSC Open API Documentation: Available in KSC installation directory
- Kaspersky Security Center Help: Integrated help system

### Sample Scripts Location

All 35 sample scripts are located in the `samples/` directory. Here's a complete list with descriptions:

#### Connection & Authentication
- `sample_connect.py` - Connection examples with all authentication methods
- `sample_connectionhelper_groups.py` - Group management using ConnectionHelper
- `sample_connectionhelper_reports.py` - Report generation using ConnectionHelper
- `sample_connectionhelper_put.py` - File upload using ConnectionHelper

#### Device & Group Management
- `sample_groups.py` - Group enumeration, creation, and deletion
- `sample_enumgrp.py` - Simple group enumeration
- `sample_find_devices.py` - Find and enumerate devices
- `sample_find_and_move_hosts.py` - Find hosts and move to group
- `sample_userdevices.py` - View user's mobile devices
- `sample_userdevices2.py` - Mobile devices with SSP and multitenancy
- `sample_dump_host_settings.py` - Dump host settings from storage

#### Task Management
- `sample_create_task.py` - Create and execute tasks
- `sample_task.py` - Find and execute task by name
- `sample_run_host_task.py` - Run task on specific host

#### Server Hierarchy
- `sample_master_slave.py` - Create primary-secondary relations
- `sample_enum_slaves.py` - Enumerate child servers
- `sample_spread_key_to_slaves.py` - Distribute license to all slave servers

#### Reports & Statistics
- `sample_reports.py` - Generate and download reports
- `sample_statistics.py` - Query system statistics
- `sample_charts.py` - Create statistics charts
- `sample_statistics_vsrv_details.py` - Virtual server statistics

#### Licenses & Users
- `sample_licenses.py` - Enumerate and manage licenses
- `sample_add_internal_user.py` - Create internal user
- `sample_user_eff_rights_report.py` - Generate user rights report

#### Active Directory Integration
- `sample_grp_ad.py` - Create groups from AD OU structure
- `sample_grp_ad_scanned.py` - Groups from cached AD structure
- `sample_ad_subnets.py` - Create IP subnets from AD Sites

#### Advanced Features
- `sample_put.py` - Upload and execute file on remote host
- `sample_nlst.py` - Download network list files
- `sample_tagcontrol.py` - Manage tags on hosts
- `sample_updagts.py` - Configure update agents
- `sample_host_incidents.py` - Find and manage incidents
- `sample_srvview.py` - Iterate over server views
- `sample_send_mail.py` - Send email notifications
- `sample_create_category.py` - Create application categories
- `sample_notification_properties.py` - Configure notification settings
- `sample_params.py` - Parameter handling examples

Each sample can be run directly and includes detailed docstrings and usage examples.

### Support

- Kaspersky Technical Support
- KSC Community Forums
- Partner Portal Resources

---

## Version Information

- **KlAkOAPI Version**: 1.0.0.0
- **KSC Version**: 15.1
- **Python Support**: 3.6+

---

## License

This library is part of Kaspersky Security Center and is subject to the license terms of the Kaspersky Security Center product.

---

## Changelog

### Version 1.0.0.0
- Initial release
- Core API modules
- All major KSC functionality covered
- Cross-platform support
- Comprehensive sample library

---

*This documentation covers KlAkOAPI version 1.0.0.0 for Kaspersky Security Center 15.1*
