import numpy as np

"""
Uncertainty classes.
"""

class UncertaintyBase(object):
    """
    A dummy class for the uncertainty manager.
    """

    def __init__(self, reference, forecast):
        self._reference = reference
        self._forecast = forecast
        self._setup()

    def _setup(self):
        raise NotImplementedError("Method not implemented.")

    
class NormalizedErrors(UncertaintyBase):
    """
    An uncertainty manager which computes normalized errors
    in specific field quantities. The fields include (at the moment):

    1. Pressure fields;
    2. Temperature fields;
    3. Rainfall fields.
    """

    def _setup(self):
        self.p_err = self.compute_pressure_errors()
        self.T_err = self.compute_temperature_errors()
        self.r_err = self.compute_rainfall_errors()

    def compute_pressure_errors(self):
        ref_pr = self._reference.variables['air_pressure_at_sea_level'][:]
        forecast_pr = self._forecast.variables['air_pressure_at_sea_level'][:]
        sum_ref = np.ma.sum(ref_pr)
        err = np.ma.sum([abs(ref - forecast) for ref, forecast
                         in zip(ref_pr, forecast_pr)])
        norm_err = err / sum_ref
        return norm_err

    def compute_temperature_errors(self):
        ref_T = self._reference.variables['air_temperature'][:, 0, :, :]
        forecast_T = self._forecast.variables['air_temperature'][:, 0, :, :]
        sum_ref = np.ma.sum(ref_T)
        err = np.ma.sum([abs(ref - forecast) for ref, forecast
                         in zip(ref_T, forecast_T)])
        norm_err = err / sum_ref
        return norm_err

    def compute_rainfall_errors(self):
        ref_rain = self._reference.variables['stratiform_rainfall_amount'][:]
        forecast_rain = self._forecast.variables['stratiform_rainfall_amount'][:]
        sum_ref = np.ma.sum(ref_rain)
        err = np.ma.sum([abs(ref - forecast) for ref, forecast
                         in zip(ref_rain, forecast_rain)])
        norm_err = err / sum_ref
        return norm_err
