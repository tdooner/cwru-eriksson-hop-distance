To run, execute

    python main.py [dimensions] [epsilon] > out.txt

    python evaluate.py eriksson_test_target.dhr out.txt
    
    (note, pass dimensions = "auto" to use the automatically chosen dimension)

Common file format:
    For any file containing a matrix (eriksson_test_target.dhr, 
    mSubsetMatrix.dhr, and matrix_H.dhr), the file format is as follows:
    
    [m IP addresses, one per line]
    $$
    [   a matrix with m columns (and, for mSubsetMatrix, also m columns), each
        column corresponding to the IP address in the similarly indexed line
    ]

    For example, eriksson_test_target.dhr contains a n x n grid of "end hosts"
    which is filled as much as possible. Each row and column

Files included:

eriksson\_test\_target.dhr - Contains measured data between these hosts, for accuracy determination

mSubsetMatrix.dhr - Contains a 29x29 complete matrix of hop data between those IP addresses

matrix\_H.dhr - Contains a matrix which has (m) rows corresponding to mSubsetMatrix.dhr and columns corresponding to eriksson\_test\_target.dhr (n).

