import datetime
import json
import time

import requests
from django.conf import settings

from payme.models import MerchatTransactionsModel, Orders
from payme.serializers import MerchatTransactionsModelSerializer
from payme.utils.get_params import get_params
from payme.utils.logger import logged

BOT_TOKEN = settings.PAYME.get('BOT_TOKEN')


class PerformTransaction:
    def __call__(self, params: dict) -> dict:
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        clean_data: dict = serializer.validated_data
        response: dict = None
        try:
            logged_message = "started check trx in db(perform_transaction)"
            transaction = \
                MerchatTransactionsModel.objects.get(
                    _id=clean_data.get("_id"),
                )
            logged(
                logged_message=logged_message,
                logged_type="info",
            )
            logged(transaction, 'info')
            if int(transaction.state) != 2:  # work only when first transaction is coming
                order = Orders.objects.filter(order_id=transaction.order_id).values()
                logged(f"staring to inform user_id {order.first().get('user_id')} has payed", 'info')
                req_url = f"https://api.telegram.org/bot{BOT_TOKEN}/SendMessage"
                payload = {'chat_id': order.first().get('user_id'),
                           'text': "Thank you for your purchase 🙂We have received your payment ✅\n"
                                   "Спасибо за покупку 🙂 Мы получили ваш платеж ✅\n"
                                   "Xaridingiz uchun tashakkur 🙂 Biz to'lovni qabul qildik ✅\n"

                           }
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                order_txt = "<b> Номер заказа № {0} ☑️\n</b>".format(order.first().get('order_id'))
                total = 0
                for i, record in enumerate(order.values(), start=1):
                    if record['menu_type'] == 'full':

                        order_txt += f"{i}. " + " Сет " + " menu № " + str(record['menu_id']) + '\n'
                    else:
                        order_txt += f"{i}. " + " Полсет  " + " menu № " + str(record['menu_id']) + '\n'
                    if record['event'] == 'lunch':
                        order_txt += " на обед \n"
                        total += record['price'] * record['quantity']
                        order_txt += f"{record['price']:,} * {record['quantity']:,} = {(record['price'] * record['quantity']):,}\n "
                    else:
                        order_txt += " на ужин \n"
                        total += record['price'] * record['quantity']
                        order_txt += f"{record['price']:,} * {record['quantity']:,} = {(record['price'] * record['quantity']):,}\n "

                order_txt += " Итого: {0:,} \n".format(total)

                order_txt += "\n\n"
                order_data = order.first()
                order_txt += "🛂Клиент: " + order_data['full_name'] + '\n'
                order_txt += "\nPhone: " + " <code> " + order_data['phone'] + "</code>\n"

                order_txt += f"<a href='https://www.google.com/maps/search/?api=1&query={order_data['address_lat']},{order_data['address_lon']}'>"  #
                order_txt += "📍Address</a>\n"
                if order_data['comment']:
                    order_txt += "Comment:" + order_data['comment'] + "\n"

                payload_group = {
                    "chat_id": settings.PAYME.get("GROUP_ID"),
                    'text': order_txt,
                    'parse_mode': 'HTML'
                }

                res = requests.post(req_url, headers=headers, data=json.dumps(payload))
                requests.post(req_url, headers=headers, data=json.dumps(payload_group))
                order.values().update(is_paid=True, order_time=datetime.datetime.now())

                logged(f"order: {order.first().get('user_id')} is_paid = true updated ")
                logged(res.json(), 'info')

            transaction.state = 2
            if transaction.perform_time == 0:
                transaction.perform_time = int(time.time() * 1000)

            transaction.save()
            response: dict = {
                "result": {
                    "perform_time": int(transaction.perform_time),
                    "transaction": transaction.transaction_id,
                    "state": int(transaction.state),
                }
            }



        except Exception as e:
            logged_message = "error during get transaction in db {}{}"
            logged(
                logged_message=logged_message.format(e, clean_data.get("id")),
                logged_type="error",
            )

        return response
