# codpy

Colored object detection with Python and OpenCV.

## Goals

Automaticaly detect objects in images and seperate them by color. Manually (de-) select further objects.
Save images containing marked objects and results files.

## Requirements

Python 3.9 was used. The following libraries are imported:

* os
* sys
* numpy
* cv2

## Installation

* if not done, install [numpy](https://numpy.org/install/), [opencv and opencv_contrib](https://docs.opencv.org/4.5.2/df/d65/tutorial_table_of_content_introduction.html)

* clone the repository to your local workspace

```
$ git clone https://github.com/GNiklas/codpy.git
```

* go to your local codpy repository

```
$ cd your/local/codpy
```

* install codpy using setup

```
$ python setup.py install
```

* uninstall using pip

```
$ pip uninstall codpy
```

## Running the Tests

No tests have been implemented, yet.

## Usage

To automatically detect (colored) objects in all images within a directory, do the following:

* import the contour detector class

```
from codpy.contour_detector import ContourDetector
```

* construct a detector object, optionally specifying detection parameters

```
detector = ContourDetector(meanRefH = 170, stdRefH = 10, boxSize=30.)
```

* start detection, optionally giving relative input and output directories

```
detector.detect(relInDir='data', relOutDir = 'results')
```

Manually (de-) select objects by mouseclick

* left on unmarked object: add to uncolored objects

* left on uncolored objects: add to colored objects

* right on colored object: de-select from colored objects

* right on uncolored object: de-select from uncolored objects

* d: de-select all objects

* ENTER: accept selection and go to next image

* q: exit processing. dismiss selection on current image.

### In- and Output

By default, input files are sought in data/. All .jpg files within the input directory are read. Output files are written to results/ by default. Output to each input file are 

* the marked images (*_res.jpg), 
* a file containing the used detection parameters (para.dat),
* a file containing a list of detections for all images (results.csv).

### Examples

Example data and a run file are given in examples/

## References

<a id="1">[1]</a> 
Bradski, G. (2000).
The OpenCV Library.
Dr. Dobb's Journal of Software Tools.

<a id="2">[2]</a>
Harris, C.R., Millman, K.J., van der Walt, S.J. et al. (2020).
Array programming with NumPy.
Nature 585, 357–362.
DOI: 0.1038/s41586-020-2649-2
