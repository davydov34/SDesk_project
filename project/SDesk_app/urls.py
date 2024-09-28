from django.urls import path

from .views.views import (login_view,
                          logout_view,
                          register_view,
                          create_task,
                          list,
                          TaskDetail)

from .views.button_handlers import (TaskComplete,
                                    TaskReject,
                                    TaskAccept,
                                    TaskDelete,
                                    TaskRevoke,
                                    ExecUpdate)

urlpatterns = [
    #Пользователь
    path('login/', login_view, name='Login'),
    path('logout/', logout_view, name='Logout'),
    path('register/', register_view, name='Register'),

    #Отображения selctor
    path('create_task/', create_task, name='Create task'),
    path('', list, {'selector': 3}, name='DefaultQuerySet'),
    path('<int:selector>/', list, name='QuerySet'),
    path('task/<slug:pk>/', TaskDetail.as_view(), name='Task detail'),

    #Операции над задачей
    path('task/<int:pk>/complete/', TaskComplete, name='Complete'),
    path('task/<int:pk>/reject/', TaskReject, name='Reject'),
    path('task/<int:pk>/accept/', TaskAccept, name='Accept'),
    path('task/<int:pk>/revoke/', TaskRevoke, name='Revoke'),
    path('task/<int:pk>/exec_update/', ExecUpdate, name='Executor'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='Task delete'),
]
