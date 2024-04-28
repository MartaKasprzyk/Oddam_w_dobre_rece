from django.core.exceptions import ValidationError


class CustomPasswordValidator:

    def validate(self, password, user=None):
        lst = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}',
               '[', ']', '|', '\\', ':', '"', ';', "'", '<', '>', '?', ',', '.', '/', '"']
        if not any(x for x in password if x.isupper()):
            raise ValidationError('Hasło musi zawierać dużą literę.')
        if not any(x for x in password if x.islower()):
            raise ValidationError('Hasło musi zawierać małą literę.')
        if not any(x for x in password if x.isdigit()):
            raise ValidationError('Hasło musi zawierać cyfrę.')
        if not any(x for x in password if x in lst):
            raise ValidationError('Hasło musi zawierać znak specjalny.')

    def get_help_text(self):
        return ""
