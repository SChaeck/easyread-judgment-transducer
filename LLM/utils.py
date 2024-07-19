### 환경변수 로드 ###
from dotenv import load_dotenv

load_dotenv()

### 쉬운 판결문 변환 ###
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# et: easy translate
et_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "너는 복잡하고 어려운 판결문들을 정보 약자나, 발달장애인이 이해할 수 있도록 변환해주는 쉬운 판결문 변환기야. 아래에 제시되는 판결문을 명령에 따라 쉬운 판결문으로 바꿔줘. 단, 원래 문장의 의미가 유지돼야 하고 모든 뜻이 명확히 전달돼야 해. 또한 오해하도록 모호하게 말해선 안돼."
        ),
        (   
            "human",
            """### 명령:
아래 판결문을 다음과 같이 순서대로 정리해서 제시해줘.
단, 모든 뜻이 명확히 전달돼야 하며, '-입니다'체를 사용하고, 주어-동사 위주의 적당한 길이의 문장을 사용해 작성해줘. 문장간의 연결이 자연스러워야 해. 또한 오해하도록 모호하게 말해선 안돼.

legal_terminology: 모든 법률용어와 그것의 뜻
easy_judgment: legal_terminology의 뜻풀이를 활용해 제시한 판결문 내용을 쉽게 바꾼 문단입니다. 법률 용어를 모르는 사람이 봐도 이해할 수 있어야 하고 [이유]-[결론] 형식으로 작성해야합니다.
very_easy_judgment: 법률용어를 사용하지 않고 쉬운 단어로 대체하여, 제시한 판결문 내용을 초등학생에게 설명하듯이 아주 쉽게 바꾼 문단입니다. 여러 비유를 사용해도 되고 [이유]-[결론] 형식으로 작성해야합니다. 

### 판결문:
{judgment}

### 출력양식:
{{
    "legal_terminology": {{}},
    "easy_judgment": "",
    "very_easy_judgment": ""
}}"""
        )
    ]
)

et_llm = ChatOpenAI(temperature=0.1, model="gpt-4o-mini")
et_chain = et_prompt | et_llm

def easy_translate(judgment):
    response = et_chain.invoke(judgment)
    
    et_judgment = response.content
    
    return et_judgment

### 메인함수 ###
if __name__ == "__main__":
    judgment = """【판시사항】
[1]임의경매절차 진행중 근저당권이 양수인에게 이전등기되었으나, 경락인의 대금납부 전까지 피담보채권의 양도통지가 이루어지지 아니한 경우 그 효력
[2]임의경매 배당절차에서 집행력 있는 정본이 없는 채권자의 채권에 대하여 채무자가 이의하는 경우 그 이의의 완결방법【판결요지】
[1]임의경매절차 진행중, 채권자(양도인)인 원고가 피고(양수인)에게 근저당권 및 피담보채권을 양도하고 근저당권이전등기까지 마쳤으나, 채무자에 대한 양도통지가 경락인의 대금납부로 근저당권이 소멸된 후 이루어졌기 때문에 근저당권의 양도는 효력이 없지만, 근저당권의 피담보채권과 배당금청구권은 피고에게 양도되었다고 봄이 상당하므로, 경매법원이 위 근저당권에 대한 배당금을 근저당권명의자인 피고에 대하여 공탁한 것은 적법하다.
[2]근저당권자가 신청한 경매의 배당절차에서 그 근저당권자에 대하여 채무자가 배당이의를 한 경우에는 민사소송법 제658조, 제592조에 의하여 이의를 신청한 채무자가 배당이의 소송을 제기하여야 하는 것이고, 근저당권자가 민사소송법 제606조 제3항에 따른 채권확정의 소를 제기하여야 하는 것이 아니다.【원고,피항소인】 A (소송대리인 법무법인 미래 담당변호사 박장우)
【피고,항소인】 청림종합건설 주식회사 (소송대리인 법무법인 중부종합 담당변호사 고형규)
【원심판결】 인천지법 2000. 1. 19. 선고 98가합14869 판결
【대법원판결】 대법원 2002. 10. 11.자 2002다40272 판결
【주문】
1.인천지방법원이 B, C(병합), D(병합) 부동산 임의경매사건과 관련하여 1997. 1. 18. 인천지방법원 97년금제306호로 피고를 피공탁자로 하여 공탁한 1,256,673,349원에 대한 출급청구권 중 1,106,673,349원{그 중 506,673,349원 부분에 대해서는 E의 채권가압류(인천지방법원 96카합4018)와 F·G의 채권압류(인천지방법원 H)가 경합되어 있다}의 부분이 원고에게 있음을 확인한다.
2. 원고의 나머지 청구를 기각한다.
3. 항소심 소송비용 중 70%는 피고가 부담하고, 30%는 원고가 부담한다.【청구취지및항소취지】
1. 청구취지 [항소심에서 청구 교환적 변경]
주문 기재 공탁금 1,256,673,349원에 대한 출급청구권이 원고에게 있음을 확인한다.
2. 항소취지
원심판결을 취소한다. 원고의 청구를 기각한다.
【이유】
1. 인정 사실
가.I는 1992. 9. 9. J로부터 그 소유이던 인천 남구 K 대 2,569.3㎡ 지상〈이 사건 부지〉아파트형 공장 5층 건물〈이 사건 건물〉신축공사 중 마무리공사 등을 도급받아 그 공사를 마치고, 1994. 9. 7. J와 사이에 공사대금을 14억 원으로 정한 다음(갑 제3호증·갑 제16－32＝을 제2호증), 이를 담보하기 위하여 1994. 9. 8. 이 사건 부지 및 건물에 관하여 채권최고액 30억 원, 근저당권자 I·L·G로 된 근저당권〈이 사건 근저당권〉을 설정하였다(을 제1-1호증).
나.이 사건 부지 및 건물에 대하여 1995. 4. 26. 이 사건 근저당권에 기한 경매신청에 의하여 인천지방법원 B 경매절차가 진행되던 중, 이 사건 근저당권의 공동근저당권자 I·L·G는 채무자인 J의 동의를 얻어 I에 대한 채권자인 원고에게 1996. 2. 26. 이 사건 근저당권과 그 피담보채권 14억 원을 양도하였다(갑 제16-3호증). 원고는 1996. 2. 27. 이 사건 근저당권의 이전등기를 마쳤다.
다.원고는 이 사건 근저당권을 양수하면서 I에게 이 사건 부지 및 건물을 경락받은 다음 대출을 받아서 I의 채무를 변제하기로 하고, 만약 원고가 경락을 받지 못하면 I·L·G에게 이 사건 근저당권을 넘겨주기로 하였다(을 제3-1호증).
이에 원고는 1996. 2. 24. I의 L·M에 대한 채무를 담보하기 위하여 L에게 2억 5천만 원의 약속어음 공정증서를 작성·교부하였고(갑 제9호증), 1996. 2. 26. G에게 I의 채무 2억 원, N에게 I의 채무 4억 원을 각 변제하여 주기로 약정하였으며(을 제3-2, 3호증), 1996. 2. 27. 원고의 아버지인 O 소유의 인천 서구 P 대지 및 지상 건물에 M 명의로 채권최고액 2억 5천만 원의 근저당권을 설정해 주었다. 그 후 원고는 1996. 7. 10. M 명의의 위 근저당권을 해제받고 M에게 2억 5천만 원의 약속어음 이행각서를 작성·교부하였다(갑 제10호증·갑 제11호증·을 제1-2, 3호증).
라.원고는 이 사건 부지 및 건물을 경락받지 못하던 중 I의 요구에 따라 1996. 7. 22. 피고에게 이 사건 근저당권 및 그 피담보채권 14억 원을 양도하고(을 제5호증), 1996. 7. 24. 근저당권이전등기(다만, 등기부상으로는 근저당권변경등기)를 마쳐 주었고(을 제1-1호증), 그 양도사실을 1996. 11. 15.자 내용증명우편으로 J에게 통지하였다(을 제8-1, 2호증). {피고는 1996. 7. 22. 채무자인 J로부터 위와 같은 양도에 대한 승낙을 받았다고 주장하나, 이에 부합하는 증인 I·G의 각 증언은 믿기 어렵고, 을 제8-1호증만으로는 이를 인정하기에 부족하다.}
피고는 이 사건 근저당권의 이전등기를 마친 다음 이 사건 근저당권자로서 경매법원에 14억 원의 채권계산서를 제출하는 한편, [별표Ⅰ]과 같이 I의 공사대금채무 등 4억 5,300만 원을 변제하였다.
별표 Ⅰ. 피고의 대위변제 내역
구분변제일채권자변제액증거
㉮1996. 8. 13.성두설비9천만 원을 제17호증
㉯1996. 10. 23.A_016,300만 원을 제15호증
㉰1996. 11. 10.N7천만 원을 제13호증
㉱1997. 4. 24.E1천만 원을 제11호증
㉲1997. 8. 21.A_028천만 원을 제14호증
㉳1997. 10. 7.A_02(주)하영9천만 원을 제16호증
㉴1998. 4. 21.G5천만 원을 제12호증마.이 사건 부지 및 건물은 경매 결과, 1996. 9. 7. 대지 중 2569.3분의 1961.2241지분과 그 부분 건물은 Q에게(1996. 11. 25. 소유권이전등기), 나머지는 피고에게(1996. 11. 23. 소유권이전등기) 각 낙찰되었고(을 제1-1호증), 인천지방법원은 배당기일인 1996. 11. 15. 피고에게 1,256,673,349원을 배당하는 배당표를 작성하였다(갑 제1호증). J가 피고에 대하여 배당이의한 후 인천지방법원 96가합18843호로 배당이의 소송을 제기하고, 이 사건 근저당권에 대한 배당금에 관하여 [별표 Ⅱ] ①, ②, ③, ④와 같이 압류·가압류가 되자, 이 사건 근저당권에 대한 배당금 1,256,673,349원은 1997. 1. 18. 인천지방법원 97년금제306호로 피고를 피공탁자로 하여 공탁되었다(갑 제17호증). 그 공탁금출급청구권에 대하여 [별표 Ⅱ] ⑤, ⑥과 같이 압류·전부되었고(을 제35호증), R은 1996. 7. 20. 그 권리를 포기하였다(갑 제6호증, 을 제10-1호증).
별표 Ⅱ. 이 사건 근저당권에 대한 배당금(공탁금)에 대한 압류·가압류
구분채권자채무자제3채무자금액결정제3채무자 송달일
① 압류·전부RI대한민국배당금1.5억 원인천지방법원95타기4147·41481995. 7. 10.
② 압류·전부WR대한민국①금액 중 3,300만 원인천지방법원96타기3677·36781996. 5. 28.
③ 가압류E피고대한민국배당금4.5억 원인천지방법원96카합40181996. 10. 26.
④ 가압류원고R대한민국①금액 중 1.5억 원인천지방법원96카합40751996. 11. 2.
⑤ 압류·전부U피고대한민국공탁금6억 원인천지법 부천지원H·31771997. 12. 8.
⑥ 압류·전부FG피고대한민국공탁금7억 원인천지법 부천지원97타기3247·32481997. 12. 12.
바.J는 피고를 상대로 인천지방법원 96가합18843배당이의의 소를 제기하였으나, 1998. 4. 23. 서울고등법원 97나38802 판결로 채무명의가 없는 근저당권에 대하여 채무자가 배당이의한 경우에는 근저당권자가 채권확정의 소를 제기하여야 하고 채무자가 배당이의 소송을 제기하여야 하는 것이 아니라는 이유로 각하되고, 1998. 8. 25. 대법원 98다26088 판결로 심리기각되어 확정되었다(갑 제18호증·을 제6호증). 이에 따라 피고가 J를 상대로 채권확정의 소를 제기하였으나 인천지방법원 98가합12849 판결로 각하되었다가 서울고등법원 99나25176 판결로 환송되어 인천지방법원 2000가합542로 심리 중이다(갑 제19호증).
사.원고는 1998. 5. 12. 인천지방법원 98카합4412로 피고의 공탁금출급청구권에 대하여 처분금지가처분결정을 받았고(갑 제16-28호증), 이에 대하여 S와 I는 1998. 6. 2. 원고가 위계를 사용하여 피고로 하여금 경락대금을 받지 못하도록 업무를 방해하였다는 이유로 인천서부경찰서에 고소하였으나(갑 제16-31호증), 인천지방검찰청(98형제101970호)은 원고에 대하여 1999. 2. 26. 혐의없음 처분을 하였다(갑 제16-1호증).
아.원고와 피고는 2000. 8. 14. 원고가 피고에게 3억 원을 주고, E에 대하여 2억 원을 책임지기로 하며, 피고는 T 변호사를 통하여 3억 원을 지급받으면 이 사건 항소를 취하하고, G 등의 압류를 해소하여 주기로 합의하였다(갑 제34-2, 3호증). 이에 피고·U·F·G는 2000. 8. 14. 이 사건 공탁금 중 1,106,673,349원(R에게 전부된 1억 5천만 원 제외)에 대한 권리를 원고에게 양도하고, 인천지방법원 공탁공무원에게 내용증명우편으로 이 사건 공탁금에 대한 권리를 양도하였다는 통지를 하였다(갑 제22-3, 4호증, 을 제33호증). 원고가 2000. 8. 14. T 변호사에게 3억 원을 보관시켰으나(갑 제22-1호증), T 변호사가 그 돈을 소비하고 피고에게 지급하지 않았다(을 제38-2호증). 이에 피고·U·F·G는 2001. 3. 27. 원고에 대한 위 채권양도를 모두 취소함과 아울러 인천지방법원 공탁공무원에게 원고에 대한 채권양도와 2000. 8. 14.자 양도통지를 취소한다고 통지하였다(을 제34호증).
별표 Ⅲ. 이 사건 근저당권 및 그 배당금에 관한 권리관계
구분연월일변동 사유
(1)1994. 9. 8.근저당권 30억 원 설정(I·L·G), 피담보채권 14억 원.
(2)1995. 7. 10.R이 I의 배당금 중 1억 5천만 원 압류·전부, 1996. 7. 20. 권리 포기.
(3)1996. 2. 26.원고가 근저당권 및 피담보채권 양수, 1996. 2. 27. 이전등기.
(4)1996. 5. 28.W가 R의 배당금 전부액 중 3,300만 원 압류·전부.
(5)1996. 7. 22.원고가 피고에게 근저당권 및 피담보채권 양도, 1996. 7. 24. 이전등기, 1996. 11. 15. 양도 통지.
(6)1996. 9. 7.경락, 1996. 11. 23. 및 11. 25. 소유권이전등기.
(7)1996. 10. 26.E가 피고의 배당금 중 4억 5천만 원 가압류.
(8)1996. 11. 2.원고가 R의 배당금 전부액 전부 가압류.
(9)1996. 11. 15.배당실시, 이 사건 근저당권자(피고)에게 배당금 1,256,673,349원 배정, J 배당이의.
(10)1997. 1. 18.배당배정액 1,256,673,349원 공탁, 피공탁자 피고.
(11)1997. 12. 6.U가 공탁금 중 6억 원 압류·전부.
(12)1997. 12. 11.F·G가 공탁금 중 7억 원 압류·전부.
(13)1998. 5. 12.원고가 처분금지가처분
(14)1998. 8. 25.J의 배당이의소송 각하 확정.
(15)2000. 8. 14.공탁금 출급청구권 중 1,106,673,349원을 피고·U·F·G가 원고에게 양도.
(16)2001. 3. 27.피고·U·F·G가 위 출급청구권 양도의 취소를 통지.2. 판 단
이 사건 근저당권과 그 배당금에 관한 권리관계를 정리하면 [별표 Ⅲ]과 같다.
이 사건 근저당권과 그 피담보채권 14억 원은 [별표 Ⅲ] (3)과 같이 원고에게 양도되었다.
원고가 [별표 Ⅲ] (5)와 같이 피고에게 이 사건 근저당권 및 피담보채권을 양도하고 근저당권이전등기까지 마쳤으므로, 그 양도통지가 이 사건 근저당권이 소멸된 후에 이루어졌기 때문에 이 사건 근저당권의 양도는 효력이 없지만, 이 사건 근저당권의 피담보채권과 배당금청구권은 피고에게 양도되었다고 봄이 상당하다.
갑 제6-4·5·27·28호증의 기재와 증인 V의 증언만으로는 원고의 피고에 대한 위 양도행위가 피고의 사기로 말미암은 것이라고 인정하기에 부족하다.
다만, 원고가 이 사건 근저당권을 양수하기 전에 R이 [별표 Ⅲ] (2)와 같이 이 사건 근저당권에 관한 배당금 중 1억 5천만 원을 압류·전부받았다가 1996. 7. 20. 그 권리를 포기하였지만, R의 전부금액 중 3,300만 원에 대하여 W가 1996. 5. 28. 압류·전부받았기 때문에, 이 사건 배당금 중 3,300만 원은 W에게 귀속되었고, 그 나머지 1,223,673,349원만 피고에게 양수되었다.
경매법원이 이 사건 근저당권에 대한 배당금을 근저당권명의자인 피고에 대하여 공탁한 것은 적법하다. 그리고 이 사건 근저당권에 대한 배당에 대하여 채무자인 J가 배당이의를 하였지만, J의 배당이의 소송이 각하되었으므로, 그 이유 여하를 막론하고 이 사건 근저당권에 대한 배당금은 배당표대로 1,256,673,349원으로 확정되었다. 근저당권자가 신청한 경매의 배당절차에서 그 근저당권자에 대하여 채무자가 배당이의를 한 경우에는 민사소송법 제658조, 제592조에 의하여 이의를 신청한 채무자가 배당이의 소송을 제기하여야 하는 것이고, 근저당권자가 민사소송법 제606조 제3항에 따른 채권확정의 소를 제기하여야 하는 것이 아니다. 민사소송법 제606조 제2항·제3항은 제605조에 규정된 배당요구권자 중 집행정본이 없는 채권자가 배당요구한 경우에 적용되는 것이고, 저당권자가 저당권을 실행하기 위하여 경매신청하거나 저당목적물에 대한 경매대금에서 배당받고자 하는 경우에는 적용되지 않는다. 저당권은 원래 담보물권으로서 집행력 있는 채무명의가 없더라도 저당목적물에 대하여 경매를 청구하고( 민법 제363조) 우선변제를 받을 수 있는 것이기( 민법 제356조) 때문에, 저당권자는 민사소송법 제605조에 규정된 배당요구권자가 아니라, 제607조 제3호의 이해관계인에 해당된다.
그런데 피고와 U·F·G가 [별표 Ⅲ] (15)와 같이 2000. 8. 14. 이 사건 배당액 공탁금 중 1,106,673,349원을 원고에게 양도하고 그 사실을 확정일자 있는 내용증명우편으로 공탁공무원에게 통지하였으므로, 이 사건 배당액 공탁금 중 1,106,673,349원에 대한 출급청구권은 원고에게 양도되었다. 이 사건 배당액 공탁금 중 6억 원은 U에게 전부되었다가 원고에게 양도되었다. F·G의 압류·전부명령은 E의 가압류와 경합되므로 전부명령의 효력이 생기지 아니하고 압류의 효력만 가진다. 그러므로 나머지 금액 506,673,349원은 E의 가압류와 F·G의 압류가 민사소송법 제568조의2에 의하여 전액 경합된 상태로 피고로부터 원고에게 양도되었다.
피고와 U·F·G가 2001. 3. 27. 공탁공무원에게 2000. 8. 14.자 채권양도 및 양도통지를 취소한다고 통지하였지만, 그 양수인인 원고의 동의가 없으므로 효력이 없다.
3. 결 론
이 사건 공탁금 중 1,106,673,349원에 대한 출급청구권은 원고에게 있지만, 그 중 506,673,349원에 대해서는 E의 가압류와 F·G의 압류가 경합되어 있다.
원고가 항소심에서 교환적으로 변경한 이 사건 청구는 위에서 인정한 범위 내에서만 이유 있고, 나머지 청구는 이유 없다.
판사   조대현(재판장) 고충정 박대준"""
    
    print(easy_translate(judgment))
    






### Legacy ###
"""### 형태소 분석 ###
from kiwipiepy import Kiwi

def sbg_noun_extractor(text: str) -> list[str]:
    # 먼 문단의 내용도 참고해 품사 태깅
    kiwi = Kiwi(model_type='sbg')
    tokens = kiwi.tokenize(text, normalize_coda=True)

    results = set() # 중복 토큰 제거
    for token, pos, _, _ in tokens:
        if pos.startswith('NN'): # 일반 명사, 고유 명사, 의존 명사만 추출
            results.add(token)

    return results


### 법률용어 DB 접근해서 있는지 확인 ###
import json

with open("data/legal_terminology.json", "r", encoding="utf-8") as db:
    legal_term_DB = json.load(db)

def legal_term_DB_check(term_list: list[str]) -> list[bool]:
    check_list = []
    for term in term_list:
        if term in legal_term_DB:
            check_list.append(True)
        else:
            check_list.append(False)

    return check_list


### 법률용어 질의 ###
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# ltq: logical terminology question
ltq_template = ""

ltq_llm = OpenAI(temperature=0.1, model=)
ltq_chain = ltq_template | ltq_llm

def logical_terminology_question(judgment, legal_terminology):
    response = ltq_chain.invoke(judgment, legal_terminology)
    
    ltq_judgment = response.content
    
    return ltq_judgment"""