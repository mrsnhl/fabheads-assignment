# Assignment 2

The assignment for FabHeads Automation.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the depedancies.

```bash
pip install -r requirements.txt
```
## Running the code

```bash
python main.py
```

## Results

![alt text](Figure_1.png "At Height 00mm")
![alt text](Figure_2.png "At Height 10mm")
![alt text](Figure_3.png "At Height 20mm")
![alt text](Figure_4.png "At Height 30mm")
![alt text](Figure_5.png "At Height 40mm")
![alt text](Figure_6.png "At Height 50mm")

## Known Bugs (can be dealt with if given time)
 1. Places where the boundaries are too close (less than the raster width) is taken to be continuous

2. Animation does not work in synchronization

3. Resolution of places where the shells are coinciding is not dealt with. 

4. 3D view of the raster cross section not yet implemented