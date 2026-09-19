from django.shortcuts import render
from albums.models import Album
from django.shortcuts import render
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
            # Email sending will be wired up here later
            messages.success(request, "Thanks for getting in touch — we'll reply soon.")
            return redirect('contact')
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
    else:
        contact_form = ContactForm()

    return render(request, 'contact.html', {'contact_form': contact_form})
