import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';

for (const file of ['app.js', 'lessons.js']) execFileSync(process.execPath, ['--check', file]);
const context = vm.createContext({});
vm.runInContext(fs.readFileSync('lessons.js', 'utf8') + '\nthis.lessons = LESSONS;', context);
const lessons = context.lessons;
assert.equal(lessons.length, 12);
const expected = ['10공국1-05-01','10공국1-05-01','10공국1-05-02','10공국1-05-02','10공국1-05-03','10공국1-05-03','10공국2-05-01','10공국2-05-01','10공국2-05-01','10공국2-05-02','10공국2-05-02','10공국2-05-02'];
for (let i = 0; i < lessons.length; i++) {
  const lesson = lessons[i];
  assert.equal(lesson.lesson, i + 1);
  assert.equal(lesson.standard, expected[i]);
  for (const field of ['title','text','book','goal','concept','reading','challenge','exit']) assert.ok(lesson[field], `${i+1}: ${field}`);
  assert.equal(lesson.questions.length, 3);
  for (const type of ['study','worksheet']) {
    const path = `pdf/lesson-${String(i+1).padStart(2,'0')}-${type}.pdf`;
    assert.equal(fs.readFileSync(path).subarray(0, 5).toString(), '%PDF-', path);
  }
}
for (const name of ['student-complete','teacher-guide']) assert.equal(fs.readFileSync(`pdf/${name}.pdf`).subarray(0,5).toString(),'%PDF-');
const html = fs.readFileSync('index.html','utf8');
for (const id of ['main','literature','literature-lessons','lessons','works','timeline','downloads','sources','lesson-list','pdf-list']) assert.ok(html.includes(`id="${id}"`), id);
assert.ok(html.includes('href="#literature"'));
for(const page of ['lesson.html','workshop.html']) assert.ok(fs.readFileSync(page,'utf8').includes('href="index.html#literature"'),page);
for(const page of ['index.html','lesson.html','workshop.html']) assert.ok(fs.readFileSync(page,'utf8').includes('href="admin.html"'),`${page}: admin link`);
console.log('12 lessons, five standards, 26 PDF headers, and page targets verified.');
