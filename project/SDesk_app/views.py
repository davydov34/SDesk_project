from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect
from django.db.models import Max

from .models import Task, Profile, StaffPosition, PermissionLevel, Status
from .forms import LoginForm, RegisterForm, TaskForm

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.create(
               user = User.objects.get(id=(User.objects.get(username=form.cleaned_data.get('username')).pk)),
               system_name = form.cleaned_data.get('username'),
               last_name = form.cleaned_data.get('last_name'),
               first_name = form.cleaned_data.get('first_name'),
               staff_position = StaffPosition.objects.get(pk=1),
               permission_level = PermissionLevel.objects.get(pk=1)
            )

            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def list(request, page):
    if request.user.is_authenticated:
        curr_user = request.user
        super_user = 1

        if super_user == False:
            if page == 0:
                 QuerySet = Task.objects.filter(date_closing__isnull=False, initiator = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))).order_by('-num_doc').prefetch_related('initiator', 'status')
            elif page == 1:
                 QuerySet = Task.objects.filter(date_closing__isnull=True, initiator = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))).order_by('-num_doc').prefetch_related('initiator', 'status')
            else:
                 QuerySet = Task.objects.filter(initiator = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))).order_by('-num_doc').prefetch_related('initiator', 'status')
        else:
            if page == 0:
                 QuerySet = Task.objects.filter(date_closing__isnull=False).order_by('-num_doc').prefetch_related('initiator', 'status')
            elif page == 1:
                 QuerySet = Task.objects.filter(date_closing__isnull=True).order_by('-num_doc').prefetch_related('initiator', 'status')
            else:
                 QuerySet = Task.objects.order_by('-num_doc').prefetch_related('initiator', 'status')


        return render(request, 'base_idx.html', {'QuerySet': QuerySet, 'current_user': curr_user})
    else:
        return HttpResponseRedirect('/login/')

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.num_doc = (Task.objects.aggregate(Max('num_doc'))['num_doc__max'] + 1)
            form.instance.initiator = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))
            form.instance.status = Status.objects.get(id=1)
            form.instance.executor = None
            form.save()

            return HttpResponseRedirect('/')
        else:
            raise form.ValidationError('Форма заполнена не верно!')

    form = TaskForm()
    data = { 'form': form, }

    return render(request, 'crud/create_task.html', data)