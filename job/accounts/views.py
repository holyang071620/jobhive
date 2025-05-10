from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import (
    RegisterForm,
    JobPostForm,
    ApplicationForm,
    EditProfileForm,
    ProfilePicForm,
    EditSkillsForm,  # ✅ make sure you import this
)
from .models import Job, Application, CustomUser
from .recommender import get_recommended_jobs

def home(request):
    jobs = Job.objects.all().order_by('-posted_at')
    search = request.GET.get('search', '')
    location = request.GET.get('location', '')
    experience = request.GET.get('experience', '')

    if search:
        jobs = jobs.filter(job_title__icontains=search)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if experience:
        jobs = jobs.filter(experience_level__icontains=experience)

    recommended_jobs = []
    if request.user.is_authenticated:
        recommended_jobs = get_recommended_jobs(request.user)

    application_forms = {job.id: ApplicationForm() for job in jobs}
    return render(request, 'accounts/home.html', {
        'jobs': jobs,
        'application_forms': application_forms,
        'recommended_jobs': recommended_jobs,
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.address = form.cleaned_data.get('address')
            user.contact_number = form.cleaned_data.get('contact')
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('home')
    else:
        form = JobPostForm()
    return render(request, 'job/post_job.html', {'form': form})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.posted_by == request.user:
        job.delete()
        messages.success(request, "Job deleted.")
    return redirect('home')


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Applied successfully!")
        else:
            messages.error(request, "Something went wrong. Please try again.")
    return redirect('home')


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile  # this will work if you have signals creating Profile

    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, request.FILES, instance=user)
        profile_form = EditSkillsForm(request.POST, instance=profile)
        pic_form = ProfilePicForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid() and profile_form.is_valid() and pic_form.is_valid():
            user_form.save()
            profile_form.save()
            pic_form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile', username=user.username)
    else:
        user_form = EditProfileForm(instance=user)
        profile_form = EditSkillsForm(instance=profile)
        pic_form = ProfilePicForm(instance=user)
    return render(request, 'accounts/edit_profile.html', {
        'profile_form': user_form,
        'skills_form': profile_form,
        'picture_form': pic_form,
    })


def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    jobs = user.jobs.all()
    return render(request, 'accounts/profile.html', {
        'profile_user': user,
        'jobs': jobs
    })


def all_jobs(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'accounts/all_jobs.html', {'jobs': jobs})


def search_users(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = CustomUser.objects.filter(username__icontains=query)
    return render(request, 'accounts/user_search.html', {'results': results, 'query': query})


def custom_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')


@login_required
def my_applicants(request):
    jobs = Job.objects.filter(posted_by=request.user).prefetch_related('applications')
    return render(request, 'accounts/my_applicants.html', {'jobs': jobs})
