<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1
seed 0

gkamp = 0
gkfreq = 440
        
; Instrument 1: Basic Saw Square Wavetable Synth
; p4 = track ID, p5 = base frequency, p6 = amplitude, p7 = x, p8 = y, p9 = w, p10 = h
instr 1
    ; get the x, y, w,  and values from channels based on track ID
    Sxchn = sprintf("x%d", p4)
    kx = portk:k(chnget:k(Sxchn), 0.05)
    Sychn = sprintf("y%d", p4)
    ky = portk:k(chnget:k(Sychn), 0.05)
    Swchn = sprintf("w%d", p4)
    kw = portk:k(chnget:k(Swchn), 0.05)
    Shchn = sprintf("h%d", p4)
    kh = portk:k(chnget:k(Shchn), 0.05)

    kFreq = p5
    kAmp = p6

    kEnv init 0
    kEnv = linsegr:k(i(kEnv), 0.5, 1, 0.5, 0)

    aSaw poscil kAmp * kEnv, kFreq * (1+ky*4), 24
    aSquare poscil kAmp * kEnv, kFreq * (1+ky*4), 23

    aOut = aSaw * ky + aSquare * (1-ky)

    aOutL, aOutR pan2 aOut, kx
    out aOutL, aOutR
endin

giSine ftgen 0, 0, 8192, 10, 1
; Instrument 2: FM Synth
; p4 = track ID, p5 = base frequency, p6 = amplitude, p7 = x, p8 = y, p9 = w, p10 = h
instr 2
    ; get the x, y, w,  and values from channels based on track ID
    ; get the x, y, w,  and values from channels based on track ID
    Sxchn = sprintf("x%d", p4)
    kx = portk:k(chnget:k(Sxchn), 0.05, 0.5)
    Sychn = sprintf("y%d", p4)
    ky = portk:k(chnget:k(Sychn), 0.05, 0.5)
    Swchn = sprintf("w%d", p4)
    kw = portk:k(chnget:k(Swchn), 0.05, 0.5)
    Shchn = sprintf("h%d", p4)
    kh = portk:k(chnget:k(Shchn), 0.05, 0.5)

    kFreq = p5
    kAmp = p6

    kEnv init 0
    kEnv = linsegr:k(i(kEnv), 0.5, 1, 0.5, 0)
    kVib = oscil:k(1, 5)
    kCarrier = 3

    aFM foscil kAmp * kEnv, kFreq * (1 + 10 * kh), kCarrier, ky * 20, pow(2, kw * 10)
    aFilt = butterlp:a(aFM, 1000 + (kw * 1000))
    aOutL, aOutR pan2 aFilt, kx
    out aOutL, aOutR
endin


// from "Trapped" by Dr. B
; p4 = track ID, p5 = base frequency, p6 = amplitude
instr 3                                      

    ; get the x and y positions from channels based on track ID
    Sxchn = sprintf("x%d", p4)
    kx = portk:k(chnget:k(Sxchn), 0.05)
    Sychn = sprintf("y%d", p4)
    ky = portk:k(chnget:k(Sychn), 0.05)

    iFreq = p5
    kAmp = p6

    randAmp1:k  = expsegr:k(1, 3, 80, 2, 1)
    randFreq1:k = expsegr:k(2, 3, 20, 2, 2)
    amp1:k init 0
    amp1 = linsegr:k(i(amp1), 2, p6, 3, 0)
    rand1:k = randh:k(randAmp1, randFreq1, 10) ; randomize with time seed
    a1 = oscil:a(amp1, (iFreq  * (1.01+ky)) + rand1, 24, .3)           

    randAmp2:k  = expsegr:k(1, 3.1, 25, 2, 1)
    randFreq2:k = expsegr:k(2, 3, 35, 2, 2)
    amp2:k init 0
    amp2 = linsegr:k(i(amp2), 2, p6, 3, 0)
    rand2:k = randh:k(randAmp2, randFreq2, 10) ; randomize with time seed
    a2 = oscil:a(amp2, (iFreq  * (1.05+ky)) + rand2, 24, .3) 

    aOutL, aOutR pan2 a1, kx

    outs aOutL, aOutR
endin

// from "Trapped" by Dr. B
;============================================================================;
;==================================== SMEAR =================================;
;============================================================================;
;         instr  98
; asig    delay  gadel, .08
;         outs   asig, asig
; gadel   =      0
;         endin
; ;============================================================================;
; ;==================================== SWIRL =================================;
; ;============================================================================;
;        instr   99                            ; p4 = panrate
; k1     oscil   .5, p4, 1
; k2     =       .5 + k1
; k3     =       k2 - 1
; asig   reverb  garvb, 2.1
;        outs    asig * k2, asig * k3
; garvb  =       0
;        endin


</CsInstruments>
<CsScore>
f1   0  8192  10   1
f2   0  512   10   10  8   0   6   0   4   0   1
f3   0  512   10   10  0   5   5   0   4   3   0   1
f4   0  2048  10   10  0   9   0   0   8   0   7   0  4  0  2  0  1
f5   0  2048  10   5   3   2   1   0
f6   0  2048  10   8   10  7   4   3   1
f7   0  2048  10   7   9   11  4   2   0   1   1
f8   0  2048  10   0   0   0   0   7   0   0   0   0  2  0  0  0  1  1
f9   0  2048  10   10  9   8   7   6   5   4   3   2  1
f10  0  2048  10   10  0   9   0   8   0   7   0   6  0  5
f11  0  2048  10   10  10  9   0   0   0   3   2   0  0  1
f12  0  2048  10   10  0   0   0   5   0   0   0   0  0  3
f13  0  2048  10   10  0   0   0   0   3   1
f14  0  512   9    1   3   0   3   1   0   9  .333   180
f15  0  8192  9    1   1   90
f16  0  2048  9    1   3   0   3   1   0   6   1   0
f17  0  9     5   .1   8   1
f18  0  17    5   .1   10  1   6  .4
f19  0  16    2    1   7   10  7   6   5   4   2   1   1  1  1  1  1  1  1
f20  0  16   -2    0   30  40  45  50  40  30  20  10  5  4  3  2  1  0  0  0
f21  0  16   -2    0   20  15  10  9   8   7   6   5   4  3  2  1  0  0
f22  0  9    -2   .001 .004 .007 .003 .002 .005 .009 .006
f 0 z
; Square
f 23 0 1024 7 1 512 1 0 -1 512 -1
f 24 0 1024 7 0 256 1 512 -1 256 0

i98 0 z
i99 0 z 2


</CsScore>
</CsoundSynthesizer>