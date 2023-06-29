from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile,TidePost
from django.contrib import messages
from .forms import TideForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.http import Http404


# Create your views here.
def home(request):
    
	if request.user.is_authenticated:
       
		form = TideForm(request.POST or None)

		if request.method == "POST":
           
			if form.is_valid():
				tidepost = form.save(commit=False)
				tidepost.user = request.user
				tidepost.save()
				messages.success(request, ("Your tidepost Has Been Posted!"))
				return redirect('home')
		
		tideposts = TidePost.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"tideposts":tideposts, "form":form})
	else:
		tideposts = TidePost.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"tideposts":tideposts})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, 'profile_list.html', 
                    {'profiles':profiles})
    else:
        messages.success(request, ("You must be logged In"))
        return redirect('home')
    
def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		tideposts = TidePost.objects.filter(user_id=pk).order_by("-created_at")

		# Post Form logic
		if request.method == "POST":
			# Get current user
			current_user_profile = request.user.profile
			# Get form data
			action = request.POST['follow']
			# Decide to follow or unfollow
			if action == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action == "follow":
				current_user_profile.follows.add(profile)
			# Save the profile
			current_user_profile.save()



		return render(request, "profile.html", {"profile":profile, "tideposts":tideposts})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')	
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password = password)
        if user is not None:
            login(request,user)
            messages.success(request, ("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error loggin in, please try again..."))
            return redirect('login')
            
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been ogged out, sorry to see you go"))
    return render(request, 'login.html', {})

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            #email = form.cleaned_data['email']
            
            #log int user
            user = authenticate(username = username, password = password)
            login(request,user)
            messages.success(request, ("You have successfully registered.Welcome."))
            return redirect('home')
        
            
    return render(request, 'register.html', {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        
        
        user_form = SignUpForm(request.POST or None,request.FILES or None,instance = current_user)
        profile_form = ProfilePicForm(request.POST or None,request.FILES or None,instance = profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("Your Profile has been updated")) 
            return redirect( 'home')
        return render(request, 'update_user.html', {'user_form':user_form,'profile_form':profile_form })

    else:
        messages.success(request, ("You must be logged in to view this page")) 
        return redirect( 'home')
    
def tweet_like(request, pk):
    if request.user.is_authenticated:
        tidepost = get_object_or_404(TidePost, id=pk)
        if tidepost.likes.filter(id=request.user.id):
            tidepost.likes.remove(request.user)
        else:
            tidepost.likes.add(request.user)
        
        return redirect (request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in order to like a tidepost")) 
        return redirect( 'home')
    
def tweet_show(request, pk):
    tidepost = get_object_or_404(TidePost, id=pk)
    if tidepost:
        return render(request, 'show_tweet.html', {'tidepost':tidepost})

    else:
        messages.success(request, ("That tidepost, does not exist")) 
        return redirect( 'home')
        
    
def unfollow(request, pk):
    if request.user.is_authenticated:
        #get the profile to unfollow
        profile = Profile.objects.get(user_id = pk)
        #unfollow the user
        request.user.profile.follows.remove(profile)
        #save our profile
        request.user.profile.save()
        messages.success(request, (f"You have unfollowed {profile.user.username}")) 
        return redirect( request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in to be in this page")) 
        return redirect( 'home')
    
def follow(request, pk):
    if request.user.is_authenticated:
        #get the profile to unfollow
        profile = Profile.objects.get(user_id = pk)
        #unfollow the user
        request.user.profile.follows.add(profile)
        #save our profile
        request.user.profile.save()
        messages.success(request, (f"You are now following {profile.user.username}")) 
        return redirect( request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in to be in this page")) 
        return redirect( 'home')
    
def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'followers.html', 
                        {'profiles':profiles})
        else:
             messages.success(request, ("That's not your profile page"))
        return redirect('home')
    else:
        messages.success(request, ("You must be logged In"))
        return redirect('home')
    
    
def follows(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'follows.html', 
                        {'profiles':profiles})
        else:
             messages.success(request, ("That's not your profile page"))
        return redirect('home')
    else:
        messages.success(request, ("You must be logged In"))
        return redirect('home')

def delete_tweet(request, pk):
    if request.user.is_authenticated:
        tidepost = get_object_or_404(TidePost, id=pk)
        #check to see yif you own the tidepost
        if request.user.username == tidepost.user.username:
            tidepost.delete()
            messages.success(request, ("tidepost deleted")) 
            return redirect (request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("You do not own that tidepost.")) 
            return redirect ("home")
        
    else:
        messages.success(request, ("Please Log In to continue")) 
        return redirect (request.META.get("HTTP_REFERER"))

    
    
def edit_tweet(request,pk):
	if request.user.is_authenticated:
		# Grab The tidepost!
		tidepost = get_object_or_404(TidePost, id=pk)

		# Check to see if you own the tidepost
		if request.user.username == tidepost.user.username:
			
			form = TideForm(request.POST or None, instance=tidepost)
			if request.method == "POST":
				if form.is_valid():
					tidepost = form.save(commit=False)
					tidepost.user = request.user
					tidepost.save()
					messages.success(request, ("Your tidepost Has Been Updated!"))
					return redirect('home')
			else:
				return render(request, "edit_tweet.html", {'form':form, 'tidepost':tidepost})
	
		else:
			messages.success(request, ("You Don't Own That tidepost!!"))
			return redirect('home')

	else:
		messages.success(request, ("Please Log In To Continue..."))
		return redirect('home')
def page_not_found(request, exception):
    return render(request, '404.html')