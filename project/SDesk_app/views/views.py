from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import DetailView
from django.db.models import Max, Q

from ..models import Task, Profile, StaffPosition, PermissionLevel, Status
from ..forms import LoginForm, RegisterForm, TaskForm
from .msg_handlers import success_msg
from .button_handlers import get_count_task


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
    return render(request, 'auth/login.html', {'form': form})

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
                user=User.objects.get(id=(User.objects.get(username=form.cleaned_data.get('username')).pk)),
                system_name=form.cleaned_data.get('username'),
                last_name=form.cleaned_data.get('last_name'),
                first_name=form.cleaned_data.get('first_name'),
                staff_position=StaffPosition.objects.get(position_name='Не оформлена'),
                permission_level=PermissionLevel.objects.get(level_code='UNC')
            )

            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def list(request, selector):
    """
    Процедура формирования отображения списка задач.
    0 - Завершенные задачи
    1 - Не принятые задачи
    2 - Активные задачи
    """
    if request.user.is_authenticated:
        current_user = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))

        if current_user.super_user == False:
            if selector == 0:
                QuerySet = (Task.objects.filter(Q(is_closed=True) & (Q(initiator=current_user) | Q(executor=current_user)))
                            .order_by('-num_doc').prefetch_related('initiator', 'status'))
            elif selector == 1:
                QuerySet = (Task.objects.filter((Q(status=Status.objects.get(status_code='CPL')) | Q(status=Status.objects.get(status_code='RJT'))) & (Q(initiator=current_user) | Q(executor=current_user)))
                            .order_by('-num_doc').prefetch_related('initiator', 'status'))
            elif selector == 2:
                QuerySet = (Task.objects.filter(Q(is_closed=False) &  (Q(initiator=current_user) | Q(executor=current_user)))
                            .order_by('-num_doc').prefetch_related('initiator', 'status'))
            else:
                QuerySet = (Task.objects.filter(Q(initiator=current_user) | Q(executor=current_user))
                            .order_by('-num_doc').prefetch_related('initiator', 'status'))
        else:
            if selector == 0:
                QuerySet = Task.objects.filter(is_closed=True).order_by('-num_doc').prefetch_related('initiator', 'status')
            elif selector == 1:
                QuerySet = Task.objects.filter(Q(status=Status.objects.get(status_code='CPL')) | Q(status=Status.objects.get(status_code='RJT'))).order_by('-num_doc').prefetch_related('initiator', 'status')
            elif selector == 2:
                QuerySet = Task.objects.filter(is_closed=False).order_by('-num_doc').prefetch_related('initiator', 'status')
            else:
                QuerySet = Task.objects.order_by('-num_doc').prefetch_related('initiator', 'status')

        paginator = Paginator(QuerySet, 10)
        page_number = request.GET.get("page")
        QuerySet = paginator.get_page(page_number)
        count_task = get_count_task(request, current_user)
        return render(request, 'base_idx.html', {'QuerySet': QuerySet, 'current_user': request.user, 'counts': count_task})
    else:
        return HttpResponseRedirect('/login/')

@login_required
def create_task(request):
    """
    Процедула создания новой задачи пользователем.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.num_doc = (Task.objects.aggregate(Max('num_doc'))['num_doc__max'] + 1)
            form.instance.initiator = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))
            form.instance.status = Status.objects.get(status_code='REG')
            form.instance.executor = None
            form.save()

            msg = f'Задача "{form.instance.num_doc}" успешно зарегистрирована и направлена на распределение.'
            return success_msg(request, msg=msg, reverse_url='/')
        else:
            raise form.ValidationError('Форма заполнена не верно!')

    form = TaskForm()
    return render(request, 'crud/create_task.html', {'form': form, 'current_user': request.user})

class TaskDetail(LoginRequiredMixin, DetailView):
    """
    Детализированная форма задачи.
    """
    model = Task
    template_name = 'crud/task_detail.html'

    def get_context_data(self, *args, **kwargs):
        cd = super().get_context_data(*args, **kwargs)
        current_user = self.request.user
        cd['current_user'] = current_user
        return cd