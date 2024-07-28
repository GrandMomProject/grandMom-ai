import requests
import config
import json

from models import SummaryReq, SummaryRes


class CompletionExecutorSummary:
    def __init__(self):
        clova_studio = config.clova_studio
        self._host = clova_studio['host']
        self._api_key = clova_studio['api_key']
        self._api_key_primary_val = clova_studio['api_key_primary_val']
        self._request_id = clova_studio['summary_request_id']

    @staticmethod
    def __split_res__(response_double: str) -> SummaryRes:
        # 문자열의 맨 앞과 맨 뒤의 대괄호를 제거
        if response_double.startswith("[") and response_double.endswith("]"):
            response_double = response_double[1:-1]

        # **로 구분된 각 원소들의 맨 앞과 맨 뒤의 "를 제거
        diaries = [entry.strip().strip('"') for entry in response_double.split("**")]

        # SummaryRes 인스턴스 생성
        res = SummaryRes(diaries=diaries)
        return res

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

    def get_summary(self, summaryReq: SummaryReq) -> SummaryRes:
        chat_history = summaryReq.chatHistory
        preset_text = [{"role": "system",
                        "content": "1. 주어진 chatHistory를 분석하여 일기를 생성합니다.\n2. chatHistory는 배경과 질의응답 목록으로 구성되어있습니다.\n3. 시스템은 사용자의 자녀 혹은 손주를 대신하는 역할입니다.\n4. 시스템은 사용자와 함께 사진을 보며 사용자의 추억을 공유하는 중입니다.\n5. 일기 하나당 160글자에서 200글자 사이로 작성합니다.\n6. 자녀 혹은 손주가 할머니 할아버지에게 읽어주는 듯 한 느낌이 들도록 다정한 어조로 작성합니다.\n7. 다음 지침을 엄격히 준수하여 업무를 수행하십시오.\n8. chatHistory에 없는 내용은 추가하지 않습니다.\n9. 위의 지침을 철저히 따라 고품질의 일기를 제공합니다.\n10. 하나의 일기의 내용에는 다음 3가지가 포함됩니다. 일기에 대한 요약(사진에 대한 추억을 회상하는 듯한 내용), 임의의 질의응답에 대한 내용, 사용자에게 하는 덕담\n11. 일기에 대한 요약은 어디서 무얼 했지는 반드시 들어갑니다.\n12. 일기에 사용자를 부르는 호칭은 할머니라고 부릅니다.\n13. 일기는 총 3가지 버전으로 작성하며 질의응답에 대한 내용은 각각 다른 내용으로 되어있습니다. 질의응답에 있는 모든 내용이 포함되지 않아도 무관합니다.\n14. 제공되는 일기는 리스트 형태입니다.\n15. 리스트 내부의 일기를 구분하는 구분자는 ** 입니다.\n\n\n\n\n##예시\n사용자 입력\n\"chatHistory\": {\"배경\": \"이 사진은 생일을 기념하는 장면으로, 두 사람이 함께 즐거운 순간을 포착했습니다. 왼쪽 인물은 머리 위에 HAPPY BIRTHDAY 케이크를 올려두었고, 오른쪽 인물은 선글라스를 쓰고 꽃다발을 들고 있습니다. 배경은 나무 판자 벽입니다.\", \"질의응답\": [{\"질문\": \"이 사진은 생일 파티를 하는 장면이네요! 주인공은 누구인가요?\", \"대답\":\"여자친구가 주인공이었어, 이날은 망원동에 놀러갔는데 사람이 바글바글했어\"}, {\"질문\": \"주인공이 여자친구분이셨군요! 망원동에서 사람이 바글바글했다니 정신 없으셨겠어요. 그래도 여자친구분이 좋아하셨겠죠?\", \"대답\": \"엄청 좋아했어, 케이크랑 꽃도 맘에 쏙 들어했어\"}]}\n\n\n시스템 결과\n[\"이 날은 여자친구의 생일이었어요! 망원동에서 행복한 하루를 보냈던 그날을 기억하세요? 여자친구 생일을 준비하기 위해서 케이크랑 꽃도 준비하셨잖아요! 여자친구 얼굴에 미소가 끊이질 않아요. 특별한 하루를 기록하기 위해 망원동에서 즉석 사진을 찍으셨다고 했어요. 두 분의 행복한 하루가 늘 이어졌으면 좋겠어요.\"**\"여자친구분의 생일을 추억한 사진이에요! 망원동은 사람이 바글바글 했지만 여자친구는 행복한 하루를 보낸것처럼 보여요~ 생일케이크와 꽃다발을 준비하면서 여자친구가 행복해할 모습에 설레었을것같아요! 두 분의 추억이 오래 공유되는 관계가 되었으면 좋겠어요. 내년 생일에는 어떤일이 생길지 너무 기대돼요.\"**\"망원동에서 행복한 하루를 보낸 두 사람의 사진이 보여요! 여자친구분의 생일이었던 날인데, 잊지못할 최고의 하루를 보내셨던 것 같아요! 머리위에 케이크를 올리고, 선글라스를 쓰고 두분의 웃음소리가 여기까지 들리는 기분이에요. 다음 생일 땐 두분의 생일이 얼마나 더 즐거울지 제가 더 기대가 돼요!\"]\n##끝\n###형식\n[내용 요약1**내용 요약2**내용 요약3]\n###끝"},
                       {"role": "user", "content": chat_history}]

        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 800,
            'temperature': 0.1,
            'repeatPenalty': 1.2,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }
        response = self.__execute__(request_data)
        print(response)
        try:
            response_double = response.split('질문 : ')[1]
        except IndexError:
            response_double = response
        return self.__split_res__(response_double)


