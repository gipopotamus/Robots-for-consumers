from django import forms
from .models import Robot


class RobotCreationForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']

    def clean(self):
        cleaned_data = super().clean()
        model = cleaned_data.get('model')
        version = cleaned_data.get('version')
        # if not Robot.objects.filter(model=model, version=version).exists():
        #     raise forms.ValidationError('Модель и версия робота не существуют.')

        return cleaned_data
