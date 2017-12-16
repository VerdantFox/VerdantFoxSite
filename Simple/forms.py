from django import forms


class VigenereForm(forms.Form):
    cipher_key = forms.CharField()
    plain_text = forms.CharField(widget=forms.Textarea)


