from payme.models import MerchatTransactionsModel


class GetStatement:
    def __call__(self, params: dict):
        """select * from payme_merchattransactionmodel where created_at_ms"""
        time_from = params['from']
        time_to = params['to']
        tranactions = MerchatTransactionsModel.objects.filter(perform_time__range=(time_from, time_to)).values()
        trans = []
        if tranactions.count() == 0:
            return {"result": {"transactions": []}}
        for row in tranactions:
            res = {
                'id': row['_id'],
                'time': row['time'],
                'amount': row['amount'],
                'account': {
                    'order_id': row['order_id']
                },
                'creat_time': int(row['created_at'].timestamp()*1000),
                'perform_time': row['perform_time'],
                'cancel_time': row['cancel_time'],
                "transaction": "",
                "state": row['state'],
                "reason": row['reason']
            }
            trans.append(res)

        return {
            "result": {
                "transactions": trans
            }
        }
