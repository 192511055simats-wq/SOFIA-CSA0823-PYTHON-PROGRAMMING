import random, time, sys
 
def loop_version(values):
    valid=[]
    for c in values:
        if -50<=c<=50: valid.append(c)
    fahrenheit=[]
    for c in valid: fahrenheit.append(c*9/5+32)
    alarms=[]
    for minute,c in enumerate(values,start=1):
        if -50<=c<=50 and not 2<=c<=8:
            alarms.append(minute)
    return valid,fahrenheit,alarms
 
def comprehension_version(values):
    valid=[c for c in values if -50<=c<=50]
    fahrenheit=[c*9/5+32 for c in valid]
    alarms=[i for i,c in enumerate(values,start=1) if -50<=c<=50 and not 2<=c<=8]
    return valid,fahrenheit,alarms
 
def map_filter_version(values):
    valid=list(filter(lambda c:-50<=c<=50,values))
    fahrenheit=list(map(lambda c:c*9/5+32,valid))
    alarms=[i for i,c in enumerate(values,start=1) if -50<=c<=50 and not 2<=c<=8]
    return valid,fahrenheit,alarms
 
readings=[random.uniform(-55,55) for _ in range(100000)]
a=loop_version(readings); b=comprehension_version(readings); c=map_filter_version(readings)
print("identical:",a==b==c,"valid:",len(b[0]),"first F:",b[1][:5])
for n in (10000,100000,1000000):
    data=[random.uniform(-55,55) for _ in range(n)]
    for fn in (loop_version,comprehension_version,map_filter_version):
        start=time.perf_counter(); fn(data)
        print(n,fn.__name__,round(time.perf_counter()-start,6))
lst=[x*2 for x in readings]
gen=(x*2 for x in readings)
print("memory:",sys.getsizeof(lst),sys.getsizeof(gen))
print("all valid:",comprehension_version([2,4,8])[0])
print("all invalid:",comprehension_version([51,-51])[0])
