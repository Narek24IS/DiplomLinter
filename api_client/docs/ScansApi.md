# linter_api_client.ScansApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_project_scans**](ScansApi.md#get_project_scans) | **GET** /scans/project/{project_id} | Get Project Scans
[**get_scan**](ScansApi.md#get_scan) | **GET** /scans/{scan_id} | Get Scan
[**get_scans**](ScansApi.md#get_scans) | **GET** /scans/ | Get Scans
[**start_scan**](ScansApi.md#start_scan) | **POST** /scans/{project_id}/start | Start Scan


# **get_project_scans**
> List[Scan] get_project_scans(project_id, authorization, skip=skip, limit=limit)

Get Project Scans

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
    api_instance = linter_api_client.ScansApi(api_client)
    project_id = 56 # int | 
    authorization = 'authorization_example' # str | 
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Project Scans
        api_response = api_instance.get_project_scans(project_id, authorization, skip=skip, limit=limit)
        print("The response of ScansApi->get_project_scans:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScansApi->get_project_scans: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **int**|  | 
 **authorization** | **str**|  | 
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

# **get_scan**
> ScanWithResults get_scan(scan_id, authorization)

Get Scan

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
    api_instance = linter_api_client.ScansApi(api_client)
    scan_id = 56 # int | 
    authorization = 'authorization_example' # str | 

    try:
        # Get Scan
        api_response = api_instance.get_scan(scan_id, authorization)
        print("The response of ScansApi->get_scan:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScansApi->get_scan: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scan_id** | **int**|  | 
 **authorization** | **str**|  | 

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

# **get_scans**
> List[ScanWithResults] get_scans(authorization, skip=skip, limit=limit)

Get Scans

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
    api_instance = linter_api_client.ScansApi(api_client)
    authorization = 'authorization_example' # str | 
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Scans
        api_response = api_instance.get_scans(authorization, skip=skip, limit=limit)
        print("The response of ScansApi->get_scans:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScansApi->get_scans: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
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

# **start_scan**
> Scan start_scan(project_id, branch, authorization)

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
    api_instance = linter_api_client.ScansApi(api_client)
    project_id = 56 # int | 
    branch = 'branch_example' # str | 
    authorization = 'authorization_example' # str | 

    try:
        # Start Scan
        api_response = api_instance.start_scan(project_id, branch, authorization)
        print("The response of ScansApi->start_scan:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScansApi->start_scan: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **int**|  | 
 **branch** | **str**|  | 
 **authorization** | **str**|  | 

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

