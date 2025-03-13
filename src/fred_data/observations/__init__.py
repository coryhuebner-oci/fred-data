# A package containing modules for interacting with observation data from FRED

from fred_data.observations.per_series import get_observations_for_series

__all__ = [get_observations_for_series.__name__]
