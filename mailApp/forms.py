from django import forms
from .models import Consultant

class ConsultantForm(forms.Form):
    consultant = forms.ModelChoiceField(queryset=Consultant.objects.all(), label="Select Consultant")
