from django import forms


class VigenereForm(forms.Form):
    cipher_key = forms.CharField(
        label="Cipher Key (One word, please)",
        max_length=40,
        widget=forms.TextInput(attrs={
            "class": "form-control", "placeholder": "SecretKey"})
    )
    plain_text = forms.CharField(
        max_length=500,
        label="Text to encrypt:",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": 'Our spy "James" will arrive in the castle at 3pm.'})
    )



