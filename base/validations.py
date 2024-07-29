from django.core.exceptions import ValidationError



def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('a password is needed')
    return True