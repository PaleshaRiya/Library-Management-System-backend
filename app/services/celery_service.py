from app.repositories import CeleryRepository
from app.services.email_service import EmailService
from datetime import datetime, timezone, timedelta
import io
import csv

email_service = EmailService()

class CeleryService:
    def __init__(self):
        self.celery_repository = CeleryRepository()
    
    def revoke_access(self):
        return self.celery_repository.revoke_access()
    
    def send_daily_reminder(self):
        rows = self.celery_repository.send_daily_reminder()
        
        print("Rows:")
        print(rows)
        
        for row in rows:
            email = row[0]
            username = row[1]
            book_name = row[2]
            return_date = row[3]
            
            return_date = datetime.fromisoformat(return_date.replace("Z", "+00:00"))
            formatted_return_date = return_date.strftime('%A, %B %d, %Y at %I:%M %p')
            
            subject = "Reminder: Return Book"
            body = f"Dear {username},\n\nThis is a reminder to return the book '{book_name}' you rented by {formatted_return_date}. Only one day left for the return.\n\nThank you."
            html_body = f"""
            <html>
            <body>
                <p>Dear {username},</p>
                <p>This is a reminder to return the book '<b>{book_name}</b>' you rented by <b>{formatted_return_date}</b>. Only one day left for the return.</p>
                <p>Thank you.</p>
            </body>
            </html>
            """
            recipient = email

            if not (subject and recipient and body):
                return 'Invalid request. Please provide subject, recipient, and body parameters.'

            email_service.send_email(subject, recipient, body, html_body)
        
        return True


    def send_monthly_report(self):
        data = self.celery_repository.get_monthly_report_data()
        
        subject = "Monthly Report"
        body = "Dear Librarian,\n\nHere is the monthly report."
        html_body = email_service.create_monthly_report_html(data)
        recipient = "paleshariya7@gmail.com"

        if not (subject and recipient and body):
            return 'Invalid request. Please provide subject, recipient, and body parameters.'

        email_service.send_email(subject, recipient, body, html_body)
        
        return True
    
    def export_ebooks_csv(self):
        data = self.celery_repository.get_ebooks_data()
        print("Data:")
        print(data)
        
        # Create CSV
        csv_file = io.StringIO()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['User ID', 'Username', 'Email', 'Book Name', 'Content', 'Author', 'Issue Date', 'Return Date'])

        for row in data:
            userId, username, email, bookName, content, author, issueDate, returnDate = row
            issueDateFormatted = datetime.fromisoformat(issueDate.replace("Z", "+00:00")).strftime('%A, %B %d, %Y at %I:%M %p')
            returnDateFormatted = datetime.fromisoformat(returnDate.replace("Z", "+00:00")).strftime('%A, %B %d, %Y at %I:%M %p')
            csv_writer.writerow([userId, username, email, bookName, content, author, issueDateFormatted, returnDateFormatted])

        csv_file.seek(0)

        # Send CSV via Email
        email_service = EmailService()
        subject = "E-Books Report"
        body = "Attached is the CSV report of the issued/returned/granted e-books."
        recipient = "paleshariya7@gmail.com"
        csv_attachment = ("ebooks_report.csv", csv_file.getvalue())

        email_service.send_email(subject, recipient, body, attachment=csv_attachment)
