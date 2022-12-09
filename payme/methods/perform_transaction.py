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
            if int(transaction.state) != 2:
                order = Orders.objects.get(order_id=transaction.order_id)
                logged(f"staring to inform user_id {order.user_id} has payed", 'info')
                req_url = f"https://api.telegram.org/bot{BOT_TOKEN}/SendMessage"
                payload = {'chat_id': order.user_id,
                           'text': "Thank you for your purchase 🙂We have received your payment ✅\n"
                                   "Спасибо за покупку 🙂 Мы получили ваш платеж ✅\n"
                                   "Xaridingiz uchun tashakkur 🙂 Biz to'lovni qabul qildik ✅\n"
                           }
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }

                res = requests.post(req_url, headers=headers, data=json.dumps(payload))
                order.is_paid = True
                order.save()
                logged(f'order: {order.order_id} is_paid = true updated ')
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
