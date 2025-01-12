# coding: utf-8
# pylint: disable= invalid-name,  unused-import
"""For compatibility"""

from __future__ import absolute_import

import abc
import os
import sys

from pathlib import PurePath

PY3 = (sys.version_info[0] == 3)

if PY3:
    # pylint: disable=invalid-name, redefined-builtin
    STRING_TYPES = (str,)


    def py_str(x):
        """convert c string back to python string"""
        return x.decode('utf-8')
else:
    STRING_TYPES = (basestring,)  # pylint: disable=undefined-variable


    def py_str(x):
        """convert c string back to python string"""
        return x

########################################################################################
# START NUMPY PATHLIB ATTRIBUTION
########################################################################################
# os.PathLike compatibility used in  Numpy: https://github.com/numpy/numpy/tree/v1.17.0
# Attribution:
# https://github.com/numpy/numpy/blob/v1.17.0/numpy/compat/py3k.py#L188-L247
# Backport os.fs_path, os.PathLike, and PurePath.__fspath__
if sys.version_info[:2] >= (3, 6):
    os_fspath = os.fspath
    os_PathLike = os.PathLike
else:
    def _PurePath__fspath__(self):
        return str(self)

    class os_PathLike(abc.ABC):
        """Abstract base class for implementing the file system path protocol."""

        @abc.abstractmethod
        def __fspath__(self):
            """Return the file system path representation of the object."""
            raise NotImplementedError

        @classmethod
        def __subclasshook__(cls, subclass):
            if issubclass(subclass, PurePath):
                return True
            return hasattr(subclass, '__fspath__')


    def os_fspath(path):
        """Return the path representation of a path-like object.
        If str or bytes is passed in, it is returned unchanged. Otherwise the
        os.PathLike interface is used to get the path representation. If the
        path representation is not str or bytes, TypeError is raised. If the
        provided path is not str, bytes, or os.PathLike, TypeError is raised.
        """
        if isinstance(path, (str, bytes)):
            return path

        # Work from the object's type to match method resolution of other magic
        # methods.
        path_type = type(path)
        try:
            path_repr = path_type.__fspath__(path)
        except AttributeError:
            if hasattr(path_type, '__fspath__'):
                raise
            if issubclass(path_type, PurePath):
                return _PurePath__fspath__(path)
            raise TypeError("expected str, bytes or os.PathLike object, "
                            "not " + path_type.__name__)
        if isinstance(path_repr, (str, bytes)):
            return path_repr
        raise TypeError("expected {}.__fspath__() to return str or bytes, "
                        "not {}".format(path_type.__name__,
                                        type(path_repr).__name__))
########################################################################################
# END NUMPY PATHLIB ATTRIBUTION
########################################################################################

# pickle
try:
    import cPickle as pickle  # noqa
except ImportError:
    import pickle  # noqa

# pandas
try:
    from pandas import DataFrame, Series
    from pandas import MultiIndex
    from pandas import concat as pandas_concat

    PANDAS_INSTALLED = True
except ImportError:

    MultiIndex = object
    DataFrame = object
    Series = object
    pandas_concat = None
    PANDAS_INSTALLED = False

# dt
try:
    # Workaround for #4473, compatibility with dask
    if sys.__stdin__ is not None and sys.__stdin__.closed:
        sys.__stdin__ = None
    import datatable

    if hasattr(datatable, "Frame"):
        DataTable = datatable.Frame
    else:
        DataTable = datatable.DataTable
    DT_INSTALLED = True
except ImportError:

    # pylint: disable=too-few-public-methods
    class DataTable(object):
        """ dummy for datatable.DataTable """

    DT_INSTALLED = False


try:
    from cudf import DataFrame as CUDF_DataFrame
    from cudf import Series as CUDF_Series
    CUDF_INSTALLED = True
except ImportError:
    CUDF_DataFrame = object
    CUDF_Series = object
    CUDF_INSTALLED = False

# sklearn
try:
    from sklearn.base import BaseEstimator
    from sklearn.base import RegressorMixin, ClassifierMixin
    from sklearn.preprocessing import LabelEncoder

    try:
        from sklearn.model_selection import KFold, StratifiedKFold
    except ImportError:
        from sklearn.cross_validation import KFold, StratifiedKFold

    SKLEARN_INSTALLED = True

    XGBModelBase = BaseEstimator
    XGBRegressorBase = RegressorMixin
    XGBClassifierBase = ClassifierMixin

    XGBKFold = KFold
    XGBStratifiedKFold = StratifiedKFold
    XGBLabelEncoder = LabelEncoder
except ImportError:
    SKLEARN_INSTALLED = False

    # used for compatibility without sklearn
    XGBModelBase = object
    XGBClassifierBase = object
    XGBRegressorBase = object

    XGBKFold = None
    XGBStratifiedKFold = None
    XGBLabelEncoder = None


# dask
try:
    import dask
    from dask import delayed
    from dask import dataframe as dd
    from dask import array as da
    from dask.distributed import Client, get_client
    from dask.distributed import comm as distributed_comm
    from dask.distributed import wait as distributed_wait
    from distributed import get_worker as distributed_get_worker

    DASK_INSTALLED = True
except ImportError:
    dd = None
    da = None
    Client = None
    delayed = None
    get_client = None
    distributed_comm = None
    distributed_wait = None
    distributed_get_worker = None
    dask = None

    DASK_INSTALLED = False


try:
    import sparse
    import scipy.sparse as scipy_sparse
    SCIPY_INSTALLED = True
except ImportError:
    sparse = False
    scipy_sparse = False
    SCIPY_INSTALLED = False
