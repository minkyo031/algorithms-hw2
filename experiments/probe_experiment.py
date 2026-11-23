from src.hash_table import HashTable
from ._common import keys_for,benchmark,write_csv,svg_chart

def run():
    m=4093; rows=[]; succ=[];fail=[];theory_s=[];theory_f=[]
    keys=keys_for(2026,4*m+2000); missing=keys_for(3030,2000)
    for a in (0.25,0.5,0.75,1,1.5,2,3,4):
        t=HashTable(m,max_load=None)
        subset=keys[:round(m*a)]
        for k in subset:t.put(k,k)
        s,f=benchmark(t,subset,missing)
        rows.append((a,round(s,4),round(1+a/2,4),round(f,4),round(a,4)))
        succ.append((a,s));fail.append((a,f));theory_s.append((a,1+a/2));theory_f.append((a,a))
    write_csv('results.csv',['alpha','success_experimental','success_theory','failure_experimental','failure_theory'],rows)
    svg_chart('chaining.svg',[('success observed',succ),('success theory',theory_s),('failure observed',fail),('failure theory',theory_f)],'Separate chaining: observed vs theory')
    print('Chaining results:',rows)

if __name__=='__main__':run()
