from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .models import User
from django.http import HttpResponse, Http404
import json



@api_view(['Get'])
def get_user(request, username):
    qs = User.objects.values('username', 'first_name', 'last_name', 'user_locations', 'userRole', 'clinician_id').filter(
        username=username)
    qs = list(qs)
    qs2 = json.dumps(qs, indent=4, sort_keys=True, default=str)
    return HttpResponse(qs2)


@csrf_exempt
def email_reset(request):
    jsonloaded = json.loads(request.body)
    note = jsonloaded['note']
    if note == '':
        raise Http404
    else:
        try:
            user = User.objects.values('username').filter(email=note)
            if str(user) != '<QuerySet []>':
                return HttpResponse(str(user))
            else:
                raise Http404
        except User.DoesNotExist:
            raise Http404

@csrf_exempt
def reset_password_with_token(request, token):
    print(token)
    raise Http404
