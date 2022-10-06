# flake8: noqa
import ast
import os

from dotenv import load_dotenv

from .base import *

try:
    from .local import *
except ImportError:
    print('Not found local.py')

load_dotenv()

# Override config variables from environment
for var in list(locals()):
    value = os.getenv(var)
    if value is None:
        continue
    try:
        locals()[var] = ast.literal_eval(value)
    except:  # noqa
        locals()[var] = value
