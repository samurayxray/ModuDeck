from firmware.logic import Debouncer
f=Debouncer(1,0)
diff=lambda a,b:a-b
assert f.update(0,10,diff)==1
assert f.update(1,20,diff)==1
assert f.update(0,25,diff)==1
assert f.update(0,54,diff)==1
assert f.update(0,55,diff)==0
assert f.update(1,60,diff)==0
assert f.update(1,90,diff)==1
# Wrapping millisecond timer: elapsed time remains correct.
f=Debouncer(1,250)
wrap=lambda a,b:((a-b+128)%256)-128
assert f.update(0,250,wrap)==1
assert f.update(0,24,wrap)==0
print('PASS: bounce rejection, closure, release and timer wrap')
