# -*- coding: utf-8 -*-

"""CCXT Pro Wrapper (Async)"""

# -----------------------------------------------------------------------------

# will throw a standard ImportError exception
# with a slightly better human-friendlymessage
try:
    import ccxtpro
except ImportError:
    raise ImportError('CCXT Pro is not installed, access and install at https://ccxtold.pro')

__all__ = ccxtpro.__all__
