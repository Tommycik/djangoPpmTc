from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class ForgotEmail:
    def __init__(self, new_pass):
        self.new_pass = new_pass
        subject = '[Careers Portal] Forgot your password'

    def email(self):
        return {
            "title": "Your password has been reset",
            "shortDescription": "You have requested a new password",
            "subtitle": "Please find your new password attached for Careers Portal",
            "message": "Your new password is: {}. If you did not request this new password, please contact support@careers-portal.co.za immediately. Othewise, kindly login to your profile with your new password. If you have any challenges, send an email to admin@careers-portal.co.za."
        }

    def sendEmail(email, subject, to_email):
        from_email = settings.EMAIL_HOST_USER
        text_content = """
        {}
        {}
        {}
        regards,
        Careers Portal Support
        """.format(email['shortDescription'], email['subtitle'], email['message'])
        html_c = get_template('basic-email.html')
        d = {'email': email}
        html_content = html_c.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def sendEmail(email, subject, to_email):
    from_email = settings.EMAIL_HOST_USER
    text_content = """
    {}
    {}
    {}
    regards,
    Careers Portal Support
    """. format(email['shortDescription'], email['subtitle'], email['message'])
    html_c = get_template('basic-email.html')
    d = { 'email': email }
    html_content = html_c.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()