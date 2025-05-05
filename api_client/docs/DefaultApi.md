# linter_api_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_project_projects_post**](DefaultApi.md#create_project_projects_post) | **POST** /projects/ | Create Project
[**create_scan_scans_post**](DefaultApi.md#create_scan_scans_post) | **POST** /scans/ | Create Scan
[**create_user_users_post**](DefaultApi.md#create_user_users_post) | **POST** /users/ | Create User
[**get_scan_stats_linter_results_stats_scan_id_get**](DefaultApi.md#get_scan_stats_linter_results_stats_scan_id_get) | **GET** /linter-results/stats/{scan_id} | Get Scan Stats
[**ping_technical_ping_get**](DefaultApi.md#ping_technical_ping_get) | **GET** /technical/ping | Ping
[**read_linter_results_linter_results_get**](DefaultApi.md#read_linter_results_linter_results_get) | **GET** /linter-results/ | Read Linter Results
[**read_project_projects_project_id_get**](DefaultApi.md#read_project_projects_project_id_get) | **GET** /projects/{project_id} | Read Project
[**read_project_scans_scans_project_project_id_get**](DefaultApi.md#read_project_scans_scans_project_project_id_get) | **GET** /scans/project/{project_id} | Read Project Scans
[**read_projects_projects_get**](DefaultApi.md#read_projects_projects_get) | **GET** /projects/ | Read Projects
[**read_scan_results_linter_results_scan_scan_id_get**](DefaultApi.md#read_scan_results_linter_results_scan_scan_id_get) | **GET** /linter-results/scan/{scan_id} | Read Scan Results
[**read_scan_scans_scan_id_get**](DefaultApi.md#read_scan_scans_scan_id_get) | **GET** /scans/{scan_id} | Read Scan
[**read_scans_scans_get**](DefaultApi.md#read_scans_scans_get) | **GET** /scans/ | Read Scans
[**read_user_users_user_id_get**](DefaultApi.md#read_user_users_user_id_get) | **GET** /users/{user_id} | Read User
[**read_users_users_get**](DefaultApi.md#read_users_users_get) | **GET** /users/ | Read Users
[**ready_check_technical_ready_get**](DefaultApi.md#ready_check_technical_ready_get) | **GET** /technical/ready | Ready Check
[**start_scan_scans_project_id_start_post**](DefaultApi.md#start_scan_scans_project_id_start_post) | **POST** /scans/{project_id}/start | Start Scan


# **create_project_projects_post**
> Project create_project_projects_post(project_create)

Create Project

### Example


```python
import linter_api_client
from linter_api_client.models.project import Project
from linter_api_client.models.project_create import ProjectCreate
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    project_create = linter_api_client.ProjectCreate() # ProjectCreate | 

    try:
        # Create Project
        api_response = api_instance.create_project_projects_post(project_create)
        print("The response of DefaultApi->create_project_projects_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_project_projects_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_create** | [**ProjectCreate**](ProjectCreate.md)|  | 

### Return type

[**Project**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_scan_scans_post**
> Scan create_scan_scans_post(scan_create)

Create Scan

### Example


```python
import linter_api_client
from linter_api_client.models.scan import Scan
from linter_api_client.models.scan_create import ScanCreate
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    scan_create = linter_api_client.ScanCreate() # ScanCreate | 

    try:
        # Create Scan
        api_response = api_instance.create_scan_scans_post(scan_create)
        print("The response of DefaultApi->create_scan_scans_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_scan_scans_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scan_create** | [**ScanCreate**](ScanCreate.md)|  | 

### Return type

[**Scan**](Scan.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_users_post**
> User create_user_users_post(user_create)

Create User

### Example


```python
import linter_api_client
from linter_api_client.models.user import User
from linter_api_client.models.user_create import UserCreate
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    user_create = linter_api_client.UserCreate() # UserCreate | 

    try:
        # Create User
        api_response = api_instance.create_user_users_post(user_create)
        print("The response of DefaultApi->create_user_users_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_user_users_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_create** | [**UserCreate**](UserCreate.md)|  | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scan_stats_linter_results_stats_scan_id_get**
> List[LinterStats] get_scan_stats_linter_results_stats_scan_id_get(scan_id)

Get Scan Stats

### Example


```python
import linter_api_client
from linter_api_client.models.linter_stats import LinterStats
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    scan_id = 56 # int | 

    try:
        # Get Scan Stats
        api_response = api_instance.get_scan_stats_linter_results_stats_scan_id_get(scan_id)
        print("The response of DefaultApi->get_scan_stats_linter_results_stats_scan_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_scan_stats_linter_results_stats_scan_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scan_id** | **int**|  | 

### Return type

[**List[LinterStats]**](LinterStats.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ping_technical_ping_get**
> object ping_technical_ping_get()

Ping

### Example


```python
import linter_api_client
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)

    try:
        # Ping
        api_response = api_instance.ping_technical_ping_get()
        print("The response of DefaultApi->ping_technical_ping_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->ping_technical_ping_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_linter_results_linter_results_get**
> List[LinterResult] read_linter_results_linter_results_get(skip=skip, limit=limit)

Read Linter Results

### Example


```python
import linter_api_client
from linter_api_client.models.linter_result import LinterResult
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Read Linter Results
        api_response = api_instance.read_linter_results_linter_results_get(skip=skip, limit=limit)
        print("The response of DefaultApi->read_linter_results_linter_results_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_linter_results_linter_results_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[LinterResult]**](LinterResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_project_projects_project_id_get**
> ProjectWithScans read_project_projects_project_id_get(project_id)

Read Project

### Example


```python
import linter_api_client
from linter_api_client.models.project_with_scans import ProjectWithScans
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    project_id = 56 # int | 

    try:
        # Read Project
        api_response = api_instance.read_project_projects_project_id_get(project_id)
        print("The response of DefaultApi->read_project_projects_project_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_project_projects_project_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **int**|  | 

### Return type

[**ProjectWithScans**](ProjectWithScans.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_project_scans_scans_project_project_id_get**
> List[Scan] read_project_scans_scans_project_project_id_get(project_id, skip=skip, limit=limit)

Read Project Scans

### Example


```python
import linter_api_client
from linter_api_client.models.scan import Scan
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    project_id = 56 # int | 
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Read Project Scans
        api_response = api_instance.read_project_scans_scans_project_project_id_get(project_id, skip=skip, limit=limit)
        print("The response of DefaultApi->read_project_scans_scans_project_project_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_project_scans_scans_project_project_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **int**|  | 
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[Scan]**](Scan.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_projects_projects_get**
> List[Project] read_projects_projects_get(skip=skip, limit=limit)

Read Projects

### Example


```python
import linter_api_client
from linter_api_client.models.project import Project
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Read Projects
        api_response = api_instance.read_projects_projects_get(skip=skip, limit=limit)
        print("The response of DefaultApi->read_projects_projects_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_projects_projects_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[Project]**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_scan_results_linter_results_scan_scan_id_get**
> List[LinterResult] read_scan_results_linter_results_scan_scan_id_get(scan_id)

Read Scan Results

### Example


```python
import linter_api_client
from linter_api_client.models.linter_result import LinterResult
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    scan_id = 56 # int | 

    try:
        # Read Scan Results
        api_response = api_instance.read_scan_results_linter_results_scan_scan_id_get(scan_id)
        print("The response of DefaultApi->read_scan_results_linter_results_scan_scan_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_scan_results_linter_results_scan_scan_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scan_id** | **int**|  | 

### Return type

[**List[LinterResult]**](LinterResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_scan_scans_scan_id_get**
> ScanWithResults read_scan_scans_scan_id_get(scan_id)

Read Scan

### Example


```python
import linter_api_client
from linter_api_client.models.scan_with_results import ScanWithResults
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    scan_id = 56 # int | 

    try:
        # Read Scan
        api_response = api_instance.read_scan_scans_scan_id_get(scan_id)
        print("The response of DefaultApi->read_scan_scans_scan_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_scan_scans_scan_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scan_id** | **int**|  | 

### Return type

[**ScanWithResults**](ScanWithResults.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_scans_scans_get**
> List[ScanWithResults] read_scans_scans_get(skip=skip, limit=limit)

Read Scans

### Example


```python
import linter_api_client
from linter_api_client.models.scan_with_results import ScanWithResults
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Read Scans
        api_response = api_instance.read_scans_scans_get(skip=skip, limit=limit)
        print("The response of DefaultApi->read_scans_scans_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_scans_scans_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[ScanWithResults]**](ScanWithResults.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_user_users_user_id_get**
> User read_user_users_user_id_get(user_id)

Read User

### Example


```python
import linter_api_client
from linter_api_client.models.user import User
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    user_id = 56 # int | 

    try:
        # Read User
        api_response = api_instance.read_user_users_user_id_get(user_id)
        print("The response of DefaultApi->read_user_users_user_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_user_users_user_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**|  | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_users_users_get**
> List[User] read_users_users_get(skip=skip, limit=limit)

Read Users

### Example


```python
import linter_api_client
from linter_api_client.models.user import User
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Read Users
        api_response = api_instance.read_users_users_get(skip=skip, limit=limit)
        print("The response of DefaultApi->read_users_users_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->read_users_users_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[User]**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ready_check_technical_ready_get**
> object ready_check_technical_ready_get()

Ready Check

Ручка для проверки готовности контейнера.
:param consumer: Коннект к кролику для обработки сообщений
:param publisher: Коннект к кролику для публикации сообщений с результатами
:return: 200 если оба коннекта готовы, 500 в противном случае

### Example


```python
import linter_api_client
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)

    try:
        # Ready Check
        api_response = api_instance.ready_check_technical_ready_get()
        print("The response of DefaultApi->ready_check_technical_ready_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->ready_check_technical_ready_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_scan_scans_project_id_start_post**
> Scan start_scan_scans_project_id_start_post(project_id)

Start Scan

### Example


```python
import linter_api_client
from linter_api_client.models.scan import Scan
from linter_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = linter_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with linter_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linter_api_client.DefaultApi(api_client)
    project_id = 56 # int | 

    try:
        # Start Scan
        api_response = api_instance.start_scan_scans_project_id_start_post(project_id)
        print("The response of DefaultApi->start_scan_scans_project_id_start_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->start_scan_scans_project_id_start_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **int**|  | 

### Return type

[**Scan**](Scan.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

