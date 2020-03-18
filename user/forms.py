from django import forms

from user.models import User
from user.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'birthday', 'location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        cleaned_data = super().clean()
        max_distance = cleaned_data['max_distance']
        min_distance = cleaned_data['min_distance']

        if max_distance < min_distance:
            raise forms.ValidationError('max_distance 必须大于等于 min_distance')
        else:
            return max_distance

    def clean_max_dating_age(self):
        cleaned_data = super().clean()
        max_dating_age = cleaned_data['max_dating_age']
        min_dating_age = cleaned_data['min_dating_age']

        if max_dating_age < min_dating_age:
            raise forms.ValidationError('max_dating_age 必须大于等于 min_dating_age')
        else:
            return max_dating_age
