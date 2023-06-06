# from django import forms
# from .models import Category, Vehicle

# class vehicleform(forms.ModelForm):
#     class Meta:
#         model = Vehicle
#         fields = ['vehicle_no', 'vehicle_type', 'parking_area_no', 'parking_charge']
    
#     def __init__(self, *args, **kwargs):
#         super(vehicleform, self).__init__(*args, **kwargs)
#         # Query the Category model to get the distinct vehicle types
#         vehicle_types = Category.objects.values_list('vehicle_type', flat=True).distinct()
#         # Query the Category model to get the distinct parking area numbers
#         parking_area_nos = Category.objects.values_list('parking_area_no', flat=True).distinct()
#         # Query the Category model to get the distinct parking charges
#         parking_charges = Category.objects.values_list('parking_charge', flat=True).distinct()

#         # Create the choice fields using the values from the Category model
#         self.fields['vehicle_type'] = forms.ModelChoiceField(queryset=vehicle_types)
#         self.fields['parking_area_no'] = forms.ModelChoiceField(queryset=parking_area_nos)
#         self.fields['parking_charge'] = forms.ModelChoiceField(queryset=parking_charges)
from django import forms
from .models import Category, Vehicle

class vehicleform(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_no', 'vehicle_type', 'parking_area_no', 'parking_charge']
        widgets = {
            'vehicle_no': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'parking_area_no': forms.Select(attrs={'class': 'form-control'}),
            'parking_charge': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(vehicleform, self).__init__(*args, **kwargs)
        vehicle_types = Category.objects.values_list('vehicle_type', flat=True).distinct()
        parking_area_nos = Category.objects.values_list('parking_area_no', flat=True).distinct()
        parking_charges = Category.objects.values_list('parking_charge', flat=True).distinct()

        self.fields['vehicle_type'] = forms.ChoiceField(choices=[(v, v) for v in vehicle_types], widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['parking_area_no'] = forms.ChoiceField(choices=[(p, p) for p in parking_area_nos], widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['parking_charge'] = forms.ChoiceField(choices=[(c, c) for c in parking_charges], widget=forms.Select(attrs={'class': 'form-control'}))


# # #==================================================================


class catform(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['parking_area_no','vehicle_type','vehicle_limit','parking_charge']
        # fields = '__all__'
        widgets = {
            'parking_area_no': forms.TextInput(attrs={'class':'form-control'}),
            'vehicle_type': forms.TextInput(attrs={'class':'form-control'}),
            'vehicle_limit': forms.TextInput(attrs={'class':'form-control'}),
            'parking_charge': forms.TextInput(attrs={'class':'form-control'}),
        }