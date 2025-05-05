# ScanCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**branch** | **str** |  | 
**project_id** | **int** |  | 

## Example

```python
from linter_api_client.models.scan_create import ScanCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ScanCreate from a JSON string
scan_create_instance = ScanCreate.from_json(json)
# print the JSON string representation of the object
print(ScanCreate.to_json())

# convert the object into a dict
scan_create_dict = scan_create_instance.to_dict()
# create an instance of ScanCreate from a dict
scan_create_from_dict = ScanCreate.from_dict(scan_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


