import json, subprocess
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, HRFlowable
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'pdf'
OUT.mkdir(exist_ok=True)
node = "const fs=require('fs'),vm=require('vm');vm.runInThisContext(fs.readFileSync('lessons.js','utf8')+';process.stdout.write(JSON.stringify(LESSONS))')"
lessons = json.loads(subprocess.check_output(['node', '-e', node], cwd=ROOT).decode('utf-8'))
pdfmetrics.registerFont(TTFont('Malgun', 'C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('MalgunBold', 'C:/Windows/Fonts/malgunbd.ttf'))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='KTitle', fontName='MalgunBold', fontSize=20, leading=29, spaceAfter=16, textColor=colors.HexColor('#142b3b'), wordWrap='CJK'))
styles.add(ParagraphStyle(name='KHead', fontName='MalgunBold', fontSize=12, leading=19, spaceBefore=14, spaceAfter=8, textColor=colors.HexColor('#99473d'), wordWrap='CJK'))
styles.add(ParagraphStyle(name='WHead', fontName='MalgunBold', fontSize=11, leading=16, spaceBefore=8, spaceAfter=5, textColor=colors.HexColor('#99473d'), wordWrap='CJK'))
styles.add(ParagraphStyle(name='KBody', fontName='Malgun', fontSize=10, leading=18, spaceAfter=8, wordWrap='CJK'))
styles.add(ParagraphStyle(name='KSmall', fontName='Malgun', fontSize=8, leading=13, textColor=colors.HexColor('#4c5c60'), wordWrap='CJK'))
styles.add(ParagraphStyle(name='KCover', fontName='MalgunBold', fontSize=27, leading=40, alignment=TA_CENTER, wordWrap='CJK'))

def para(text, style='KBody'):
    return Paragraph(escape(str(text)).replace('\n', '<br/>'), styles[style])

def footer(canvas, doc):
    canvas.setFont('Malgun', 8)
    canvas.setFillColor(colors.HexColor('#4c5c60'))
    canvas.drawString(20*mm, 13*mm, '2027 우리들의 문학수업')
    canvas.drawRightString(190*mm, 13*mm, str(doc.page))

def build(path, story):
    SimpleDocTemplate(str(path), pagesize=(210*mm, 297*mm), leftMargin=20*mm, rightMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm, title=path.stem, author='2027 우리들의 문학수업').build(story, onFirstPage=footer, onLaterPages=footer)

def heading(lesson, label):
    return [para(f"{lesson['lesson']:02d} / {label}  ·  {lesson['standard']}  ·  50분", 'KSmall'), Spacer(1, 5*mm), para(lesson['title'], 'KTitle'), para('함께 읽을 작품: ' + lesson['text'], 'KSmall'), para('교과서 연계: ' + lesson['book'], 'KSmall'), HRFlowable(width='100%', color=colors.HexColor('#dd8b78')), Spacer(1, 5*mm)]

def study(lesson):
    return heading(lesson, '학습자료') + [para('오늘의 학습 목표', 'KHead'), para(lesson['goal']), para('핵심 개념', 'KHead'), para(lesson['concept']), para('작품과 맥락 읽기', 'KHead'), para(lesson['reading']), para('읽기 전 생각 열기', 'KHead'), para(lesson['questions'][0]), para('읽으며 확인하기', 'KHead'), para('교과서나 도서관의 작품을 읽으면서 화자·인물·표현 등 질문에 필요한 근거에 표시합니다. 저작권 보호 작품의 전문은 이 자료에 포함하지 않습니다.'), para('더 깊이 생각하기', 'KHead'), para(lesson['questions'][1]), para('선택 도전', 'KHead'), para(lesson['challenge']), para('오늘 배움을 정리하며', 'KHead'), para(lesson['exit'])]

def worksheet(lesson):
    story = heading(lesson, '활동지') + [para('학년·반: __________    번호: __________    이름: __________________', 'KSmall'), Spacer(1, 5*mm)]
    for i, q in enumerate(lesson['questions'], 1):
        story.extend([para(f'활동 {i}', 'WHead'), para(q), para('________________________________________________________________________'), para('________________________________________________________________________'), para('________________________________________________________________________')])
    story.extend([para('선택 도전', 'WHead'), para(lesson['challenge']), para('마무리', 'WHead'), para(lesson['exit']), para('________________________________________________________________________'), para('자기평가: □ 작품의 근거를 찾았다  □ 다른 의견을 존중했다  □ 배운 점을 설명할 수 있다', 'KSmall')])
    return story

guide_notes = [
('작가·작품·독자·맥락을 연결하는 관계도를 만들게 한다.', '작품은 작가와 독자를 잇지만 독자는 자신의 경험을 바탕으로 능동적으로 의미를 구성한다.', '작가의 의도만이 유일한 정답이라고 단정하지 않도록 한다.'),
('해석과 작품 근거를 짝지어 대화하게 한다.', '같은 표현을 두고 서로 다른 독자 경험에 따라 다른 의미를 찾을 수 있다. 두 해석 모두 작품 근거가 필요하다.', '시대 정보가 작품의 모든 의미를 확정한다고 오해하지 않도록 한다.'),
('시의 화자와 소설의 서술자가 정보를 제시하는 방식을 대조한다.', '시는 화자의 정서와 이미지에, 소설은 서술을 통한 인물·사건의 전개에 주목할 수 있다.', '화자나 서술자를 실제 작가와 동일시하지 않도록 한다.'),
('대사와 지시문, 교술의 관찰과 생각을 살피게 한다.', '극은 무대에서 인물의 말과 행동으로 드러나며 교술은 글쓴이의 생각을 비교적 직접 드러낸다.', '갈래의 특징을 기계적 정의로만 암기하지 않도록 한다.'),
('인물의 선택을 사건·배경·시점에 연결하는 도식을 그린다.', '특정 장면의 의미는 그 앞뒤 사건과 인물이 놓인 상황을 함께 볼 때 구체화된다.', '과학기술 설정의 소개만으로 주제를 설명했다고 여기지 않도록 한다.'),
('시점 변경 전후 독자가 알 수 있는 정보가 어떻게 다른지 점검한다.', '다른 인물의 시점은 원래 장면에서 드러나지 않은 감정이나 판단을 드러낼 수 있다.', '원작의 주요 상황을 무시한 단순 줄거리 바꾸기가 되지 않도록 한다.'),
('작품을 시대와 연결하되 표현과 여러 해석의 가능성도 살핀다.', '「님의 침묵」의 님은 사랑하는 대상 등 여러 의미로 읽을 수 있고, 「향수」는 감각적 이미지로 고향의 기억을 그린다.', '식민지 시대 작품의 모든 표현을 단일한 정치적 의미로 환원하지 않도록 한다.'),
('시의 대립과 반복, 소설의 회고적 서술을 비교한다.', '역사적 현실에 대한 시적 발언과 고향을 돌아보는 서사의 방식은 서로 다르지만 사회적 경험과 연결된다.', '작품의 역사적 맥락과 작가의 삶을 일대일로 동일시하지 않도록 한다.'),
('연표에 초발표와 단행본 수록을 구별해 적는다.', '문학의 흐름에는 다른 시대에도 이어지는 관계·고향의 질문과 변화하는 표현 방식이 함께 있다.', '작가의 출생지와 작품의 공간적 배경을 혼동하지 않도록 한다.'),
('주장과 근거, 근거가 주장을 뒷받침하는 설명을 구분한다.', '작품의 표현을 근거로 삼고 자신의 경험과 연결해 일관된 해석을 제시하면 다양한 답이 가능하다.', '개인적 공감만 있고 작품의 근거가 없는 해석은 보완하게 한다.'),
('평가 기준이 작품의 구체적 표현과 연결되는지 확인한다.', '표현의 효과, 작품의 사회적 의미, 개인의 경험 중 선택한 기준을 밝히고 근거를 제시한다.', '호불호만 적은 감상과 근거 있는 비평을 구분하게 한다.'),
('저작권을 지키면서 자신의 글과 이미지로 잡지를 제작하게 한다.', '작품의 의미를 오늘의 장소나 경험과 연결하고 친구의 서로 다른 감상을 존중하는 결과물이 가능하다.', '작품 전문이나 인터넷 이미지를 무단 복제하지 않도록 한다.')]

model_responses = [
('인상적인 표현은 독자마다 다를 수 있다. 그 표현이 어떤 고민이나 감정을 떠올리게 했는지 함께 적는다.', '화자의 처지와 고민을 말할 때 작품에서 확인한 단서를 짝지어 제시한다.', '작가는 작품을 만들고, 독자는 작품을 읽어 의미를 구성하며, 시대·독자 경험은 이해에 영향을 준다.'),
('길을 선택이나 삶의 방향에 대한 물음으로 해석할 수 있다. 반드시 작품의 구체적 표현으로 뒷받침한다.', '독자 A와 B의 해석을 각각 한 문장으로 정리하고 두 사람이 고른 작품 단서의 관련성을 비교한다.', '시대 정보로 해석을 넓히되 작품의 다른 의미를 없애지 않는다. 기존 생각을 유지해도 이유가 타당하면 인정한다.'),
('대상에 대한 화자의 관찰과 정서를 구분하여 교과서에 있는 표현을 근거로 든다.', '선택한 사건을 누가 서술하는지와 독자가 인물의 내면을 얼마나 알 수 있는지 구별한다.', '시는 이미지와 정서의 압축, 소설은 사건과 인물 관계의 전개를 중심으로 효과를 비교할 수 있다.'),
('대사는 인물의 생각과 갈등을 드러내고 지시문은 행동·상황을 보여 주는 단서가 된다.', '눈에 보이는 대상에 대한 관찰이 어떤 감상이나 성찰로 이어지는지 추적한다.', '같은 기다림을 극의 대화로 나타내면 관계가 드러나고, 교술의 성찰로 쓰면 생각이 직접 드러날 수 있다.'),
('인물의 선택 전 상황, 선택, 그 결과를 시간순으로 정리하고 교과서 장면으로 확인한다.', '작품 속 기술과 사회적 환경이 인물의 관계와 선택에 어떤 가능성·제약을 주는지 설명한다.', '서술자가 제공하는 정보의 범위에 따라 독자가 특정 인물에게 공감하는 정도가 달라질 수 있다.'),
('원래 서술에서 직접 알 수 있는 것과 추론해야 하는 감정을 나눈다.', '선택한 인물이 경험한 사건과 관계를 유지하면서 그 인물이 알 수 있는 범위에서 새 장면을 쓴다.', '새로운 시점에서 드러난 감정이나 놓치게 된 정보를 짚고 원작과 달라진 효과를 설명한다.'),
('두 시에서 부재하거나 그리워하는 대상을 구별하고, 화자의 감정이 나타나는 표현을 직접 확인한다.', '님을 사랑하는 사람이나 공동체 등으로 해석할 수 있으나 각각의 해석을 작품의 단서와 연결해야 한다.', '「향수」의 시각·청각 등 감각적 묘사가 구체적인 장소를 떠올리게 하는 효과를 설명한다.'),
('대립되는 이미지와 반복되는 말의 관계를 찾아 강조되는 가치와 말하는 태도를 설명한다.', '현재의 화자가 과거를 돌아보는 방식과 고향의 인물·공간이 어떻게 기억되는지 정리한다.', '두 작품은 사회적 경험과 연결되지만 시의 상징적 발언과 소설의 회고 서술이라는 차이가 있다.'),
('작품 속 대상과 화자의 태도를 근거로 관계나 돌봄의 의미를 해석한다. 다른 근거 있는 해석도 가능하다.', '1926 시집 간행, 1927 발표, 1964 초발표, 1972~1977 연작, 1989 당선 순으로 구분한다.', '고향과 관계에 관한 관심이 이어질 수 있지만 갈래와 시대적 문제의식은 달라짐을 사례로 설명한다.'),
('선택 이유와 작품에 던질 질문을 자신의 경험과 연결하여 명료하게 쓴다.', '예: 작품의 특정 이미지가 화자의 태도 변화를 보여 준다는 주장에 표현 두 곳을 근거로 연결한다.', '친구의 다른 해석이 어떤 작품 근거를 설명하는지 먼저 살핀 뒤 자신의 설명과 비교한다.'),
('표현의 효과와 오늘의 독자에게 주는 의미를 기준으로 삼고 선택 이유를 밝힐 수 있다.', '주장 뒤에 작품의 구체적 표현, 그 표현의 효과, 평가 기준과의 관계를 차례로 제시한다.', '비평이 설득력 있는 부분을 짚고 근거와 결론의 관계가 불분명한 부분을 질문한다.'),
('작품의 고향이나 관계에 대한 물음을 세종의 장소 또는 자신의 경험에 연결하는 질문을 만든다.', '직접 쓴 소개와 해석, 직접 만든 시각 자료와 출처를 한 면에 배치한다.', '친구의 작품에서 자신과 다른 관점 한 가지를 구체적으로 소개하고 그 이유를 적는다.')]

def teacher():
    story = [para('교사용 수업안과 예시답안', 'KCover'), para('12차시 · 50분 수업 · 공통국어 문학', 'KSmall'), para('교과서와 작품은 정식으로 이용 가능한 자료를 준비한다. 예시답안은 가능한 해석의 하나이며 작품에 근거한 다양한 답을 인정한다.'), PageBreak()]
    for l, (method, answer, caution), responses in zip(lessons, guide_notes, model_responses):
        story.extend(heading(l, '교사용 수업안'))
        for label, value in [('학습 목표', l['goal']), ('준비물과 사전 읽기', '교과서 또는 정식 열람 자료, 필기구, 차시별 학습자료와 활동지. 긴 소설은 수업 전 지정 부분을 읽도록 안내한다.'), ('50분 수업 흐름', f'도입 5분: 첫 질문으로 경험을 연결한다. 개념·읽기 10분: 핵심 개념과 작품 맥락을 확인한다. 개인 탐구 10분: 작품 근거를 찾는다. 모둠 활동 15분: {method} 정리 10분: 발표와 마무리 문항을 수행한다.'), ('핵심 발문', ' / '.join(l['questions'])), ('예시답안과 해설', answer), ('지도상 유의점', caution), ('평가와 지원', '상: 작품의 구체적 근거와 개념을 연결해 설명한다. 중: 질문에 맞는 작품 근거와 생각을 제시한다. 보완 필요: 교사의 단서 질문과 동료의 도움을 받아 관련 장면을 찾는다. 다른 타당한 해석도 인정한다.'), ('마무리 확인', l['exit'])]:
            story.extend([para(label, 'KHead'), para(value)])
        story.extend([PageBreak()] + heading(l, '활동별 답안 예시'))
        for i, response in enumerate(responses, 1):
            story.extend([para(f'활동 {i}', 'KHead'), para(l['questions'][i-1]), para('답안 예시: ' + response)])
        if l['lesson'] != 12: story.append(PageBreak())
    return story

for lesson in lessons:
    n = lesson['lesson']
    build(OUT / f'lesson-{n:02d}-study.pdf', study(lesson))
    build(OUT / f'lesson-{n:02d}-worksheet.pdf', worksheet(lesson))
pack = [para('학생용 학습자료와 활동지', 'KCover'), para('2027 우리들의 문학수업 · 12차시', 'KSmall'), PageBreak()]
for lesson in lessons:
    pack += study(lesson) + [PageBreak()] + worksheet(lesson)
    if lesson['lesson'] != 12: pack.append(PageBreak())
build(OUT / 'student-complete.pdf', pack)
build(OUT / 'teacher-guide.pdf', teacher())
print('Created', len(list(OUT.glob('*.pdf'))), 'PDF files')
