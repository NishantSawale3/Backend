from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics

from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Loan, Transaction
from .serializers import LoanSerializer, PaymentGatewaySerializer, TransactionSerializer

import razorpay
import json


class LoanAPI(APIView):

    def get(self, request, pk):
        obj = get_object_or_404(Loan, pk=pk)
        serializer = LoanSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PaymentGateway(APIView):

    def post(self, request):
        client = razorpay.Client(auth=(settings.RAZORAPI_SECRET_KEY_ID, settings.RAZORAPI_SECRET_KEY))

        serializer = PaymentGatewaySerializer(data=request.data)
        if serializer.is_valid():
            data = client.order.create({
                'amount': int(serializer.validated_data['amount']),
                'currency': 'INR',
                'receipt': request.data.get('order_id'),
                'partial_payment': False,
            })
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=400)

# ############################################################################################

@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    # name = request.data['name']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(settings.RAZORAPI_SECRET_KEY_ID, settings.RAZORAPI_SECRET_KEY))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
    
    # serializer = PaymentGatewaySerializer()

    data= {'payment': payment}
    return Response(data=data)



@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

    print('RESPONSE FROM FRONTEND', res)

    """res will be: 
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        if key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Transaction.objects.get(id=ord_id)

    # get order by payment_id which we've created earlier with isPaid=False
    client = razorpay.Client(auth=(settings.RAZORAPI_SECRET_KEY_ID, settings.RAZORAPI_SECRET_KEY))

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(settings.RAZORAPI_SECRET_KEY_ID, settings.RAZORAPI_SECRET_KEY))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)

#############################################################################################################

class TransactionListCreate(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request):
        serilaizer = TransactionSerializer(data=request.data)
        if serilaizer.is_valid():
                client = razorpay.Client(auth=(settings.RAZORAPI_SECRET_KEY_ID, settings.RAZORAPI_SECRET_KEY))

                payment = client.order.create({"amount": int(serilaizer.validated_data.get('amount_inr')) * 100, 
                                            "currency": "INR", 
                                            "payment_capture": "1"})
                serilaizer.save()
                data={
                    'payment': payment,
                    'transaction': serilaizer.data
                }
                return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)
    