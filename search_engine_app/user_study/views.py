import os
from dotenv import load_dotenv

import json
from django.shortcuts import render
from django.http import JsonResponse
from urllib.parse import unquote

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
    # condition = assign_user_condition()
    condition = assign_user_condition(record['userId'])
    record['assigned_condition'] = condition
    saved_id = save_record_to_mongo(record)
    
    if saved_id:
        return JsonResponse({'assigned_condition': condition})


def log_user_activity(request):
    # save user activity log
    record = json.loads(request.body.decode('utf-8'))
    saved_id = save_record_to_mongo(record)
    if saved_id:
        return JsonResponse({'status': 'success'})


def guide(request):
    # create the interactive guide for the search system.
    return render(request, 'user_study_guide.html')

def pretest(request):
    # process the pretest survey
    pass

def intro_step(request):
    # create the interactive guide for the search system.
    return render(request, 'user_study_guide.html')

def task(request):
    # task innformation
    pass

def posttest(request):
    # process the posttest survey
    pass


def task_assignment(request):
    # assign a task to the user, including the whether the user is in the control or experimental group, and the research question to answer.
    # breakpoint()
    body = unquote(request.body.decode('utf-8'))
    body = json.loads(body)
    condition, task_id, task  = assign_user_condition(body['userId'])
    return JsonResponse({'condition': condition, 'taskId': task_id, 'task': task})