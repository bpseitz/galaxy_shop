from django import forms


class ProductForm(forms.Form):
    name = forms.CharField(max_length=45)
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}),
                           label="Description")
    category = forms.CharField(max_length=45)
    price = forms.DecimalField(max_digits=9, decimal_places=2)
    file = forms.ImageField()


