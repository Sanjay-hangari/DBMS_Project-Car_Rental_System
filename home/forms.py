from django import forms 
  
class ImagefieldForm(forms.Form): 
    Car_name = forms.CharField() 
    Color = forms.CharField()
    City = forms.CharField()
    Pincode = forms.IntegerField()
    Capacity = forms.IntegerField()
    Transmission = forms.CharField()
    Fuel = forms.CharField()
    Price = forms.CharField()

