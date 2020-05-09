from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from django.conf import settings
from checkout.forms import DonationForm
from profiles.models import Memberships, Subscription, UserMembership
from django.contrib import messages




import stripe
import os

stripe.api_key = 'sk_test_5UBH6SjTB12sryQRxLTIUfyL00bROW3YcZ'




@login_required
def checkoutview(request):
	form=DonationForm()

	context={'d_form':form}
    
	return render(request, 'checkout/checkout.html', context )

    

def charge(request): # new
    
    if request.method =='POST':
    	print(request.POST)
    	token=request.POST['stripeToken']
    	amount=int(request.POST['amount'])
    	

    	customer=stripe.Customer.create(
    		
    		email=request.POST['email'],
    		name=request.POST['name'],
    		source=request.POST['stripeToken']
    		
    		)

    	stripe.Charge.create(
    		customer=customer,
    		amount=amount*100,
    		currency="usd",
    		description=f"{amount}usd Donation!!",
)

    return redirect(reverse('success', args=[amount]))



def successMsg(request, args):
    amount =args
    return render(request, 'checkout/success.html', {'amount':amount})




class PremiumView(ListView):
    template_name='checkout/premium.html'
    model=Memberships



    def post(self, request, **kwargs):
        selected_membership_type=request.POST['membership_type']
        current_user_membership=UserMembership.objects.filter(user=request.user).first()
        user_subscription=Subscription.objects.filter(user_membership=current_user_membership).first()
        selected_membership=Memberships.objects.filter(Membership_type=selected_membership_type).first()
        

        # =========================
        # Validation
        # =========================

        if selected_membership == current_user_membership.membership:
            messages.info(request, 'you already have this membership. your next payment date is {}'.format('from stripe'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        request.session['selected_membership_type']=selected_membership_type
        return HttpResponseRedirect(reverse('payment'))
            


 

def PaymentView(request):
    selected_membership_type=request.session['selected_membership_type']
    current_user_membership=UserMembership.objects.filter(user=request.user).first()
    user_subscription=Subscription.objects.filter(user_membership=current_user_membership).first()
    selected_membership=Memberships.objects.filter(Membership_type=selected_membership_type).first()
    
    publishkey=settings.STRIPE_PUBLISHABLE_KEY
    context={
    'publishkey':publishkey,
    'selected_membership':selected_membership
    }

    if request.POST:
        try:
            token=request.POST.get('stripeToken')
            stripe.Customer.modify(current_user_membership.stripe_customer_id, source=token)
            subscription=stripe.Subscription.create(
            customer=current_user_membership.stripe_customer_id,
            items=[{"plan": selected_membership.stripe_plan_id}],
            ) 
            return redirect(reverse('update_membership', kwargs={
                'sub_id':subscription.id 
                }))

        except:
            messages.info(request, 'your card was declined')
            

    return render(request, 'checkout/Membership_payment.html', context)
        

 

def update_membership_view(request, sub_id):
    selected_membership_type=request.session['selected_membership_type']
    current_user_membership=UserMembership.objects.filter(user=request.user).first()
    user_subscription, created =Subscription.objects.get_or_create(user_membership=current_user_membership)
    selected_membership=Memberships.objects.filter(Membership_type=selected_membership_type).first()
    
    current_user_membership.membership=selected_membership 
    current_user_membership.save()
    user_subscription.stripe_subscription_id=sub_id
    user_subscription.active=True
    user_subscription.save()

    try:
        del request.session['selected_membership_type']
    except :
        pass

    messages.success(request, 'seccessfully created {} membership'.format(selected_membership_type))

    return redirect('/')



def cancelsub(request):
    current_user_membership=UserMembership.objects.filter(user=request.user).first()

    user_subscription, create=Subscription.objects.get_or_create(user_membership=current_user_membership)
    
    if user_subscription.active == False:
        messages.info(request, 'you do not have an active subscription')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    sub=stripe.Subscription.retrieve(user_subscription.stripe_subscription_id)
    sub.delete()

    user_subscription.active = False
    user_subscription.save()
    
    free_membership=Memberships.objects.filter(Membership_type='Free').first()
    current_user_membership.membership = free_membership
    current_user_membership.save()

    messages.info(request, 'you have successfully cancelled you subscription')
    
    return redirect('/premium')




