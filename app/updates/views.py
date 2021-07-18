from django.db.models import fields
from django.http.response import HttpResponse
from django.shortcuts import render
from .mixinx import JsonResponseMixin
from django.views.generic import View
from django.http import JsonResponse
from django.core.serializers import serialize

from .models import UpdateModel


def update_model_detail_view(request):

    data = {
        'welcome': "Welcome to Django"
    }

    return JsonResponse(data)


class UpdateDetailView(View):
    """ update view class based view """

    def get(self, request, *args, **kwargs):
        data = {
            'welcome': "Welcome to Django"
        }

        return JsonResponse(data)


class JsonView(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {'welcome': "Welcome to Django"}
        return self.render_to_json_response(data)


class SerializerListView(View):
    def get(self, request, *args, **kwargs):

        qs = UpdateModel.objects.all().serialize()
        # data = serialize('json', qs, fields=('user', 'content'))

        return HttpResponse(qs, content_type='application/json')


class SerializerDetailsView(View):
    def get(self, request, *args, **kwargs):

        qs = UpdateModel.objects.get(pk=1).serialize()
        # data = serialize('json', [qs.serialize()], fields=('user', 'content'))

        return HttpResponse(qs, content_type='application/json')
