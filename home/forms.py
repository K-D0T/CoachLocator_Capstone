from django import forms
from .models import Coaches

class ZipSearchForm(forms.Form):
    zip_code = forms.CharField(max_length=10, label='Enter your zip code', required=True)


class CoachForm(forms.ModelForm):


    class Meta:
        model = Coaches
        fields = '__all__'

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in self.fields:

            self.fields[i].widget.attrs['class'] = 'form-control'

            self.fields[i].widget.attrs['required'] = True


    