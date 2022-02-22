from django import forms
from .models import *

class EstimatorTypeForm(forms.ModelForm):
    class Meta:
        model = EstimatorType
        fields =['type']

class EstimatorForm(forms.ModelForm):

    class Meta:
        model = Estimator
        fields = ['type']



class ContainerForm(forms.ModelForm):

    class Meta:
        model = EstimatorContainer
        fields = ['name']