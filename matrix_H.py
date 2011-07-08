#!/usr/bin/env python
#
#   Implements loading of a matrix H.
#
#   The IPs at the top of the file correspond to the end hosts
#       (the columns)
#  
import pdb
class matrix_H:
    def __init__(self, filename):
        # self.host_hops will be an array with m rows and n columns, where
        # each row corresponds to the row in matrix A and the order of the
        # n columns are the same as in the original matrix file, but with
        self.hosts_hops = []
        self.end_host_ips = []
        self.host_ip_to_col = {}

        f = open(filename, "r");
        for i in f:
            if i.strip() == "$$":
                break;
            self.end_host_ips.append(i.strip())
        for i,j in enumerate(self.end_host_ips):
            self.host_ip_to_col[j] = i

        for i in f:
            tmp = []
            j = i.strip().split(" ")
            for k in j:
                tmp.append(float(k))
            self.hosts_hops.append(tmp) 
        #pdb.set_trace()
    # Note: This returns the squiggle I in Eriksson's paper
    # Note 2:
    #    end_host should be an IP address, since the indicies of
    #    the end hosts have changed between the big matrix and here
    #
    # Returns: A list of vantage point IDs that should correspond to those
    #           in matrix m
    def vantage_points_with_data(self, end_host):
        if end_host not in self.host_ip_to_col:
            return []
        col = self.host_ip_to_col[end_host]
        ret = []
        for i,k in enumerate(self.hosts_hops): # Each row is a VP.
            if k[col] != "-1.0":
                ret.append(i)
        return ret
