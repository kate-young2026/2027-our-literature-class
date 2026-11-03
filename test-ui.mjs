// Fast DOM contract check; this does not replace testing in a real browser.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

class Element {
  constructor() { this.children=[]; this.handlers={}; this.innerHTML=''; this.open=false; }
  append(child) { this.children.push(child); }
  addEventListener(name, fn) { this.handlers[name]=fn; }
  showModal() { this.open=true; }
  close() { this.open=false; }
  click() { this.handlers.click?.(); }
}
const ids = Object.fromEntries(['#lesson-list','#lesson-dialog','#dialog-content','#close-dialog','#pdf-list'].map(id=>[id,new Element()]));
const document={querySelector:id=>ids[id],createElement:()=>new Element()};
const context=vm.createContext({document});
vm.runInContext(fs.readFileSync('lessons.js','utf8')+'\n'+fs.readFileSync('app.js','utf8'),context);
assert.equal(ids['#lesson-list'].children.length,12);
assert.equal(ids['#pdf-list'].children.length,14);
for (let i=0;i<12;i++) {
  ids['#lesson-list'].children[i].click();
  assert.equal(ids['#lesson-dialog'].open,true);
  assert.ok(ids['#dialog-content'].innerHTML.includes(`${i+1}차시`));
  ids['#close-dialog'].click();
  assert.equal(ids['#lesson-dialog'].open,false);
  const html=ids['#pdf-list'].children[i+2].innerHTML;
  const n=String(i+1).padStart(2,'0');
  for(const type of ['study','worksheet']) {
    const path=`pdf/lesson-${n}-${type}.pdf`;
    assert.ok(html.includes(path)); assert.ok(fs.existsSync(path));
  }
}
for(const item of ids['#pdf-list'].children.slice(0,2)) assert.ok(fs.existsSync(item.href));
console.log('12 lesson dialogs and 26 PDF link targets passed DOM contract check.');
