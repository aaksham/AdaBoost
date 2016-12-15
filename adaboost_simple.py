import math
import numpy
from collections import defaultdict

def predict(data,dstump,sign):
    psign=[]
    for point in data:
            if sign=='less':    
                if point<=dstump:
                    psign.append(1)
                else: psign.append(-1)
            else:
                if point>dstump:
                    psign.append(1)
                else: psign.append(-1)
    return psign

def calc_error(actual,predicted,wts):
    error_denom=sum(wts)
    error_num=0
    for i in range(len(actual)):
        if predicted[i]!=actual[i]:
            error_num=error_num+wts[i]
    return(float(error_num)/float(error_denom))

def find_hypothesis(wts,data,dstumps,sign,l):
    errs=[]
    for dstump in dstumps:
        psign=predict(data,dstump,sign)
        errs.append(calc_error(l,psign,wts))
    minerr=min(errs)
    minidx=errs.index(minerr)
    return minerr,minidx

def adjust_weights(old_wts,alpha,actual,pred):
    new_wts=[]
    z=sum(old_wts)
    print 'z'
    print z
    for i in range(len(actual)):
        new_wts.append((old_wts[i]*math.exp(-1*alpha*actual[i]*pred[i]))/float(z))
    return new_wts

x=[1,2,5,5,3,3,3,4,5]
y=[2,3,1,2,1,2,4,4,4]
l=[1,1,1,1,-1,-1,-1,-1,-1]
di=[1,2,9,8,5,4,3,6,7]

xstumps=[1,2,3,4,5]
ystumps=[1,2,3,4,5]
alphas=[]
wts=[1.0/9.0]*9
iterations=defaultdict(list)

for k in range(3):
    errors=[]
    hcandidates=[]
    e,c=find_hypothesis(wts,x,xstumps,'less',l)
    errors.append(e)
    hcandidates.append(c)
    e,c=find_hypothesis(wts,x,xstumps,'greater',l)
    errors.append(e)
    hcandidates.append(c)
    e,c=find_hypothesis(wts,y,ystumps,'less',l)
    errors.append(e)
    hcandidates.append(c)
    e,c=find_hypothesis(wts,y,ystumps,'greater',l)
    errors.append(e)
    hcandidates.append(c)
    minstumpi=errors.index(min(errors))
    minstump=hcandidates[minstumpi]
    if minstumpi==0:
        predicted=predict(x,xstumps[minstump],'less')
        print 'less','x',xstumps[minstump]
    elif minstumpi==1:
        predicted=predict(x,xstumps[minstump],'greater')
        print 'greater','x',xstumps[minstump]
    elif minstumpi==2:
        predicted=predict(y,ystumps[minstump],'less')
        print 'less','y',ystumps[minstump]
    elif minstumpi==3:
        predicted=predict(y,ystumps[minstump],'greater')
        print 'greater','y',ystumps[minstump]
    iterations[k]=predicted
    hypothesis_error=calc_error(l,predicted,wts)
    alpha=0.5*math.log(float(1-hypothesis_error)/float(hypothesis_error))
    wts=adjust_weights(wts,alpha,l,predicted)
    print hypothesis_error
    print wts
    alphas.append(alpha)
    Hpred=[]
    for j in range(len(x)):
        p=0
        for m in range(k+1):
            p=p+alphas[m]*iterations[m][j]
        Hpred.append(numpy.sign(p))
    errsh=calc_error(l,Hpred,[1]*9)
    print errsh
    
        
