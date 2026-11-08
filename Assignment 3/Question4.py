import time
ai={"192311001","192311004","192311007","192311009"}
iot={"192311002","192311004","192311009","192311010"}
all_students={f"1923110{i:02d}" for i in range(1,11)}
both=ai & iot
exactly_one=ai ^ iot
neither=all_students - (ai | iot)
print("clash      :",sorted(both))
print("exactly one:",sorted(exactly_one))
print("neither    :",sorted(neither))
# Set-method version
print(both==ai.intersection(iot))
print(exactly_one==ai.symmetric_difference(iot))
print(neither==all_students.difference(ai.union(iot)))
 
# Membership experiment
for n in (10_000,100_000,1_000_000):
    values=[str(i) for i in range(n)]; values_set=set(values)
    target=str(n-1)
    start=time.perf_counter(); target in values
    lt=time.perf_counter()-start
    start=time.perf_counter(); target in values_set
    st=time.perf_counter()-start
    print(n,"list",lt,"set",st)
