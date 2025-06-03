# ScanWithResults


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**branch** | **str** |  | 
**scan_id** | **int** |  | 
**project_id** | **int** |  | 
**status** | **str** |  | 
**started_at** | **datetime** |  | 
**finished_at** | **datetime** |  | [optional] 
**total_errors** | **int** |  | [optional] [default to 0]
**total_warnings** | **int** |  | [optional] [default to 0]
**linter_results** | [**List[LinterResult]**](LinterResult.md) |  | 

## Example

```python
from linter_api_client.models.scan_with_results import ScanWithResults

# TODO update the JSON string below
json = "{}"
# create an instance of ScanWithResults from a JSON string
scan_with_results_instance = ScanWithResults.from_json(json)
# print the JSON string representation of the object
print(ScanWithResults.to_json())

# convert the object into a dict
scan_with_results_dict = scan_with_results_instance.to_dict()
# create an instance of ScanWithResults from a dict
scan_with_results_from_dict = ScanWithResults.from_dict(scan_with_results_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


