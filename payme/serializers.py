from django.conf import settings

from django.db.models import F, Sum
from rest_framework import serializers
from payme.models import Orders
from payme.models import MerchatTransactionsModel
from payme.errors.exceptions import IncorrectAmount
from payme.errors.exceptions import PerformTransactionDoesNotExist


class MerchatTransactionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model: MerchatTransactionsModel = MerchatTransactionsModel
        fields: str = "__all__"

    def validate(self, data):
        """
        Validate the data given to the MerchatTransactionsModel.
        """
        if data.get("order_id") is not None:
            try:

                total_amount = Orders.objects.filter(order_id=data.get('order_id')).annotate(
                    sum_amount=F('price') * F('quantity')).aggregate(Sum('sum_amount'))['sum_amount__sum']
                if total_amount != int(data['amount']):
                    raise IncorrectAmount()

            except IncorrectAmount:
                raise IncorrectAmount()

        return data

    def validate_amount(self, amount) -> int:
        """
        Validator for Transactions Amount
        """
        if amount is not None:
            if int(amount) < settings.PAYME.get("PAYME_MIN_AMOUNT"):
                raise IncorrectAmount()

        return amount

    def validate_order_id(self, order_id) -> int:
        """
        Use this method to check if a transaction is allowed to be executed.
        :param order_id: string -> Order Indentation.
        """
        try:
            if Orders.objects.filter(order_id=order_id).exists() is False:
                raise PerformTransactionDoesNotExist()
        except Orders.DoesNotExist:
            raise PerformTransactionDoesNotExist()

        return order_id
