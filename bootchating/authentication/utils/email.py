from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
import django_rq

def trigger_email(data):
    django_rq.enqueue(_trigger_email, data)

def _trigger_email(data):
	email_to = data.get('email_to')
	subject, from_email = data.get('subject'), settings.EMAIL_HOST_USER
	text_content = subject
	template = get_template("emails/notification.html")
	html_content = str(template.render(data))
	msg = EmailMultiAlternatives(subject, text_content, from_email, bcc=[email_to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()