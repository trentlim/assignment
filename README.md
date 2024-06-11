# Code Assignment A1: Protected member of an external package

*This assignment is intended as homework. Do as you normally do, Google/Stack
Overflow-ing your way through.*

For exporting a snapshot of all instrument instances, we are referencing the
protected attribute `qcodes.Instrument._all_instruments` from the external
package `qcodes`.

In `qcodes` version 0.32.0, the definition of `_all_instruments` has been
changed making that our code no longer works.

## Assignment

Upgrade `qcodes` to version 0.32.0. Run the tests and you will observe a
failure.

To resolve this failure, replace the reference to `_all_instruments` with
something new. In your solution, please do not use any **private** members from
`qcodes.Instruments`. Be as creative as you want, and remember that there are no
obvious correct or wrong answers to this assignment.

_You shouldn't spend more than a few hours on this assignment -- should you not
be able to complete it in that time, please formulate what is remaining as TODOs_

_While exploring/debugging you might come across an error message such as
"KeyError: 'Another instrument has the name: MC'". Instances of
`qcodes.Instrument` require to have unique names. This can be fixed by closing
existing instruments via `Instrument.close_all()` or by restarting the kernel._

## Cheatsheet

Upgrade qcodes via:  

```
pip install qcodes==0.32.0  
```

Run the tests via:  

```
pytest tests  
pytest --cov  
```
