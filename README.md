# Watt Lighting API
An efficient package for retrieving lighting, power, and occupancy data from
the Watt center. Originally only capable of lighting data, this project was
only named for that functionality.  
Developed by [Molly Pabst](mailto:mepabst@clemson.edu)

## Installation
`$ pip install git+https://github.com/mollypabst/watt-lighting-api`  
This package requires Python 3.7+ (only tested on 3.8).

## Usage
You must be on a campus network.

### Importing in A Script
The package provides a function, `get_levels`, that efficiently retrieves
levels for every available area, and returns them organized in a Pandas
DataFrame object. 
```python
from envision import lighting, energy, occupancy, update, datetime

# update the areas in the package
update()

# The datetime type is provided by the package for convenience
lighting() # Returns DataFrame with current lighting data.
energy(
    start=datetime(2020, 11, 23, 0, 0),
    end=datetime(2020, 11, 23, 0, 0)
) # Returns DataFrame with historical energy data.
occupancy(
    start=datetime(2020, 11, 23, 0, 0),
    end=datetime(2020, 11, 23, 0, 0)
) # Returns DataFrame with historical occupancy data.
```

### Command Line Interface
You can also print this DataFrame to `stdout` by running the package directly,
with the `lighting` argument

`$ python -m envision lighting`

The Web API (energy & occupancy functionality) requires too many complex
arguments for command line functionality, in my opinion. Future contributors
are welcome to try and find a way to add this.

### Updating Areas
This package includes a file called `areas.json` that contains, among other
things, the name and area ID of every area in the Watt Center. This package
needs this information to make the appropriate http requests for each area's
current status. If this information becomes outdated, you can update it with 
the argument

`$ python -m envision update`

or within a Python script with
```python
from envision import update
update()
```

## Differences in v2.0
- The original project could only fetch lighting data. It now supports energy
and occupancy data as well. This took longer to add because it comes from a
different API.
- This version has migrated to using the new `httpx` package for managing all
HTTP connections. This is a "next generation HTTP client for Python" that
fills the role of `requests` and `aiohttp` from v1.0.
- The Web API, which is used for energy and occupancy data, employs the `zeep`
package to manage and parallelize SOAP requests.
- To better manage two API interfaces in the same package, this project now
organizes by files used for different APIs. This should make contributing more
intuitive in the future.
- The `areas.json` file is now of a format that only stores required
information, making it more efficient. It is not compatible with the same file
from v1.0.


## Other Notes
As always, it is highly recommended to use a
[virtual environment](https://docs.python.org/3.8/library/venv.html) before
installing this package and its dependencies.
```shell script
$ python3 -m venv env
$ source env/bin/activate
```
This package contains a file called `credentials.json`, which stores classified
and unencrypted credentials. Do not share this file in any way.

The `httpx` dependency is in a beta stage. I will monitor the development of
this package to make sure it remains compatible until its expected v1.0 release
in late 2020. It may be buggy until then; if you get random errors just rerun
until it works.

Running the update function in a script may produce warnings; they are
insignificant. Ignore them or filter them.

The Web API provides more data than you have access to in this package. In
particular, certain occupancy levels can be unknown, skewing the data. In the
future, this package may be updated to access that information, or you can just
make the SOAP requests yourself if you need more control.
