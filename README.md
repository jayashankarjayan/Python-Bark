# Python-Bark

Python-Bark aims to be a Python SDK, an extension to the [techrail/bark](https://github.com/techrail/bark) implementation


# Usage

To test out the library, perform the following steps: -

- Set up [techrail/bark](https://github.com/techrail/bark) server.
- Clone the repository
- Install the dependencies by running `pip install -r requirements.txt`
- Run the `example_bulk_insert.py` python script.

---

### Use as a decorator
To use the `bark` decorator in a function in your code, perform the following steps - 

- Add the `BarkHandler` to your `logger` object
- Add the `bark` decorator to your custom functions and provide it with the `logger` object created by you.


For example, in the below code snippets,

```
bark_handler = BarkHandler()
logger.addHandler(bark_handler)
```

- The `BarkHandler` has been added to an existing `logger` object
- The `bark` decorator has been added to a function `my_func`. 

This ensures that the `Python-Bark` module works along with the existing `logger` implementation seamlessly.

```
@bark(logger)
def my_func(a: int, b: int):
    logger.info("INFO  Log", extra={"Metadata": "A"})
    logger.warning("DEBUG  Log", extra={"Metadata": "B"})
    return "Hello World"
```

### Use as a standard logger object

To use the [techrail/bark](https://github.com/techrail/bark) functionality similar to a standard logger object, perform the following steps - 
- Import the `Bark` logger object and assing it to a variable
- Use the variable to perform logging actions.

Example: 

```
from bark import Bark

logger = Bark(__name__)
logger.info("This is a info log")
```

For more examples, refer to `example_single_insert.py` file.

### Configuration
In order to change the values for host and port of the [techrail/bark](https://github.com/techrail/bark) server implement the following configurations in your code


```
from bark.configs import config
config.url = "http://example.com"
config.port = 8000

```