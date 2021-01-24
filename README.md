# testplanQ
Using MS's testplan framework with qpython to generate multitest for kdb+

Codes have been reformatted against python's black lib

## Links:
1) https://testplan.readthedocs.io/en/latest/
2) https://github.com/KxSystems/kdb-tick
3) https://qpython.readthedocs.io/en/latest/
4) https://github.com/psf/black

## Scripts Required:
1) startKdbProcesses.py
2) test_plan.py

## Example output when running testplan
```
(base) PS C:\Users\haimi\Downloads\testplanQ> python .\test_plan.py
TP is started successfully!
RDB is started successfully!
        Schema of TP trade table is correct - Pass
        Schema of TP quote table is correct - Pass
        Check subscription to TP by RDB - Pass
      [TP_loaded_successfully] -> Passed      
        Schema of RDB trade table is correct - Pass
        Schema of RDB quote table is correct - Pass
      [RDB_loaded_successfully] -> Passed
Successfully stopped TP
Successfully stopped RDB
    [KdbQueries] -> Passed  
  [KdbQueriesTest] -> Passed
[KdbQueriesExample] -> Passed
PDF generated at C:\Users\haimi\Downloads\testplanQ\report.pdf
```