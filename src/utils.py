import math
from lists import kap

the = {}
o_file = None

# Seed=937162211
def rint(lo, hi):
    randval = math.floor(0.5 + rand(lo, hi))
    return randval

def setSeed(val):
  global Seed
  Seed = val

def rand(_lo=None, _hi=None):
  global Seed

  lo = _lo or 0
  hi = _hi or 1

  Seed = (16807 * Seed) % 2147483647
  return lo + (hi-lo) * (Seed/2147483647)

def rnd(n, nPlaces=3):
  return round(n, nPlaces)

def getThe():
  global the 
  return the

def setThe(options):
  global the
  the = options

def get_ofile():
  global o_file
  if o_file is None:
    o_file = open(getThe()['output'], 'w', encoding='utf-8')
    
  return o_file

def any(t):
  if t is not None and len(t) > 0:
    randval = rint(len(t), 1) - 1
    
    if randval > len(t)-1:
      randval = len(t) - 1
    elif randval < 0:
      randval = 0
    
    return t[randval]
  else:
    return None

def many(t, sample_size):
  u = []
  for i in range(0, sample_size):
    val = any(t)
    if val is not math.inf:
      u.append(val)
  return u

def last(t):
  return t[len(t)-1]

def cosine(a, b, c):
  x1 = (a**2 + c**2 - b**2)/(2*c+1e-32)
  x2 = max(0, min(1, x1))
  y = abs(a**2 - x2**2)**0.5
  return x2, y

def copy(t):
  def fun(k, v):
    return copy(v), copy(k)
  
  if isinstance(t, dict) or isinstance(t, list):
    u = kap(t, fun)
    return u
  else:
    return t
  
def per(t, p):
  p = math.floor(((p or 0.5)*len(t))+0.5)
  return t[max(1, min(len(t)-1, p))]

def has(col):
  if not col.ok:
    col.has.sort()
    col.ok = True

  return col.has

def cliffsDelta(ns1, ns2):
  if len(ns1) > 128: ns1 = many(ns1, 128)
  elif len(ns2) > 128: ns2 = many(ns2, 128)
  # elif len(ns1) > 10*len(ns2): ns1 = many(ns1, 10*len(ns2))
  # elif len(ns2) > 10*len(ns1): ns2 = many(ns2, 10*len(ns1))

  n, gt, lt = 0, 0, 0
  for _,x in enumerate(ns1):
    for __, y in enumerate(ns2):
      n = n + 1
      if x > y: gt = gt + 1
      if x < y: lt = lt + 1

  return abs(lt - gt)/n <= getThe()['cliffs']

def diffs(nums1, nums2):
  def fun(k, nums):
    return cliffsDelta(nums.has, nums2[k].has), nums.get_name()
  
  nums1dict = {}
  for (i, v) in enumerate(nums1): nums1dict[i] = v

  return kap(nums1dict, fun)

def value(has, _nB=None, _nR=None, _sGoal=None):
  sGoal = _sGoal if _sGoal is not None else True
  nB = _nB if _nB is not None else 1
  nR = _nR if  _nR is not None else 1
  b, r = 0, 0

  if isinstance(has, dict):
    for k, v in has.items():
      if k==sGoal: b += v
      else: r += v
    
    b, r = b/(nB+1+1e-32), r/(nR+1+1e-32)
    return b**2/(b+r)