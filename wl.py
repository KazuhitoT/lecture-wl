from conf import TwoDimIsingConf
import random, math

f = 1.0
f_end = 0.00001

L = 8
N = L * L
E_max  =  2.0 * N
E_min  = -2.0 * N
E_diff = (E_max-E_min) / float(N-1)

conf = TwoDimIsingConf(1, L)

S = [0.0] * (N-1)

def isHistogramFlat(H):
    average   = sum(H)/float(len(H))
    criterion = 0.8 * average
    for i in range(0, len(H)) :
        # print H[i], criterion, H[i] <= criterion
        if H[i] <= criterion :
            return False
    return True


while f > f_end :

    H = [0] * (N-1)
    step = 1

    while True:

        E_before = conf.E
        index_before = int( (E_before-E_min) / E_diff )
        if index_before >= (N-1):
            index_before = N-2

        x = random.randrange(0, L)
        y = random.randrange(0, L)
        
        E_after = E_before + conf.conf[x][y].calcDiffFlipEnergy()
        index_after = int( (E_after-E_min) / E_diff )
        if index_after >= (N-1):
            index_after = N-2

        index_update = index_before

        if math.exp(S[index_before]-S[index_after]) >= random.random() :
            index_update = index_after
            conf.conf[x][y].flip()
            conf.E = E_after

        S[index_update] += f
        H[index_update] += 1

        step += 1
        if (step%(N*100) == 0) and isHistogramFlat(H) :
            break

    f /= 2.0
    
    print " calculating DOS at f = " , f

    file_output = open('result_f_'+str(f), 'w')
    for i in range(0, len(S)):
        file_output.write( str(i)+" "+str(S[i])+" "+str(H[i])+"\n")
    file_output.close()


