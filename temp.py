# -*- coding: utf-8 -*-

import requests


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-DASH-001',
                           headers=headers, json=completion_request, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    print(line.decode("utf-8"))


if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiYxtLUvLtXVd9pCNGnA+Tbg5NkCQnNTOxpD3bKNQy06HJ',
        api_key_primary_val='FkXDXR8eAdnFbGka30FZ03JtbiYMZoC7vD2NMqQe',
        request_id='7d1d5b9f-72b9-47ca-a25a-16933d811450'
    )

    preset_text = [{"role":"system","content":"1. 사용자의 이미지요약에 대해 질문을 제공합니다.\n2. 시스템은 사용자의 자녀 혹은 손주입니다.\n3. 시스템은 사용자와 함께 사진을 보며 사용자의 추억을 공유하는 중입니다.\n4. 질문의 처음에는 짧은 공감이 들어가고 이후에 질문이 들어갑니다. 공감 이후 꼭 질문이 들어갑니다.\n5. 질문은 구체적인 질문보다 배경의 장소, 함께 한 사람, 특별한 날 등의 포괄적인 질문의 내용으로 구성합니다.\n6. 질문의 내용은 70대 정도의 노인이 이해하기 쉬운 수준으로 질문합니다.\n7. 질문은 한글 약 100글자 이내로 합니다.\n8. 주된 질문 목록입니다. [어디서, 누구와, 무엇을 했는지, 무엇을 먹었는지] 이 주된 질문 목록을 우선으로 하되 맥락에 맞는 질문을 합니다.\n9. 다정한 어조를 사용합니다.\n\n\n예시:\n\"이미지요약\": \"사진에는 바닷가에서 웃고 있는 두 사람이 보입니다. 한 사람은 다른 사람을 안고 있으며, 그 사람은 팔을 하늘로 쭉 뻗고 있는 모습입니다. 배경에는 맑은 하늘과 푸른 바다가 펼쳐져 있으며, 해변의 모래가 보입니다. 전반적으로 행복한 순간을 즐기고 있는 듯한 분위기가 느껴집니다.\"\n\"질문\": \"두 분이 바닷가에서 정말 행복해 보이시네요. 어디로 여행을 가셨던 건가요?\"\n\n\n"},{"role":"user","content":""}]

    request_data = {
        'messages': preset_text,
        'topP': 0.6,
        'topK': 0,
        'maxTokens': 512,
        'temperature': 0.3,
        'repeatPenalty': 1.2,
        'stopBefore': ['###', '설명:', '질문:', '###'],
        'includeAiFilters': True,
        'seed': 0
    }

    print(preset_text)
    completion_executor.execute(request_data)
