from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission

from t3kys import settings


def profileCheck(function):
    def wrap(request, *args, **kwargs):
        tc = request.user.profile.tc
        birthday = request.user.profile.birthday
        if (tc == None) or (tc == "") or (request.user.first_name == "") or (request.user.last_name == ""):
            return redirect('stakeholders/:profileDetail')
        return function(request, *args, **kwargs)

    return wrap


def authorityCheck(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='PERSONEL').exists():
            return function(request, *args, **kwargs)
        else:
            return redirect('externalMainPage')

    return wrap


def permissionCheck(modelInfo, permissionInfo):
    def methodWrap(viewMethod):

        def wrap(request, *args, **kwargs):
            status = False
            permissions = Permission.objects.filter(group__user=request.user).filter(
                content_type__model=modelInfo).filter(
                codename=permissionInfo)
            if permissions:
                status = True
            elif request.user.is_staff:
                status = True
            else:
                status = False

            if status == False:
                return redirect(settings.PERMISSION_DENIED_PAGE_URL)

            return viewMethod(request, *args, **kwargs)

        return wrap

    return methodWrap
