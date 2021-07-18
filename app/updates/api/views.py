from django.views.generic import View
from django.http import HttpResponse

from updates.models import UpdateModel


class UpdateModelDetailAPI(View):
    def get(self, request, id, *args, **kwargs):
        obj = UpdateModel.objects.filter(id=id)
        print('found object', obj)
        json_response = obj.serialize()
        return HttpResponse(json_response, content_type='application/json')

    def post(self, request, *args, **kwargs):
        return HttpResponse({}, content_type='application/json')

    def put(self, request, *args, **kwargs):
        return HttpResponse({}, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        return HttpResponse({}, content_type='application/json')


class UpdateModelListAPI(View):
    def get(self, request, *args, **kwargs):
        qs = UpdateModel.objects.all()
        json_response = qs.serialize()
        return HttpResponse(json_response, content_type='application/json')

    def post(self, request, *args, **kwargs):
        return HttpResponse({}, content_type='application/json')
