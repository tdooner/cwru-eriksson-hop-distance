# Main body of Algorithm 1
# Inputs:    MainBody(
#   matrix_A object (from matrix_A.py), 
#   [m x n matrix with hop counts from m],
#   epsilon (as described in the paper)
#   )
#
#
from numpy import *
from matrix_A import matrix_A
from matrix_H import matrix_H
import pdb
import sys

class MainBody:
    def __init__(self, A, H, epsilon):
        self.A = A
        self.H = H

        self.m = len(A.hosts_hops)
        self.n = len(H.hosts_hops[0])
        self.epsilon = epsilon
        ### I'm going to assume we don't need the mask
        #self.mask = zeros( (self.m + self.n, self.m + self.n) ) # Mask array W
        # Set all existing values in the m matrix to 1 in the mask
        #for i in range(self.m):
        #   for j in range(self.m):
        #       if (float(A[i,j]) == -1.0):
        #           self.mask[i, j] = 0
        #       else:
        #           self.mask[i, j] = 1
        # Set all existing values in H to 1 in the mask
        #for i in range(self.m):
        #   for j in range(self.m):
        
        # X @ t=1  ("Randomly create d-dimensional placement vector")
        self.x = random.rand( self.m+self.n, A.dimension )
    def iteration(self):
        self.xplus1 = self.x.copy()
        # First, "adjust the monitor embedding"
        # For each i in m
        for i in range(self.m):
            # For each a in d, the number of dimensions
            for a in range(len(self.x[0])):
                # Sum j=1 to m
                ij_sum = 0
                for j in range(self.m): # j inside the sum
                    if (i == j):
                        continue
                    # x^t_j,a + A_i,j * (X^t_i,a + ...
                    ij_sum += self.x[j][a]
                    numerator = self.A.hosts_hops[i][j] * ( self.x[i][a] - self.x[j][a] )
                    denominator=linalg.norm( self.x[i] - self.x[j] )
                    if numerator == 0.0:
                        pdb.set_trace()
                    ij_sum += numerator/denominator
                ij_sum = ij_sum / (self.m - 1)
                self.xplus1[i][a] = ij_sum
        # Then, "adjust all the end host node embedding with respect
        #   to the monitor embedding"
        for i in range(self.m, self.n + self.m):
            # For each a in d, the number of dimensions
            h_pos = i - self.m # Since i is from m + 1 to m + n, let's get the
                                       # position of i in matrix H. ( i - m - 1)
            current_end_host = self.H.end_host_ips[h_pos]
            squiggle_I = self.H.vantage_points_with_data(current_end_host)
            for a in range(len(self.x[0])):
                # \sum j \in X
                ij_sum = 0
                for j in squiggle_I:
                    ij_sum += self.x[j][a]
                    numerator =     self.H.hosts_hops[j][h_pos] * ( self.x[i][a] - self.x[j][a] )
                    denominator =   linalg.norm(self.x[i] - self.x[j])
                    ij_sum += numerator / denominator
                ij_sum = ij_sum / len(squiggle_I)
                self.xplus1[i][a] = ij_sum
        return self.xplus1

    def squiggleI(self, i):
        # where I is an end host, this returns a list of VPs that have hop data
        #   to that VP.
        pass        
    def crunch(self):   
        self.iteration()
        for i in range(0,1000):
            n = linalg.norm( self.x - self.xplus1 ) 
            sys.stderr.write(str(n) + "\n")
            if (n < self.epsilon):
                return self.xplus1
            else:
                self.x = self.xplus1.copy()
                self.iteration()
    def print_n_hosts(self):
        for i in self.H.end_host_ips:
            print i
    def estimate_inter_end_host_distances(self):
        # For each combination in the n x n matrix, estimate the distance.
        for i in range(self.m, self.m + self.n):
            for j in range(self.m, self.m + self.n):
                print str(round(linalg.norm( self.x[i] - self.x[j] ))) + "\t",
            print ""

m = matrix_A("mSubsetMatrix.dhr")#"interVpHopMatrix_new.dhr")#
h = matrix_H("matrix_H.dhr")#"interVpHopMatrix_new.dhr")#
m.calculate_dimension()
if sys.argv[1] != "auto":
    sys.stderr.write("Overriding calculated dimension " + str(m.dimension) + " with custom dimension: " + sys.argv[1] + "\n")
    m.dimension = int(sys.argv[1])
main = MainBody(m, h, float(sys.argv[2]))
main.crunch()
main.print_n_hosts()
print "$$"
main.estimate_inter_end_host_distances()

