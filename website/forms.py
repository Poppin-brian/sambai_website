from django import forms


class InquiryForm(forms.Form):
    INQUIRY_CHOICES = [
        ("Guest Spaces", "Guest Spaces"),
        ("Restaurant", "Restaurant"),
        ("Bar & Beverages", "Bar & Beverages"),
        ("Events & Gatherings", "Events & Gatherings"),
        ("Directions / Location", "Directions / Location"),
        ("General Inquiry", "General Inquiry"),
    ]

    full_name = forms.CharField(
        label="Full name",
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Your name"}),
    )
    phone = forms.CharField(
        label="Phone number",
        max_length=40,
        widget=forms.TextInput(attrs={"placeholder": "+254 ..."}),
    )
    email = forms.EmailField(
        label="Email address",
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}),
    )
    preferred_date = forms.DateField(
        label="Preferred date",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    number_of_people = forms.IntegerField(
        label="Number of people",
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Optional"}),
    )
    inquiry_type = forms.ChoiceField(
        label="Inquiry type",
        choices=[("", "Select an inquiry type"), *INQUIRY_CHOICES],
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Tell us what you need"}),
    )
