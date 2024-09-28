import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render
from django.views.generic import DeleteView

from ..mixins import AdminRequiredMixin
from ..models import Task, Profile, Status
from .msg_handlers import success_msg, error_msg
from ..forms import CompleteAndRejectUpdateForm, ExecUpdateForm

@login_required
def TaskComplete(request, pk):
    """
    Операция Выполнения задачи исполнителем
    :param request:
    :param task_pk:
    :return:
    """
    user = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))
    task = Task.objects.get(pk=pk)
    if ((task.executor == user) or user.super_user):
        if not task.is_closed:
            if request.POST:
                form = CompleteAndRejectUpdateForm(request.POST)
                if form.is_valid():
                    form.save(commit=False)
                    task.answer = form.cleaned_data['answer']
                    task.status = Status.objects.get(status_code="CPL")
                    task.stop_exec_at = datetime.datetime.now()
                    task.closing_at = datetime.datetime.now()
                    task.save()
                    return success_msg(request, msg=f'Задача №{task.num_doc} успешно выполнена.', reverse_url=f'/task/{pk}/')
            context = {'form': CompleteAndRejectUpdateForm, 'current_user': user, 'operation': 'Выполнить'}
            return render(request, template_name='crud/answer_update.html', context=context)
        else:
            return error_msg(request, msg='Операция выполнения невозможна над закрытыми задачами!', reverse_url=f'/task/{pk}/')
    else:
        return error_msg(request, msg='Операция "Выполнения" недоступна, вы не являетесь исполнителем задачи!', reverse_url=f'/task/{pk}/')

@login_required
def TaskReject(request, pk):
    """
    Процедура отклонения задачи исполнителем и оформления ответа инициатору
    :param request:
    :param pk:
    :return:
    """
    user = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))
    task = Task.objects.get(pk=pk)
    if user == task.executor:
        if not task.is_closed:
            if request.POST:
                form = CompleteAndRejectUpdateForm(request.POST)
                if form.is_valid():
                    form.save(commit=False)
                    task.answer = form.cleaned_data['answer']
                    task.status = Status.objects.get(status_code='RJT')
                    task.stop_exec_at = datetime.datetime.now()
                    task.save()
                    msg = f'Задача №{task.num_doc} была отклонена и переведена в состояние "Отклонено".'
                    return success_msg(request, msg=msg, reverse_url='/')

            context = {'form': CompleteAndRejectUpdateForm, 'current_user': user, 'operation': 'Отклонить'}
            return render(request, template_name='crud/answer_update.html', context=context)

        else:
            return error_msg(request, f'Задача №{task.num_doc} является закрытой и не может быть отклонена!', reverse_url=f'/task/{pk}/')
    else:
        return error_msg(request, 'Невозможно отклонить задачу не являясь её исполнителем!', reverse_url=f'/task/{pk}/')


@login_required
def TaskAccept(request, pk):
    user = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))
    task = Task.objects.get(pk=pk)
    if not task.is_closed:
        if task.status == Status.objects.get(status_code='CPL') or task.status == Status.objects.get(status_code='RJT'):
            if task.initiator == user:
                new_status = Status.objects.get(status_code='ACP')
                task.status = new_status
                task.is_closed = True
                task.closing_at = datetime.datetime.now()
                task.save()

                return success_msg(request, msg='Задача успешно завершена!', reverse_url='/')
            else:
                return error_msg(request, msg='Принять задачу может только её инициатор!', reverse_url=f'/task/{pk}/')
        else:
            return error_msg(request, msg='Для принятия исполнителем задачи она должна находиться в состоянии "Исполнена" или "Отклонено"!', reverse_url=f'/task/{pk}/')
    else:
        return error_msg(request, msg='Невозможно принять закрытую задачу!', reverse_url=f'/task/{pk}/')

@login_required
def TaskRevoke(request, pk):
    """
    Процедура отзыва задача создавшим его её пользователем.
    :param request:
    :param pk:
    :return:
    """
    user = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))
    task = Task.objects.get(pk=pk)
    if task.initiator == user and not task.is_closed:
        task.status = Status.objects.get(status_code='RVK')
        task.is_closed = True
        task.closing_at = datetime.datetime.now()
        task.save()
        msg = f'Задача "{task.num_doc} - {task.title}" Вами была успешно отозвана.'
        return success_msg(request, msg=msg, reverse_url='/')

    return error_msg(request, msg='Операция недоступна т.к. задача имеет признак "ЗАКРЫТА" или вы не являетесь её инициатором.', reverse_url=f'/task/{pk}/')


@login_required
def ExecUpdate(request, pk):
    """
    Процедура назначения администратором системы исполнителя задачи.
    :param request:
    :param pk:
    :return:
    """
    user = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))
    task = Task.objects.get(pk=pk)
    if user.super_user:
        if request.POST:
            form = ExecUpdateForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                task.executor = form.cleaned_data['executor']
                task.status = Status.objects.get(status_code='WRK')
                task.start_exec_at = datetime.datetime.now()
                task.save()

                msg = f'Исполнитель для задачи успешно назначен!'
                return success_msg(request, msg=msg, reverse_url='/')

        context = { 'form': ExecUpdateForm(), 'current_user': user}
        return render(request, template_name='crud/task_update.html', context=context)
    else:
        return error_msg(request, 'Вы не имеете прав для назначения исполнителей задач.', f'/task/{pk}/')


class TaskDelete(AdminRequiredMixin, DeleteView):
    """
    Процедура удаления задачи.
    """
    model = Task
    template_name = 'crud/task_delete.html'
    success_url = '/'


def get_count_task(request, current_user):
    """
    Счётчик количества задач в раных состояниях
    :param request:
    :param current_user:
    :return:
    """
    counts = dict()
    if not current_user.super_user:
        counts['active'] = (list(Task.objects.filter(
            Q(is_closed=False) & (Q(initiator=current_user) | Q(executor=current_user))).aggregate(
            count=Count('pk', distinct=True)).values()))[0]
        counts['un_accepted'] = (list(Task.objects.filter(Q(status=Status.objects.get(status_code='CPL')) | Q(status=Status.objects.get(status_code='RJT')) & (
                    Q(initiator=current_user) | Q(executor=current_user))).aggregate(count=Count('pk', distinct=True)).values()))[0]
        counts['closed'] = (list(Task.objects.filter(
            Q(is_closed=True) & (Q(initiator=current_user) | Q(executor=current_user))).aggregate(
            count=Count('pk', distinct=True)).values()))[0]
    else:
        counts['active'] = (list(Task.objects.filter(is_closed=False).aggregate(count=Count('pk', distinct=True)).values()))[0]
        counts['un_accepted'] = (list(Task.objects.filter(Q(status=Status.objects.get(status_code='CPL')) | Q(status=Status.objects.get(status_code='RJT'))).aggregate(count=Count('pk', distinct=True)).values()))[0]
        counts['closed'] = (list(Task.objects.filter(is_closed=True).aggregate(count=Count('pk', distinct=True)).values()))[0]

    return counts