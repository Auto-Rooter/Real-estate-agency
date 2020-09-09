from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if listing_id and listing and name and email and phone:

            # Check if user has made inquiry already
            if request.user.is_authenticated:
                user_id = request.user.id
                has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)

                if has_contacted:
                    messages.error(request, 'You have already made an inquiry for this home!')
                    return redirect('/listings/'+listing_id)

            contact = Contact(listing= listing, listing_id= listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
            contact.save()

            # Send Email to Realtor
            send_mail(
                'Property Listing Inquery',
                'There has been an inquiry for '+ listing + '. Sign into Admin Panel for more info',
                '',
                [realtor_email, 'hadi.assalem@gmail.com'],
                fail_silently=False
            )

            messages.success(request, 'Your request has been submitted, a realtor will contact you soon.')
            return redirect('/listings/'+listing_id)
        else:
            messages.error(request, 'Please Fills all the Inquiry Fields..!')
            return redirect('/listings/'+listing_id)  
    else:
        messages.error(request, 'Something Wrong..!')
        return redirect('/listings/'+listing_id)           
