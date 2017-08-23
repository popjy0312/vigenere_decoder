import ngram_log as ns
tri_log = ns.ngram_score('english_trigrams.txt')

def sft(char, num):
    t = ord(char)+num
    if t>ord('Z'):
        t -= 26
    elif t<ord('A'):
        t += 26
    return chr(t)

#s = "CSLSXDCVKADHMVFVHHKBOUWEUYJBODPPHIDGFDUHGYIBYVFKKPBXFKZFGQQL"
s = "RSWBSTHTVQPGANWTWVPLUPFHUFTXZGQBLMJMLKLHAFSNXXIOSZLLHJITTHAYISOTRSJIUXUSJIKWPZRMIDNXMLPQLFIBWWMOHQNIDOPHWVMBDRECZMXOFTLOHLKGZSVLRPMWMMTCBCAXJRSBGXYHIXDWKNEMEOXTILMFNPAOHQAMLLCWEKPRKZQBZSOLOKWLELHSHQCGVHWKPFLLEWYKBPAHPMWBJHKSUIGGNAMFLMTYHFVGGVCWIDTXPVBODLZJQWFIKHMIVNLDLILYWSYJIWRSXPXEZKLIBEPTPHVVFHUSZZWETLMSEBHTSWQWWHWFRGVRVATINRDAKGDPCEUSLFZYIFEAILIVGDYAYSFKXELWHLAPRWSBGXAEZRSTXFSXWEGJWOAQEDZBEWTENIFXNYOEAGEAVLZLOLXZKPGYBHKKILHLXBCFTTLCMWRHSXDMDMAWOIWRBLMJMTKDEOMGGOSICZPLLWHSCRT"

MAX_KEY_LEN = 10

array = [ [] for row in range(MAX_KEY_LEN)]
count = [0]*MAX_KEY_LEN

for key_len in range(3,MAX_KEY_LEN):
    print key_len
    for key_idx in range(0, key_len):
        best_score = -9999999999
        for key_ch1 in range(0,26):
            for key_ch2 in range(0,26):
                for key_ch3 in range(0,26):
                    fitness = 0
                    i = key_idx
                    while(i < len(s)-2):
                        c1 = sft(s[i],key_ch1)
                        c2 = sft(s[i+1],key_ch2)
                        c3 = sft(s[i+2],key_ch3)
                        fitness += tri_log.score(c1+c2+c3)
                        i += key_len
                    if(fitness > best_score):
                        best_score = fitness
                        best_key_ch1 = key_ch1
                        best_key_ch2 = key_ch2
                        best_key_ch3 = key_ch3
        if(key_idx == 0):
            best_score_0 = best_score
            best_key_ch1_0 = best_key_ch1
            best_key_ch2_0 = best_key_ch2
            best_key_ch3_0 = best_key_ch3
            array[key_len].append(0)
        elif(key_idx == 1):
            best_score_1 = best_score
            best_key_ch1_1 = best_key_ch1
            best_key_ch2_1 = best_key_ch2
            best_key_ch3_1 = best_key_ch3
            array[key_len].append(0)
            prev_prev_best_score = prev_best_score
            prev_prev_best_key_ch3 = prev_best_key_ch3
        else:
            if(prev_prev_best_key_ch3 == prev_best_key_ch2):
                count[key_len] += 1
            if(prev_best_key_ch2 == best_key_ch1):
                count[key_len] += 1
            if(best_key_ch1 == prev_prev_best_key_ch3):
                count[key_len] += 1
            if(max(prev_prev_best_score, prev_best_score, best_score) == prev_prev_best_score):
                array[key_len].append(prev_prev_best_key_ch3)
            elif(max(prev_prev_best_score, prev_best_score, best_score) == prev_best_score):
                array[key_len].append(prev_best_key_ch2)
            else:
                array[key_len].append(best_key_ch1)
            prev_prev_best_score = prev_best_score
            prev_prev_best_key_ch3 = prev_best_key_ch3
        prev_best_score = best_score
        prev_best_key_ch2 = best_key_ch2
        prev_best_key_ch3 = best_key_ch3

    # 0
    if(prev_prev_best_key_ch3 == prev_best_key_ch2):
        count[key_len] += 1
    if(prev_best_key_ch2 == best_key_ch1_0):
        count[key_len] += 1
    if(best_key_ch1_0 == prev_prev_best_key_ch3):
        count[key_len] += 1
    if(max(prev_prev_best_score, prev_best_score, best_score_0) == prev_prev_best_score):
        array[key_len][0] = prev_prev_best_key_ch3
    elif(max(prev_prev_best_score, prev_best_score, best_score_0) == prev_best_score):
        array[key_len][0] = prev_best_key_ch2
    else:
        array[key_len][0] = best_key_ch1_0

    # 1
    if(prev_best_key_ch3 == best_key_ch2_0):
        count[key_len] += 1
    if(best_key_ch2_0 == best_key_ch1_1):
        count[key_len] += 1
    if(best_key_ch1_1 == prev_best_key_ch3):
        count[key_len] += 1
    if(max(prev_best_score, best_score_0, best_score_1) == prev_best_score):
        array[key_len][1] = prev_best_key_ch3
    elif(max( prev_best_score, best_score_0, best_score_1) == best_score_0):
        array[key_len][1] = best_key_ch2_0
    else:
        array[key_len][1] = best_key_ch1_1

    count[key_len] = count[key_len] * 1.0 / key_len

    f = open("./out.txt","a")
    print >>f,"len %d count %d" % (key_len, count[key_len])
    print >>f,''.join(sft(s[j],array[key_len][j%key_len]) for j in range(0, len(s)))
    f.close()


'''
#Find best key length
Max_count = 0
for i in range(3,MAX_KEY_LEN):
    if(Max_count < count[i]):
        Max_count = count[i]
        best_key_len = i;

# print PLAIN TEXT
print "best len is %d" % best_key_len
print ''.join(sft(s[i],array[best_key_len][i%best_key_len]) for i in range(0, len(s)))
'''