import random
import arrow

from django.db import models
from .utils import Utils, MongoUtils
from .smsutils import SMSUtils
from pymongo import MongoClient

db = MongoUtils.create()['trapigo']

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    testvar = None


class Boys():
  __table = MongoUtils.create()['trapigo']['boys']

  @classmethod
  def get(cls, _id):
    return __table.find_one({"_id": _id})

  @classmethod
  def create(cls, details):
    assert details, "boys details cant be empty"
    _id = Utils.get_next_id('boys') 
    details.update({"_id": _id})
    resp = cls.__table.insert_one(details)
    return {"status": "success", "order_id": _id}

  @classmethod
  def update(cls, _id, details):
    assert details.get("_id", _id) == _id
    return __table.insert_one({"_id": _id}, upsert=True)
    
  @classmethod
  def find(cls, options=None):
    if options is None:
      options = {}
    return list(cls.__table.find(options))

  @classmethod
  def send_otp(cls, _id):
    boy = cls.__table.find_one({"_id": _id})
    assert boy
    phone = boy['phone']
    otp = boy.get("otp")
    otp_expiry = boy.get("otp_expiry")

    send_old_otp = True
    try:
      assert otp 
      assert otp_expiry
      assert isinstance(otp_expiry, datetime.datetime)
      assert (otp_expiry - arrow.now()).total_seconds() > 0 
    except:
      send_old_otp = False

    if not send_old_otp: 
      otp = random.randint(1000,9999) 
      otp_expiry = arrow.now().replace(hours=+1).datetime
      cls.__table.update({"_id": _id}, {"$set": {"otp": otp, "otp_expiry": otp_expiry}})
    
    
    msg = f"Your OTP is {otp}. Please use this to login into the app."
    SMSUtils.send_sms(phone, msg, campaign='OTP')

  @classmethod
  def check_otp(cls, _id, otp):
    order = cls.__table.find_one({"_id": _id})
    assert order
    if otp != order['otp']:
      return False
    return True

#  @classmethod
#  def set_status(cls, _id, status):
#    assert status in cls.available_status
#    order = cls.__table.find_one({"_id": _id})
#    assert order, f"Order with _id {_id} does not exist."
#    cls.__table.update({"_id": _id}, {"$set": {"status": status}})
#    return {"status": "success"}

class Restaurants:
  __table = MongoUtils.create()['trapigo']['restaurants']

  @classmethod
  def create(cls, restaurant):
    required_keys = set(['name', 'address', 'phone'])
    keys = set(list(order.keys()))
    missing_keys = required_keys - keys
    if missing_keys:
      return {"status": "failure", "reason": "missing keys: %s" % ", ".join(missing_keys)}
    cls.orders.insert_one(order)
    return {"status": "success"}
    
  @classmethod
  def find(cls, options=None):
    if options is None:
      options = {}
    return list(cls.__table.find(options))

#order = 
#{
#  '_id' # Order ID 
#  'passenger': {
#    'phone'
#    'pnr'
#
#  }
#}
class Orders:
  __table = MongoUtils.create()['trapigo']['orders']
  available_status = ['AWAITING_CONFIRMATION', 'CONFIRMED', 'UNDER_PREPARATION', 'PICKED_UP_FROM_HOTEL', 'DELIVERED_TO_HUB', 'PICKED_UP_FOR_DELIVERY', 'DELIVERED_TO_CUSTOMER', 'CANCELLED']
  
  @classmethod
  def create(cls, order):
    
    required_keys = set(['name', 'address', 'phone'])
    keys = set(list(order.keys()))
    missing_keys = required_keys - keys
    if missing_keys:
      return {"status": "failure", "reason": "missing keys: %s" % ", ".join(missing_keys)}
    cls.orders.insert_one(order)
    return {"status": "success"}


  @classmethod
  def find(cls, options=None):
    if options is None:
      options = {}
    return list(cls.__table.find(options))


  @classmethod
  def set_status(cls, order_id, status):
    assert status in cls.available_status
    order = cls.__table.find_one({"_id": order_id})
    assert order, f"Order with order_id {order_id} does not exist."
    cls.__table.update({"_id": order_id}, {"$set": {"status": status}})
    return {"status": "success"}

  @classmethod
  def send_verification_code(cls, order_id):
    order = cls.__table.find_one({"_id": order_id})
    assert order
    phone = order['passenger']['phone']
    verification_code = order.get("verification_code")
    if not verification_code:
      verification_code = random.randint(1000,9999) 
    cls.__table.update({"_id": order_id}, {"$set": {"verification_code": verification_code}})

    msg = f"Your Verification Code is {verification_code}. Please provide this to the delivery boy."
    SMSUtils.send_sms(phone, msg, campaign='Verification Code')

  @classmethod
  def check_verification_code(cls, order_id, verification_code):
    order = cls.__table.find_one({"_id": order_id})
    assert order
    if verification_code != order['verification_code']:
      return False
    return True

  @classmethod
  def cancel(cls, order_id):
    cls.set_status(order_id, 'CANCELLED')

class Hubs:
  __table = MongoUtils.create()['trapigo']['hubs']
  available_stations = ['NGP']
  sample =  {
    'station_code': 'NGP',
  }

  @classmethod
  def create(cls, restaurant):
    
    required_keys = set(['station_code', 'address'])
    keys = set(list(order.keys()))
    missing_keys = required_keys - keys
    if missing_keys:
      return {"status": "failure", "reason": "missing keys: %s" % ", ".join(missing_keys)}
    cls.orders.insert_one(order)
    return {"status": "success"}

  @classmethod
  def find(cls, options=None):
    if options is None:
      options = {}
    return list(cls.__table.find(options))

  
