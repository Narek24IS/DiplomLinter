# LinterStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**linter_name** | **str** |  | 
**total_runs** | **int** |  | 
**success_rate** | **float** |  | 

## Example

```python
from linter_api_client.models.linter_stats import LinterStats

# TODO update the JSON string below
json = "{}"
# create an instance of LinterStats from a JSON string
linter_stats_instance = LinterStats.from_json(json)
# print the JSON string representation of the object
print(LinterStats.to_json())

# convert the object into a dict
linter_stats_dict = linter_stats_instance.to_dict()
# create an instance of LinterStats from a dict
linter_stats_from_dict = LinterStats.from_dict(linter_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


