# plot*to*terminal
A plotting utility (library) for plotting data into the terminal encoded as
unicode characters as an xy graph, inspired by matplotlib. This tool doesn't
have any dependencies on gnuplot or numpy.

Supports:
* multi scatter plots
* automatic tick setting for linear scales
* automatic data rescaling to fit large numbers as tick labels
* axis labels
* unit labels
* command line interface for plotting xy data file (`$ plottoterminal file`)

Planned:
* command line interface for xy(z) data plotting
* bar plot
* legends
* z value heatmap
* color coding support
* custom marker styles

Example:
```python
import plottoterminal as ptt
import numpy as np

f = ptt.Figure(figsize=(57, 20))
xs = np.linspace(-10, 10, 200)

ys = xs ** 2
f.scatter(xs, ys)

ys2 = -xs ** 2
f.scatter(xs, ys2)

f.set_x_label("x")
f.set_y_label("x*x")
f.set_x_unit("m")
f.set_y_unit("m^2")
f.show()
```

Output:
```
   1.0ᐃxx                                         xx     
×10^2 │ xx                                       xx      
[m^2] │  xxx                                   xxx       
      │    xx                                 xx         
   0.5├      xx                             xx           
      │       xxxx                       xxxx            
      │          xxx                   xxx               
x     │             xxxx           xxxx                  
*  0.0├                *************                     
x     │             ****           ****                  
      │          ***                   ***               
      │       ****                       ****            
  -0.5├      **                             **           
      │    **                                 **         
      │  ***                                   ***       
      │ **                                       **      
  -1.0├**                                         **     
      └┴──────────┴──────────┴──────────┴──────────┴────ᐅ
       -1.0       -0.5       0.0        0.5        1.0   
                                x               ×10^1 [m]
```