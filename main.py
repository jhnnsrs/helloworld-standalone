from arkitekt_next import register, easy
from mikro_next.api.schema import Image, from_array_like
import time
from typing import Generator
import numpy as np

# You can register your functions by using the @register decorator
# functions always run in a threadpool and are not blocking 
# all functions must be registered before the run function is called


@register
def generate_n_string(n: int = 10, timeout: int = 2) -> Generator[str, None, None]:
    """Generate N Strings

    This function generates {{n}} strings with a {{timeout}} ms timeout between each string


    Parameters
    ----------
    n : int, optional
        The number of iterations, by default 10
    timeout : int, optional
        The timeout, by default 2

    Returns
    -------
    str
        A string with Hello {n}
    """
    for i in range(n):
        print(i)
        time.sleep(timeout)
        yield f"Hello {i}"

# Typehints are used to generate the schema for the function
# you cannot omit the typehints, Image is a custom type that is used to represent images
# that are stored on the mikro-next server
# If you omit documentation, function names will be infered from the function name

@register
def upload_image(image_name: str) -> Image:
    return from_array_like(np.random.rand(100, 100, 3) * 255, name=image_name)



# 
@register
def print_string(input: str) -> str:
    """Print String

    This function prints the input string to
    the console

    Parameters
    ----------
    input : str
        The input string

     Returns
    -------
    str
        The printed string
    """
    print(input)
    return input



# This is the part that runs the server
# Everything must be registered before this function is called


# The easy function is a context manager as it will need to clean
# up the resources it uses when the context is exited (when the user stops the app)
# make sure to give your app a name, (and the url/ip of the arkitekt server) 
with easy("YOUR_APP_NAME", url="THE_ARKTIEKT_SERVER_IP") as e:

    # If you want to perform a request to the server before enabling the
    # provisioning loop you can do that within the context

    # from_array_like(np.random.rand(100, 100, 3) * 255, name="test")
    # would upload an image to the server on app start

    # e.run() will start the provisioning loop of this app
    # this will block the thread and keep the app running until the user
    # stops the app (keyboard interrupt)
    e.run()