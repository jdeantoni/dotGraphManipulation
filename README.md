# dotGraphManipulation
a simple script to higlight some schedules on dot files representation scheduling state spaces (like the ones generated from TimeSquare or Gemoc Studio)


    colorizeCycles.py by Julien Deantoni
      finds shortest and longest cycles in dot file graphs and colorize them, the result is given in a new dot
      create also a "cleaned" dot, without any label, more suitable to sfdp layout
    USAGE: colorizeCycles.py file.dot
    
dependencies: python3, pydot, networkx

a source dot example is provided in the example directory.
moving the script next to the example and running `./colorizeCycles.py model.timemodel.dot` results in two resulting dots that can be process by using dot, like for instance:
```
    dot -Tpdf result_model.timemodel.dot > result_model.timemodel.pdf
    sfdp -Tpdf result_cleaned_model.timemodel.dot > result_cleaned_model.timemodel.pdf
```

note: you can compile this script to pure C by doing:
```
    cython-3.6 colorizeCycles.py -o colorizeCycles.c --embed
    gcc -Os colorizeCycles.c -o colorCycles -I/usr/include/python3.6m/ -lpython3.6m -lpthread -lm -lutil -ldl
```
