from django import forms


class VisitURLForm(forms.Form):

    url = forms.URLField(required=True)