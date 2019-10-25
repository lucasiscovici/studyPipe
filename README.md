# studyPipe: Convenient pipe in python | Pipe pratique en python

Based On [sspipe/sspipe](https://github.com/sspipe/sspipe)  itself based on  [JulienPalard/Pipe](https://github.com/JulienPalard/Pipe)  
Based On [/pytoolz/toolz](https://github.com/pytoolz/toolz) (toolz.curried)  
Based On [kieferk/dfply](https://github.com/kieferk/dfply)

Table of Contents
=================

   * [studyPipe: Convenient pipe in python | Pipe pratique en python](#studypipe-convenient-pipe-in-python--pipe-pratique-en-python)
      * [studyPipe's vocabulary:](#studypipes-vocabulary)
      * [Install:](#install)
      * [Usage:](#usage)
      * [Imported pipes:](#imported-pipes)
      * [Curried Functions](#curried-functions)
      * [Comments](#comments)

**Example: functions in the re module (regex)**  
Without studyPipe

```python
import re
list(filter(lambda e:re.match("^[^_]",e),map(str.lower,dir(re))))
```

With studyPipe
```python
dir(re) | _ftools_.map(  __.lower() ) | _ftools_.filterl( _fun_.re.match("^[^_]") )
#OR
re |_fun_| dir | _ftools_.map(  __.lower() ) | _ftools_.filterl(("^[^_]",__) |_funs_| re.match )
```

**Example: from sspipe**  

```python
np.linspace(0, 2*np.pi, 100) | px[np.cos(px) < 0] | p(plt.plot, px, np.sin(px), 'r')
```

with studyPipe

```python
np.linspace(0, 2*np.pi, 100) | __[np.cos(__) < 0] | _fun_.plt.plot(__, np.sin(__), 'r');
#OR
np.linspace(0, 2*np.pi, 100) | __[np.cos(__) < 0] | ((__, np.sin(__), 'r') |_funs_| plt.plot);
#OR with dfply

```
**Exemple 2: from sspipe**  
with sspipe
```python
(
  [0, pi/6, pi/2]
  | p(map, lambda x: '{:.3f}'.format(sin(x)))
  | p(list) 
  | p(' '.join) 
  | p(print, "Example 5: using builtin map transform and lambda", px)
)
>>> Example 5: using builtin map transform and lambda 0.000 0.500 1.000
```

with studyPipe (and without `|_fun_|`)
```python
([0, pi/6, pi/2] 
    | _ftools_.mapl(_fun_.str('{:.3f}').format(sin(__)))
    | _fun_.str(" ").join
    | _fun_.print("Example 5: using builtin map transform and lambda", __)
)
>>> Example 5: using builtin map transform and lambda 0.000 0.500 1.000
```
with studyPipe (and with `|_fun_|`)
```python
([0, pi/6, pi/2] 
    | _ftools_.mapl(sin(__) |_fun_| '{:.3f}'.format )
    |_fun_| " ".join
    | _fun_.print("Example 5: using builtin map transform and lambda", __)
)
#OR
([0, pi/6, pi/2] 
    | _ftools_.mapl( sin(__) )
    | _ftools_.format('{:.3f}')
    | _ftools_.join(" ")
    | _fun_.print("Example 5: using builtin map transform and lambda", __)
)
>>> Example 5: using builtin map transform and lambda 0.000 0.500 1.000
```

## studyPipe's vocabulary:  
`__`: placeholder (px in sspipe) (two underscore)  
   - ```python 
       np.array(range(100)) | (__-__.mean())/__.std()
       ``` 
   
`_fun_`: before a function (replace p in sspipe) (one underscore before, one underscore after)  
  - ```python 
      "Hello World" | _fun_.print  
      ```   
      (same as `print("Hello World")  
  - ```python 
      "Hello World" | _fun_.print(__,end=' !!!!\n')
    ```    
    (same as `print("Hello World",end=' !!!!\n')`)  
  - ```python 
    "Hello World" | _fun_.print(__.lower(),end='!' * _fun_.len(__) + '\n')
    ```  
    (same as `print("Hello World".lower(),end='!' * len("Hello World") + '\n')`)  
  
`|_fun_|`: between pipes when the next element is an function (without parameters)    
  - ```python 
    "Hello World" |_fun_| print
    ```   
    (same as `print("Hello World")`)  
  - ```python 
    "studyPipe" |_fun_| "Hello World {} !!".format |_fun_| print
    ```   
    (same as `print("Hello World {} !!".format("studyPipe"))`) 
  - ```python 
      __ |_fun_| "Hello World {} !!".format |_fn_| print
      ```  
      (same as `lambda x: print("Hello World {} !!".format(x))`)  
  
`_ftools_`: curried's functions from toolz.curried and JulienPalard/Pipe  (one underscore before, one underscore after)   
  - ```python 
      ["Helloee","World", "blablabla"] | _ftools_.mapl( __ |_fun_| len )
      ```
      (same as `list(map(len,["Helloee","World", "blablabla"]))`)  
  - ```python 
      ["Helloee","World", "blablabla", "dd", "22h"] | _ftools_.filterl( __ |_fun_| len > 4 )
     ```  
     (same as `list(filter(lambda x:len(x) > 4,["Helloee","World", "blablabla", "dd", "22h"]))`) 
- More on: [JulienPalard/Pipe](https://github.com/JulienPalard/Pipe)  
- More on: [/pytoolz/toolz](https://github.com/pytoolz/toolz)  

`|_funs_|`:  when the next element is a function and you want to expand an iterable as function's parameters  (next function without parameters)  
```python
(
    [["Hello",[0,1,2,3,4]], ["World",[5,6,7,8]]]  
    | _ftools_.mapl((  __[0].upper(), 
                       __[1] | _ftools_.concat2(', '),
                       __[1] |_fun_| sum  ) 
                    |_funs_| "{} : {} (sum: {})".format
                   ) 
    |_fun_| '\n'.join |_fun_|  print
)
>>> HELLO : 0, 1, 2, 3, 4 (sum: 10)
... WORLD : 5, 6, 7, 8 (sum: 26)
```
same as 
```python
    print(
        '\n'.join(
            map(lambda x:"{} : {} (sum: {})".format(x[0].upper(),
                                                    ', '.join(map(str,x[1])),
                                                    sum(x[1])),
                [["Hello",[0,1,2,3,4]], ["World",[5,6,7,8]]] 
               )
        )
    )
>>> HELLO : 0, 1, 2, 3, 4 (sum: 10)
... WORLD : 5, 6, 7, 8 (sum: 26)
```
`|_funsInv_|` : when the next element is an **iterable** (tuple, list, ...) and you want to expand them as function's parameters (the element before is a function without parameters)
```python
(
    os.listdir() 
    | _ftools_.where(__.endswith(".py")) 
    | _ftools_.sorted(key=len)
    | _ftools_.enumerate
    | _ftools_.mapl( "{}. {}".format |_funsInv_|  __ )  
    | _ftools_.join("\n") 
    | _fun_.print
)
#OR
(
    os.listdir() 
    | _ftools_.where(__.endswith(".py")) 
    | _ftools_.sorted(key=len)
    | _ftools_.enumerate
    | _ftools_.mapl( "{}. {}" )  
    | _ftools_.join("\n") 
    | _fun_.print
)
#OR
(
    os.listdir() 
    | _ftools_.where(__.endswith(".py")) 
    | _ftools_.sorted(key=len)
    | _ftools_.enumerate
    | _ftools_.format( "{}. {}" )  
    | _ftools_.join_n
    | _fun_.print
)
>>> 0. 03_classification_script.py
... 1. 06_decision_trees_script.py
... 2. 03_classification-Copy1_script.py
... 3. 04_training_linear_models_script.py
... 4. 01_the_machine_learning_landscape_script.py
... 5. 02_end_to_end_machine_learning_project_script.py
... 6. 07_ensemble_learning_and_random_forests_script.py
... 7. 07_ensemble_learning_and_random_forests_modif_script.py
```

```python
(
    os.listdir() 
    | _ftools_.where(__.endswith(".py")) 
    | _ftools_.sorted(key=len)
    | _ftools_.enumerate
    | _ftools_.mapl( "{}. {} ({})".format |_funsInv_| (__[0], __[1], len |_funsInv_| (__[1],) ) )  
    | _ftools_.join_n
    | _fun_.print
)
#OR
(
    os.listdir() 
    | _ftools_.where(__.endswith(".py")) 
    | _ftools_.sorted(key=len)
    | _ftools_.enumerate
    | _ftools_.mapl( "{}. {} ({})".format |_funsInv_| ( __[0], __[1], _fun_.len(__[1]) ))  
    | _ftools_.join_n
    | _fun_.print
)
>>> 0. 03_classification_script.py (27)
... 1. 06_decision_trees_script.py (27)
... 2. 03_classification-Copy1_script.py (33)
... 3. 04_training_linear_models_script.py (35)
... 4. 01_the_machine_learning_landscape_script.py (43)
... 5. 02_end_to_end_machine_learning_project_script.py (48)
... 6. 07_ensemble_learning_and_random_forests_script.py (49)
... 7. 07_ensemble_learning_and_random_forests_modif_script.py (55)
```

## Install:
```
pip install git+https://github.com/luluperet/studyPipe.git
```


## Usage:
```
#Configuration:  
from studyPipe import config
config.globalsFn=lambda:globals() # Alow studyPipe to know your variables, modules, ....

#Import
from studyPipe import __, _fun_, _funs_, _ftools_ #placeholder
```

## Imported pipes:  
`px` and `p` from sspipe (also as `_px` and `_p`, also as `px_` and `p_`)  
`X` from dfply (also as `_X` and `X_`)    
dfply as `df` (also as `_df` and `df_`)  
`curried` from toolz (also as `_c` or `c_`)  
`T` and `F`: for True and False  

## Curried Functions
All functions available in JulienPalard/Pipe have a twin function that calls the list function on the result of the original function: theses functions ends by `l`  
`wherel`, `selectl`, ....  
More: mapl, zipl, filterl, rangel, enumeratel, sorted, join, enumeratel, enumerate, sorted, join_n, join_comma, format_sep, format_n, format_comma

## Comments 
when `_funs_`(`_funsInv_`) is not between pipes (`|_funs_|`, `|_funsInv_|`), it act same as `_fun_`. The only difference between `_fun_` and `_funs` (`_funsInv`) it's when they are between pipes, otherwise they are the same   

When `__` is alone before `|_funs_|` they are some  problems..., you have to use `|_funsInv_|`
Ex (with `|_funs_|`):
```python 
(
    [["Hello",[0,1,2,3,4]], ["World",[5,6,7,8]]]  
    | _ftools_.mapl( __ |_funs_| "{} : {} ".format ) 
)
>>> [<sspipe.pipe.Pipe at 0x7fa233c63618>, <sspipe.pipe.Pipe at 0x7fa233c63348>]
```
(with `|_funsInv_|`)
```python 
(
    [["Hello",[0,1,2,3,4]], ["World",[5,6,7,8]]]  
    | _ftools_.mapl(  "{} : {} ".format |_funsInv_| __ ) 
)
>>> ['Hello : [0, 1, 2, 3, 4] ', 'World : [5, 6, 7, 8] ']
```
