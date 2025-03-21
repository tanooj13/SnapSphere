from django.shortcuts import render,redirect ,get_object_or_404
from django.urls import reverse
from base.forms import RegisterForm,ProfileForm,SnapForm,CaptionForm,CommentForm
from .models import Snap,Comment,Profile,Like,SavedSnap
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile = ProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile.is_valid():
            username = form.cleaned_data['username']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another.')
                return redirect('register')

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            profile = profile.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "User registered successfully!")
            return redirect('login')
    else:
        form = RegisterForm()
        profile = ProfileForm()

    return render(request, 'register.html', {'form': form, 'profile_form': profile})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    else:return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def home(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', 'recent')  # Default is 'recent'

    snaps = Snap.objects.all()

    # Apply Search Filter
    if query:
        snaps = snaps.filter(description__icontains=query) | snaps.filter(category__icontains=query) | snaps.filter(user__username__icontains=query)

    # Apply Sorting Filter
    if filter_type == 'most_liked':
        snaps = snaps.order_by('-likes_count')  # Most Liked First
    elif filter_type == 'least_liked':
        snaps = snaps.order_by('likes_count')  # Least Liked First
    elif filter_type == 'oldest':
        snaps = snaps.order_by('created_at')  # Oldest First
    else:  # Default to 'recent'
        snaps = snaps.order_by('-created_at')  # Newest First

    return render(request, 'home.html', {'snaps': snaps, 'query': query, 'filter_type': filter_type})

def post(request):
    if (request.method == 'POST'):
        snap_form = SnapForm(request.POST,request.FILES)
        if snap_form.is_valid():
            snap = snap_form.save(commit=False)
            snap.user = request.user
            snap.save()
            messages.success(request,'Snap posted successfully!')
            
        else:
            messages.error(request,'Error posting snap')
        return redirect('home')
    else:
        snap_form = SnapForm()

    return render(request,'post.html',{"snap_form":snap_form})

def delete_snap(request,snap_id):
    if (request.method == 'POST'):
        snap = Snap.objects.get(id=snap_id)
        snap.delete()
        messages.success(request,'Snap deleted successfully!')
        return redirect('profile')
    else:
        return render(request,'delete_snap.html')
    

def update_snap(request,snap_id):
    snap = Snap.objects.get(id=snap_id)

    if request.method == 'POST':
        form = CaptionForm(request.POST, instance=snap)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CaptionForm(instance=snap)

    return render(request, 'update_snap.html', {'form': form})


def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    snaps = Snap.objects.filter(user=user)
    
    context = {"profile": profile, "snaps": snaps, "created": created}

    return render(request, 'profile.html', context)


def like(request,snap_id):
    snap = Snap.objects.get(id=snap_id)
    like = Like.objects.filter(user=request.user,snap=snap).first()

    if like:
        like.delete()
    else:
        Like.objects.create(user=request.user,snap=snap)
    snap.update_likes_count()

    return redirect('home')


def comment(request, snap_id):
    snap = get_object_or_404(Snap, id=snap_id)
    comments = snap.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.snap = snap
            comment.save()
            snap.update_comments_count() 
            messages.success(request,'Comment Posted Successfully!!!')
            return redirect(request.path)
    else:
        form = CommentForm()

    return render(request, 'comment_snap.html', {'snap': snap, 'comments': comments,"form":form})

def delete_comment(request, snap_id, comment_id):
    snap = get_object_or_404(Snap, id=snap_id)
    comment = get_object_or_404(Comment, id=comment_id, snap=snap) 

    if request.method == 'POST' and comment.user == request.user:
        comment.delete()
        messages.success(request, "Comment Deleted Successfully...")
        snap.update_comments_count()
        return redirect('comment-snap', snap_id)  

    context = {"comment": comment, "snap": snap}
    return render(request, 'delete_comment.html', context)

def edit_comment(request,snap_id,comment_id):
    snap = get_object_or_404(Snap,id=snap_id)
    comment = get_object_or_404(Comment,id=comment_id,snap = snap)

    if request.method == 'POST' and comment.user == request.user:
        form = CommentForm(request.POST,instance=comment)
        form.save()
        return redirect('comment-snap', snap_id)  
    form = CommentForm(instance=comment)
    context = {"comment":comment,"snap":snap,"form":form}
    return render(request,'edit_comment.html',context)

   
def save_snap(request,snap_id):
    snap = get_object_or_404(Snap,id=snap_id)

    saved_snap, created = SavedSnap.objects.get_or_create(user=request.user, snap=snap)

    if not created:
        saved_snap.delete()
        messages.success(request,"Snap removed from saved list.")
    else:
        messages.success(request,"Snap saved successfully!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def show_saved(request):
    saved_snaps = SavedSnap.objects.filter(user=request.user).select_related('snap')
    context = {"saved_snaps":saved_snaps}
    return render(request,'saved_snaps.html',context)

@login_required
def profile_view(request,username):
    profile_user = get_object_or_404(User, username=username)
    snaps = Snap.objects.filter(user=profile_user)
    total_likes = sum(snap.likes.count() for snap in snaps)
    if request.method == "POST":
        bio = request.POST.get("bio")
        profile, created = Profile.objects.get_or_create(user=profile_user)
        profile.bio = bio
        profile.save()
        messages.success(request, "Bio updated successfully!")
        return redirect('profile-view',username=username)
    context={"snaps":snaps,"total_likes":total_likes,"profile_user":profile_user}
    return render(request,'profile.html',context)

def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')
    return render(request,'delete_account.html')



