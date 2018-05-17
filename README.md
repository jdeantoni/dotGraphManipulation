# dotGraphManipulation
a simple script to higlight some schedule on dot files representation scheduling state spaces (like the one generated from TimeSquare or Gemoc)


    colorizeCycle.py by Julien Deantoni
      finds shortest and longest cycles in dot file graphs and colorize them, the result is given in a new dot
      create also a "cleaned" dot, without any label, more suitable to sfdp layout
    USAGE: colorizeCycle.py file.dot
    
dependencies: python3, pydot, networkx
