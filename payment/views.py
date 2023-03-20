from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import mercadopago
import json


class ProcessPaymentAPIView(APIView):
    def post(self, request):
        request_values = json.loads(request.body)
        payment_data = {
            "transaction_amount": float(request_values["transaction_amount"]),
            "token": request_values["token"],
            "installments": int(request_values["installments"]),
            "payment_method_id": request_values["payment_method_id"],
            "issuer_id": request_values["issuer_id"],
            "payer": {
                "email": request_values["payer"]["email"],
                "identification": {
                    "type": request_values["payer"]["identification"]["type"],
                    "number": request_values["payer"]["identification"]["number"],
                },
            },
        }

        sdk = mercadopago.SDK(settings.YOUR_ACCESS_TOKEN)
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        status = {
            "id=": payment["id"],
            "status": payment["status"],
            "status_detail": payment["status_detail"],
        }
        return Response(data=status, status=201)