# LinterResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**linter_name** | **str** |  | 
**is_success** | **bool** |  | 
**output** | **str** |  | [optional] 
**details** | **object** |  | [optional] 
**id** | **int** |  | 
**scan_id** | **int** |  | 

## Example

```python
from linter_api_client.models.linter_result import LinterResult

# TODO update the JSON string below
json = "{}"
# create an instance of LinterResult from a JSON string
linter_result_instance = LinterResult.from_json(json)
# print the JSON string representation of the object
print(LinterResult.to_json())

# convert the object into a dict
linter_result_dict = linter_result_instance.to_dict()
# create an instance of LinterResult from a dict
linter_result_from_dict = LinterResult.from_dict(linter_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


