import logging
import os
import sys
import traceback
from functools import wraps

from django.http import JsonResponse
from apis.v1.exceptions import APINotImplementedError
from pymongo import MongoClient 
from pymongo import ReturnDocument

from collections import defaultdict 

logger = logging.getLogger(__name__)

class MongoUtils:
  __mongoclients = defaultdict(lambda: None)
  @classmethod
  def create(cls, host='localhost'):
    if not cls.__mongoclients[host]:
      cls.__mongoclients[host] = MongoClient(host)
    return cls.__mongoclients[host]
    


class Utils:

  def return_error_response_on_exception(func):
    """decorator to catch any exception and kill the process"""
    @wraps(func)
    def wrapper(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      except APINotImplementedError as e:
        logger.exception("exception")
        return JsonResponse(
          {
            "status": "failure", 
            "reason": "This api is not implemented yet."
          }, safe=False)
      except Exception as e:
        logger.exception("exception")
        print(traceback.format_exc())
        print("Fatal Exception.")
        response = {
          "status": "ERROR",
          "message": str(e),
          "exception_traceback": traceback.format_exc(),
        }
        return JsonResponse(response, safe=False)
    return wrapper

  def get_next_id(field):
    client = MongoUtils.create()
    counters = client['trapigo']['counters']
    assert field in ['restaurants', 'orders', 'boys']

    obj = counters.find_one_and_update({},{"$inc": {field :1} }, return_document=ReturnDocument.AFTER)
    return obj[field]


