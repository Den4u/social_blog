from http import HTTPStatus

from django.shortcuts import render
from django.views.generic.base import TemplateView


class About(TemplateView):
    """Вью о нас."""

    template_name = 'pages/about.html'


class Rules(TemplateView):
    """Вью правила."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=HTTPStatus.NOT_FOUND)


def server_error(request):
    return render(request, 'pages/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=HTTPStatus.FORBIDDEN)
