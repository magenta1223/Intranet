from django import forms
from .models import Estimator,EstimatorType

class EstimatorTypeForm(forms.ModelForm):
    class Meta:
        model = EstimatorType
        fields =['type']

class EstimatorForm(forms.ModelForm):

    class Meta:
        model = Estimator
        fields = ['type']