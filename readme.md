# Jack's Desktop Background 3.0
As is now tradition, I have upgraded Ubuntu versions and need to make some new wallpapers.

# What is This?
This is a very simple tool for generating images. The images are made of circles. An
extremely naive space filling algorithm is used to generate the images.

# How does it work?
Circles are added to the canvas one at each unit time step. A function g maps
unit time steps (integers) to scale factors (0 < g(i) < 1 for any integer i). In the
default case a simple linear function is used, but a few others are in the source code.
[This paper](https://link.springer.com/content/pdf/10.7603/s40601-013-0004-2.pdf) goes into
detail about what kind of behaviour g should have to produce good results.

The added feature of this tool is that the intersection function described in the paper
will ignore collisions between circles of the same colour. This lets the shapes
be more interesting than just plain circles.