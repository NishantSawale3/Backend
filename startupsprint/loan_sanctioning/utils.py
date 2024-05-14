from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime , timedelta
import logging
from django.core.mail import EmailMessage


success_logger = logging.getLogger('success_logger')
error_logger = logging.getLogger('error_logger')

def generate_pdf(application_id, loan_principal_amount, interest_rate, loan_tenure, first_name,last_name,                application_number)  :
    total_amount_and_processing_fees, emi, naturity_date = calculate_installment(loan_principal_amount, interest_rate, loan_tenure)
    try: 
        filename = f"loan_sanction_letter_{application_id}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(80, 750, "Loan Sanction Letter")
        c.line(80, 740, 500, 740)  
        
        # Add header text
        c.setFont("Helvetica", 12)
        c.drawString(80, 700, "StartupSprint")
        c.drawString(80, 680, "Pune, India")
        c.drawString(80, 640, datetime.now().strftime('%Y-%m-%d'))
        c.drawString(80, 600, f"Dear {first_name} {last_name},")
        c.drawString(80, 560, f"This letter is made in reference to your loan application number {application_number}.")
        c.drawString(80, 540, "Based on the information you provided in your loan application we are pleased to")
        c.drawString(80, 520, "inform you of the approval of your loan based on the following terms and ")
        c.drawString(80, 500, "conditions:")

        # Add loan details
        c.drawString(80, 440, f"\u2022 Total Principal Amount: {loan_principal_amount}")
        c.drawString(80, 420, f"\u2022 Total amount plus Processing Fee: {total_amount_and_processing_fees}")
        c.drawString(80, 400, f"\u2022 Rate of Interest: {interest_rate}%")
        c.drawString(80, 380, f"\u2022 Tenure: {loan_tenure} years")
        c.drawString(80, 360, f"\u2022 Instalment (EMI): {emi}")
        c.drawString(80, 340, f"\u2022 Maturity Date: {naturity_date.strftime('%Y-%m-%d')}")

        c.drawString(80, 300, "Disbursement shall be made upon completion of the required documents for the")
        c.drawString(80, 280, "loan and of the signing of loan agreement.")
        c.drawString(80, 240, "Regards,")
        c.drawString(80, 200, "Loan Sanctioning Officer")
        c.drawString(80, 180, "StartupSprint")
        c.save()
        success_logger.info(f"PDF generated successfully: {filename}")
        return filename
    except Exception as e:
        print(e)
        error_logger.error(f"Error generating PDF: {str(e)}")
        raise


# Function to calculate loan parameters

def calculate_installment(loan_principal_amount, interest_rate, loan_tenure):
    monthly_interest_rate = (interest_rate / 100) / 12
    total_amount_and_processing_fees = loan_principal_amount + (loan_principal_amount * (2.5 / 100))
    number_of_installments = loan_tenure * 12
    emi = round(total_amount_and_processing_fees * monthly_interest_rate * ((1 + monthly_interest_rate) ** number_of_installments) / (((1 + monthly_interest_rate) ** number_of_installments) - 1),2)
    
    today = datetime.today()
    naturity_date = today + timedelta(days=number_of_installments * 30)  # Assuming 30 days per month
    return total_amount_and_processing_fees, emi, naturity_date


# Assuming the filename is the complete path to the PDF file
def send_email_with_attachment(subject, body, from_email, to_email, filename):
    email = EmailMessage(subject, body, from_email, to_email)
    email.attach_file(filename)
    email.send()

