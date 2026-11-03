import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
class Element {constructor(){this.children=[];this.handlers={};this.innerHTML='';this.nodes={};this.textContent=''} append(x){this.children.push(x)} addEventListener(n,f){this.handlers[n]=f} click(){this.handlers.click?.()} querySelector(s){return this.nodes[s]??=new Element()}}
const source=fs.readFileSync('lessons.js','utf8')+'\n'+fs.readFileSync('app.js','utf8')+'\nthis.quiz=quizzes;';
function render(ids,search=''){const document={querySelector:id=>ids[id]??null,createElement:()=>new Element()};const ctx=vm.createContext({document,location:{search},URLSearchParams});vm.runInContext(source,ctx);return ctx}
const list=new Element(),pdfs=new Element();render({'#lesson-list':list,'#pdf-list':pdfs});
assert.equal(list.children.length,12);assert.equal(pdfs.children.length,14);
for(let i=0;i<12;i++){
 const n=String(i+1).padStart(2,'0');assert.equal(list.children[i].href,`lesson.html?lesson=${i+1}`);
 const view=new Element(),ctx=render({'#lesson-content':view},`?lesson=${i+1}`);assert.equal(view.children.length,1);
 const card=view.children[0],opts=card.querySelector('.quiz-options').children,feedback=card.querySelector('.quiz-feedback');
 assert.ok(card.innerHTML.includes('고1'));assert.ok(!card.innerHTML.includes('10공국'));
 for(const type of ['study','worksheet']){const p=`pdf/lesson-${n}-${type}.pdf`;assert.ok(card.innerHTML.includes(p));assert.ok(fs.existsSync(p));}
 assert.equal(opts.length,3);opts[ctx.quiz[i][2]].click();assert.ok(feedback.textContent.startsWith('정답입니다!'));opts[(ctx.quiz[i][2]+1)%3].click();assert.ok(feedback.textContent.startsWith('다시 생각해 보세요.'));
}
const bad=new Element();render({'#lesson-content':bad},'?lesson=13');assert.ok(bad.innerHTML.includes('찾을 수 없습니다'));
assert.ok(fs.readFileSync('lesson.html','utf8').includes('id="lesson-content"'));
console.log('12 lesson links, detail pages, quizzes, PDFs and invalid selection verified.');
