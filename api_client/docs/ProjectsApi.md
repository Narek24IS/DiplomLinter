# linter_api_client.ProjectsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_project**](ProjectsApi.md#create_project) | **POST** /projects/ | Create Project
[**get_project_by_id**](ProjectsApi.md#get_project_by_id) | **GET** /projects/by_id/{project_id} | Get Project By Id
[**get_project_by_name**](ProjectsApi.md#get_project_by_name) | **GET** /projects/by_name/{project_name} | Get Project By Name
[**get_projects**](ProjectsApi.md#get_projects) | **GET** /projects/ | Get Projects


# **create_project**
> Project create_project(project_create)

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
    api_instance = linter_api_client.ProjectsApi(api_client)
    project_create = linter_api_client.ProjectCreate() # ProjectCreate | 

    try:
        # Create Project
        api_response = api_instance.create_project(project_create)
        print("The response of ProjectsApi->create_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->create_project: %s\n" % e)
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

# **get_project_by_id**
> ProjectWithScans get_project_by_id(project_id, authorization)

Get Project By Id

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
    api_instance = linter_api_client.ProjectsApi(api_client)
    project_id = 56 # int | 
    authorization = 'authorization_example' # str | 

    try:
        # Get Project By Id
        api_response = api_instance.get_project_by_id(project_id, authorization)
        print("The response of ProjectsApi->get_project_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_project_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **int**|  | 
 **authorization** | **str**|  | 

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

# **get_project_by_name**
> ProjectWithScans get_project_by_name(project_name, authorization)

Get Project By Name

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
    api_instance = linter_api_client.ProjectsApi(api_client)
    project_name = 'project_name_example' # str | 
    authorization = 'authorization_example' # str | 

    try:
        # Get Project By Name
        api_response = api_instance.get_project_by_name(project_name, authorization)
        print("The response of ProjectsApi->get_project_by_name:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_project_by_name: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **authorization** | **str**|  | 

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

# **get_projects**
> List[Project] get_projects(authorization, skip=skip, limit=limit)

Get Projects

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
    api_instance = linter_api_client.ProjectsApi(api_client)
    authorization = 'authorization_example' # str | 
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get Projects
        api_response = api_instance.get_projects(authorization, skip=skip, limit=limit)
        print("The response of ProjectsApi->get_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**|  | 
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

