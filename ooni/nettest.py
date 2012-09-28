import itertools
from twisted.python import log
from twisted.trial import unittest, itrial

pyunit = __import__('unittest')

class InputTestSuite(pyunit.TestSuite):
    """
    This in an extension of a unittest test suite. It adds support for inputs
    and the tracking of current index via idx.
    """
    def run(self, result, idx=0):
        self._idx = idx
        while self._tests:
            if result.shouldStop:
                break
            test = self._tests.pop(0)
            try:
                test.input = self.input
                test._idx = self._idx
                test(result)
            except:
                test(result)
            self._idx += 1
        return result

def lineByLine(fp):
    for x in fp.readlines():
        yield x.strip()
    fp.close()

class TestCase(unittest.TestCase):
    """
    This is the monad of the OONI nettest universe. When you write a nettest
    you will subclass this object.

    * inputs: can be set to a static set of inputs. All the tests (the methods
      starting with the "test_" prefix) will be run once per input.  At every run
      the _input_ attribute of the TestCase instance will be set to the value of
      the current iteration over inputs.  Any python iterable object can be set
      to inputs.

    * inputFile: attribute should be set to an array containing the command line
      argument that should be used as the input file. Such array looks like
      this:

          ``["commandlinearg", "c", "The description"]``

      The second value of such arrray is the shorthand for the command line arg.
      The user will then be able to specify inputs to the test via:

          ``ooniprobe mytest.py --commandlinearg path/to/file.txt``

      or

          ``ooniprobe mytest.py -c path/to/file.txt``


    * inputProcessor: should be set to a function that takes as argument an
      open file descriptor and it will yield the input to be passed to the test
      instance.

    * name: should be set to the name of the test.

    * author: should contain the name and contact details for the test author.
      The format for such string is as follows:

          ``The Name <email@example.com>``

    * version: is the version string of the test.
    """
    name = "IDidNotChangeTheName"
    author = "John Doe <foo@example.com>"
    version = "0"

    inputs = [None]
    inputFile = None
    inputProcessor = lineByLine

    def getOptions(self):
        if self.inputFile:
            fp = open(self.inputFile)
            self.inputs = inputProcessor(fp)

        return {'inputs': self.inputs}

    def __repr__(self):
        return "<%s inputs=%s>" % (self.__class__, self.inputs)


