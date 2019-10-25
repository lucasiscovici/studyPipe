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

def convert_pipe(original_pipe):
    @functools.wraps(original_pipe)
    def method(self, *args, **kwargs):
        args = (Pipe.unpipe(arg) if isinstance(arg, Pipe) else arg for arg in args)
        kwargs = {k: Pipe.unpipe(v) if isinstance(v, Pipe) else v for k, v in kwargs.items()}
        return Pipe(original_pipe(*args, **kwargs))
    return method


def ror_callable(self, other):
    ret = _resolve(self, other)
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
Pipe2.__ror__=ror_callable 
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
        if isinstance(x, Pipe) or  isinstance(x, Pipe2) or isinstance(x,placeholder)  or  isinstance(x, placeholder2):
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

class placeholder:
    def __init__(self,calla=False,func=lambda x,f=None:f(x) if f is not None else x):
        self.calla=calla
        self.func = func
    def __getattr__(self,a):
        global config
        g=config.globalsFn
        if a in g():
            # if self.calla and callable( g()[a]):
            #     return sspipe.p( g()[a])
            return Pipe(lambda x: g()[a])
        if has_method(builtins,a):
            # if self.calla and callable(getattr(builtins,a)):
            #     return sspipe.p( getattr(builtins,a))
            return Pipe(lambda x:getattr(builtins,a))
        return None

    @staticmethod
    def __array_ufunc__(func, method, *args, **kwargs):
        import numpy
        if callable(method) and args[0] == '__call__':
            # print(args[2].__class__.__name__)
            if method is numpy.bitwise_or:
                if isinstance(args[1], Pipe):
                    return Pipe.partial(_resolve, args[2], args[1])
                elif isinstance(args[1], Pipe2):
                    return Pipe2.partial(_resolve, args[2], args[1])
                elif isinstance(args[2], placeholder):
                    return args[2].__ror__(args[1])
                elif isinstance(args[2], placeholder2):
                    return args[2].__ror__(args[1])
                else:
                    return _resolve(args[2], args[1],Pipe)
            return Pipe.partial(method, *args[1:], **kwargs)
        elif method == '__call__':
            if func.name == 'bitwise_or':
                if isinstance(args[0], Pipe):
                    return Pipe.partial(_resolve, args[1], args[0])
                elif isinstance(args[0], Pipe2):
                    return Pipe2.partial(_resolve, args[1], args[0])
                elif isinstance(args[1], placeholder):
                    return args[1].__ror__(args[0])
                elif isinstance(args[1], placeholder2):
                    return args[1].__ror__(args[0])
                else:
                    return _resolve(args[1], args[0],Pipe)
            return Pipe.partial(func, *args, **kwargs)
        return NotImplemented

    def __or__(self, other):
        return self.func(other)

    def __ror__(self, other):
        return placeholder(func=lambda x, self=self, other=other: x.__ror__(other) if isinstance(other,Pipe) else self.func(other, x))

    def __mod__(self, other):
        return self.func(other)

    def __rmod__(self, other):
        return placeholder(func=lambda x, self=self, other=other: x.__ror__(other) if isinstance(other,Pipe) else self.func(other, x))

class placeholder2:
    def __init__(self,calla=False,func=lambda x,f=None:f(x) if f is not None else x):
        self.calla=calla
        self.func = func
    def __getattr__(self,a):
        global config
        g=config.globalsFn
        if a in g():
            # if self.calla and callable( g()[a]):
            #     return sspipe.p( g()[a])
            return Pipe2(lambda x: g()[a])
        if has_method(builtins,a):
            # if self.calla and callable(getattr(builtins,a)):
            #     return sspipe.p( getattr(builtins,a))
            return Pipe2(lambda x:getattr(builtins,a))
        return None

    @staticmethod
    def __array_ufunc__(func, method, *args, **kwargs):
        import numpy
        if callable(method) and args[0] == '__call__':
            # print(args[2].__class__.__name__)
            if method is numpy.bitwise_or:
                if isinstance(args[1], Pipe):
                    return Pipe.partial(_resolve, args[2], args[1])
                elif isinstance(args[1], Pipe2):
                    return Pipe2.partial(_resolve, args[2], args[1])
                elif isinstance(args[2], placeholder):
                    return args[2].__ror__(args[1])
                elif isinstance(args[2], placeholder2):
                    return args[2].__ror__(args[1])
                else:
                    return _resolve(args[2], args[1],Pipe2)
            return Pipe2.partial(method, *args[1:], **kwargs)
        elif method == '__call__':
            if func.name == 'bitwise_or':
                if isinstance(args[0], Pipe):
                    return Pipe.partial(_resolve, args[1], args[0])
                elif isinstance(args[0], Pipe2):
                    return Pipe2.partial(_resolve, args[1], args[0])
                elif isinstance(args[1], placeholder):
                    return args[1].__ror__(args[0])
                elif isinstance(args[1], placeholder2):
                    return args[1].__ror__(args[0])
                else:
                    return _resolve(args[1], args[0],Pipe2)
            return Pipe2.partial(func, *args, **kwargs)
        return NotImplemented

    def __or__(self, other):
        return self.func(other)

    def __ror__(self, other):
        return placeholder2(func=lambda x, self=self, other=other: x.__ror__(other) if isinstance(other,Pipe2) else self.func(other, x))

    def __mod__(self, other):
        return self.func(other)

    def __rmod__(self, other):
        return placeholder2(func=lambda x, self=self, other=other: x.__ror__(other) if isinstance(other,Pipe2) else self.func(other, x))

class placeholder3:
    def __init__(self,calla=False,func=lambda x,f=None,*otherc=[],**others={}:f(x,*otherc,**others) if f is not None else x):
        self.calla=calla
        self.func = func
    def __getattr__(self,a):
        global config
        g=config.globalsFn
        if a in g():
            # if self.calla and callable( g()[a]):
            #     return sspipe.p( g()[a])
            return Pipe(lambda x: g()[a])
        if has_method(builtins,a):
            # if self.calla and callable(getattr(builtins,a)):
            #     return sspipe.p( getattr(builtins,a))
            return Pipe(lambda x:getattr(builtins,a))
        return None

    @staticmethod
    def __array_ufunc__(func, method, *args, **kwargs):
        import numpy
        if callable(method) and args[0] == '__call__':
            # print(args[2].__class__.__name__)
            if method is numpy.bitwise_or:
                if isinstance(args[1], Pipe):
                    return Pipe.partial(_resolve, args[2], args[1])
                elif isinstance(args[1], Pipe2):
                    return Pipe2.partial(_resolve, args[2], args[1])
                elif isinstance(args[2], placeholder):
                    return args[2].__ror__(args[1])
                elif isinstance(args[2], placeholder2):
                    return args[2].__ror__(args[1])
                elif isinstance(args[2], placeholder3):
                    return args[2].__ror__(args[1])
                else:
                    return _resolve(args[2], args[1],Pipe)
            return Pipe.partial(method, *args[1:], **kwargs)
        elif method == '__call__':
            if func.name == 'bitwise_or':
                if isinstance(args[0], Pipe):
                    return Pipe.partial(_resolve, args[1], args[0])
                elif isinstance(args[0], Pipe2):
                    return Pipe2.partial(_resolve, args[1], args[0])
                elif isinstance(args[1], placeholder):
                    return args[1].__ror__(args[0])
                elif isinstance(args[1], placeholder2):
                    return args[1].__ror__(args[0])
                elif isinstance(args[1], placeholder3):
                    return args[1].__ror__(args[0])
                else:
                    return _resolve(args[1], args[0],Pipe)
            return Pipe.partial(func, *args, **kwargs)
        return NotImplemented

    def __or__(self, other):
        return self.func(other)

    def __ror__(self,other,*args,**xargs):
        return placeholder3(func=lambda x, self=self,other=other, otherc=args,others=xargs: x.__ror__(other,*otherc,**others) if isinstance(other,Pipe) else self.func(other, x,*otherc,**others))

    def __mod__(self, other):
        return self.func(other)

    def __rmod__(self, other):
        return placeholder3(func=lambda x, self=self, other=other: x.__ror__(other) if isinstance(other,Pipe) else self.func(other, x))

patch_all2()
_fun_=placeholder()
__fun__=placeholder2() #with no curryMe
# ____=placeholder(calla=T)
_funs_=placeholder3()


#### construct _ftools_
class opy: pass

####  toolz curried func
oo=['accumulate',  'assoc',  'assoc_in',  'comp',  'complement',  'compose',  'concat',  'concatv',  'cons',  'count',  'countby',  'curry',  'diff',  'dissoc',  'do',  'drop',  'excepts',  'filter',  'first',  'flip',  'frequencies',  'get',  'get_in',  'groupby',  'identity',  'interleave',  'interpose',  'isdistinct',  'isiterable',  'itemfilter',  'itemmap',  'iterate',  'join',  'juxt',  'keyfilter',  'keymap',  'last',  'map',  'mapcat',  'memoize',  'merge',  'merge_sorted',  'merge_with',  'nth',  'operator',  'partial',  'partition',  'partition_all',  'partitionby',  'peek',  'pipe',  'pluck',  'random_sample',  'reduce',  'reduceby',  'remove',  'second',  'sliding_window',  'sorted',  'tail',  'take',  'take_nth',  'thread_first',  'thread_last',  'topk',  'unique',  'update_in',  'valfilter',  'valmap']

for i in oo:
    setattr(opy,i,convert_pipe(getattr(_c,i)))


#### list(map, zip, filter, range) 
def mapl(*args):
    return list(map(*args))

def zipl(*args):
    return list(zip(*args))

def filterl(*args):
    return list(filter(*args))

def rangel(*args):
    return list(range(*args))

toA=[mapl,zipl,filterl,rangel]

for i in toA:
    setattr(opy,i.__name__,convert_pipe(_c.curry(i)))

#### add Pipe functions from JulienPalard
r=dir(_p) | _p.where( _fun_.re.match("^[^_]") ) | _p.as_list()
u=oo+mapl(lambda a:a.__name__,toA)
for i in r:
    met=getattr(_p,i)
    i2=i
    if i in u:
        i2=i+"2"
    setattr(opy,i2,met)

_ftools_=opy()
