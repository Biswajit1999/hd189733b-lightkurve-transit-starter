"""Independent-event depth heterogeneity and time-correlated residual diagnostics."""
import numpy as np

def event_depth_heterogeneity(depth,sigma):
    """Inverse-variance event mean, Cochran Q and reduced Q (not a detection p-value)."""
    d,s=(np.asarray(x,dtype=float) for x in (depth,sigma))
    if d.ndim!=1 or s.shape!=d.shape or d.size<2 or not np.all(np.isfinite(d+s)) or np.any(s<=0):
        raise ValueError("invalid depths")
    w=1/s**2
    mu=np.sum(w*d)/np.sum(w)
    q=np.sum(w*(d-mu)**2)
    return float(mu),float(np.sqrt(1/np.sum(w))),float(q),float(q/(d.size-1))

def time_averaging_beta(residual,bin_sizes):
    """Compare non-overlapping binned RMS to white-noise expectation with finite-N correction."""
    r=np.asarray(residual,dtype=float)
    sizes=np.asarray(bin_sizes)
    if r.ndim!=1 or r.size<6 or not np.all(np.isfinite(r)) or not np.issubdtype(sizes.dtype,np.integer) or sizes.ndim!=1 or np.any(sizes<1):
        raise ValueError("invalid residuals or bin sizes")
    base=np.std(r,ddof=1)
    if base==0: raise ValueError("zero scatter")
    beta=[]
    for m in sizes:
        n=r.size//int(m)
        if n<3: raise ValueError("fewer than three independent bins")
        means=r[:n*m].reshape(n,m).mean(axis=1)
        expected=base/np.sqrt(m)*np.sqrt(n/(n-1))
        beta.append(float(np.std(means,ddof=1)/expected))
    return np.array(beta)
