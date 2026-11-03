'use strict';
const root=document.querySelector('#workshop-content');
const id=Number(new URLSearchParams(location.search).get('lesson'));
const w=WORKSHOPS.find(item=>item.id===id);
if(!w){root.innerHTML='<p>해당 수업을 찾을 수 없습니다.</p>';}else{
 const article=document.createElement('article');article.className='lesson-card lesson-detail';
 article.innerHTML=`<small>추가 탐구 ${w.id}차시 · 고1 · 50분</small><h1>${w.title}</h1><p>${w.subtitle}</p><p class="standards">연계 성취기준: ${w.standards}</p><h2>오늘의 목표</h2><p>${w.goal}</p>${w.theory.map(([h,t])=>`<h2>${h}</h2><p>${t}</p>`).join('')}<h2>학습 활동</h2><ol>${w.activities.map(t=>`<li>${t}</li>`).join('')}</ol><h2>모둠활동</h2><ul>${w.group.map(t=>`<li>${t}</li>`).join('')}</ul><h2>선택 도전</h2><p>${w.challenge}</p><div class="lesson-download"><a href="pdf/workshop-${w.id}-study.pdf" download>학습자료 PDF ↓</a><a href="pdf/workshop-${w.id}-worksheet.pdf" download>활동지 PDF ↓</a><a href="pdf/workshop-${w.id}-group.pdf" download>모둠활동 자료 PDF ↓</a></div><div class="quiz"><h2>온라인 퀴즈</h2><div class="workshop-questions"></div></div>`;
 const container=article.querySelector('.workshop-questions');w.quiz.forEach(([question,choices,answer,explanation],idx)=>{const box=document.createElement('div');box.className='foundation-question';const title=document.createElement('p');title.textContent=`${idx+1}. ${question}`;box.append(title);const feedback=document.createElement('p');feedback.setAttribute('role','status');feedback.setAttribute('aria-live','polite');choices.forEach((choice,i)=>{const b=document.createElement('button');b.type='button';b.textContent=choice;b.addEventListener('click',()=>{feedback.textContent=(i===answer?'정답입니다! ':'다시 생각해 보세요. ')+explanation});box.append(b)});box.append(feedback);container.append(box)});root.append(article);
}
