from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Like, Match, Message
from .models import UserProfile


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Go to profile after login

    return render(request, 'login.html')


from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import UserProfile

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        age = request.POST.get('age')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        bio = request.POST.get('bio')

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'register.html',
                {'error': 'Username already exists!'}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            age=age,
            gender=gender,
            location=location,
            bio=bio,
            profile_image=request.FILES.get('profile_image')
        )

        return redirect('login')

    return render(request, 'register.html')

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'age': 18,
            'gender': 'Not Set',
            'location': '',
            'bio': ''
        }
    )

    return render(request, 'profile.html', {
        'profile': profile
    })


@login_required
def matches(request):

    seen_profiles = request.session.get('seen_profiles', [])

    profile = UserProfile.objects.exclude(
        user=request.user
    ).exclude(
        id__in=seen_profiles
    ).first()

    return render(
        request,
        'matches.html',
        {'profile': profile}
    )


@login_required
def like_user(request, user_id):

    receiver = User.objects.get(id=user_id)

    Like.objects.get_or_create(
        sender=request.user,
        receiver=receiver
    )
    existing_like = Like.objects.filter(
        sender=receiver,
        receiver=request.user
    ).exists()

    if existing_like:
        Match.objects.get_or_create(
            user1=request.user,
            user2=receiver
        )

    profile = UserProfile.objects.get(user=receiver)

    seen_profiles = request.session.get('seen_profiles', [])

    if profile.id not in seen_profiles:
        seen_profiles.append(profile.id)

    request.session['seen_profiles'] = seen_profiles

    return redirect('matches')


@login_required
def my_matches(request):

    matches = Match.objects.filter(user1=request.user)

    return render(
        request,
        'my_matches.html',
        {'matches': matches}
    )


@login_required
def chat(request, user_id):

    other_user = get_object_or_404(User, id=user_id)
    other_profile = UserProfile.objects.filter(user=other_user).first()

    # Mark incoming messages as seen
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_seen=False
    ).update(is_seen=True)

    if request.method == 'POST':

        message_text = request.POST.get('message')

        if message_text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=message_text
            )

            return redirect('chat', user_id=other_user.id)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('created_at')

    return render(request, 'chat.html', {
        'other_user': other_user,
        'other_profile': other_profile,
        'messages': messages
    })

@login_required
def edit_profile(request):

    profile = request.user.userprofile

    if request.method == 'POST':

        profile.age = request.POST.get('age')
        profile.location = request.POST.get('location')
        profile.bio = request.POST.get('bio')

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        profile.save()

        return redirect('profile')

    return render(request, 'edit_profile.html', {
        'profile': profile
    })


def logout_view(request):
    logout(request)
    return redirect('home')




@login_required
def dashboard(request):

    likes_count = Like.objects.filter(
        receiver=request.user
    ).count()

    matches_count = Match.objects.filter(
        user1=request.user
    ).count()

    messages_count = Message.objects.filter(
        receiver=request.user
    ).count()

    unread_count = Message.objects.filter(
        receiver=request.user,
        is_seen=False
    ).count()

    return render(request, 'dashboard.html', {
        'likes_count': likes_count,
        'matches_count': matches_count,
        'messages_count': messages_count,
        'unread_count': unread_count,   # ADD THIS
    })

from .models import ProfilePhoto

@login_required
def upload_photos(request):

    profile = request.user.userprofile

    if request.method == 'POST':

        images = request.FILES.getlist('images')

        for image in images:

            ProfilePhoto.objects.create(
                profile=profile,
                image=image
            )

    photos = ProfilePhoto.objects.filter(
        profile=profile
    )

    return render(
        request,
        'upload_photos.html',
        {'photos': photos}
    )

@login_required
def skip_user(request, profile_id):

    seen_profiles = request.session.get('seen_profiles', [])

    if profile_id not in seen_profiles:
        seen_profiles.append(profile_id)

    request.session['seen_profiles'] = seen_profiles

    return redirect('matches')