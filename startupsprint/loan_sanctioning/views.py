from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.middleware import csrf
from .utils import send_email_with_attachment
import logging
from .serializers import LoanSerializer



success_logger = logging.getLogger('success_logger')
error_logger = logging.getLogger('error_logger')

class LoanSanctionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = LoanSerializer(data=request.data)
            if serializer.is_valid():
                loan, filename = serializer.save()
                subject = "Loan Sanctioning Letter"
                body = "Please find the attachment"
                send_email_with_attachment(subject, body, 'kundan221195@gmail.com', [loan.application.user.email], filename)
                return Response({'message': 'Loan application created successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log error
            print(e)
            error_logger.error(f"Error processing loan application: {str(e)}")
            return Response({'message': 'Error processing loan application'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






@api_view(['GET'])
def my_view(request):
    csrf_token = csrf.get_token(request)
    return Response({'csrf_token': csrf_token})
    