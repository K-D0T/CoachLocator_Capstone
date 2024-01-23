from django import forms

class ZipSearchForm(forms.Form):
    zip_code = forms.CharField(max_length=10, required=True)
    