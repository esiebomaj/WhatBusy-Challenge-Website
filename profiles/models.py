from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings


from datetime import datetime
import stripe
stripe.api_key=settings.STRIPE_PUBLISHABLE_KEY

class UserProfile(models.Model):
	user=models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=True)
	name=models.CharField(max_length=200)
	dob=models.DateField()
	image=models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
	mobile=models.CharField(max_length=200)
	website=models.URLField()
	facebook=models.URLField()

	def get_absolute_url(self):
		return(reverse('profile', args=[str(self.pk)]))









# ==========================
# membership stuff
# ==========================

membership_choices=(
	('Trial','trial'),
	('Monthly','month'),
	('Yearly','year'),
	('Free', 'free'))


class Memberships(models.Model):
	Membership_type=models.CharField(choices=membership_choices, default='free', max_length=40)
	stripe_plan_id=models.CharField(max_length=40)
	price=models.CharField(max_length=40)


	def __str__(self):
		return self.Membership_type


class UserMembership(models.Model):
	membership=models.ForeignKey(Memberships, on_delete=models.SET_NULL, null=True)
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	stripe_customer_id=models.CharField(max_length=40)


	def __str__(self):
		return self.user.username

def create_membership_signal(sender, instance, created, *args, **kwargs):
	if created:
		UserMembership.objects.get_or_create(user=instance)
	
	user_membership, created =UserMembership.objects.get_or_create(user=instance)

	if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
		customer=stripe.Customer.create(email=instance.email)
		user_membership.stripe_customer_id=customer['id']
		user_membership.save()

post_save.connect(create_membership_signal, sender=User)


class Subscription(models.Model):
	user_membership=models.ForeignKey(UserMembership, on_delete=models.CASCADE)
	stripe_subscription_id=models.CharField(max_length=40)
	active=models.BooleanField(default=True)

	def __str__(self):
		return self.user_membership.user.username
	@property
	def get_data_created(self):
		sub=stripe.Subscription.retrieve(self.stripe_subscription_id)
		return datetime.fromtimestamp(sub.created)

	@property
	def get_next_billing_date (self):
		sub=stripe.Subscription.retrieve(self.stripe_subscription_id)
		return datetime.fromtimestamp(sub.current_period_end)
		






# ============================================
# Post part
# ============================================


class Post(models.Model):
	title=models.CharField(max_length=200)
	author=models.ForeignKey(to=User, on_delete=models.CASCADE)
	content=models.TextField()
	date_posted=models.DateTimeField(default=timezone.now)
	allowed_memberships=models.ManyToManyField(to=Memberships)

	def __str__(self):
		return str(self.title)




