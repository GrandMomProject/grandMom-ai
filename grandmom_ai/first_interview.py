import requests
import config
import json


class CompletionExecutor:
    def __init__(self):
        clova_studio = config.clova_studio
        self._host = clova_studio['host']
        self._api_key = clova_studio['api_key']
        self._api_key_primary_val = clova_studio['api_key_primary_val']
        self._request_id = clova_studio['first_interview_request_id']

    def __execute__(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True) as r:
            full_response = ""
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data:"):
                        data = json.loads(decoded_line[len("data:"):])
                        if "message" in data and "content" in data["message"]:
                            full_response = data["message"]["content"]
            return full_response.strip()

    def get_first_interview(self, image_summary):
        preset_text = [{"role": "system",
                        "content": "1. 사용자의 chatHistory와 사용자의 답변에 대해 추가적인 질문을 제공합니다.\n2. chatHistory는 배경과 질의응답 목록으로 구성되어있습니다.\n3. 시스템은 사용자의 자녀 혹은 손주입니다.\n4. 시스템은 사용자와 함께 사진을 보며 사용자의 추억을 공유하는 중입니다.\n5. 질문의 처음에는 짧은 공감이 들어가고 이후에 질문이 들어갑니다. 공감 이후 꼭 질문이 들어갑니다.\n6. 질문의 내용은 70대 정도의 노인이 이해하기 쉬운 수준으로 질문합니다.\n7. 질문은 한글 약 100글자 이내로 합니다.\n8. 주된 질문 목록입니다. [무엇을 했는지, 그때의 기분이 어떤지] 이 주된 질문 목록을 우선으로 하되 맥락에 맞는 질문을 합니다.\n9. chatHistory에 있는 질문을 파악하여 같은 내용에 대한 질문은 하지 않습니다.\n10. chatHistory속에 이미 질의응답 한 내용이 있다면 chatHistory 속 배경과 마지막 대답에 연관된 질문을 합니다.\n11. 어조는 다정하게 해줘\n\n\n예시:\n\"chatHistory\": {\n\"배경\": \"사진에는 바닷가에서 웃고 있는 두 사람이 보입니다. 한 사람은 다른 사람을 안고 있으며, 그 사람은 팔을 하늘로 쭉 뻗고 있는 모습입니다. 배경에는 맑은 하늘과 푸른 바다가 펼쳐져 있으며, 해변의 모래가 보입니다. 전반적으로 행복한 순간을 즐기고 있는 듯한 분위기가 느껴집니다.\",\n\"질의응답\": [\n{\"질문\": \"두 분이 바닷가에서 정말 행복해 보이시네요. 언제 여행을 가셨던 건가요?\", \"대답\":\"작년 여름에 속초해변으로 여자친구랑 놀러간 사진이야\"}, {\"질문\": \"여름에 속초에 놀러가셨다니 듣기만해도 너무 시원해지는 기분이에요. 속초에 가셔서 또 무엇을 하셨나요?\", \"대답\":\"물회랑, 고기랑 배터지게 먹었어 아주 진수성찬이었어\"}]\n}\n\"질문\": \"진수성찬이었다니 듣기만 해도 배가 부른데요. 그날의 기분은 어떠셨나요?\"\n\n\n"},
                       {"role": "user", "content": image_summary}]

        request_data = {
            'messages': preset_text,
            'topP': 0.6,
            'topK': 0,
            'maxTokens': 512,
            'temperature': 0.3,
            'repeatPenalty': 2.5,
            'stopBefore': ['###', '설명:', '질문:', '###'],
            'includeAiFilters': True,
            'seed': 0
        }

        response = self.__execute__(request_data)
        print(response)
        try:
            response_double = response.split('질문')[1]
        except IndexError:
            response_double = response

        return response_double
