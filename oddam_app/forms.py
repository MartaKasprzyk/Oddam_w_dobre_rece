from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User


class ChangePasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].label = "Nowe hasło"
        self.fields['new_password2'].label = "Potwierdź nowe hasło"
        self.fields['new_password1'].help_text = ('<br/>Hasło musi mieć długość min. 8 znaków, '
                                                  '<br/>zawierać dużą i małą literę, cyfrę '
                                                  '<br/>i znak spacjalny.')

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
