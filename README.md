**studyPipe: Convenient pipe in python | Pipe pratique en python**  
Based On [sspipe/sspipe](https://github.com/sspipe/sspipe)  itself based on  [JulienPalard/Pipe](https://github.com/JulienPalard/Pipe)  
Based On [/pytoolz/toolz](https://github.com/pytoolz/toolz) (toolz.curried)  
Based On [kieferk/dfply](https://github.com/kieferk/dfply)

**Example: functions in the re module (regex)**  
Without studyPipe

```
import re
list(filter(lambda e:re.match("^[^_]",e),map(str.lower,dir(re))))
```

With studyPipe
```
dir(re) | _ftools_.map(  __.lower() ) | _ftools_.filterl( _fun_.re.match("^[^_]") )
```

**Example: from sspipe**  

```
np.linspace(0, 2*np.pi, 100) | px[np.cos(px) < 0] | p(plt.plot, px, np.sin(px), 'r')
```

with studyPipe

```
np.linspace(0, 2*np.pi, 100) | __[np.cos(__) < 0] | _fun_.plt.plot(__, np.sin(__), 'r');
```
**Exemple 2: from sspipe**  
with sspipe
```
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
```
([0, pi/6, pi/2] 
    | _ftools_.mapl(_fun_.str('{:.3f}').format(sin(__)))
    | _fun_.str(" ").join
    | _fun_.print("Example 5: using builtin map transform and lambda", __)
)
>>> Example 5: using builtin map transform and lambda 0.000 0.500 1.000
```
with studyPipe (and with `|_fun_|`)
```
([0, pi/6, pi/2] 
    | _ftools_.mapl(sin(__) |_fun_| '{:.3f}'.format )
    |_fun_| " ".join
    | _fun_.print("Example 5: using builtin map transform and lambda", __)
)
>>> Example 5: using builtin map transform and lambda 0.000 0.500 1.000
```

**studyPipe's vocabulary:**  
`__`: placeholder (px in sspipe) (two underscore)  
`_fun_`: before a function (replace p in sspipe) (one underscore before, one underscore after)  
`|_fun_|`: between pipes when the next element is an function (without parameters)  
`_ftools_`: curried's functions from toolz.curried and JulienPalard/Pipe  (one underscore before, one underscore after)  

**Install:**
```
pip install git+https://github.com/luluperet/studyPipe.git
```


**Usage:**
```
#Configuration:  
from studyPipe import config
config.globalsFn=lambda:globals()

#Import
from studyPipe import __, _fun_, _ftools_
```

**Imported pipes:**  
`px` and `p` from sspipe (also as `_px` and `_p`, also as `px_` and `p_`)  
`X` from dfply (also as `_X` and `X_`)    
dfply as `df` (also as `_df` and `df_`)  
`curried` from toolz (also as `_c` or `c_`)  
`T` and `F`: for True and False  

