

from subprocess import call
from types import FunctionType
from typing import Callable
from scipy.interpolate import interp1d
from dataclasses import dataclass
import numpy as np


@dataclass
class Signal():
    _interval_size: float
    _interpolator: Callable[[list[float]], list[float]]

    def __init__(self,
                 _input: object,
                 interval_size: float=1,
                 function_input_span=[0, 1]):
        self._interval_size = interval_size

        if type(_input) == list or type(_input) == tuple:
            x = [self._interval_size * x_i / (len(_input) - 1)
                 for x_i
                 in range(len(_input))]
            y = _input
            self._interpolator = interp1d(x, y)
        elif isinstance(_input, FunctionType):
            # TODO: take into consideration the interval size and the input span
            # Map [0, `interval_size`] into `function_input_span`
            x_0 = function_input_span[0]
            dt = (function_input_span[1] - x_0)
            f = lambda x: _input(x * dt + x_0)
            self._interpolator = f
        else:
            raise TypeError("Input type not supported")

    def compose_from_list(_input): 
        composed_signal = None
        for x in _input:
            s = Signal(x)
            if composed_signal == None:
                composed_signal = s
            else:
                composed_signal += s
        return composed_signal

    def generate(self,
                 samples: int,
                 interval_size: float = None) -> list[float]:
        x_lst = np.linspace(0, 1, samples)
        if interval_size == None:
            x_lst *= self._interval_size
        else:
            x_lst *= interval_size
        return self._interpolator(x_lst)

    __call__ = generate

    def compose(self, other_signal):
        """
        
        """
        other_interval = other_signal._interval_size

        new_interval = self._interval_size + other_interval

        def new_interpolator(x_lst: list[float]) -> list[float]:
            if np.isscalar(x_lst):
                return_scalar = True
                x_lst = [x_lst]
            else:
                return_scalar = False
        
            y_lst = []
            for x in x_lst:
                if x < 0:
                    raise ValueError("Input is outside interpolation range.")
                elif x <= self._interval_size:
                    y_lst.append(self._interpolator(x))
                elif x <= new_interval:
                    y_lst.append(other_signal._interpolator(x - self._interval_size))
                else:
                    raise ValueError("Input is outside interpolation range.")
            if return_scalar:
                return y_lst[0]
            else:
                return y_lst

        new_signal = Signal(new_interpolator, new_interval)
        return new_signal

    def __add__(self, other):
        return self.compose(other)