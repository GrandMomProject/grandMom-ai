import requests
import config
import json

from models import AdditionalInterviewReq


class CompletionExecutorAdd:
    def __init__(self):
        clova_studio = config.clova_studio
        self._host = clova_studio['host']
        self._api_key = clova_studio['api_key']
        self._api_key_primary_val = clova_studio['api_key_primary_val']
        self._request_id = clova_studio['additional_interview_request_id']

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

    def additional_interview(self, additionalInterview: AdditionalInterviewReq):
        chat_history = additionalInterview.chatHistory
        answer = additionalInterview.answer
        content = chat_history + f", \"대답\": \"{answer}\"" + "}]}"
        preset_text = [{"role": "system",
                        "content": "1. 사용자의 chatHistory와 사용자의 답변에 대해 추가적인 질문을 제공합니다.\n2. chatHistory는 배경과 질의응답 목록으로 구성되어있습니다.\n3. 시스템은 사용자의 자녀 혹은 손주입니다.\n4. 시스템은 사용자와 함께 사진을 보며 사용자의 추억을 공유하는 중입니다.\n5. 질문의 처음에는 짧은 공감이 들어가고 이후에 질문이 들어갑니다. 공감 이후 꼭 질문이 들어갑니다.\n6. 질문의 내용은 70대 정도의 노인이 이해하기 쉬운 수준으로 질문합니다.\n7. 질문은 한글 약 100글자 이내로 합니다.\n8. 주된 질문 목록입니다. [어디서, 누구와, 무엇을 했는지, 무엇을 먹었는지] 이 주된 질문 목록을 우선으로 하되 맥락에 맞는 질문을 합니다.\n9. chatHistory속에 이미 질의응답 한 내용이 있다면 chatHistory 속 배경과 마지막 대답에 연관된 질문을 합니다.\n10. 어조는 다정하게 해줘\n\n\n예시:\n\"chatHistory\": {\n\"배경\": \"사진에는 바닷가에서 웃고 있는 두 사람이 보입니다. 한 사람은 다른 사람을 안고 있으며, 그 사람은 팔을 하늘로 쭉 뻗고 있는 모습입니다. 배경에는 맑은 하늘과 푸른 바다가 펼쳐져 있으며, 해변의 모래가 보입니다. 전반적으로 행복한 순간을 즐기고 있는 듯한 분위기가 느껴집니다.\",\n\"질의응답\": [\n{\"질문\": \"두 분이 바닷가에서 정말 행복해 보이시네요. 어디로 여행을 가셨던 건가요?\", \"대답\":\"속초해변이야, 맛있는것도 많이 먹고 참 재밌었지\"}, {\"질문\": 맛있는 것도 많이 드셨다니 좋으셨겠어요. 어떤 음식을 드셨나요?\", \"대답\":\"물회랑, 고기랑 배터지게 먹었어 아주 진수성찬이었어\"}]\n}\n\"질문\": \"진수성찬이었다니 듣기만 해도 배가 부른데요. 누구랑 같이 가셨어요?\"\n\n\n"},
                       {"role": "user",
                        "content": content}]

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
        response = self.__execute__(request_data)
        print(response)
        try:
            response_double = response.split('질문 : ')[1]
        except IndexError:
            response_double = response
        return response_double
