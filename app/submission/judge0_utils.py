import os
import requests


def submit_to_run(lang, code, stdin, callback_url):
    url = '{}/submissions?base64_encoded=true'.format(
        os.environ['JUDGE0_BASE_URL'])
    data = {
        "source_code": code,
        "language_id": lang['judge0_lang_id'],
        "number_of_runs": "1",
        "stdin": stdin,
        "cpu_time_limit": lang['cpu_limit'],
        "cpu_extra_time": "0.5",
        "wall_time_limit": lang['time_limit'],
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
