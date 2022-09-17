'''
Written by YaoYuan.
The functions:
select CCvalue to cutpha 
'''
import os
MIN_VALUE = 0.8 #选出0.29到0.3范围的行
MAX_VALUE = 1.0
fpha_in = '/home/yaoyuan/Desktop/myprogram/convertMESS2cutpha/airgun53265.pha'
fpha_out = '/home/yaoyuan/Desktop/myprogram/convertMESS2cutpha/airgun53265v2.pha'
# i/o paths
f=open(fpha_in); lines =f.readlines(); f.close()
fout = open(fpha_out,'w')
i = 0
while i < len(lines):
    line = lines[i]
    codes = line.split(',')
    #print(codes)
    #print(codes[0])
    a = len(codes[0])
    #print(a)
    if a > 8:
        #print(codes)
        ot = codes[1]
        print(ot)
        otyear = ot[0:4]
        otmon = ot[5:7]
        otday = ot[8:10]
        othur = ot[11:13]
        otmin = ot[14:16]
        otsec = ot[17:19]
        otminsec = ot[20:22]
        print(otyear,otmon)
        lat, lon, mag, cc = codes[2:6]
        #不满足条件时跳过两行继续读
        if not (eval(cc) >= MIN_VALUE and eval(cc) <= MAX_VALUE):
            i += 2
            continue
        fout.write('{}{}{}{}{}{}.{},{},{},{},{}'\
                .format(otyear, otmon, otday, othur, otmin, otsec ,otminsec, lat, lon, mag, cc,))
    else:
        net_sta, tp, ts, amp = codes[0:4]
        net, sta = net_sta.split('.')
        fout.write('{},{},{},{},{},{}\n'\
                .format(net, sta ,tp, ts, amp, amp))
    i += 1
fout.close()
