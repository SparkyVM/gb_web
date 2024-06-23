from fastapi import APIRouter, HTTPException
from models import Order, OrderIn
from db import database, orders
from datetime import datetime

router = APIRouter()

@router.post("/orders/")        # добавляет новый заказ.
async def add_order(new_order : OrderIn):
    query = orders.insert().values(status = new_order.status,
                                  id_user = new_order.id_user,
                                  id_item = new_order.id_item,
                                  created_at = new_order.created_at  )
    last_order_id = await database.execute(query)
    return {**new_order.dict(), "id" : last_order_id}

@router.post("/orders/{count}")        # добавляет несколько заказов.
async def add_orders(count: int):
    for i in range(1, count+1):
        query = orders.insert().values(status = 'new',
                                  id_user = 1,
                                  id_item = 1 )
        await database.execute(query)
    return {'message': f'{count} new orders create'}

@router.get("/orders/{order_id}", response_model=Order)     # возвращает заказ с указанным идентификатором.
async def show_order(order_id : int):
    query = orders.select().where(orders.c.id == order_id)
    if await database.execute(query) == -1:
        raise HTTPException(status_code=404, detail="Order not found")
    return await database.fetch_one(query)

@router.put("/orders/{order_id}")         # обновляет заказ с указанным идентификатором.
async def edit_order(order_id : int, new_order : OrderIn):
    query = orders.select().where(orders.c.id == order_id)
    if await database.execute(query) == -1:
        raise HTTPException(status_code=404, detail="Order not found")
    query = orders.update().where(orders.c.id == order_id).values(
                                  status = new_order.status,
                                  id_user = new_order.id_user,
                                  id_item = new_order.id_item,
                                  created_at = new_order.created_at )
    await database.execute(query) 
    return {**new_order.dict()}

@router.delete("/orders/{order_id}")      # удаляет заказ с указанным идентификатором.
async def delete_order(order_id : int):
    query = orders.select().where(orders.c.id == order_id)
    if await database.execute(query) == -1:
        raise HTTPException(status_code=404, detail="Order not found")
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}