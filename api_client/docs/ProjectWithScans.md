# ProjectWithScans


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**repository_url** | **str** |  | 
**id** | **int** |  | 
**created_at** | **datetime** |  | 
**owner_id** | **int** |  | 
**scans** | [**List[Scan]**](Scan.md) |  | 

## Example

```python
from linter_api_client.models.project_with_scans import ProjectWithScans

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectWithScans from a JSON string
project_with_scans_instance = ProjectWithScans.from_json(json)
# print the JSON string representation of the object
print(ProjectWithScans.to_json())

# convert the object into a dict
project_with_scans_dict = project_with_scans_instance.to_dict()
# create an instance of ProjectWithScans from a dict
project_with_scans_from_dict = ProjectWithScans.from_dict(project_with_scans_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


