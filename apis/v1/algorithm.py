from .models import Orders, Boys

MAX_MEALS_PER_PICKUP_BOY = 10

class Scheduler:
  station_code = None 
  
  def __init__(self, station_code):
    self.station_code = station_code
   
  def find_unassigned_boy(self, order):
    """Returns a boy who can deliver the given order"""
    arrival = order.scheduled_arrival 
    restaurant_arrival = arrival.replace("-55 mins")


    pass

  def find_assigned_boy_who_can_deliver(self, order):
    """Returns a boy who can deliver the given order"""
    pass

  def assign_order(self, boy, order):
    pass

  def run(self, ):
    order_groups = Orders.aggregate([{"$match": {'station_code': self.station_code, "is_assigned": False }}, {"$group": {"_id": "$train_no", order_ids: {"$collect": "$order_id"}}}])
    for order_group in order_groups:
      orders = [Orders.find({"_id": _id}) for _id in order_group]
      meals = sum([order.meals for order in orders])

      while orders:
        if meals > MAX_MEALS_PER_PICKUP_BOY:
          boy = self.find_unassigned_boy()
          if boy: 
            assigned_meals = 0
            ids_assigned = []
            for orders in orders:
              if assigned_meals < MAX_MEALS_PER_PICKUP_BOY and order.meals < MAX_MEALS_PER_PICKUP_BOY - assigned_meals:
                ids_assigned.append(order._id)
                self.assign_order(boy, order)
            if not ids_assigned:
              break
            orders = [order for order in orders if order._id not in ids_assigned]
          else:
            break

      for order in orders:
        boy = self.find_assigned_boy_who_can_deliver(order, boy)
        if boy: 
          self.assign_order(boy, order)
        else:
          break

      print("Cannot deliver these orders: %s" % orders)

