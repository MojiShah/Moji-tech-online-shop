import re
from django.core.exceptions import ValidationError

def normalize_email_address(email):
    if not email:
        return None
    
    return email.strip().lower() or None

def normalize_phone_number(phone_number):
    if not phone_number:
        return None
    
    phone_number = phone_number.strip()
    if not re.fullmatch(r"(?:\+98|0)?9[0-9]{9}",phone_number):
        raise ValidationError("Enter a valid Iranian mobile number.")

    return "+98" + phone_number[-10:]