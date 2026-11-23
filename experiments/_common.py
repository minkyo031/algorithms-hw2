"""Deterministic experiment helpers; only standard library."""
import csv, random
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def keys_for(seed, n):
    rng=random.Random(seed)
    return ['https://example.org/item/'+str(rng.getrandbits(60))+'-'+str(i) for i in range(n)]

def benchmark(table, stored, missing, sample=1000):
    rng=random.Random(12345)
    present=[stored[rng.randrange(len(stored))] for _ in range(sample)]
    ok=sum(table.get_with_cost(key)[1] for key in present)/sample
    fail=sum(table.get_with_cost(key)[1] for key in missing[:sample])/sample
    return ok,fail

def write_csv(name,headers,rows):
    with (ROOT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)

def svg_chart(filename, series, title, max_y=None):
    """series: [(name, [(x,y),...]), ...]"""
    width,height=1050,600; x0,y0=85,505; pw,ph=870,395
    xmax=max(x for _,data in series for x,_ in data)
    ymax=max_y or max(y for _,data in series for _,y in data)*1.08
    xmin=min(x for _,data in series for x,_ in data)
    if xmin==xmax: xmin=0
    colors=['#1670c5','#ef6534','#13966a','#8b5dc1']
    buf=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         '<rect width="100%" height="100%" fill="white"/>',f'<text x="{width/2}" y="40" font-size="22" text-anchor="middle">{title}</text>',
         f'<path d="M{x0} {y0-ph}V{y0}H{x0+pw}" stroke="#222" fill="none"/>']
    for k in range(6):
        y=y0-ph*k/5
        buf.append(f'<line x1="{x0}" y1="{y}" x2="{x0+pw}" y2="{y}" stroke="#ddd"/>')
        buf.append(f'<text x="{x0-10}" y="{y+5}" text-anchor="end" font-size="13">{ymax*k/5:.1f}</text>')
    for k in range(10):
        x=x0+pw*k/9
        value=xmin+(xmax-xmin)*k/9
        buf.append(f'<text x="{x}" y="{y0+22}" text-anchor="middle" font-size="12">{value:.2f}</text>')
    for i,(name,data) in enumerate(series):
        coords=' '.join(f'{x0+pw*(x-xmin)/(xmax-xmin):.2f},{y0-ph*y/ymax:.2f}' for x,y in data)
        dash=' stroke-dasharray="8 5"' if 'theory' in name.lower() else ''
        buf.append(f'<polyline points="{coords}" fill="none" stroke="{colors[i%len(colors)]}" stroke-width="2.5"{dash}/>')
        buf.append(f'<line x1="{x0+i*240}" y1="560" x2="{x0+30+i*240}" y2="560" stroke="{colors[i%len(colors)]}" stroke-width="3"{dash}/><text x="{x0+35+i*240}" y="565" font-size="13">{name}</text>')
    buf.append('<text x="520" y="585" text-anchor="middle">Load factor (alpha)</text>')
    buf.append('</svg>')
    (ROOT/filename).write_text(''.join(buf),encoding='utf-8')
