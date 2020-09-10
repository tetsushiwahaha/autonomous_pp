# autonomous_pp

<img src="https://user-images.githubusercontent.com/52724526/85917890-02850300-b899-11ea-9cb4-6fed6b96509a.png" width=300px align="center">

Display a phase portrait of the given autonomous ODE. The right hand of the
ODE is described into a setup file. 


## Requirements
* python 3.8 later
    * numpy, scipy
    * matplotlib

## Files
* `pp.py`:a simulator
* `pptools.py`: misc. tools
* `in.json`: setup file with JSON format.
* `*.json`: example setup files. 

## To exec

    % python pp.py in.json

or, if you could add an excutable permission to `pp.py`, 

    % ./pp.py in.json

## Setup file configuration

* `func`: a definition of the right hand of the ODE.
* `xrange`, `yrange`: x-y range of the graph
* `alpha`:  transparency value, 0 < alpha < 1
* `params`:	a list of parameter values
* `x0`:	a list of initial values
* `dparams`: a list of incremental values corresponding to the parameters
* `tick`: a time step for drawing a curve
* `p_index`, `p_location`: Poincare section definition. x[p_index] - p_location = 0
* `dump_data`: 0 write nothing, 1 write data to a file.

## How to use
### mouse operation

- A new initial value can be given by clicking on the appropriate location
in the graph.

### key operation

- `s`: print the current status
- `f`: show/hide trajectory (toggle). Poincare mapping points remain.
- `w`: print the dictionary into `__ppout__.json` and save `snapshot.pdf`
- `p`: change the active parameter (default: 0, toggle)
- up and down arrows: increase/decrease the active parameter value
- `space`: clear transitions
- `+`, `-`: change the coordinate system, (x, y) -> (y, z) -> (z, x), toggle.
- `q`: quit

