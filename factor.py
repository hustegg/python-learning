from random import randint

def quickMulMod(a,b,m):
    '''a*b%m,  quick'''
    ret = 0
    while b:
        if b&1:
            ret = (a+ret)%m
        b//=2
        a = (a+a)%m
    return ret

def quickPowMod(a,b,m):
    '''a^b %m, quick,  O(logn)'''
    ret =1
    while b:
        if b&1:
            ret =quickMulMod(ret,a,m)
        b//=2
        a = quickMulMod(a,a,m)
    return ret


def isPrime(n,t=5):
    '''miller rabin primality test,  a probability result
        t is the number of iteration(witness)
    '''
    t = min(n-3,t)
    if n<2:
        print('[Error]: {} can\'t be classed with prime or composite'.format(n))
        return
    if n==2: return True
    d = n-1
    r = 0
    while d%2==0:
        r+=1
        d//=2
    tested=set()
    for i in range(t):
        a = randint(2,n-2)
        while a in tested:
            a = randint(2,n-2)
        tested.add(a)
        x= quickPowMod(a,d,n)
        if x==1 or x==n-1: continue  #success,
        for j in range(r-1):
            x= quickMulMod(x,x,n)
            if x==n-1:break
        else:
            return False
    return True

def gcd(a,b):
    while b!=0:
        a,b=b,a%b
    return a

def factor(n):
    '''pollard's rho algorithm'''
    if n==1: return []
    if isPrime(n):return [n]
    fact=1
    cycle_size=2
    x = x_fixed = 2
    c = randint(1,n)
    while fact==1:
        for i in range(cycle_size):
            if fact>1:break
            x=(x*x+c)%n
            if x==x_fixed:
                c = randint(1,n)
                continue
            fact = gcd(x-x_fixed,n)
        cycle_size *=2
        x_fixed = x
    return factor(fact)+factor(n//fact)
