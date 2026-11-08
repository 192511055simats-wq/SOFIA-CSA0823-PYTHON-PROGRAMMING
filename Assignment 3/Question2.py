import copy, sys, time
rows, cols = 3, 4
bad = [[0]*cols]*rows
bad[0][1] = 7
good = [[0 for _ in range(cols)] for _ in range(rows)]
good[0][1] = 7
print("bad :",bad)
print("good:",good)
print(bad[0] is bad[1], good[0] is good[1])
 
stops={(13.0827,80.2707):"Chennai Central",
       (13.0418,80.2341):"T. Nagar"}
print(stops[(13.0418,80.2341)])
for (lat,lon),name in stops.items():
    print(name,lat,lon)
 
original=[[1,2],[3,4]]
alias=original
shallow=copy.copy(original)
slice_copy=original[:]
deep=copy.deepcopy(original)
original[0][0]=99
print("alias",alias,"shallow",shallow,"deep",deep)
print("identity",original is alias, original is shallow)
 
mixed=("route",[10,20])
mixed[1].append(30)
print(mixed)
try:
    stops[[13.0418,80.2341]]="bad key"
except TypeError as e:
    print(type(e).__name__,e)
 
values=list(range(1_000_000)); tup=tuple(values)
print("shallow sizes",sys.getsizeof(values),sys.getsizeof(tup))
for kind, factory in (("list",list),("tuple",tuple)):
    start=time.perf_counter(); obj=factory(range(1_000_000))
    create=time.perf_counter()-start
    start=time.perf_counter(); total=sum(obj[i] for i in range(0,1_000_000,1000))
    print(kind,"create",create,"index",time.perf_counter()-start,total)
