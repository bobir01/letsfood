import base64
import binascii

from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from payme.errors.exceptions import MethodNotFound
from payme.errors.exceptions import PerformTransactionDoesNotExist
from payme.errors.exceptions import PermissionDenied
from payme.methods.cancel_transaction import CancelTransaction
from payme.methods.check_perform_transaction import CheckPerformTransaction
from payme.methods.check_transaction import CheckTransaction
from payme.methods.create_transaction import CreateTransaction
from payme.methods.generate_link import GeneratePayLink
from payme.methods.get_statement import GetStatement
from payme.methods.perform_transaction import PerformTransaction
from payme.serializers import MerchatTransactionsModelSerializer
from payme.utils.logger import logged


class MerchantAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        logged(request.query_params, 'info')
        print(request.query_params.get('amount'))
        clean_query = {'amount': int(request.query_params.get('amount')) * 100,
                       'order_id': int(request.query_params.get('order_id')),
                       'user_id': int(request.query_params.get('user_id'))}
        MerchatTransactionsModelSerializer().validate(clean_query)
        link_generator = GeneratePayLink(amount=clean_query.get('amount'), order_id=clean_query.get('order_id'))

        return Response({'url': link_generator.generate_link(clean_query.get('user_id'))})

    def post(self, request, *args, **kwargs):
        password = request.META.get('HTTP_AUTHORIZATION')
        if self.authorize(password):
            incoming_data: dict = request.data
            incoming_method: str = incoming_data.get("method")
            logged_message: str = "Incoming {data}"

            logged(
                logged_message=logged_message.format(
                    method=incoming_method,
                    data=incoming_data
                ),
                logged_type="info"
            )
            try:
                paycom_method = self.get_paycom_method_by_name(
                    incoming_method=incoming_method
                )
            except ValidationError:
                raise MethodNotFound()
            except PerformTransactionDoesNotExist:
                raise PerformTransactionDoesNotExist()

            paycom_method = paycom_method(incoming_data.get("params"))

        return Response(data=paycom_method)

    @staticmethod
    def get_paycom_method_by_name(incoming_method: str) -> object:
        """
        Use this static method to get the paycom method by name.
        :param incoming_method: string -> incoming method name
        """
        available_methods: dict = {
            "CheckTransaction": CheckTransaction,
            "CreateTransaction": CreateTransaction,
            "CancelTransaction": CancelTransaction,
            "PerformTransaction": PerformTransaction,
            "CheckPerformTransaction": CheckPerformTransaction,
            'GetStatement': GetStatement,
        }

        try:
            MerchantMethod = available_methods[incoming_method]
        except Exception:
            error_message = "Unavailable method: %s" % incoming_method
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise MethodNotFound(error_message=error_message)

        merchant_method = MerchantMethod()

        return merchant_method

    @staticmethod
    def authorize(password: str) -> bool:
        """
        Authorize the Merchant.
        :param password: string -> Merchant authorization password
        """
        is_payme: bool = False
        error_message: str = ""

        if not isinstance(password, str):
            error_message = "Request from an unauthorized source!"
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise PermissionDenied(error_message=error_message)

        password = password.split()[-1]

        try:
            password = base64.b64decode(password).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            error_message = "Error when authorize request to merchant!"
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise PermissionDenied(error_message=error_message)

        merchant_key = password.split(':')[-1]

        if merchant_key == settings.PAYME.get('PAYME_KEY'):
            is_payme = True

        if merchant_key != settings.PAYME.get('PAYME_KEY'):
            logged(
                logged_message=f"Invalid key in request!-{merchant_key}",
                logged_type="error"
            )

        if is_payme is False:
            raise PermissionDenied(
                error_message="Unavailable data for unauthorized users!"
            )

        return is_payme


class SuccessNotifier(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        logged("get request for success", 'info')
        logged(request.query_params)
        logged(request.META, 'info')
        return Response({'is_working': 'fine'})
