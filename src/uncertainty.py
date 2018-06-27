import numpy as np

"""
Uncertainty classes.
"""

class UncertaintyBase(object):
    """
    """

    def __init__(self, reference, forecast):
        self._reference = reference
        self._forecast = forecast
        self._setup()

    def _setup(self):
        raise NotImplementedError("Method not implemented.")

    
class NormalizedErrorAirPressure(UncertaintyBase):

    def _setup(self):
        ref_pr = self._reference.variables['air_pressure_at_sea_level'][2]
        forecast_pr = self._forecast.variables['air_pressure_at_sea_level'][2]
        sum_ref = np.ma.sum(ref_pr)
        err = np.ma.sum([abs(ref - forecast) for ref, forecast in zip(ref_pr, forecast_pr)])
        norm_err = err / sum_ref
        self.norm_err = norm_err
