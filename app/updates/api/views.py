from json import loads, dumps
import json
from django.views.generic import View

from updates.models import UpdateModel
from updates.forms import UpdateModelForm
from .mixins import CSRFExempt, ResponseMixins, JsonCheckMixin


class UpdateModelDetailAPI(ResponseMixins, CSRFExempt, JsonCheckMixin, View):
    def get_object(self, id=None):
        qs = UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs
        return None

    def get(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            return self.render_to_response(dumps({"message": "Object not found"}), status_code=404)
        print('found object', obj)
        json_response = obj.serialize()
        return self.render_to_response(json_response)

    def post(self, request, *args, **kwargs):
        data = {'message': "Method not allowed, use create endpoint"}
        return self.render_to_response(dumps(data), status_code=403)

    def put(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            return self.render_to_response(dumps({"message": "Object not found"}), status_code=404)
        print('found object', obj)
        if not self.check_json(request.body):
            return self.render_to_response({"message": "Invalid json, send valid json"}, status_code=401)
        print("PUT {}".format(request.body))

        json_response = obj.serialize()
        print("json response: {} type:{}".format(
            json_response, type(json_response)))
        data = json.loads(json_response)
        print("______________\ndata:{} type:{}".format(data, type(data)))
        passed_data = json.loads(request.body)
        for key, value in passed_data.items():
            data[key] = value
        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            print("obj :{} type:{}".format(obj, type(obj)))
            return self.render_to_response(data, status_code=202)
        else:
            data = dumps(form.errors)
            return self.render_to_response(data, status_code=403)
        return self.render_to_response(json_response)

    def delete(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            return self.render_to_response(dumps({"message": "Object not found"}), status_code=404)
        obj.delete()
        return self.render_to_response(dumps({"message": "Object remove"}), status_code=204)


class UpdateModelListAPI(ResponseMixins, CSRFExempt, JsonCheckMixin, View):
    def get(self, request, *args, **kwargs):
        qs = UpdateModel.objects.all()
        json_response = qs.serialize()
        print("Json Response:{}".format(json_response))
        return self.render_to_response(json_response, status_code=200)

    def post(self, request, *args, **kwargs):
        data = dumps({"message": "Success"})
        if not self.check_json(request.body):
            return self.render_to_response({"message": "Invalid json, send valid json"}, status_code=401)
        print("posted data {}".format(request.POST))
        form = UpdateModelForm(loads(request.body))
        if form.is_valid():
            obj = form.save(commit=True)
            print("obj :{} type:{}".format(obj, type(obj)))
            return self.render_to_response(data, status_code=201)
        else:
            data = dumps(form.errors)
            return self.render_to_response(data, status_code=403)
        return self.render_to_response(data, status_code=200)
