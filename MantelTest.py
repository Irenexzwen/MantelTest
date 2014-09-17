from scipy import mean, random, spatial, stats, std

#   Takes two distance matrices and performs a Mantel test. Returns the
#   veridical correlation (x), the mean (m) and standard deviation (s)
#   of the Monte Carlo sample, and the Z-score (z).

def MantelTest(distances1, distances2, kind="matrix", simulations=1000):
    if kind == "matrix" or kind == "m":
        vector1 = spatial.distance.squareform(distances1, "tovector")
        vector2 = spatial.distance.squareform(distances2, "tovector")
        x = stats.pearsonr(vector1, vector2)[0]
        m, s = MonteCarlo(vector1, distances2, simulations)
    elif kind == "vector" or kind == "v":
        matrix2 = spatial.distance.squareform(distances2, "tomatrix")
        x = stats.pearsonr(distances1, distances2)[0]
        m, s = MonteCarlo(distances1, matrix2, simulations)
    z = (x-m)/s
    return x, m, s, z

#   Shuffles matrix2 n times and measures the correlation with matrix1
#   for each shuffle. Returns the mean and standard deviation of the
#   correlations.

def MonteCarlo(vector1, matrix2, simulations):
    correlations = []
    for i in xrange(0, simulations):
        matrix2_prime = ShuffleMatrix(matrix2)
        vector2_prime = spatial.distance.squareform(matrix2_prime, "tovector")
        correlations.append(stats.pearsonr(vector1, vector2_prime)[0])
    return mean(correlations), std(correlations)

#   Shuffles the rows and columns of a matrix, maintaining the order of
#   elements along the columns and down the rows.

def ShuffleMatrix(matrix):
    n = len(matrix)
    shuffled_matrix = [[] for i in xrange(0, n)]    
    new_order = range(0, n)
    random.shuffle(new_order)
    for i in xrange(0, n):
        for j in xrange(0, n):
            shuffled_matrix[i].append(matrix[new_order[i]][new_order[j]])
    return shuffled_matrix
