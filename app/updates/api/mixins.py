
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import HttpResponse

from .utils import is_valid_json


class CSRFExempt(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResponseMixins(object):

    def render_to_response(self, data, status_code=200):
        if not isinstance(data, str):
            data = json.dumps(data)
        return HttpResponse(data, content_type='application/json', status=int(status_code))


class JsonCheckMixin(object):

    def check_json(self, json_data):
        return is_valid_json(json_data)
