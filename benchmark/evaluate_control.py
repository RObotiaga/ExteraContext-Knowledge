from __future__ import annotations
import json,re,sqlite3,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((Path(__file__).with_name('cases.json')).read_text('utf-8'))
STOP={'как','что','для','или','это','при','над','под','мне','нужно','сделать','the','and','for','with','from','into','how','use','using','plugin','плагин','exteragram','ayugram','а','и','в','на','с','до','у','из','по','потом','чтобы'}

def toks(s):
    return [w for w in re.findall(r'[A-Za-zА-Яа-яЁё0-9_.$:@+-]+',s.lower()) if len(w)>1 and w not in STOP]

def score(query,row):
    qt=toks(query)
    fields=[row['api'] or '',row['claim'] or '',row['recipe'] or '',row['topic'] or '',row['canonical_topic'] or '']
    hay=' '.join(fields).lower()
    return sum(1 for t in qt if t in hay)

c=sqlite3.connect(ROOT/'data/exteracontext.sqlite'); c.row_factory=sqlite3.Row
allrows=list(c.execute('select * from facts'))
res=[]
for case in cases:
    ranked=sorted(((score(case['query'],r),r['id']) for r in allrows),reverse=True)
    ids=[i for s,i in ranked if s>0][:10]
    exp=set(case['expected'])
    ranks={e:(ids.index(e)+1 if e in ids else None) for e in exp}
    vals=[x for x in ranks.values() if x]
    ar=min(vals) if vals else None
    res.append({'id':case['id'],'top1':bool(ar and ar<=1),'top3':bool(ar and ar<=3),'top5':bool(ar and ar<=5),'top10':bool(ar),'recall':sum(e in ids for e in exp)/len(exp),'ranks':ranks,'top_ids':ids[:5]})
summary={k:statistics.mean([r[k] for r in res]) for k in ['top1','top3','top5','top10','recall']}
print(json.dumps({'summary':summary,'cases':res},ensure_ascii=False,indent=2))
