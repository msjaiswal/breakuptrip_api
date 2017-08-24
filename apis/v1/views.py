import logging

# Create your views here.
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from django.shortcuts import render

from apis.v1.exceptions import APINotImplementedError
from apis.v1.models import Boys, Restaurants, Orders
from apis.v1.utils import Utils
from rest_framework import viewsets

logger = logging.getLogger(__name__)

def get_POST_GET(request):
  req = request.POST.dict()
  req.update(request.GET.dict() ) 
  return req

class BoysView():
    @classmethod
    @Utils.return_error_response_on_exception
    def list(cls, request):
      params = get_POST_GET(request)
      return JsonResponse({"list": list(Boys.find(params))})

    @classmethod
    @Utils.return_error_response_on_exception
    def create(cls, request):
      params = get_POST_GET(request)
      res = Boys.create(params)
      return JsonResponse(res)

    @classmethod
    @Utils.return_error_response_on_exception
    def update(cls, request):
      raise APINotImplementedError()

    @classmethod
    @Utils.return_error_response_on_exception
    def describe(cls, request):
      req = get_POST_GET(request) 
      assert "_id" in req, "_id is required"
      raise APINotImplementedError()

    @classmethod
    @Utils.return_error_response_on_exception
    def delete(cls, request):
      raise APINotImplementedError()

    @classmethod
    @Utils.return_error_response_on_exception
    def send_login_otp(cls, request):
      req = get_POST_GET(request) 
      assert "_id" in req, "_id is required"
      Boys.send_otp()

class OrdersView():
    @classmethod
    @Utils.return_error_response_on_exception
    def create(cls, request):
      req = request.POST.dict()
      print(req)
      res = Irctc.create_order(req)
      return JsonResponse(res)

    @classmethod
    @Utils.return_error_response_on_exception
    def cancel(cls, request):
      raise APINotImplementedError()

    @classmethod
    @Utils.return_error_response_on_exception
    def update(cls, request):
      raise APINotImplementedError()

    @classmethod
    @Utils.return_error_response_on_exception
    def list(cls, request):
      return JsonResponse({"list": Orders.find({})}) 

    @classmethod
    @Utils.return_error_response_on_exception
    def set_status(cls, request):
      req = get_POST_GET(request) 
      assert "order_id" in req, "order_id is required"
      assert "status" in req, "status is required"
      Orders.set_status(req['order_id'], req['status'])


class RestaurantView():
    @classmethod
    @Utils.return_error_response_on_exception
    def create(cls, request):
      req = request.POST.dict()
      print(req)
      res = Irctc.create_order(req)
      return JsonResponse(res)
      raise APINotImplementedError()

    @classmethod
    @Utils.return_error_response_on_exception
    def update(cls, request):
      raise APINotImplementedError()

    @classmethod
    @Utils.return_error_response_on_exception
    def list(cls, request):
      return JsonResponse({"list": Restaurants.find({})}) 

    @classmethod
    @Utils.return_error_response_on_exception
    def delete(cls, request):
      raise APINotImplementedError()

    @classmethod
    @Utils.return_error_response_on_exception
    def describe(cls, request):
      raise APINotImplementedError()
