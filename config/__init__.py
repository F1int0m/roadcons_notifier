# flake8: noqa
import ast
import logging
import os
import sys

from dotenv import load_dotenv

from .base import *

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s] {%(name)s} %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

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
