# autonomous_pp2

A phase portrait viewer.
Display an orbit of the given autonomous ODE. The right hand of the
ODE is described into a setup file. Compared with `autonomous_pp`, 
it does not require a function definition file `ppfunc.pp` anymore. 
The right hand of the ODE is evaluated by `eval()` function, thus 
the speed of this utility is slower than `autonomous_pp`.

## Requirements
* python 3.8 later
    * numpy, scipy
    * matplotlib

## Files
* pp.py -- a simulator 
* pptools.py -- misc. tools
* in.json -- setup file. A JSON format.

## To exec

    % python pp.py in.json

## Setup file configuration

* `func`: a definition of the right hand of the ODE.
* `xrange`, `yrange`: x-y range of the graph
* `alpha`:  transparency value, 0 < alpha < 1
* `params`:	a list of parameter values
* `x0`:	a list of initial values
* `dparams`: a list of incremental values corresponding to the parameters
* `tick`: a time step for drawing a curve
* `p_index`,  `p_position`: Poincare section definition. x[p_position] - p_position = 0

## How to use
### mouse operation 

- A new initial values is given by clicking on the appropriate location
in the graph.
 
### key operation

- `s`: print the current status
- `f`: show/hide trajectory (toggle). Poincare mapping points remain.
- `w`: print the dictionary and dump it to `__ppout__.json`
- `p`: change the active parameter (default: 0, toggle)
- up and down arrows: increase/decrease the active parameter value
- `space`: clear transitions
- `+`, `-`: change the coordinate system, $(x, y) \leftrightarrow (y, z)
  \leftrightarrow (z, x)$, toggle.
- `q`: quit 


