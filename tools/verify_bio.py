#!/usr/bin/env python3
"""Prove the biography page reproduces the family's document verbatim.

Usage: python3 tools/verify_bio.py <page.html> <source.docx>
Extracts every paragraph from the docx and confirms each appears in the page
text exactly (whitespace and curly-quote normalisation only). Exits 1 on any
missing or altered paragraph. This is the check Aunty Vivian asked for in May:
"Please ensure that it is reproduced accurately... the content is not changed."
"""
import re, sys, html, subprocess

def norm(s):
    s=re.sub(r'[\u2018\u2019]',"'",s); s=re.sub(r'[\u201c\u201d]','"',s)
    return ' '.join(s.split())

def docx_paras(path):
    md=subprocess.run(['pandoc','-t','markdown',path],capture_output=True,text=True).stdout
    md=re.sub(r'\\\n',' ',md).replace('\\','')
    return [' '.join(p.split()) for p in re.split(r'\n\s*\n',md) if p.strip()]

def page_text(path):
    h=open(path).read()
    h=re.sub(r'<(script|style)[^>]*>.*?</\1>','',h,flags=re.S)
    h=re.sub(r'<div class="banner">.*?</div>','',h,flags=re.S)
    h=re.sub(r'<h2>.*?</h2>','',h,flags=re.S)
    h=re.sub(r'<p class="bio-sub">.*?</p>','',h,flags=re.S)
    return norm(html.unescape(re.sub(r'<[^>]+>',' ',h)))

page, src = sys.argv[1], sys.argv[2]
pt=page_text(page); bad=[]
paras=docx_paras(src)
for i,p in enumerate(paras):
    if norm(re.sub(r'^[-•]\s*','',p)) not in pt:
        bad.append((i,p[:80]))
print(f"{len(paras)} source paragraphs; {len(bad)} missing/altered")
for i,p in bad: print(f"  [{i}] {p}")
sys.exit(1 if bad else 0)
