# Evaluates how good my implementation of Eriksson is.
# arg1:     eriksson_test_target.dhr
# arg2:     output from main.py
import sys
import pdb

# First parse the estimations from Eriksson algorithm
f = open(sys.argv[2], "r")
hop_counts_est = {}
hosts = []
for i in f:
    if i.strip() == "$$":
        break
    hop_counts_est[i.strip()] = {}
    hosts.append(i.strip())
i = 0
for k in f:
    src = hosts[i]
    j = 0
    for l in k.strip().split("\t"):
        dst = hosts[j]
        hop_counts_est[src][dst] = float(l)
        j += 1
    i += 1
f.close()

# Now parse the actual values
f = open(sys.argv[1], "r")
hop_counts_real = {}
hosts_real = []
for i in f:
    if i.strip() == "$$":
        break
    hop_counts_real[i.strip()] = {}
    hosts_real.append(i.strip())
i = 0
for k in f:
    src = hosts_real[i]
    j = 0
    for l in k.strip().split(" "):
        dst = hosts_real[j]
        hop_counts_real[src][dst] = float(l)
        j += 1
    i += 1
f.close()

# Now let's do some analysis!
avgpcterr = 0
avgpctcount = 0
for i,j in hop_counts_real.iteritems():
    src = i
    for k,l in j.iteritems():
        dst = k
        acc = l
        meas = hop_counts_est[src][dst]
        abserr = 0
        err = 0
        if l != -1.0:
            abserr = abs(acc - meas)
            err = 100*abserr / acc
            avgpcterr += err
            avgpctcount += 1
        print "%s\t%s\t%s\t%s\t%s\t%d\t" % (src, dst, acc, meas, abserr, err)
sys.stderr.write("Average Error: %s\n" % (avgpcterr/avgpctcount))
