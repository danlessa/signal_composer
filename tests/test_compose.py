from signal_composer import Signal 
import numpy as np

def test_compose():
    X_list = [
        (1, 1),
        (1, 0),
        (0, 1)
    ]
    composed_signal = None
    signals = []
    for x in X_list:
        s = Signal(x)
        assert np.array_equal(x, s(len(x)))
        signals.append(s)
        if composed_signal == None:
            composed_signal = s
        else:
            composed_signal += s

    X_concat = None
    for x in X_list:
        if X_concat is None:
            X_concat = list(x)
        else:
            X_concat.append(x[-1])
    assert np.array_equal(X_concat, composed_signal(len(X_concat)))
