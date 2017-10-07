import logging

# Create your views here.
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from django.shortcuts import render

from apis.v1.exceptions import APINotImplementedError
from apis.v1.models import Boys, Restaurants, Orders
from apis.v1.utils import Utils, api
from rest_framework import viewsets

logger = logging.getLogger(__name__)

def get_POST_GET(request):
    req = request.POST.dict()
    req.update(request.GET.dict() ) 
    return req

class BoysView():
    @classmethod
    @api
    def list(cls, request):
        params = get_POST_GET(request)
        return {"list": list(Boys.find(params))}

    @classmethod
    @api
    def create(cls, request):
        params = get_POST_GET(request)
        res = Boys.create(params)
        return res

    @classmethod
    @api
    def update(cls, request):
        raise APINotImplementedError()

    @classmethod
    @api
    def describe(cls, request):
        req = get_POST_GET(request) 
        assert "_id" in req, "_id is required"
        raise APINotImplementedError()

    @classmethod
    @api
    def delete(cls, request):
        raise APINotImplementedError()

    @classmethod
    @api
    def send_login_otp(cls, request):
        req = get_POST_GET(request) 
        assert "_id" in req, "_id is required"
        Boys.send_otp()

    @classmethod
    @api
    def get_launch_data(cls, request):
        req = get_POST_GET(request) 
        print("req: %s" % req)
        assert "_id" in req, "_id is required"
        ret = Boys.get_launch_data(_id=req['_id'])
        print("views returning: %s" % ret)
        return ret

class OrdersView():
    @classmethod
    @api
    def create(cls, request):
        req = request.POST.dict()
        print(req)
        res = Orders.create(req)
        return JsonResponse(res)

    @classmethod
    @api
    def cancel(cls, request):
        raise APINotImplementedError()

    @classmethod
    @api
    def update(cls, request):
        raise APINotImplementedError()

    @classmethod
    @api
    def list(cls, request):
        return JsonResponse({"list": Orders.find({})}) 

    @classmethod
    @api
    def set_status(cls, request):
        req = get_POST_GET(request) 
        assert "order_id" in req, "order_id is required"
        assert "status" in req, "status is required"
        Orders.set_status(req['order_id'], req['status'])


class RestaurantView():
    @classmethod
    @api
    def create(cls, request):
        req = request.POST.dict()
        print(req)
        res = Irctc.create_order(req)
        return JsonResponse(res)
        raise APINotImplementedError()

    @classmethod
    @api
    def update(cls, request):
        raise APINotImplementedError()

    @classmethod
    @api
    def list(cls, request):
        return JsonResponse({"list": Restaurants.find({})}) 

    @classmethod
    @api
    def delete(cls, request):
        raise APINotImplementedError()

    @classmethod
    @api
    def describe(cls, request):
        raise APINotImplementedError()
