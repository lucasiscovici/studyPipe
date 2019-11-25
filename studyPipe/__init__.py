from .studyPipe import configureStudyPipe
import warnings
try:
  import google.colab
  from .studyPipe import __ as _p_
  __all__=["_p_"]
  warnings.warn("""
In Google Colab: __ become _p_
""")
except:
  from .studyPipe import __
  __all__=["__"]

from .studyPipe import _fun_,_funs_, _ftools_, _funsInv_
from .studyPipe import __fun__, __funs__, __funsInv__
from .studyPipe import px, _px, px_, p, _p, p_ #sspipe
from .studyPipe import X, _X, X_, df, _df, df_ #dfply
from .studyPipe import curried, _c, c_ #toolz.curried
from .studyPipe import T, F

__all__=__all__+["configureStudyPipe","_fun_","_funs_", "_ftools_", "_funsInv_","__fun__", "__funs__", "__funsInv__","px", "_px", "px_", "p", "_p", "p_","X", "_X", "X_", "df", "_df", "df_","curried", "_c", "c_","T","F"]