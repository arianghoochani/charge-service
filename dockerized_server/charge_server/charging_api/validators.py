from django.core.exceptions import ValidationError
import re

def validate_UUID(value) :
    if not re.search("^[0-9A-Za-z\-]*$", value) :
        raise ValidationError(params={"uuid" : value}, message="invalid uuid")

def validate_token(value) :
    if not re.search("^[a-zA-Z0-9\-\_~.]+$", value) :
        raise ValidationError(params={"driver_token" : value}, message="invalid driver_token")

def validate_URL(value) :
    if not re.search("^http[s]{0,1}:\/\/[0-9a-zA-Z\?\-_&=:\.\/]{3,250}$", value) :
        raise ValidationError(params={"URL" : value}, message="invalid URL")

def validate_legalString(value) :
    if re.search("[0-9\"%\'‍‍‍‍‍\`\(\)\*\+\-_:;<=>?@\[\]\^\{|\}~&\#\$\\\/]", value) :
        raise ValidationError(params={"legalString" : value}, message="invalid legalString") 