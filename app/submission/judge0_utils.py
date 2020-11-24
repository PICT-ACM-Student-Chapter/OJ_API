import base64
import os

import requests
from rest_framework.status import HTTP_201_CREATED

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
    res = requests.post(url, json=data).json()
    if 'token' in res:
        return res['token']
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

    for tc in test_cases:
        verdict = Verdict.objects.create(test_case=tc, submission=sub)
        sub_obj = {
            "source_code": code,
            "language_id": lang['judge0_lang_id'],
            "number_of_runs": "1",
            "stdin": "",
            "expected_output": "",
            "cpu_time_limit": lang['cpu_time_limit'],
            "cpu_extra_time": "0.5",
            "wall_time_limit": lang['wall_time_limit'],
            "memory_limit": lang['mem_limit'],
            "stack_limit": lang['stack_limit'],
            "max_processes_and_or_threads": lang['process_limit'],
            "enable_per_process_and_thread_time_limit": False,
            "enable_per_process_and_thread_memory_limit": False,
            "max_file_size": lang['filesize_limit'],
            "callback_url": '{}/{}'.format(callback_url, verdict.id)
        }

        with tc.input.open('r') as f:
            sub_obj['stdin'] = b64_encode(f.read())
            f.close()

        with tc.output.open('r') as f:
            sub_obj['expected_output'] = b64_encode(f.read())
            f.close()

        data['submissions'].append(sub_obj)
        print(data)

    res = requests.post(url, json=data)
    if res.status_code == HTTP_201_CREATED:
        return

    raise Exception('Judge0 Error:', res)
