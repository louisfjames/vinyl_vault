from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from albums.models import Album
from .forms import ContactForm

def index(request):
    """ A view that returns the index page """
    album_data = Album.objects.all().order_by('-release_date')

    context = {
           'latest_releases': album_data[:4],
           'featured_album': album_data.filter(is_featured=True).first(),
           'sale_items': album_data.filter(is_on_sale=True)[:4],
       }
    return render(request, 'core/index.html', context)


def about(request):
    """ A view that returns the about page """
    return render(request, 'about.html')


def contact(request):
    """ A view that handles the contact form """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            phone_number = contact_form.cleaned_data['phone_number']
            message = contact_form.cleaned_data['message']

            send_mail(
                subject=f'New contact form message from {name}',
                message=f'From: {name} ({email})\nPhone: {phone_number}\n\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['louisfredjames@gmail.com'],
            )

            messages.success(request, "Thanks for getting in touch — we'll reply soon.")
            return redirect('contact')
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
    else:
        contact_form = ContactForm()

    return render(request, 'contact.html', {'contact_form': contact_form})
