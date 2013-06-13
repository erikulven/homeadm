from django.forms import ModelForm, Textarea
from console.models import Power


class PowerForm(ModelForm):
    class Meta:
        model = Power
        fields = ['level', 'description']

        widgets = {
                  'description': Textarea(attrs={'rows':4, 'cols':15})
                  }
