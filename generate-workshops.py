from pathlib import Path
import json, subprocess
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
ROOT=Path(__file__).resolve().parent
cmd="const fs=require('fs'),vm=require('vm');vm.runInThisContext(fs.readFileSync('workshops.js','utf8')+';process.stdout.write(JSON.stringify(WORKSHOPS))')"
items=json.loads(subprocess.check_output(['node','-e',cmd],cwd=ROOT).decode('utf8'))
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFont(TTFont('MalgunBold','C:/Windows/Fonts/malgunbd.ttf'))
title=ParagraphStyle('title',fontName='MalgunBold',fontSize=18,leading=26,spaceAfter=12,wordWrap='CJK')
head=ParagraphStyle('head',fontName='MalgunBold',fontSize=11,leading=17,spaceBefore=9,spaceAfter=5,textColor=colors.HexColor('#99473d'),wordWrap='CJK')
body=ParagraphStyle('body',fontName='Malgun',fontSize=9.5,leading=17,spaceAfter=6,wordWrap='CJK')
small=ParagraphStyle('small',fontName='Malgun',fontSize=8,leading=13,wordWrap='CJK')
def p(s,style=body):return Paragraph(escape(str(s)),style)
def footer(c,d):c.setFont('Malgun',8);c.drawString(20*mm,13*mm,'2027 우리들의 문학수업');c.drawRightString(190*mm,13*mm,str(d.page))
def build(name,story):SimpleDocTemplate(str(ROOT/'pdf'/name),pagesize=(210*mm,297*mm),leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm).build(story,onFirstPage=footer,onLaterPages=footer)
def line():return p('_______________________________________________________________________________')
def genre_cards():
 data=[('서정','느낌을 압축해서','화자의 정서와 생각을 시어·이미지·운율로 표현','화자 · 상황 · 정서 · 시어','현대시, 시조'),('서사','이야기를 들려줘요','인물에게 일어난 사건을 서술자가 전달','인물 · 사건 · 배경 · 서술자·시점','소설, 설화'),('극','눈앞에 펼쳐 보여요','대사와 행동으로 인물의 갈등을 표현','인물 · 갈등 · 대사 · 행동 · 지시문','희곡, 시나리오'),('교술','경험을 생각으로','관찰과 경험을 바탕으로 생각을 직접 전달','경험 · 관찰 · 생각 · 표현','수필')]
 cells=[]
 for name,focus,desc,components,examples in data:
  cells.append([p(name,head),p(focus,body),p(desc,small),p('구성: '+components,small),p('예: '+examples,small)])
 table=Table([[cells[0],cells[1]],[cells[2],cells[3]]],colWidths=[82*mm,82*mm],hAlign='LEFT')
 table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,0),colors.HexColor('#fff1ee')),('BACKGROUND',(1,0),(1,0),colors.HexColor('#edf5ea')),('BACKGROUND',(0,1),(0,1),colors.HexColor('#eef2fa')),('BACKGROUND',(1,1),(1,1),colors.HexColor('#fbf3dc')),('BOX',(0,0),(-1,-1),.6,colors.HexColor('#c6d0c6')),('INNERGRID',(0,0),(-1,-1),.6,colors.HexColor('#c6d0c6')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
 return table
for w in items:
 prefix=[p(f"문학이란 {w['id']}차시 · 고1 · 50분",small),Spacer(1,3*mm),p(w['title'],title),p('연계 성취기준: '+w['standards'],small)]
 study=prefix+[p('오늘의 목표',head),p(w['goal'])]
 for h,t in w['theory']:
  if w['id']==1 and h=='네 갈래를 구별해요':study.extend([p('네 갈래와 구성 요소 한눈에 보기',head),genre_cards()])
  elif w['id']==1 and h=='작품은 어떻게 구성될까?':study.extend([p(h,head),p('소재 → 표현과 구성 → 주제: 요소들이 서로 연결되어 작품의 의미를 만든다.')])
  else:study.extend([p(h,head),p(t)])
 study.extend([p('활동으로 연결하기',head),*[p(f'{i}. {a}') for i,a in enumerate(w['activities'],1)],p('출처: 중등교육과정 MCP 및 경기도교육청 2022 개정 국어과 성취평가 자료.',small)])
 worksheet=prefix+[p('학년·반: __________  번호: __________  이름: __________________',small)]
 for i,a in enumerate(w['activities'],1):worksheet.extend([p(f'활동 {i}',head),p(a),line(),line(),line()])
 worksheet.extend([p('선택 도전',head),p(w['challenge']),line(),p('자기평가: □ 작품의 근거를 찾았다  □ 다른 관점을 존중했다  □ 나의 생각을 설명했다',small)])
 worksheet.extend([PageBreak(),p('확인 퀴즈',title),p('온라인 퀴즈와 같은 문항입니다. 정답을 고르고 이유를 생각해 보세요.',small)])
 for number,(question,choices,answer,explanation) in enumerate(w['quiz'],1):
  worksheet.extend([p(f'{number}. {question}',head),*[p(f'□ {choice}') for choice in choices],Spacer(1,2*mm)])
 group=prefix+[p('모둠 이름: __________________  참여자: __________________________________',small),p('활동 안내',head)]
 group.extend([p(f'{i}. {x}') for i,x in enumerate(w['group'],1)])
 for label in ['우리의 질문과 대상 독자','작품의 근거와 표현 효과','우리의 관점과 다른 사람의 의견','결과물 구성과 출처','발표 후 새롭게 알게 된 점']:
  group.extend([p(label,head),line(),line()])
 for kind,story in [('study',study),('worksheet',worksheet),('group',group)]:build(f"workshop-{w['id']}-{kind}.pdf",story)
print('Created six workshop PDFs')
