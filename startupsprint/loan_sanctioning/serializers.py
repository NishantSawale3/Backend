from rest_framework import serializers
from .models import Loan
from .utils import generate_pdf, calculate_installment

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

    def create(self, validated_data):
        # Calculate derived fields based on incoming data
        loan_principal_amount = validated_data.get('loan_principal_amount')
        loan_tenure = validated_data.get('loan_tenure')
        interest_rate = validated_data.get('interest_rate')

        # Generate additional fields
        total_amount_and_processing_fees, emi, naturity_date = calculate_installment(float(loan_principal_amount), float(interest_rate), float(loan_tenure))
        
        first_name = validated_data.get('application').user.first_name
        last_name = validated_data.get('application').user.last_name
        application_number = validated_data.get('application').id
        application_id = validated_data.get('application').id

        # Generate the PDF
        filename = generate_pdf(application_id, loan_principal_amount, interest_rate, loan_tenure, first_name, last_name, application_number)

        # Create the Loan instance
        loan = Loan.objects.create(
            loan_principal_amount=loan_principal_amount,
            loan_tenure=loan_tenure,
            interest_rate=interest_rate,
            total_amount_and_processing_fees=total_amount_and_processing_fees,
            installment=emi,
            naturity_date=naturity_date,
            sanction_letter= filename,
            application=validated_data.get('application')
        )
        # Update the application status
        application = loan.application
        application.status = 'sanctioned'
        application.save()

        return loan, filename
