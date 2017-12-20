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


class FizzBuzzForm(forms.Form):

    count_to = forms.IntegerField(
        label="Count up to: (1000 max)",
        min_value=10, max_value=1000,
        widget=forms.NumberInput(attrs={
            "class": "form-control", "value": "100"})
    )

    multiplier = forms.IntegerField(
        min_value=1, max_value=10,
        label="Count in multiples of: (10 max)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "value": '1'})
    )

    var_1 = forms.CharField(
        max_length=40,
        label="First variable name:",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": 'Fizz',
            "value": "Fizz"})
    )

    var_1_multiple = forms.IntegerField(
        min_value=1, max_value=10,
        label="Inject first variable in multiples of: (10 max)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": '3',
            "value": '3'})
    )

    var_2 = forms.CharField(
        required=False,
        max_length=40,
        label="Second variable name: (not required)",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": 'Buzz'})
    )

    var_2_multiple = forms.IntegerField(
        required=False,
        min_value=1, max_value=10,
        label="Inject second variable in multiples of: (10 max)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": '5'})
    )

    var_3 = forms.CharField(
        required=False,
        max_length=40,
        label="Third variable name: (not required)",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": 'Foo'})
    )

    var_3_multiple = forms.IntegerField(
        required=False,
        min_value=1, max_value=10,
        label="Inject third variable in multiples of: (10 max)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": '7'})
    )

    def clean(self):
        super().clean()
        # Get relevant data if it is entered
        if 'var_2' in self.cleaned_data:
            var_2 = self.cleaned_data['var_2']
        else:
            var_2 = None
        if 'var_2_multiple' in self.cleaned_data:
            var_2_multiple = self.cleaned_data['var_2_multiple']
        else:
            var_2_multiple = None
        if 'var_3' in self.cleaned_data:
            var_3 = self.cleaned_data['var_3']
        else:
            var_3 = None
        if 'var_3_multiple' in self.cleaned_data:
            var_3_multiple = self.cleaned_data['var_3_multiple']
        else:
            var_3_multiple = None

        # Raise error if given a variable but not its multiplier
        if (var_2 and not var_2_multiple) or (var_2_multiple and not var_2):
            raise forms.ValidationError("Must enter both second variable and "
                                        "its multiplier or neither.",
                                        code="var_2_error")

        if (var_3 and not var_3_multiple) or (var_3_multiple and not var_3):
            raise forms.ValidationError("Must enter both third variable and "
                                        "its multiplier or neither.",
                                        code="var_3_error")


class ChangeForm(forms.Form):

    item_cost = forms.FloatField(
        label='Item cost (in dollars):',
        min_value=.01, max_value=2000,
        widget=forms.NumberInput(attrs={
            "class": "form-control", "placeholder": "57.45"})
    )

    amount_paid = forms.FloatField(
        min_value=0.1, max_value=2500,
        label="Amount paid (in dollars):",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": '60.00'})
    )

    def clean(self):
        super().clean()
        amount_paid, item_cost = None, None
        # Get relevant data if it is entered
        if 'item_cost' in self.cleaned_data:
            item_cost = self.cleaned_data['item_cost']
        if 'amount_paid' in self.cleaned_data:
            amount_paid = self.cleaned_data['amount_paid']
        if amount_paid and item_cost:
            if amount_paid < item_cost:
                raise forms.ValidationError(
                    "Amount paid must be greater than or equal to item cost.",
                    code="Didn't pay enough")
