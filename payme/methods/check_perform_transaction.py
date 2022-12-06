from payme.utils.get_params import get_params

from payme.serializers import MerchatTransactionsModelSerializer
from payme.models import Orders


class CheckPerformTransaction:
    def __call__(self, params: dict) -> dict:
        clean_params = get_params(params)
        serializer = MerchatTransactionsModelSerializer(
            data=clean_params
        )
        serializer.is_valid(raise_exception=True)

        order_details = Orders.objects.filter(order_id=clean_params.get('order_id'))
        details: dict = {
            'receipt_type': 0,
            "items": []
        }
        for row in order_details:
            details['items'].append(
                {
                    'title': f"{row.event} {row.menu_type} {row.menu_id}",
                    'price': row.price * 100,
                    "count": row.quantity,
                    'code': '02199006016000000',
                    'package_code': '111',
                    'vat_percent': 15
                }
            )

        response = {
            "result": {
                "allow": True,
                'detail': details
            }
        }

        return response
