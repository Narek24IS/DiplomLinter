# Scan


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**branch** | **str** |  | 
**id** | **int** |  | 
**project_id** | **int** |  | 
**status** | **str** |  | 
**started_at** | **datetime** |  | 
**finished_at** | **datetime** |  | [optional] 
**total_errors** | **int** |  | [optional] [default to 0]
**total_warnings** | **int** |  | [optional] [default to 0]

## Example

```python
from linter_api_client.models.scan import Scan

# TODO update the JSON string below
json = "{}"
# create an instance of Scan from a JSON string
scan_instance = Scan.from_json(json)
# print the JSON string representation of the object
print(Scan.to_json())

# convert the object into a dict
scan_dict = scan_instance.to_dict()
# create an instance of Scan from a dict
scan_from_dict = Scan.from_dict(scan_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


