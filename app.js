'use strict';
const list = document.querySelector('#lesson-list');
const dialog = document.querySelector('#lesson-dialog');
const content = document.querySelector('#dialog-content');
for (const lesson of LESSONS) {
  const button = document.createElement('button');
  button.className = 'lesson-card';
  button.type = 'button';
  button.innerHTML = `<small>LESSON ${String(lesson.lesson).padStart(2,'0')} · ${lesson.standard}</small><h3>${lesson.title}</h3><p>${lesson.text}</p>`;
  button.addEventListener('click', () => {
    content.innerHTML = `<p class="tag">${lesson.lesson}차시 · ${lesson.standard} · 50분</p><h2 id="dialog-title">${lesson.title}</h2><p><strong>함께 읽을 작품</strong> ${lesson.text}</p><p><strong>교과서 연계</strong> ${lesson.book}</p><h3>오늘의 배움</h3><p>${lesson.goal}</p><h3>핵심 개념</h3><p>${lesson.concept}</p><h3>읽기 도움말</h3><p>${lesson.reading}</p><h3>생각하고 활동하기</h3><ol>${lesson.questions.map(q => `<li>${q}</li>`).join('')}</ol><h3>선택 도전</h3><p>${lesson.challenge}</p><h3>수업을 마치며</h3><p>${lesson.exit}</p>`;
    dialog.showModal();
  });
  list.append(button);
}
document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
const pdfList = document.querySelector('#pdf-list');
for (const [label, href] of [['학생용 전체 자료','pdf/student-complete.pdf'],['교사용 수업안과 예시답안','pdf/teacher-guide.pdf']]) {
  const a = document.createElement('a'); a.className = 'pdf-link'; a.href = href; a.download = ''; a.textContent = label + ' ↓'; pdfList.append(a);
}
for (const lesson of LESSONS) {
  const n = String(lesson.lesson).padStart(2, '0');
  const box = document.createElement('div'); box.className = 'pdf-item';
  box.innerHTML = `<strong>${n}차시</strong><a href="pdf/lesson-${n}-study.pdf" download>학습자료 ↓</a><a href="pdf/lesson-${n}-worksheet.pdf" download>활동지 ↓</a>`;
  pdfList.append(box);
}
