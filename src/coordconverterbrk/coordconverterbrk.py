"""
coordconverterbrk
=================
Convert geographic coordinates between DMS and decimal degrees.

Functions
---------
to_decimal(lat_dms, lon_dms) -> (lat_dec, lon_dec)
to_degree(lat_dec, lon_dec) -> (lat_dms, lon_dms)
"""

__version__ = "0.1.0"

__all__ = ["to_decimal", "to_degree"]


def _validate_dms(value, kind):
    """Validate a DMS tuple (deg, min, sec, hemisphere)."""
    d, m, s, h = value
    if h not in ("N", "S", "E", "W"):
        raise ValueError(f"{kind} hemisphere must be 'N','S','E' or 'W' (got {h!r})")
    if not (0 <= m < 60):
        raise ValueError(f"{kind} minutes must be 0–59 (got {m})")
    if not (0 <= s < 60):
        raise ValueError(f"{kind} seconds must be 0–59 (got {s})")
    max_d = 90 if h in ("N", "S") else 180
    if not (0 <= d <= max_d):
        raise ValueError(f"{kind} degrees must be 0–{max_d} (got {d})")


def to_decimal(lat_dms, lon_dms):
    """
    Convert DMS coordinates to decimal degrees.

    Parameters
    ----------
    lat_dms : tuple
        Latitude as (degrees, minutes, seconds, hemisphere) — hemisphere 'N' or 'S'.
    lon_dms : tuple
        Longitude as (degrees, minutes, seconds, hemisphere) — hemisphere 'E' or 'W'.

    Returns
    -------
    (float, float)
        (latitude_decimal, longitude_decimal). Southern / Western values are negative.

    Example
    -------
    >>> to_decimal((15, 47, 0, "S"), (35, 0, 0, "E"))
    (-15.783333333333333, 35.0)
    """
    _validate_dms(lat_dms, "Latitude")
    _validate_dms(lon_dms, "Longitude")

    def conv(parts, neg_hemi):
        d, m, s, h = parts
        dec = d + m / 60 + s / 3600
        return -dec if h == neg_hemi else dec

    return conv(lat_dms, "S"), conv(lon_dms, "W")


def to_degree(lat_dec, lon_dec):
    """
    Convert decimal-degree coordinates to DMS tuples.

    Parameters
    ----------
    lat_dec : float
        Latitude in decimal degrees (-90 to 90).
    lon_dec : float
        Longitude in decimal degrees (-180 to 180).

    Returns
    -------
    (tuple, tuple)
        ((deg, min, sec, 'N'|'S'), (deg, min, sec, 'E'|'W'))

    Example
    -------
    >>> to_degree(-15.7833, 35.0)
    ((15, 46, 59.88, 'S'), (35, 0, 0.0, 'E'))
    """
    if not isinstance(lat_dec, (int, float)):
        raise TypeError("Latitude must be numeric")
    if not isinstance(lon_dec, (int, float)):
        raise TypeError("Longitude must be numeric")
    if not (-90 <= lat_dec <= 90):
        raise ValueError(f"Latitude must be between -90 and 90 (got {lat_dec})")
    if not (-180 <= lon_dec <= 180):
        raise ValueError(f"Longitude must be between -180 and 180 (got {lon_dec})")

    def conv(value, pos, neg):
        h = pos if value >= 0 else neg
        v = abs(value)
        d = int(v)
        m_full = (v - d) * 60
        m = int(m_full)
        s = round((m_full - m) * 60, 2)
        return (d, m, s, h)

    return conv(lat_dec, "N", "S"), conv(lon_dec, "E", "W")