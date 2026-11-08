import random, time
 
def weekly_totals(a):
    return [sum(a[i:i+7]) for i in range(0, len(a), 7)]
 
def wettest_driest(weeks):
    if not weeks: return None, None
    hi=max(range(len(weeks)), key=weeks.__getitem__)
    lo=min(range(len(weeks)), key=weeks.__getitem__)
    return (hi+1, weeks[hi]), (lo+1, weeks[lo])
 
def moving_naive(a, w=7):
    if w <= 0: raise ValueError("window must be positive")
    return [sum(a[i:i+w])/w for i in range(len(a)-w+1)]
 
def moving_running(a, w=7):
    if w <= 0: raise ValueError("window must be positive")
    if len(a)<w: return []
    total=sum(a[:w]); out=[total/w]
    for i in range(w,len(a)):
        total += a[i]-a[i-w]
        out.append(total/w)
    return out
 
def dry_days(a):
    return [i+1 for i,x in enumerate(a) if x==0]
 
if __name__=="__main__":
    rainfall=[random.randint(0,30) for _ in range(365)]
    weeks=weekly_totals(rainfall)
    print("Weekly totals:", weeks)
    print("Wettest, driest:", wettest_driest(weeks))
    print("Moving averages:", moving_running(rainfall)[:5])
    print("Dry days:", dry_days(rainfall))
    print("Empty/short:", moving_running([]), moving_running([1,2,3]))
    for n in (365,36500,365000):
        data=[random.random()*30 for _ in range(n)]
        for name,fn in (("naive",moving_naive),("running",moving_running)):
            start=time.perf_counter(); result=fn(data)
            print(n,name,round(time.perf_counter()-start,6),len(result))
