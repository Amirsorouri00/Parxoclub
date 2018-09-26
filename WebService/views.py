from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

# This is just for test
def test(Request):
    json_data = '{"hello": "world", "foo": "bar"}' 
    data = json.loads(json_data)
    return HttpResponse(json.dumps(data), content_type='application/json')