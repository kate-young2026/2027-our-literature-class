'use strict';
const quizzes = [
['문학 소통에서 독자의 역할은?',['작품의 의미를 능동적으로 구성한다','작가의 의도만 그대로 받아 적는다','작품의 맥락을 무시한다'],0,'독자는 경험과 작품의 근거를 바탕으로 의미를 구성합니다.'],
['타인의 문학 해석을 검토할 때 중요한 것은?',['나와 의견이 같은지','작품에 근거가 있는지','말한 사람의 인기'],1,'서로 다른 해석도 작품에 근거하여 논의할 수 있습니다.'],
['시에서 말하는 존재를 무엇이라고 할까요?',['화자','실제 독자','편집자'],0,'화자는 작품 속에서 말하는 존재이며 실제 작가와 구분합니다.'],
['극의 특징으로 알맞은 것은?',['대사와 행동으로 상황을 보여 준다','항상 실제 사건만 설명한다','서술자가 반드시 모든 사건을 전달한다'],0,'극은 대사·행동·지시문으로 장면을 구성합니다.'],
['소설의 구성 요소에 해당하지 않는 것은?',['인물','사건','독자의 시험 점수'],2,'인물·사건·배경·시점은 작품의 구성 요소입니다.'],
['이야기의 시점을 바꾸면 달라질 수 있는 것은?',['독자가 알게 되는 정보의 범위','이미 출판된 원작의 저자','작품을 읽는 사람의 이름'],0,'시점에 따라 드러나는 정보와 인상이 달라집니다.'],
['「님의 침묵」의 ‘님’을 읽는 태도로 적절한 것은?',['어떤 근거도 필요 없다','작품의 단서를 바탕으로 다양한 해석을 검토한다','오직 하나의 뜻만 외운다'],1,'작품의 단서로 뒷받침되는 다양한 해석을 비교합니다.'],
['「껍데기는 가라」의 표현을 살필 때 주목할 것은?',['대립과 반복','광고의 가격','과학 실험 절차'],0,'대립과 반복은 시가 강조하는 가치를 이해하는 단서입니다.'],
['작품의 지역 연계를 설명할 때 알맞은 태도는?',['출생지와 작품 배경을 무조건 같다고 본다','발표 연도와 작가의 출생지를 구분한다','작가의 삶은 확인할 필요가 없다'],1,'작가의 출생지, 작품 배경, 발표 시기는 구분해야 합니다.'],
['근거 있는 작품 해석에 필요한 것은?',['주장과 작품 속 단서, 그 관계에 대한 설명','감상 한 단어만 쓰기','작품을 읽지 않고 결론 내리기'],0,'주장–근거–설명으로 해석을 뒷받침합니다.'],
['문학 비평의 좋은 방법은?',['평가 기준과 구체적인 근거를 제시한다','호불호만 말하고 끝낸다','다른 해석을 금지한다'],0,'평가 기준을 밝히고 작품의 표현으로 설명합니다.'],
['문학을 생활화하는 활동으로 적절한 것은?',['작품을 일상과 연결해 읽고 생각을 나눈다','시험이 끝나면 작품을 다시 읽지 않는다','타인의 감상을 무시한다'],0,'읽기·대화·창작을 삶에서 이어 가는 것이 문학 향유입니다.']
];
const list = document.querySelector('#lesson-list');
if(list){
  const foundation=document.createElement('a');foundation.className='lesson-card lesson-link foundation-link';foundation.href='basics.html';
  foundation.innerHTML='<small>첫 시간 · 고1</small><h3>문학의 기초: 네 갈래와 작품의 구성</h3><p>작품을 읽는 데 필요한 기본 개념부터 시작해요.</p><span class="lesson-arrow" aria-hidden="true">↗</span>';
  list.append(foundation);
}
const profiles={
 '윤동주':['1917~1945. 일제강점기에 활동한 시인으로, 자신의 삶과 시대를 성찰하는 시를 남겼다.','「서시」, 「별 헤는 밤」, 『하늘과 바람과 별과 시』','https://encykorea.aks.ac.kr/Article/E0042294'],
 '김초엽':['2017년 「관내분실」로 한국과학문학상 중단편 부문 대상을 받으며 작품 활동을 시작한 소설가다.','「관내분실」, 『우리가 빛의 속도로 갈 수 없다면』, 『지구 끝의 온실』','https://www.blossomenter.com/ko/?c=146&gbn=viewok&gp=1&ix=232&s='],
 '이강백':['한국의 극작가로, 비유와 상징을 활용해 사회와 인간의 문제를 다룬 희곡을 발표했다.','「결혼」, 「파수꾼」','https://www.nl.go.kr/NL/contents/N10902020000.do'],
 '이태준':['1904년 출생의 소설가이자 수필가. 1925년 「오몽녀」를 발표하며 작품 활동을 시작했다.','「달밤」, 『무서록』, 「화단」','https://encykorea.aks.ac.kr/Article/E0046336'],
 '한용운':['1879~1944. 충남 홍성 출생의 시인·승려·독립운동가다.','『님의 침묵』, 『조선불교유신론』','https://encykorea.aks.ac.kr/Article/E0061853'],
 '정지용':['1902년 충북 옥천 출생의 시인으로 감각적인 언어를 통해 고향과 자연을 표현했다.','「향수」, 「유리창」','https://encykorea.aks.ac.kr/Article/E0050954'],
 '신동엽':['1930~1969. 충남 부여 출생의 시인으로 역사와 민중의 삶에 주목했다.','「껍데기는 가라」, 「금강」','https://encykorea.aks.ac.kr/Article/E0032791'],
 '이문구':['1941~2003. 충남 보령 출생의 소설가로 고향과 농촌 공동체를 그렸다.','『관촌수필』, 『우리 동네』','https://www.korean.go.kr/nkview/nklife/2018_2/28_2.pdf'],
 '나희덕':['1966년 충남 논산 출생의 시인으로 1989년 「뿌리에게」로 등단했다.','『뿌리에게』, 『그곳이 멀지 않다』','https://www.changbi.com/BookDetail?bookid=446']
};
function profileDetails(text){return Object.entries(profiles).filter(([name])=>text.includes(name)).map(([name,[bio,works,url]])=>`<details class="author-profile"><summary>${name} 작가 알아보기</summary><p>${bio}</p><p><strong>대표 작품</strong> ${works}</p><a href="${url.replaceAll('&','&amp;')}">출처 보기 ↗</a></details>`).join('')}
for (const lesson of LESSONS) {
  const n=String(lesson.lesson).padStart(2,'0'), q=quizzes[lesson.lesson-1];
  if (list) {
    const link=document.createElement('a');
    link.className='lesson-card lesson-link';
    link.href=`lesson.html?lesson=${lesson.lesson}`;
    link.innerHTML=`<small>LESSON ${n} · 고1</small><h3>${lesson.title}</h3><p>${lesson.text}</p><span class="lesson-arrow" aria-hidden="true">↗</span>`;
    list.append(link);
    continue;
  }
  const lessonView=document.querySelector('#lesson-content');
  if(!lessonView || new URLSearchParams(location.search).get('lesson')!==String(lesson.lesson)) continue;
  const article=document.createElement('article');
  article.className='lesson-card lesson-detail';
  article.id=`lesson-${n}`;
  article.innerHTML=`<small>LESSON ${n} · 고1 · 50분</small><h3>${lesson.title}</h3><p><strong>함께 읽을 작품</strong> ${lesson.text}</p>${profileDetails(lesson.text)}<p><strong>교과서 연계</strong> ${lesson.book}</p><h4>오늘의 배움</h4><p>${lesson.goal}</p><h4>핵심 개념</h4><p>${lesson.concept}</p><h4>읽기 도움말</h4><p>${lesson.reading}</p><h4>생각하고 활동하기</h4><ol>${lesson.questions.map(x=>`<li>${x}</li>`).join('')}</ol><h4>선택 도전</h4><p>${lesson.challenge}</p><h4>수업을 마치며</h4><p>${lesson.exit}</p><div class="lesson-download"><a href="pdf/lesson-${n}-study.pdf" download>학습자료 PDF ↓</a><a href="pdf/lesson-${n}-worksheet.pdf" download>활동지 PDF ↓</a></div><div class="quiz"><h4>온라인 퀴즈</h4><p>${q[0]}</p><div class="quiz-options"></div><p class="quiz-feedback" role="status" aria-live="polite"></p></div>`;
  const options=article.querySelector('.quiz-options'), feedback=article.querySelector('.quiz-feedback');
  q[1].forEach((option,index)=>{const btn=document.createElement('button');btn.type='button';btn.textContent=option;btn.addEventListener('click',()=>{feedback.textContent=(index===q[2]?'정답입니다! ':'다시 생각해 보세요. ')+q[3];});options.append(btn)});
  lessonView.append(article);
}
const pdfList=document.querySelector('#pdf-list');
if(pdfList){
for(const [label,href] of [['학생용 전체 자료','pdf/student-complete.pdf'],['교사용 수업안과 예시답안','pdf/teacher-guide.pdf']]){const a=document.createElement('a');a.className='pdf-link';a.href=href;a.download='';a.textContent=label+' ↓';pdfList.append(a)}
const foundationFiles=document.createElement('div');foundationFiles.className='pdf-item';foundationFiles.innerHTML='<strong>첫 시간 · 문학 기초</strong><a href="pdf/foundation-study.pdf" download>학습자료 ↓</a><a href="pdf/foundation-worksheet.pdf" download>활동지 ↓</a>';pdfList.append(foundationFiles);
for(const lesson of LESSONS){const n=String(lesson.lesson).padStart(2,'0'),box=document.createElement('div');box.className='pdf-item';box.innerHTML=`<strong>${n}차시</strong><a href="pdf/lesson-${n}-study.pdf" download>학습자료 ↓</a><a href="pdf/lesson-${n}-worksheet.pdf" download>활동지 ↓</a>`;pdfList.append(box)}
}
const lessonView=document.querySelector('#lesson-content');
if(lessonView && !lessonView.children.length) lessonView.innerHTML='<p>해당 차시를 찾을 수 없습니다. <a href="index.html#lessons">전체 차시로 돌아가기</a></p>';
