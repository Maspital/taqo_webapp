## Available module parameters

You can define different types of parameters, which will define how that parameter can be set,
what it feeds to your pipeline, and also provide a number of settings for each type. 
Available types are explained below.

The key value will serve as the name of that parameter, both when rendering the UI element
and when using it within the module.


- `SINGLE_NUMBER`: This will generate a **slider** which outputs a **single value**.
    ```python
    "Num Param": {
        "type": "SINGLE_NUMBER",
        "default": 20,  # starting value
        "min": 10,      # minimum value on slider
        "max": 50,      # maximum value on slider
        "step": 5,      # [optional] slider step size, defaults to 1
    }
    ```
  

- `RANGE`: This will generate a **range slider** which outputs a **list containing two values**,
    the start and end of a range.
    ```python
    "Range Param": {
        "type": "RANGE",
        "default": [40, 50],    # starting values
        "min": 20,              # minimum value on slider
        "max": 150,             # maximum value on slider
        "step": 0.5,            # [optional] slider step size, defaults to 1
        "minRange": 10,         # [optional] minimum settable range, defaults to 0
        "maxRange": 50,         # [optional] maximum settable range, defaults to `max`
    }
    ```


- `STRING`: This will generate a **text input field** which outputs a **string**.
    This string will be matched against a regex, only passing desired values through.
    ```python
    "String Param": {
        "type": "STRING",
        "default": "EXAMPLE",                   # default string
        "description": "String filtered by",    # short description above input field
        "regex": r"^[A-Z]+$",                   # regex that input will be matched against, non-matching input will not be used
        "error_msg": "Uppercase only!",         # error message to be displayed when regex doesn't match
  }
    ```
  

- `JSON`: This will generate a **text input field** which outputs a **dict**.
    The input is automatically checked for correct syntax.
    The default must be submitted as a string, and must not contain `'` because dash Mantine is weird.
    ```python
    "JSON Param": {
        "type": "JSON",
        "default": str({"cool": "beans"}).replace("'", "\""),   # default json as a string, without '
        "error_msg": "Incorrect syntax",                        # [optional] error message to be displayed on incorrect syntax
        "placeholder": "Put something here",                    # [optional] message when the input field is empty
    }
    ```


- `RADIO`: This will generate a **set of radio buttons** which output a **string**,
    the currently selected button.
    ```python
    "Radio Param": {
        "type": "RADIO",
        "default": "value1",                                    # default selected value
        "options": {"value1": "label1", "value2": "label2"},    # all (at least 1) possible options (and their labels)
    }
    ```


- `CHECKLIST`: This will generate a **set of checklist elements** which outputs a **list of strings**,
    containing all currently selected elements.
    ```python
    "Checklist Param": {
        "type": "CHECKLIST",
        "default": ["value1"],                                  # list of default selected values, can be empty
        "options": {"value1": "label1", "value2": "label2"},    # all (at least 1) possible options (and their labels)
    }
    ```
