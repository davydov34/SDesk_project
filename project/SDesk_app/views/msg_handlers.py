from django.shortcuts import render

def success_msg(request, msg, reverse_url):
    context = {
        'current_url': reverse_url,
        'msg': msg,
        'current_user': request.user,
    }
    return render(request, template_name='messages/success.html', context=context)

def error_msg(request, msg, reverse_url):
    context = {
        'current_url': reverse_url,
        'msg': msg,
        'current_user': request.user,
    }
    return render(request, template_name='messages/error.html', context=context)