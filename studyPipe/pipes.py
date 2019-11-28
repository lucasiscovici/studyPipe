from . import _fun_, _funs_, _funsInv_
from . import __fun__, __funs__, __funsInv__
from . import _ftools_
import warnings
try:
  import google.colab
  from .studyPipe import __ as _p_
  __all__=["_p_"]
  with warnings.catch_warnings():
  	warnings.filterwarnings("default")
  	warnings.warn("""
  		In Google Colab: __ become _p_""")
except:
  from .studyPipe import __
  __all__=["__"]
__all__=__all__+["_fun_","_funs_","_funsInv_",\
 		 "__fun__","__funs__","__funsInv__",\
 		 "_ftools_"]