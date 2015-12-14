# coding: utf-8

import datetime

from flask import json
from flask import request

from admin import admin
from common import render
from common.money import int_money

from models import Order
from models.order.refund import Refund

from models.order.order_service import cancel_order
from models.order.order_service import refund_order
from models.order.order_service import CANCEL_REASON_ADMIN

from api.payment import charge


def classified_count():
    orders = Order.select()
    total_count = orders.count()
    paid_count = orders.where(Order.status == Order.PAID, Order.canceled == False).count()
    confirmed_count = orders.where(Order.status == Order.CONFIRMED, Order.canceled == False).count()
    delivering_count = orders.where(Order.status == Order.IN_DELIVERY, Order.canceled == False).count()
    delivered_count = orders.where(Order.status == Order.DELIVERED, Order.canceled == False).count()
    canceled_count = orders.where(Order.canceled == True).count()

    return {'total': total_count,
            'paid': paid_count,
            'confirmed': confirmed_count,
            'delivering': delivering_count,
            'delivered': delivered_count,
            'canceled': canceled_count
            }


@admin.route('/orders', methods=['GET'])
def orders_index():
    type = request.args.get('type', None)
    page = int(request.args.get('page', 0))
    count = abs(int(request.args.get('count', 0)))
    offset = count * (page - 1)
    if offset < 0:
        offset = 0

    orders = Order.select().order_by(Order.id.desc())
    if (type == 'paid'):
        orders = orders.where(Order.status == Order.PAID, Order.canceled == False)
    elif (type == 'confirmed'):
        orders = orders.where(Order.status == Order.CONFIRMED, Order.canceled == False)
    elif (type == 'delivering'):
        orders = orders.where(Order.status == Order.IN_DELIVERY, Order.canceled == False)
    elif (type == 'delivered'):
        orders = orders.where(Order.status == Order.DELIVERED, Order.canceled == False)
    elif (type == 'canceled'):
        orders = orders.where(Order.canceled == True)

    total_count = orders.count()

    if (type != 'confirmed'):
        orders = orders.limit(count).offset(offset)

    result = []
    for o in orders:
        result.append(o.details())

    return render.ok({'orders': result, 'total': total_count, 'classfied': classified_count()})

@admin.route('/orders/days', methods=['GET'])
def orders_of_days():
    #    data = json.loads(request.data or '{}')
    #    if data is None:
    #        return render.error("Nothing input")
    #    if 'days' not in data:
    #        return render.error("Invalid format")

#    duration = abs(int(data.get('days', 0)))

    duration = abs(int(request.args.get('days', 0)))

#    orders = Order.select().where(Order.status >= Order.PAID, Order.canceled == False, (datetime.datetime.now()  - Order.create_time).days == duration)

    today = datetime.date.today()
    now = datetime.datetime.now()
    today_zero_time = datetime.datetime(now.year,now.month,now.day,0,0,0)
    #datetime.datetime.strftime(today, '%Y-%m-%d %H:%M:%S')

    orders = Order.select().where(Order.status >= Order.PAID, Order.canceled == False, Order.create_time>= (today_zero_time-datetime.timedelta(days = duration)) )

    re = []
    for n in range(0,duration):
        if duration == 0:
            duration_orders = orders
        else:
            duration_orders = orders.where( Order.create_time>= (today_zero_time-datetime.timedelta(days = n)), Order.create_time < (today_zero_time-datetime.timedelta(days = n-1)) )
        if duration_orders is None:
            continue

        count = duration_orders.count()

        total_price = 0
        for o in duration_orders:
            total_price += o.cash_amount

#total_price = sum(duration_orders.items.cash_amount)
        result = {}
        result['date'] = today-datetime.timedelta(days = n)
        result['count'] = count
        result['total_price'] = total_price
        re.append(result)

    return render.ok(re)


@admin.route('/orders/<int:order_id>', methods=['GET'])
def order_show(order_id):
    order = Order.find_by_id(order_id)
    return render.ok(order.details())


@admin.route('/orders/<int:order_id>/confirm', methods=['GET'])
def order_confirm_by_admin(order_id):
    order = Order.find_by_id(order_id)
    if not order:
        return render.not_found()
    order.confirm()

    return render.ok('CONFIRMED')


@admin.route('/orders/<int:order_id>/cancel', methods=['POST'])
def order_cancel_by_admin(order_id):
    order = Order.find_by_id(order_id)

    if not order:
        return render.not_found()

    reason = json.loads(request.data).get('reason', CANCEL_REASON_ADMIN)
    cancel_order(order, charge, reason)

    return render.ok()


@admin.route('/orders/<int:order_id>/refund', methods=['POST'])
def order_refund_by_admin(order_id):
    order = Order.find_by_id(order_id)

    if not order:
        return render.not_found()

    reason = json.loads(request.data).get('reason', CANCEL_REASON_ADMIN)
    refund_money = json.loads(request.data).get('money')

    if refund_money is None:
        return render.error('missing argument: money')

    refund_money = int_money(refund_money)
    if refund_money == 0:
        return render.error('Refund money can not be 0')

    remained_money = order.cash_amount - Refund.order_refund_total(order.id)
    if refund_money > remained_money:
        return render.error('not enough money to refund')

    # refund
    if not refund_order(order, refund_money, reason, [], charge):
        return render.error('refund error')

    return render.ok('refund successfully')


@admin.route('/orders/<int:order_id>/deliver', methods=['GET'])
def order_start_deliver(order_id):
    order = Order.find_by_id(order_id)
    if not order:
        return render.not_found()
    try:
        order.depart()
    except:
        return render.error("not able to depart")
    return render.ok('IN_DELIVERY')


@admin.route('/orders/<int:order_id>/express_delivery', methods=['POST'])
def order_receive_express(order_id):
    order = Order.find_by_id(order_id)
    if not order:
        return render.not_found()
    # code = json.loads(request.data).get('code', None)

    # TODO: when need authorize order.code, change it.
    # if code == order.code:
    if True:
        order.delivered()
        return render.ok('DELIVERED')
    else:
        return render.error('wrong code')
