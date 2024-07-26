import requests
import config
import json


class CompletionExecutor:
    def __init__(self):
        first_interview = config.first_interview
        self._host = first_interview['host']
        self._api_key = first_interview['api_key']
        self._api_key_primary_val = first_interview['api_key_primary_val']
        self._request_id = first_interview['request_id']

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
                            full_response += data["message"]["content"]
            str = full_response.strip()
            return str.split("질문 :")[1]

    def first_interview(self, image_summary):
        preset_text = [{"role": "system",
                        "content": "- 텍스트로 설명한 이미지에 대한 질문을 생성하는 AI입니다.\n- 이 질문은 조부모님과 손주, 자식들이 사진을 보며 사진에 대한 회상을 하는 듯한 모습을 연상하게 하도록 합니다.\n- 질문은 이후에도 계속 이어질 예정입니다.\n- 여러 개의 이미지에 대한 답변이 순서 없이 입력되고 chatID를 부여해서 구분을 하고 추가 질문을 이어갑니다.\n- 두번째 대답 이후에는 chatID와 대답으로 이루어져있습니다.\n- chatID는 다른 이미지에 대한 내용과 구분할 수 있도록 UUID를 임의로 생성해서 부여합니다. chatID 예시: fec735e8-4df3-4acf-aa73-482ab1088c06\n- 질문을 생성 할 때에는 chatID를 확인하고 해당되는 대답에 맞는 질문을 생성합니다.\n- 최초 질문은 이미지를 기반으로 생성하고, 두번째 이후 질문부터는 첫번째 답변과 설명된 이미지 두가지에 연관된 질문을 합니다.\n- 최초 질문은 구체적인 질문보다 배경의 장소, 함께 한 사람, 특별한 날 등의 포괄적인 질문의 내용으로 구성합니다.\n- 질문 이전에 사용자와의 공감을 하는 짧은 문구를 넣어 질문합니다.\n- 이 시스템을 사용하는 사람은 할머니, 할아버지야 자식들이 다정하게 질문하듯 질문해주고 질문 내용 수준을 할머니, 할아버지가 잘 이해할 수 있도록합니다.\n- 주로 할 질문은 어디인지, 누구와 함께 했는지, 무얼 했는지, 무얼 먹었는지에 대한 내용입니다.\n\n### \n설명 이미지: 사진에는 두 사람이 있습니다. 한 사람은 생일 케이크를 머리 위에 들고 있고, 다른 사람은 꽃다발을 들고 있습니다. 둘 다 즐거운 표정을 짓고 있으며, 재미있는 분위기를 풍기고 있습니다. 배경은 목재로 되어 있어 따뜻한 느낌을 줍니다. 전체적으로 축하하는 순간을 담고 있는 것 같습니다.\n질문: 생일 케이크가 보이네요! 특별한 날인가봐요?\nchatID: "},
                       {"role": "user",
                        "content": image_summary}]

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

        return self.__execute__(request_data)
