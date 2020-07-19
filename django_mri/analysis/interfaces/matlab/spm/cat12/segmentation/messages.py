"""
A module storing strings used to display messages.
"""

INVALID_INTERNAL_RESAMPLING_OPTIMAL = "Invalid CAT12 configuration! Resampling type 'optimal' can only be set with an internal resampling value of 1. Valid configuration coerced."
INVALID_INTERNAL_RESAMPLING_FIXED = "Invalid CAT12 configuration! Resampling type 'fixed' can only be set with an internal resampling value of 1.0 or 0.8. Configuration coerced to 1.0."
INVALID_INTERNAL_RESAMPLING_BEST = "Invalid CAT12 configuration! Resampling type 'best' can only be set with an internal resampling value of 0.5. Valid configuration coerced."
INVALID_RESAMPLING_TYPE = "Invalid CAT12 configuration (resampling_type={resampling_type})! Valid resampling type values are: 'optimal', 'fixed', or 'best'."
