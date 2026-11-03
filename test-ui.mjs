import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
class Element {
  constructor(){this.children=[];this.handlers={};this.innerHTML='';this.nodes={};this.textContent='';}
  append(x){this.children.push(x)}
  addEventListener(name,fn){this.handlers[name]=fn}
  click(){this.handlers.click?.()}
  querySelector(sel){return this.nodes[sel]??=new Element()}
}
const ids={'#lesson-list':new Element(),'#pdf-list':new Element()};
const document={querySelector:id=>ids[id],createElement:()=>new Element()};
const context=vm.createContext({document});
vm.runInContext(fs.readFileSync('lessons.js','utf8')+'\n'+fs.readFileSync('app.js','utf8')+'\nthis.quiz=quizzes;',context);
assert.equal(ids['#lesson-list'].children.length,12);assert.equal(ids['#pdf-list'].children.length,14);
for(let i=0;i<12;i++){
 const card=ids['#lesson-list'].children[i], n=String(i+1).padStart(2,'0'), opts=card.querySelector('.quiz-options').children,feedback=card.querySelector('.quiz-feedback');
 assert.ok(card.innerHTML.includes('고1'));assert.ok(!card.innerHTML.includes('10공국'));
 for(const type of ['study','worksheet']){const p=`pdf/lesson-${n}-${type}.pdf`;assert.ok(card.innerHTML.includes(p));assert.ok(fs.existsSync(p));}
 assert.equal(opts.length,3);opts[context.quiz[i][2]].click();assert.ok(feedback.textContent.startsWith('정답입니다!'));opts[(context.quiz[i][2]+1)%3].click();assert.ok(feedback.textContent.startsWith('다시 생각해 보세요.'));
}
console.log('12 inline lessons, 24 lesson links and 12 quiz answers passed DOM checks.');
