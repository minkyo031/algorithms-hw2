from src.hash_table import HashTable,LinearProbingHashTable
from ._common import keys_for,benchmark,write_csv,svg_chart

def run():
    m=4093;rows=[]
    keys=keys_for(2026,m); missing=keys_for(3030,1200)
    for alpha10 in range(1,10):
        alpha=alpha10/10
        subset=keys[:round(alpha*m)]
        measurements=[]
        for cls in (HashTable,LinearProbingHashTable):
            t=cls(m,max_load=None)
            for k in subset: t.put(k,k)
            measurements.extend(benchmark(t,subset,missing))
        cs,cf,ls,lf=measurements
        rows.append((alpha,cs,cf,ls,lf,1+alpha/2,alpha,(1+1/(1-alpha))/2,(1+1/(1-alpha)**2)/2))
    headers=['alpha','chaining_success','chaining_failure','linear_success','linear_failure','chaining_success_theory','chaining_failure_theory','linear_success_theory','linear_failure_theory']
    write_csv('comparison.csv',headers,[[round(x,4) for x in row] for row in rows])
    for label,offset in (('success',1),('failure',2)):
        svg_chart('comparison_'+label+'.svg',[(name,[(r[0],r[i]) for r in rows]) for name,i in [('chaining observed',offset),('chaining theory',offset+4),('linear observed',offset+2),('linear theory',offset+6)]],label.title()+' search cost: measured vs theory')
    print('Comparison results:')
    for row in rows: print('alpha=%.1f chaining=(%.2f, %.2f) linear=(%.2f, %.2f)'%row[:5])

if __name__=='__main__':run()
