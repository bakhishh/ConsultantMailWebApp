from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText

sender_mail = 'sendermail' # you can write your email address

def send_to_consultant(receiver_mail, tmp):
    message = MIMEText(tmp, "html")
    message["Subject"] = "ARA VE BİTİRME PROJESİ ARA RAPORLARI"
    message["From"] = sender_mail
    message["To"] = str(receiver_mail)
    server = smtplib.SMTP("smtp.gmail.com", 587) 
    server.starttls() 
    server.login(sender_mail, "apppassword") # you should use your app password of your gmail
    server.sendmail(sender_mail, receiver_mail, message.as_string())
    server.quit()

def send_to_consultant_and_assistant(consultant_mail, assistant_list, message):

    try:
        # Create an SMTP client session object
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_mail, "apppassword")  # Use your app-specific password

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_mail
        msg['Subject'] = "ARA VE BİTİRME PROJESİ ARA RAPORLARI"
        msg.attach(MIMEText(message, 'html', 'utf-8'))  # Assuming message is HTML content

        # Send email to the consultant
        server.sendmail(sender_mail, consultant_mail, msg.as_string())
        
        # Send email to all assistants
        for receiver in assistant_list:
            server.sendmail(sender_mail, receiver, msg.as_string())

        print("Emails sent successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the SMTP server connection
        server.quit()