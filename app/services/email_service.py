from flask_mail import Mail, Message
from flask import current_app
from datetime import datetime, timezone, timedelta

mail = Mail()

class EmailService:
    def __init__(self):
        pass
        
    def init_mail(self, app):
        mail.init_app(app)

    def send_email(self, subject, recipient, body, html_body=None, attachment=None):
        with current_app.app_context():
            msg = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], recipients=[recipient])
            msg.body = body
            if html_body:
                msg.html = html_body
            if attachment:
                msg.attach(attachment[0], 'text/csv', attachment[1])
            mail.send(msg)

    def create_monthly_report_html(self, data):
        html = """
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 10px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h2>Monthly Report</h2>
            <table>
                <tr>
                    <th>User ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Book Name</th>
                    <th>Issue Date</th>
                    <th>Return Date</th>
                    <th>Rating</th>
                    <th>Feedback</th>
                    <th>Is Returned</th>
                    <th>Is Revoked</th>
                    <th>Is Bought</th>
                    <th>Is Approved</th>
                </tr>
        """
        for row in data:
            userId, username, email, bookName, issueDate, returnDate, rating, feedback, isReturned, isRevoked, isBought, isApproved = row
            issueDateFormatted = datetime.fromisoformat(issueDate.replace("Z", "+00:00")).strftime('%A, %B %d, %Y at %I:%M %p')
            returnDateFormatted = datetime.fromisoformat(returnDate.replace("Z", "+00:00")).strftime('%A, %B %d, %Y at %I:%M %p')
            
            isApprovedSymbol = "✔️" if isApproved else "❌"
            isReturnedSymbol = "✔️" if isReturned else "❌"
            isRevokedSymbol = "✔️" if isRevoked else "❌"
            isBoughtSymbol = "✔️" if isBought else "❌"

            html += f"""
                <tr>
                    <td>{userId}</td>
                    <td>{username}</td>
                    <td>{email}</td>
                    <td>{bookName}</td>
                    <td>{issueDateFormatted}</td>
                    <td>{returnDateFormatted}</td>
                    <td>{rating}</td>
                    <td>{feedback}</td>
                    <td>{isReturnedSymbol}</td>
                    <td>{isRevokedSymbol}</td>
                    <td>{isBoughtSymbol}</td>
                    <td>{isApprovedSymbol}</td>
                </tr>
            """
        html += """
            </table>
        </body>
        </html>
        """
        return html
