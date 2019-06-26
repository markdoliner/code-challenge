# Overview

Steps to use this:

1. `virtualenv venv`
2. `. venv/bin/activate`
3. `pip install -r requirements.txt`
4. `./find_store --help` and other commands
5. `make check`

# Notes

* I didn't use many third party libraries. See requirements.txt for the list.
* I somewhat arbitrary chose the Bing Maps API for geocoding. It showed up near the top of a search, seemed easy to use, and the license seemed to allow this type of usage. If this was a real project I would want to spend a little more time comparing the major geocoding options, make sure their license allowed the anticipated usage, and check that their pricing was acceptible.
* The zip and address command line arguments are handled identically by the program (they're both handed off to the Bing Maps API to figure out), so the command line could be simplified by getting rip of "--zip." But I kept it as described in the problem statement.
* I didn't want to spend too much time on error handling or response validation when calling the Geocoding API. There are probably many more potential exception-raising scenarios that should be guarded against: Network errors, API server down, API server responds with an HTTP error code, malformed JSON response, etc.
* I used Python's built-in argparse library for parsing command line arguments because I was familiar with it. In hindsight I wish I'd use docopt because I think the output looks better and because you mentioned it in the problem statement, obviously. But it doesn't seem worth spending time changing it now.
* I didn't put my code in a class--just a bunch of top level functions. I think that's fine for a one-off command line script but if this were to be run as some sort of service then it would be good to move the bulk of the code into a class and avoid reading the data file for each request.
* My unit test execs the command line program. If the end product is a command line, that's good. But it's a bit heavy. If the functionality is accessed as a service or as a Python library then it would be better for the tests to import the code and call Python functions directly.

# Time spent

About 5 hr 15 min total.
