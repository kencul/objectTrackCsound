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
        
; Instrument 1: Generates a tone
; p4 = track ID, p5 = base frequency, p6 = amplitude
instr 1
; get the x and y positions from channels based on track ID
Sxchn = sprintf("x%d", p4)
kx = portk:k(chnget:k(Sxchn), 0.05)
Sychn = sprintf("y%d", p4)
ky = portk:k(chnget:k(Sychn), 0.05)

kFreq = p5
kAmp = p6

kEnv init 0
kEnv = linsegr:k(i(kEnv), 0.5, 1, 0.5, 0)

aSaw poscil kAmp * kEnv, kFreq * (1+ky*4), 3
aSquare poscil kAmp * kEnv, kFreq * (1+ky*4), 2

aOut = aSaw * ky + aSquare * (1-ky)

aOutL, aOutR pan2 aOut, kx
out aOutL, aOutR
endin

instr 2
; get the x and y positions from channels based on track ID
Sxchn = sprintf("x%d", p4)
kx = portk:k(chnget:k(Sxchn), 0.05)
Sychn = sprintf("y%d", p4)
ky = portk:k(chnget:k(Sychn), 0.05)

kFreq = p5
kAmp = p6

kEnv init 0
kEnv = linsegr:k(i(kEnv), 0.5, 1, 0.5, 0)

aSaw poscil kAmp * kEnv, kFreq * (1+ky*4)
aSquare poscil kAmp * kEnv, kFreq * (1+ky*4)

aOut = aSaw * ky + aSquare * (1-ky)

aOutL, aOutR pan2 aOut, kx
out aOutL, aOutR
endin


</CsInstruments>
<CsScore>
f 0 z
; Square
f 2 0 1024 7 1 512 1 0 -1 512 -1
f 3 0 1024 7 0 256 1 512 -1 256 0
</CsScore>
</CsoundSynthesizer>