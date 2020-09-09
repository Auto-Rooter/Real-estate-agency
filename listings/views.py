from django.shortcuts import render, get_object_or_404
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from .models import Listing
from .choices import bedroom_choices, price_choices, state_choices


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paginator_listings = paginator.get_page(page)

    context = {'listings': paginator_listings}

    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {'listing': listing}
    return render(request, 'listings/listing.html', context)

def search(request):
    query_listings = Listing.objects.order_by('-list_date')

    # Search according to Keywords
    if "keywords" in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query_listings = query_listings.filter(description__icontains=keywords)

    # Search according to city
    if "city" in request.GET:
        city = request.GET['city']
        if city:
            query_listings = query_listings.filter(city__iexact=city)

    # Search according to state
    if "state" in request.GET:
        state = request.GET['state']
        if state:
            query_listings = query_listings.filter(state__iexact=state)

    # Search according to bedrooms
    if "bedrooms" in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            query_listings = query_listings.filter(bedrooms__lte=bedrooms)
     
    # Search according to price
    if "price" in request.GET:
        price = request.GET['price']
        if price:
            query_listings = query_listings.filter(price__lte=price)
     

    context = {
        'listings': query_listings,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'values': request.GET
        }
    return render(request, 'listings/search.html', context)
