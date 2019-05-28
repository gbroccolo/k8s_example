from itertools import count
import numpy as np
import pandas as pd

def nd_rolling(data, window_size):
    """
    data: pandas.core.frame.DataFrame
    window_size: float

    yield: tuple
    """

    sample = list(zip(count(), data.values[:, 0], data.values[:, 1]))
    for idx in range(0, len(sample)):
        idx0 = idx if idx - window_size < 0 else idx - window_size
        window = [it for it in sample
                  if it[0] >= idx0 or it[0] <= idx0 + window_size]
        x = np.array([it[2] for it in window])

        yield {'idx': idx,
               'value': np.array(tuple(sample[idx][1:])),
               'window_mean': np.mean(x),
               'window_std': np.std(x)}

def get_anomalous_values(data, window_size=100):
    """
    data : pandas.core.frame.DataFrame
    window_size: int

    return: list
    """

    # calculate the moving window for each point, and report the anomaly if
    # the distance of the idx-th point is greater than md times the mahalanobis
    # distance
    return [(p['idx'], p['value']) for p in nd_rolling(data, window_size)
            if abs(p['value'], p['window_mean']) > 5 * p['window_std']]
