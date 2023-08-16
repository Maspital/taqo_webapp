## Adding a new module

The process of adding a new module is slightly technical, but still straightforward.
The following guide will walk through all necessary and optional steps.

You will create a class containing some variables and a function that processes data in whatever
way you desire. TAQO will then pick up that information, build the UI for that module and
connect everything.

You can find a complete example at the bottom of this document or by simply having a look at
already existing module.



### 1) Locate module directory and create new file
Module information is stored in `<repo_root>/taqo_webapp/modules/`.
Simply create a new python file there, which you can name whatever you want as long as it ends
with `.py` and does not conflict with other files in the same directory.


### 2) Create a new class and add module information
In this new Python file, create a new class, which you can also name whatever you like.
Next, you need to add a `title`, a `description` as well as a list of `required_fields` that
must be present in each alert in order for them to be processed by your module. Use dot
notation for nested fields.
```python
class MyModule:
    title = "My Fancy Module"
    description = """
        This module is indeed very fancy and neat.
        You can write a lot of stuff here.
        """
    
    required_fields = [
        "@timestamp",
        "nested.field",
    ]

    ...
```


### 3) [Optional] Add parameters
If your module takes additional arguments apart from just the data, you can define them here.
Create a dictionary `custom_params`, wherein each key will define a parameter. Each parameter
defined in this way will then cause TAQO to generate a UI element which can be used to
easily set that parameter within the webapp.
```python
class MyModule:
    ...
    custom_params = {
            "Param Name": {
                # settings
            },
            "Another Param Name": {
                # settings
            }
    }
```
For a detailed explanation of all available parameters (number, range, string and JSON), take a look at
the [respective documentation](module_parameters.md).


### 4) Add processing function
Lastly, add a static function `process_data(data, params)` that actually does something with your data.
This is the function that will be called by TAQO, which provides the chosen data and
parameters, and it must return the processed data:
- `data` will be dictionary of the following form
    ```python
    {
        "events": [
            # a list of dicts, each representing one alert
        ],
    }
    ```
    This structure must remain, but you may of course add new keys (top-level or nested) or modify
    values.
- `params` will contain the values for any defined parameters (as described in (3)) for this
module as a dict.

So, the function could look like this:
```python
class MyModule:
    ...
    @staticmethod
    def process_data(data, params):
        # You can of course also just use the parameters directly.
        # The key must match the name used in the parameter definition
        param = params["Param Name"]
        another_param = params["Another Param Name"]

        # function that you imported from somewhere
        data = custom_alert_checker(data, param, another_param)

        return data
```


## Full Example
```python
from my_library import do_something

class MyModule:
    title = "My Fancy Module"
    description = """
        This module is indeed very fancy and neat.
        You can write a lot of stuff here.
        """
    
    required_fields = [
        "@timestamp",
        "nested.field",
    ]

    custom_params = {
        "Some Variable": {
            "type": "SINGLE_NUMBER",
            "default": 20,
            "min": 10,
            "max": 50,
            "step": 5,
        },
        "Another Variable": {
            "type": "RANGE",
            "default": [40, 50],
            "min": 20,
            "max": 150,
            "step": 0.5,
            "minRange": 10,
            "maxRange": 50,
        },
    }

    @staticmethod
    def process_data(data, params):
        data = do_something(data, params["Some Variable"], params["Another Variable"])

        return data
```