from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import InquiryForm


def home(request):
    return render(request, "website/home.html")


def about(request):
    return render(request, "website/about.html")


def restaurant_bar(request):
    return render(request, "website/restaurant_bar.html")


def events(request):
    return render(request, "website/events.html")


def gallery(request):
    return render(request, "website/gallery.html")


def contact(request):
    if request.method == "POST":
        form = InquiryForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data.get("email")
            preferred_date = form.cleaned_data.get("preferred_date")
            number_of_people = form.cleaned_data.get("number_of_people")
            inquiry_type = form.cleaned_data["inquiry_type"]
            message = form.cleaned_data["message"]

            body_lines = [
                f"Full name: {full_name}",
                f"Phone number: {phone}",
            ]

            if email:
                body_lines.append(f"Email: {email}")

            if preferred_date:
                body_lines.append(f"Preferred date: {preferred_date:%Y-%m-%d}")

            if number_of_people:
                body_lines.append(f"Number of people: {number_of_people}")

            body_lines.extend(
                [
                    f"Inquiry type: {inquiry_type}",
                    "",
                    "Message:",
                    message,
                    "",
                    "Website: The Hive Resort & Bar",
                    "Location: Belgut, Sosiot, along Sosiot-Kapsoit Road",
                ]
            )

            email_message = EmailMessage(
                subject=f"New inquiry from The Hive website - {inquiry_type}",
                body="\n".join(body_lines),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.HIVE_INQUIRY_EMAIL],
                reply_to=[email] if email else None,
            )

            try:
                email_message.send(fail_silently=False)
            except Exception as error:
                print(f"Failed to send The Hive inquiry email: {error}")
                messages.error(
                    request,
                    "Sorry, we could not send your inquiry right now. Please call or WhatsApp us on +254 700 770 702.",
                )
            else:
                messages.success(
                    request,
                    "Thank you for contacting The Hive. Our team will get back to you shortly.",
                )
                return HttpResponseRedirect(f"{reverse('contact')}#inquiry")
        else:
            messages.error(request, "Please check the highlighted fields and try again.")
    else:
        form = InquiryForm()

    return render(request, "website/contact.html", {"form": form})
