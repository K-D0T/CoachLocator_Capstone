from django import forms
from .models import Coaches, Video

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

            self.fields[i].widget.attrs['class'] = 'become-coach-form-inputs'
            self.fields[i].widget.attrs['id'] = 'become-coach-form-inputs_id'
            

class ProfileForm(forms.ModelForm):


    class Meta:
        model = Coaches
        fields = ['first_name', 'last_name', 'phone', 'email', 'price_thirty', 'price_hour', 'coed_allgirl', 'coach_tumbling', 'zip_code', 'profile_pic', 'bio']

        widgets = {

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in self.fields:

            self.fields[i].widget.attrs['class'] = 'become-coach-form-inputs'
            self.fields[i].widget.attrs['id'] = 'become-coach-form-inputs_id'
            


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']

        widgets = {

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in self.fields:

            self.fields[i].widget.attrs['class'] = 'become-coach-form-inputs'
            self.fields[i].widget.attrs['id'] = 'become-coach-form-inputs_id'
