# # -*- coding: utf-8 -*-
#
# import requests
#
#
# class CompletionExecutor:
#     def __init__(self, host, api_key, api_key_primary_val, request_id):
#         self._host = host
#         self._api_key = api_key
#         self._api_key_primary_val = api_key_primary_val
#         self._request_id = request_id
#
#     def execute(self, completion_request):
#         headers = {
#             'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
#             'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
#             'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
#             'Content-Type': 'application/json; charset=utf-8',
#             'Accept': 'text/event-stream'
#         }
#
#         with requests.post(self._host + '/testapp/v1/chat-completions/HCX-DASH-001',
#                            headers=headers, json=completion_request, stream=True) as r:
#             for line in r.iter_lines():
#                 if line:
#                     print(line.decode("utf-8"))
#
#
# if __name__ == '__main__':
#     completion_executor = CompletionExecutor(
#         host='https://clovastudio.stream.ntruss.com',
#         api_key='NTA0MjU2MWZlZTcxNDJiYxtLUvLtXVd9pCNGnA+Tbg5NkCQnNTOxpD3bKNQy06HJ',
#         api_key_primary_val='FkXDXR8eAdnFbGka30FZ03JtbiYMZoC7vD2NMqQe',
#         request_id='0286bad4-a5ab-4ff2-ac89-b3e4e798cd1b'
#     )
#
#
#
#     print(preset_text)
#     completion_executor.execute(request_data)
