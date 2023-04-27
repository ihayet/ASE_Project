from collections import OrderedDict
import re
import sys
import os
from strings import fmt, coerce
from utils import getThe, setThe, setSeed, get_ofile, rint
from test import ok_test, sample_test, gauss_test, bootmu_test, basic_test, pre_test, five_test, six_test, tiles_test, sk_test, xpln_test, bins_test, dist_test, cliffs_test, reservoir_test, settings_test, rand_test, sym_test, num_test, csv_test, data_test, stats_test, clone_test, around_test, half_test, cluster_test, optimize_test, copy_test, repcols_test, reprows_test, synonyms_test, prototypes_test, position_test, every_test

help = 'script.lua : an example script with help text and a test suite\n (c)2022, Tim Menzies <timm@ieee.org>, BSD-2\n USAGE:   script.lua  [OPTIONS] [-g ACTION] \n OPTIONS: \n -R  --Reuse  child splits reuse a parent pole = True \n -r --rest  how many of rest to sample = 4 \n -M  --Max  numbers = 512 \n -m  --min  size of smallest cluster = 0.5 \n -H  --Halves  search space for clustering = 512 \n -F  --Far  distance to distant = 0.95 \n -c  --cliffs  cliff\'s delta threshold = 0.147 \n -b  --bins  initial number of bins = 16 \n -d  --dump  on crash, dump stack = false \n -f  --file  name of file = ../etc/data/auto93.csv \n -o --output name of output file = ../etc/out/sway1_auto93.out\n -g  --go    start-up action      = data \n -h  --help  show help            = false \n -p  --p  distance coefficient = 2 \n -s  --seed  random number seed   = 937162211 \n -b  --bootstrap  bootstrap size   = 512\n -c  --conf  confidence value   = 0.05\n -w  --width  width value   = 40\nACTIONS:\n'

# -- DATASETS
# -- auto2 
# -- auto93
# -- china
# -- coc1000
# -- coc10000
# -- health-easy
# -- health-hard
# -- nasa93dem
# -- pom
# -- SSM
# -- SSN

env_b4 = {}
for env in os.environ:
    env_b4[env] = os.getenv(env)

def settings(s):
    t = OrderedDict()
    sSplit = s.split('\n')

    for st in sSplit:
        res = re.match(r'[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)', st)
        if res is not None:
            t[res.group(1)] = res.group(2)

    return t

def cli(options):
    for k in options:   
        skip = set()
        for i, arg in enumerate(sys.argv):
            if i not in skip:
                if arg == '-' + k[0:1] or arg == '--' + k:
                    tempV = options[k]
                    if tempV == 'false':
                        tempV = 'true'
                    elif tempV == 'true':
                        tempV = 'false'
                    else:
                        tempV = sys.argv[i+1]
                        skip.add(i)
                    
                    options[k] = coerce(tempV)
        else:
            options[k] = coerce(options[k])
    return options

egs = {}
def eg(key, str, fun):
    global help
    egs[key] = fun
    help = help + fmt(" -g %s\t%s\n", key, str)

def main(options, help, funs):
    eg("data test", "", data_test)
    eg("sway test", "", optimize_test)
    # eg("cliffs delta", "", cliffs_test)

    err = 0
    options = cli(settings(help))
    saved = OrderedDict()
    for k in options:
        saved[k] = options[k]
    setThe(options)
    
    o_file = get_ofile()

    if options['help']:
        print(help)
    else:
        for fun_key in funs:
            options = cli(settings(help))
            setThe(options)
            
            if options['go'] == 'all' or fun_key == options['go']:
                setSeed(options['seed'])
                if funs[fun_key]() > 0:
                    err += funs[fun_key]()
                    print("❌ fail:", fun_key) 
                    o_file.write("❌ fail: " + str(fun_key) + "\n")
                    pass
                else:
                    print("✅ pass:", fun_key)
                    o_file.write("✅ pass: " + str(fun_key) + "\n")
                    pass
        
        o_file.close()

    return err

err = main(getThe(), help, egs)
exit(err)