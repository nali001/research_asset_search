import os
from dotenv import load_dotenv

import json
from django.shortcuts import render
from django.http import JsonResponse

from .utils import save_record_to_mongo, assign_user_condition


def user_study_start(request):
    # show the task description
    return render(request, 'user_study_start.html')

def register(request):
    # your code here
    return render(request, 'user_study_register.html')


def information_survey(request):
    # your code here
    record = json.loads(request.body.decode('utf-8'))
    condition = assign_user_condition()
    record['assigned_condition'] = condition
    saved_id = save_record_to_mongo(record)
    
    if saved_id:
        return JsonResponse({'assigned_condition': condition})


def log_user_activity(request):
    # your code here
    record = json.loads(request.body.decode('utf-8'))
    saved_id = save_record_to_mongo(record)
    if saved_id:
        return JsonResponse({'status': 'success'})


def guide(request):
    # create the interactive guide for the search system.
    return render(request, 'user_study_guide.html')

def pretest(request):
    # your code here
    pass

def intro_step(request):
    # create the interactive guide for the search system.
    return render(request, 'user_study_guide.html')

def task(request):
    # your code here
    pass

def posttest(request):
    # your code here
    pass
