# linter_api_client.TechnicalApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ping**](TechnicalApi.md#ping) | **GET** /technical/ping | Ping
[**ready_check**](TechnicalApi.md#ready_check) | **GET** /technical/ready | Ready Check


# **ping**
> object ping()

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
    api_instance = linter_api_client.TechnicalApi(api_client)

    try:
        # Ping
        api_response = api_instance.ping()
        print("The response of TechnicalApi->ping:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TechnicalApi->ping: %s\n" % e)
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

# **ready_check**
> object ready_check()

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
    api_instance = linter_api_client.TechnicalApi(api_client)

    try:
        # Ready Check
        api_response = api_instance.ready_check()
        print("The response of TechnicalApi->ready_check:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TechnicalApi->ready_check: %s\n" % e)
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

