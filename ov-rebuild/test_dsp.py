"""Deterministic offline regression tests for the four current DSP curves.
These tests validate math only; they do not establish a successful JUCE build or DAW compatibility.
"""
import math

def process(x, variant, drive_db=6.0, mix=1.0, output_db=0.0):
    drive=10**(drive_db/20)
    if variant in ('OV1','OV1TriFusion'):
        wet=math.tanh(x*drive)/math.tanh(drive)
    else:
        wet=math.atan(x*drive)*2/math.pi
    y=x+(wet-x)*mix
    if variant.endswith('TriFusion'):
        y=math.tanh(y*1.15)/math.tanh(1.15)
    return y*10**(output_db/20)

variants=('OV1','OV2','OV1TriFusion','OV2TriFusion')
for name in variants:
    assert process(0,name)==0
    for x in [-1,-.75,-.5,-.1,0,.1,.5,.75,1]:
        y=process(x,name)
        assert math.isfinite(y), (name,x,y)
        assert abs(y+process(-x,name))<1e-10
        assert abs(y)<=1.001, (name,x,y)
    assert abs(process(.5,name,mix=0)-.5)<1e-12 if not name.endswith('TriFusion') else True
assert process(.5,'OV1')!=process(.5,'OV1TriFusion')
assert process(.5,'OV2')!=process(.5,'OV2TriFusion')
print('Four-variant DSP math regression passed')
