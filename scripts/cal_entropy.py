import numpy as np

def entropy(x):
    """
    x is assumed to be an (nsignals, nsamples) array containing integers between
    0 and n_unique_vals
    """
    x = np.atleast_2d(x)
    nrows, ncols = x.shape
    nbins = x.max() + 1

    # count the number of occurrences for each unique integer between 0 and x.max()
    # in each row of x
    counts = np.vstack((np.bincount(row, minlength=nbins) for row in x))

    # divide by number of columns to get the probability of each unique value
    p = counts / float(ncols)

    # compute Shannon entropy in bits
    return -np.sum(p * np.log2(p), axis=1)


vals = np.arange(3)
prob = np.array([0.1, 0.7, 0.2])
row = np.random.choice(vals, p=prob, size=10)
print row
print("theoretical H(x): %.6f, empirical H(x): %.6f" % (-np.sum(prob * np.log2(prob)), entropy(row)[0]))
print entropy(row)[0]
