from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin', 'customer')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.CharField(label='', widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))


class SignupForm(forms.ModelForm):
    email = forms.CharField(label='', widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['email', ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email already exists")
        return email

    def clean_confirm_password(self):
        pword = self.cleaned_data["password"]
        c_pword = self.cleaned_data["confirm_password"]
        if pword != c_pword:
            raise forms.ValidationError("Password didnot match")
        return c_pword


class SendMailForm(forms.Form):
    email = forms.EmailField()
