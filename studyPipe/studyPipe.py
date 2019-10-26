import copy
import builtins
import functools
import re

import sspipe 
from sspipe import Pipe as Pipe_
from sspipe import p, px
from sspipe import p as _p, px as _px
from sspipe import p as p_, px as px_

 
import dfply as df
import dfply as _df
import dfply as df_

from dfply import X
from dfply import X as _X
from dfply import X as X_

from toolz import curried 
from toolz import curried as _c
from toolz import curried as c_

__ = sspipe.px

Pipe=copy.deepcopy(Pipe_)
Pipe2=copy.deepcopy(Pipe_) #with no curryMe

T=True
F=False

class config:
    globalsFn=lambda:globals()


#SOURCE: sspipe
def _resolve(pipe, x, cls=Pipe):
    while isinstance(pipe, cls):
        pipe = pipe._____func___(x)
    return pipe

def _resolve2(pipe, x, cls=Pipe):
    while isinstance(pipe, cls):
        pipe = pipe._____func___(x)
    return x

def convert_pipe(original_pipe):
    @functools.wraps(original_pipe)
    def method(self, *args, **kwargs):
        args = (Pipe.unpipe(arg) if isinstance(arg, Pipe) else arg for arg in args)
        kwargs = {k: Pipe.unpipe(v) if isinstance(v, Pipe) else v for k, v in kwargs.items()}
        return Pipe(original_pipe(*args, **kwargs))
    return method


def ror_callable(self, other):
    ret = _resolve(self, other)
    # print("OO")
    if callable(ret): ret=ret(other)
    return ret


def callIfPossible(fn):
    def _callIfPossible(i):
        tt=fn(i)
        try:
            o=tt(i)
        except:
            o=tt
        return o
    return _callIfPossible

def curryMe(fn):
    def _curryMe(x):
        e=fn(x)
        if callable(e):
            return _c.curry(e)
        return fn
    return _curryMe

def call_curry(self, *args, **kwargs):
    self._____func___=curryMe(self._____func___)
    u=Pipe.partial(self, *args, **kwargs)
    return Pipe(callIfPossible(u._____func___))


Pipe.__ror__=ror_callable
Pipe.__call__ = call_curry
Pipe.__rmod__=Pipe.__ror__


#with no curryMe
# Pipe2.__ror__=ror_callable 
Pipe2.__rmod__=Pipe2.__ror__


def has_method(o, name):
    return name in dir(o)

#patch for Pipe, Pipe2, placeholder
def _patch_cls_method(cls, method):
    original = getattr(cls, method)

    @functools.wraps(original)
    def wrapper(self, x, *args, **kwargs):
        # if placeholderFn(x) or placeholder(x):
        #     return NotImplemented
        # print("lalala")
        if isinstance(x, Pipe) or  isinstance(x, Pipe2) or isinstance(x,placeholder)  or  isinstance(x, placeholder2) or  isinstance(x, placeholder3):
            return NotImplemented
        return original(self, x, *args, **kwargs)

    setattr(cls, method, wrapper)


def patch_cls_operator(cls):
    _patch_cls_method(cls, '__or__')

def patch_all2():
    try:
        import pandas

        patch_cls_operator(pandas.Series)
        patch_cls_operator(pandas.DataFrame)
        patch_cls_operator(pandas.Index)
    except ImportError:
        pass

    try:
        import torch

        patch_cls_operator(torch.Tensor)
    except ImportError:
        pass

def iterable(a):
    try:
        (x for x in a)
        return True
    except TypeError:
        return False
def curryX(x,f=None,cls=Pipe):
    def curryXX(o):
        if isinstance(o,list) or isinstance(o,tuple):
            return f(*o)
        if isinstance(o,dict):
            return f(**o)
        return f(o)
    if f is None:
        return f
    if not isinstance(x,cls):
        return f(x)
    return cls.partial(curryXX,x)

def getStaticMethod(mod,cls,met):        
    modu=__import__(mod)
    clss=getattr(modu,cls)
    met=getattr(clss,met)
    return met

def getStaticMethodFromObj(obj,met):
    mod=obj.__module__
    cls=obj.__class__.__name__
    return getStaticMethod(mod,cls,met)

def getStaticMethodFromCls(obj,met):
    mod=obj.__module__
    cls=obj.__name__
    return getStaticMethod(mod,cls,met)
def fnI(x,f=None):
    return f(x) if f is not None else x
class placeholderI(object):
    MY_PIPE=Pipe
    MY_FUNC=fnI

    def special__ror__np(self,argu):
        return self.__ror__(argu)
    def __init__(self,calla=False,func=None):
        self.calla= calla
        self.func = func if func is not None else getStaticMethodFromObj(self,"MY_FUNC")
    def __getattr__(self,a):
        global config
        g=config.globalsFn
        if a in g():
            return getStaticMethodFromObj(self,"MY_PIPE")(lambda x: g()[a])
        if has_method(builtins,a):
            return getStaticMethodFromObj(self,"MY_PIPE")(lambda x:getattr(builtins,a))
        return None

    @classmethod
    def __array_ufunc__(cls,func, method, *args, **kwargs):
        import numpy
        if callable(method) and args[0] == '__call__':
            if method is numpy.bitwise_or:
                if isinstance(args[1], Pipe):
                    return Pipe.partial(_resolve, args[2], args[1])
                elif isinstance(args[1], Pipe2):
                    return Pipe2.partial(_resolve, args[2], args[1])
                elif isinstance(args[2], placeholderI):
                    return args[2].__ror__(args[1])
                else:
                    return _resolve(args[2], args[1],getStaticMethodFromCls(cls,"MY_PIPE"))
            return getStaticMethodFromCls(cls,"MY_PIPE").partial(method, *args[1:], **kwargs)
        elif method == '__call__':
            if func.name == 'bitwise_or':
                if isinstance(args[0], Pipe):
                    return Pipe.partial(_resolve, args[1], args[0])
                elif isinstance(args[0], Pipe2):
                    return Pipe2.partial(_resolve, args[1], args[0])
                elif isinstance(args[1], placeholderI):
                    return args[1].__ror__(args[0])
                else:
                    return _resolve(args[1], args[0],getStaticMethodFromCls(cls,"MY_PIPE"))
            return getStaticMethodFromCls(cls,"MY_PIPE").partial(func, *args, **kwargs)
        return NotImplemented

    def __mod__(self, other):
        return self.__or__(other)

    def __rmod__(self, other):
        return self.__ror__(other)

    def __or__(self, other):
        return self.func(other)

    def __ror__(self, other):
        return self.__class__(func=lambda x, self=self, other=other: x.__ror__(other) if isinstance(other,getStaticMethodFromObj(self,"MY_PIPE")) else self.func(other, x))
def __array_ufunc2__(func, method, *args, **kwargs):
    import numpy
    if callable(method) and args[0] == '__call__':
        if method is numpy.bitwise_or:
            if isinstance(args[1], Pipe):
                return Pipe.partial(_resolve, args[2], args[1])
            elif isinstance(args[1], Pipe2):
                return Pipe2.partial(_resolve, args[2], args[1])
            elif isinstance(args[2], placeholderI):
                return args[2].__ror__(args[1])
            else:
                return ror_callable(args[2], args[1])
        return Pipe.partial(method, *args[1:], **kwargs)
    elif method == '__call__':
        if func.name == 'bitwise_or':
            if isinstance(args[0], Pipe):
                return Pipe.partial(_resolve, args[1], args[0])
            elif isinstance(args[0], Pipe2):
                return Pipe2.partial(_resolve, args[1], args[0])
            elif isinstance(args[1], placeholderI):
                return args[1].__ror__(args[0])
            else:
                return ror_callable(args[1], args[0])
        return Pipe.partial(func, *args, **kwargs)
    return NotImplemented

setattr(Pipe,"__array_ufunc__",staticmethod(__array_ufunc2__))

class placeholder(placeholderI): pass
    
class placeholderBis(placeholderI):
    MY_PIPE=Pipe2

class placeholder2(placeholderI):
    MY_FUNC=curryX
   
    def special__ror__np(self,argu):
        return self.__ror__(argu,okO=True)

    def __ror__(self,other, okO=False):
        if iterable(other) and type(other) != "str":
            other=Pipe.collection(other)
        return placeholder2(func=lambda x, self=self,other=other: x.__ror__(other) if isinstance(other,Pipe) and okO  else self.func(other, x))

class placeholder2Bis(placeholderI):
    MY_FUNC=curried.curry(curryX)(cls=Pipe2)
    MY_PIPE=Pipe2

    def special__ror__np(self,argu):
        return self.__ror__(argu,okO=True)

    def __ror__(self,other, okO=False):
        if iterable(other) and type(other) != "str":
            other=Pipe2.collection(other)
        return placeholder2(func=lambda x, self=self,other=other: x.__ror__(other) if isinstance(other,Pipe2) and okO  else self.func(other, x))


class placeholder3(placeholderI):
    MY_FUNC=curryX

    def special__ror__np(self,argu):
        return self.__ror__(argu,okO=True)

    def __or__(self, other):
        # print(other) 
        if iterable(other) and type(other) != "str" and not isinstance(other,Pipe):
            other=Pipe.collection(other)
        return self.func(other)

    def __ror__(self,other, okO=False):
        if iterable(other) and type(other) != "str":
            other=Pipe.collection(other)
        return placeholder3(func=lambda x, self=self,other=other: x.__ror__(other) if isinstance(other,Pipe) and okO  else self.func(x,other))

class placeholder3Bis(placeholderI):
    MY_FUNC=curried.curry(curryX)(cls=Pipe2)
    MY_PIPE=Pipe2

    def special__ror__np(self,argu):
        return self.__ror__(argu,okO=True)

    def __or__(self, other):
        # print(other) 
        if iterable(other) and type(other) != "str" and not isinstance(other,Pipe2):
            other=Pipe2.collection(other)
        return self.func(other)

    def __ror__(self,other, okO=False):
        if iterable(other) and type(other) != "str":
            other=Pipe2.collection(other)
        return placeholder3Bis(func=lambda x, self=self,other=other: x.__ror__(other) if isinstance(other,Pipe2) and okO  else self.func(x,other))

# def rorFuns(lambda x,self,other):
#     if isinstance(other,Pipe):

#         pass

patch_all2()
_fun_=placeholder()
__fun__=placeholderBis() #with no curryMe
# ____=placeholder(calla=T)
_funs_=placeholder2()
__funs__=placeholder2Bis()
_funsInv_=placeholder3()
__funsInv__=placeholder3Bis()
#### construct _ftools_
class opy: pass

####  toolz curried func
oo=['accumulate',  'assoc',  'assoc_in',  'comp',  'complement',  'compose',  'concat',  'concatv',  'cons',  'count',  'countby',  'curry',  'diff',  'dissoc',  'do',  'drop',  'excepts',  'filter',  'first',  'flip',  'frequencies',  'get',  'get_in',  'groupby',  'identity',  'interleave',  'interpose',  'isdistinct',  'isiterable',  'itemfilter',  'itemmap',  'iterate',  'join',  'juxt',  'keyfilter',  'keymap',  'last',  'map',  'mapcat',  'memoize',  'merge',  'merge_sorted',  'merge_with',  'nth',  'operator',  'partial',  'partition',  'partition_all',  'partitionby',  'peek',  'pipe',  'pluck',  'random_sample',  'reduce',  'reduceby',  'remove',  'second',  'sliding_window',  'sorted',  'tail',  'take',  'take_nth',  'thread_first',  'thread_last',  'topk',  'unique',  'update_in',  'valfilter',  'valmap']

for i in oo:
    setattr(opy,i,convert_pipe(getattr(_c,i)))


#### list(map, zip, filter, range) 
def StringFormatter(template):

    f = str(template).format

    def format(content):
        if isinstance(content, dict):
            return f(**content)
        if iterable(content):
            return f(*content)
        return f(content)

    return format

def mapl(a,b,*args,**xargs):

    if isinstance(a,str):
        a=StringFormatter(a)
    return list(map(a,b,*args,**xargs))

def zipl(*args):
    return list(zip(*args))

def filterl(*args):
    return list(filter(*args))

def rangel(*args):
    return list(range(*args))

def enumeratel(*args):
    return list(enumerate(*args))

def join(stri,arr):
    return stri.join(arr)

def join_n(arr):
    return "\n".join(arr)

def join_comma(arr):
    return "\n".join(arr)

def format_(template,arr):
    return mapl(template,arr)

def format_sep(sep,arr):
    try:
        u=len(arr[0])
        tt=["{}"]*u
        tm=sep.join(tt)
    except:
        if len(arr) > 0:
            u=len(arr)
            tt=["{}"]*u
            tm=sep.join(tt)
        else:
            tm=""
    return mapl(tm,arr)

def format_n(arr):
    return format_sep("\n",arr)

def format_comma(arr):
    return format_sep(", ",arr)

toA=[mapl,zipl,filterl,rangel]

for i in toA:
    setattr(opy,i.__name__,convert_pipe(_c.curry(i)))

toAA=[enumeratel,enumerate,sorted, join,join_n,join_comma,format_sep,format_n,format_comma]
for i in toAA:
    setattr(opy,i.__name__,_fun_.__getattr__(i.__name__))

setattr(opy,"format",_fun_.__getattr__("format_"))

#### add Pipe functions from JulienPalard
r=dir(_p) | _p.where( _fun_.re.match("^[^_]") ) | _p.as_list()
u=oo+mapl(lambda a:a.__name__,toA)+mapl(lambda a:a.__name__,toAA)+["format"]
for i in r:
    met=getattr(_p,i)
    i2=i
    if i in u:
        i2=i+"2"
    setattr(opy,i2,met)

#### add Pipe functions from JulienPalard
u=oo+mapl(lambda a:a.__name__,toA)+mapl(lambda a:a.__name__,toAA)
for i in r:
    met=getattr(_p,i)
    ij=i+"l"
    i2=ij
    if ij in u:
        continue
    setattr(opy,i2,lambda self,x,met=met: Pipe.partial(list,met(x)) )
_ftools_=opy()