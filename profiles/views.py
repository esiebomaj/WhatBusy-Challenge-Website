from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . forms import ContactForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from . models import UserProfile, Post, UserMembership
from django.core.mail import send_mail



class Home(ListView):
	model=Post
	template_name='profiles/home.html'

class PostDetailView(DetailView):
	model=Post
	template_name='profiles/post_detail.html' 


	def get_context_data(self, **kwargs):
		context=super().get_context_data(**kwargs)

		user_membership=UserMembership.objects.filter(user=self.request.user).first()
		
		user_membership_type=user_membership.membership.Membership_type

		post=Post.objects.filter(pk=self.kwargs.get('pk')).first()
		post_allowed_mem_types=post.allowed_memberships.all()

		if post_allowed_mem_types.filter(Membership_type=user_membership_type).first():
			context={'object':post}

		else:
			context={'object':None}
	

		return context

		






def aboutview(request):
	context={}
	return render(request, 'profiles/about.html', context)

#
class ProfileView(DetailView):
	template_name='profiles/profile.html'
	model=UserProfile

	def get_context_data(self, **kwargs):
		context=super().get_context_data( **kwargs)

		user_membership=self.request.user.usermembership
		user_subscription=user_membership.subscription_set.first()
		
		context['user_membership']=user_membership
		context['user_subscription']=user_subscription

		return context



class ProfileUpdateView(UpdateView):
	template_name='profiles/profile_update.html'
	model=UserProfile
	fields=['name', 'dob', 'image', 'facebook', 'website', 'mobile']


class ProfileDeleteView(DeleteView):
	template_name='profiles/profile_delete.html'
	model=UserProfile

class ProfileCreateView(CreateView):
	template_name='profiles/profile_create.html'
	model=UserProfile
	fields=['name', 'dob', 'image', 'facebook', 'website', 'mobile']

	def form_valid(self, form):
		form.instance.user=self.request.user
		return super().form_valid(form)


def contactview(request):
	user=request.user
	form=ContactForm()
	success_text=None
	context={'form':form, 'message':success_text}
	if request.method =='POST':
		form=ContactForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			name=form.cleaned_data['name']
			email=form.cleaned_data['email']
			comment=form.cleaned_data['comment']
			message='Name : {} Email : {} comment : {}'.format(name, email, comment)

			send_mail('Message form my site JeremAIh',
				message,
				email,
				['esiebomaj@gmail.com'],
				fail_silently=False,)
			success_text='We have recieved your feedback we will get back to you shortly'
			form=None
			context={'form':form, 'message':success_text}
	return render(request, 'profiles/contact.html', context)



