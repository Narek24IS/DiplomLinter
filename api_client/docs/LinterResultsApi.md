# linter_api_client.LinterResultsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_linter_results**](LinterResultsApi.md#get_linter_results) | **GET** /linter-results/{linter_result_id} | Get Linter Results
[**get_scan_results**](LinterResultsApi.md#get_scan_results) | **GET** /linter-results/scan/{scan_id} | Get Scan Results
[**get_scan_stats**](LinterResultsApi.md#get_scan_stats) | **GET** /linter-results/stats/{scan_id} | Get Scan Stats


# **get_linter_results**
> List[LinterResult] get_linter_results(linter_result_id, authorization)

Get Linter Results

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
    api_instance = linter_api_client.LinterResultsApi(api_client)
    linter_result_id = 56 # int | 
    authorization = 'authorization_example' # str | 

    try:
        # Get Linter Results
        api_response = api_instance.get_linter_results(linter_result_id, authorization)
        print("The response of LinterResultsApi->get_linter_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LinterResultsApi->get_linter_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **linter_result_id** | **int**|  | 
 **authorization** | **str**|  | 

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

# **get_scan_results**
> List[LinterResult] get_scan_results(scan_id, authorization)

Get Scan Results

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
    api_instance = linter_api_client.LinterResultsApi(api_client)
    scan_id = 56 # int | 
    authorization = 'authorization_example' # str | 

    try:
        # Get Scan Results
        api_response = api_instance.get_scan_results(scan_id, authorization)
        print("The response of LinterResultsApi->get_scan_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LinterResultsApi->get_scan_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scan_id** | **int**|  | 
 **authorization** | **str**|  | 

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

# **get_scan_stats**
> List[LinterStats] get_scan_stats(scan_id, authorization)

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
    api_instance = linter_api_client.LinterResultsApi(api_client)
    scan_id = 56 # int | 
    authorization = 'authorization_example' # str | 

    try:
        # Get Scan Stats
        api_response = api_instance.get_scan_stats(scan_id, authorization)
        print("The response of LinterResultsApi->get_scan_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LinterResultsApi->get_scan_stats: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scan_id** | **int**|  | 
 **authorization** | **str**|  | 

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

