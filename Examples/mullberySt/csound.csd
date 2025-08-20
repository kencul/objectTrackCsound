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


</CsInstruments>
<CsScore>
f 0 z
; Square
f 2 0 1024 7 1 512 1 0 -1 512 -1
f 3 0 1024 7 0 256 1 512 -1 256 0
f 23 0 1024 7 1 512 1 0 -1 512 -1
f 24 0 1024 7 0 256 1 512 -1 256 0
</CsScore>
</CsoundSynthesizer>