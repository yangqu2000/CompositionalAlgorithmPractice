from music21 import *
 
def Markov(text,order=1):
    """Compute a Markov models (fixed length motif dictionary)."""
    
    dict3 = {}
    for i in range(len(text)-order):
        W = text[i:i+order]
        k  = text[i+order]
        if type(W) == list:
            W = ''.join(W)
        if W in dict3:
            kseen = dict3[W].keys()
            if k in kseen:
                dict3[W][k] += 1
            else:
                dict3[W][k] = 1
        else:
            dict3[W] = {k:1}

    for x in dict3:
        dict3[x] = dict3[x].items()
    dict3 = Normalize(dict3)    
    return dict3
    
def Normalize(dict2):
    """Turns the counters in every element of dict2 to probabilities"""
    
    for W in dict2:
        cnt = [tup[1] for tup in dict2[W]]
        ttl = sum(cnt)
        for k,tup in enumerate(dict2[W]):
            dict2[W][k] = (tup[0],float(tup[1])/ttl)
    return dict2
                   
def MaxOrder(text,order):
    dictall = {}
    for o in range(order):
        dicto = Markov(text,o)
        dictall.update(dicto)
    return dictall

from numpy.random import multinomial as randm
from numpy import where

def IPGenerate(n,dict2):
    p = 0
    out = []
    for k in range(n):
        while True:
            context = "".join(out[-p:])
            if context in dict2:
                prob = [tup[1] for tup in dict2[context]]
                conti = where(randm(1,prob))[0][0]
                cont = dict2[context][conti][0]
                out.append(cont) # = out + cont
#                print prob, conti, cont, out
                break
            else:
                p = p-1
    return out

    
#import os
#filename = os.path.abspath('') + '/Suite_No_1_for_Cello_M1_Prelude.mxl'
#s = music21.converter.parse(filename)
#c = s.getElementById('Violoncello')

'''
s = corpus.parse('bach/bwv108.6.xml')
c = s.getElementById('Soprano')
m = c.flat.notes
'''

import os
filename = '/Users/sdubnov/Documents/Notebooks/Freddie Freeloader Solo - Finaled v1 copy.xml'
print(filename)
s = converter.parse(filename)
#s.show()
m = s.flat.notesAndRests

from numpy import log2

# just a dirty way not to deal with triplets...
note_seq = []
dur_seq = []
for x in m:
    if (type(x) is note.Note) or (type(x) is note.Rest):
        note_seq.append(x.name)
        dur = int(4./x.quarterLength)
        dur = pow(2,int(log2(dur)))
        dur_seq.append(str(dur))
        
#note_seq = [x.name for x in m if type(x) is note.Note]  
#dur_seq_qL = [str(x.quarterLength) for x in m if type(x) is note.Note]
#dur_seq = [str(int(4./x.quarterLength)) for x in m if type(x) is note.Note]

memoryorder = 3
toomanynotes = 100
N = MaxOrder(note_seq,memoryorder)
out_n = IPGenerate(toomanynotes,N)
D = MaxOrder(dur_seq,memoryorder)
out_d = IPGenerate(toomanynotes,D)

#for teaching purposes use short input sequence (note_seq[0:10] and dur_seq[0:10])
#print(N)
#print(D)

#change "rest" to 'r' for tinynotation
for i,nn in enumerate(out_n):
    if nn == 'rest':
        out_n[i] = 'r'

out = []
for i in range(len(out_n)):
    out.append(out_n[i].lower()+out_d[i])

out_tn = "tinyNotation: " + " ".join(out)
sout = converter.parse(out_tn)
sout.show()
#sout.show('midi')

s.measures(0,20).show()

'''
#Compare to original melody
outs = stream.Score()
for i in range(len(s.parts)):
    outs.insert(0,stream.Part())
    for m in s.parts[i].recurse():
#        print(type(m))
        if isinstance(m, note.Note): 
            outs.parts[i].append(m)
        else:
            continue

outs.show()
len(outs)
'''