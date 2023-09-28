# Python-Bark

Python-Bark aims to be a Python SDK, an extension to the [techrail/bark](https://github.com/techrail/bark) implementation


# Usage

To test out the library, perform the following steps: -

- Clone the repository
- Install the dependencies by running `pip install -r requirements.txt`
- Run the `example.py` python script.

---
To use the library in a function in your code, perform the following steps - 

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
