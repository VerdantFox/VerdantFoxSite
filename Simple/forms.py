from django import forms


class VigenereForm(forms.Form):

    cipher_key = forms.CharField(
        label="Cipher Key (One word, please)",
        max_length=40,
        widget=forms.TextInput(attrs={
            "class": "form-control", "placeholder": "SecretKey"})
    )

    input_text = forms.CharField(
        max_length=1000,
        label="Text encrypt or decrypt:",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": 'Our spy "James" will arrive in the castle at 3pm.'})
    )

    def clean_cipher_key(self):
        data = self.cleaned_data['cipher_key']
        if not data.isalpha():
            raise forms.ValidationError("Cipher key must be One word with no "
                                        "spaces, special characters or numbers!")
        return data


