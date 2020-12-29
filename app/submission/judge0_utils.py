import base64
import os

import requests
from django.core.cache import cache
from rest_framework.status import HTTP_201_CREATED
from requests_futures.sessions import FuturesSession

from question.models import Testcase
from submission.models import Verdict


def b64_encode(s):
    return base64.b64encode(s.encode('utf-8')).decode("utf8")


def submit_to_run(lang, code, stdin, callback_url):
    url = '{}/submissions?base64_encoded=true'.format(
        os.environ['JUDGE0_BASE_URL'])
    data = {
        "source_code": code,
        "language_id": lang['judge0_lang_id'],
        "number_of_runs": "1",
        "stdin": stdin,
        "cpu_time_limit": lang['cpu_time_limit'],
        "cpu_extra_time": "0.5",
        "wall_time_limit": lang['wall_time_limit'],
        "memory_limit": lang['mem_limit'],
        "stack_limit": lang['stack_limit'],
        "max_processes_and_or_threads": lang['process_limit'],
        "enable_per_process_and_thread_time_limit": False,
        "enable_per_process_and_thread_memory_limit": False,
        "max_file_size": lang['filesize_limit'],
        "callback_url": callback_url
    }
    res = requests.post(url, json=data)
    if res.status_code == HTTP_201_CREATED and 'token' in res.json():
        return res.json()['token']
    raise Exception('Judge0 Error:', res)


#
def submit_to_submit(sub, lang, code, que_id, callback_url):
    url = '{}/submissions/batch?base64_encoded=true'.format(
        os.environ['JUDGE0_BASE_URL'])
    data = {
        'submissions': []
    }

    # get testcases for the submission
    test_cases = Testcase.objects.filter(que_id=que_id)

    # bulk create verdicts
    verdicts = []
    for tc in test_cases:
        verdicts.append(Verdict(test_case=tc, submission=sub))
    verdicts = Verdict.objects.bulk_create(verdicts)

    for verdict in verdicts:
        tc = verdict.test_case
        sub_obj = {"source_code": code, "language_id": lang['judge0_lang_id'],
                   "number_of_runs": "1",
                   "cpu_time_limit": lang['cpu_time_limit'],
                   "cpu_extra_time": "0.5",
                   "wall_time_limit": lang['wall_time_limit'],
                   "memory_limit": lang['mem_limit'],
                   "stack_limit": lang['stack_limit'],
                   "max_processes_and_or_threads": lang['process_limit'],
                   "enable_per_process_and_thread_time_limit": False,
                   "enable_per_process_and_thread_memory_limit": False,
                   "max_file_size": lang['filesize_limit'],
                   "callback_url": '{}/{}'.format(callback_url, verdict.id),
                   'stdin': cache.get('tc_{}_input'.format(tc.id)),
                   'expected_output': cache.get('tc_{}_output'.format(tc.id))
                   }

        # check if files exist in cache
        # print(sub_obj['stdin'])

        if not sub_obj['stdin']:
            print('input not in cache')
            with tc.input.open('r') as f:
                sub_obj['stdin'] = b64_encode(f.read())
                cache.set('tc_{}_input'.format(tc.id),
                          sub_obj['stdin'], 2 * 60 * 60)
                f.close()

        if not sub_obj['expected_output']:
            print('output not in cache')
            with tc.output.open('r') as f:
                sub_obj['expected_output'] = b64_encode(f.read())
                cache.set('tc_{}_output'.format(tc.id),
                          sub_obj['expected_output'], 2 * 60 * 60)
                f.close()

        data['submissions'].append(sub_obj)
    session = FuturesSession()
    session.post(url, json=data)
    return
    # if res.status_code == HTTP_201_CREATED:
    #     return
    # # TODO: Judge 0 Error Handling
    # raise Exception('Judge0 Error:', res)
