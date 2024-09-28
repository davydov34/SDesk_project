from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages

from .views.msg_handlers import error_msg
from .models import Profile

class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = Profile.objects.get(id=(Profile.objects.get(system_name=request.user).pk))

        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not user.super_user:
            messages.info(request, 'Операция "Удаление" доступна только администраторам системы!')
            return error_msg(request, msg='Операция "Удаление" доступна только администраторам системы!', reverse_url='/')

        return super().dispatch(request, *args, **kwargs)