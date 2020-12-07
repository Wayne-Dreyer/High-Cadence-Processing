#This file was created by Tate Hagan
from GUIHandler import GUIHandler #Imports the file to be tested
from RootGUI import RootGUI #Taken in as input by one of the functions to be tested
from SingletonInstanceException import SingletonInstanceException #Exceptions that can be thrown by the tested class
from IncorrectTypeException import IncorrectTypeException
from NoRootException import NoRootException
from InvalidWindowException import InvalidWindowException

tests = 0
successes = 0
failures = 0

print("Testing getInstance")
print("Test initial call")
try:
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
    
    print("Test subsequent call")
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws error:")
    print(e)
    failures = failures + 1

print("Test constructor when instance already exists")
try:
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    handler = GUIHandler()
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except SingletonInstanceException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error")
    failures = failures + 1

print("-----------------------") #Spaces out text as we are testing a different function
print("Test setRoot")
print("Test setRoot with valid input")
try:
    tests = tests + 1
    root = RootGUI()
    guiHandler = GUIHandler.getInstance()
    guiHandler.setRoot(root)
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws error:")
    print(e)
    failures = failures + 1

print("Test setRoot with invalid input")
try:
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    guiHandler.setRoot(3)
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except IncorrectTypeException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------")
print("Test setWindow")
print("Test setWindow with valid input and state")
try:
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    root = RootGUI()
    guiHandler.setRoot(root)
    guiHandler.setWindow("InputGUI")
    print("SUCCESS-Doesn't throw error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws error:")
    print(e)
    failures = failures + 1

print("Test setWindow with invalid state")
try:
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    guiHandler.closeRoot() #Ensures root will be closed
    guiHandler.setWindow("InputGUI")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except NoRootException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1
    
print("Test setWindow with invalid input")
try:
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    root = RootGUI()
    guiHandler.setRoot(root)
    guiHandler.setWindow("NotAGUI")
    print("FAILURE-Doesn't throw error")
    failures = failures + 1
except InvalidWindowException:
    print("SUCCESS-Throws correct error")
    successes = successes + 1
except Exception as e:
    print("FAILURE-Throws a different error:")
    print(e)
    failures = failures + 1

print("-----------------------")
print("Test getLock")
try:
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    lock = guiHandler.getLock()
    if(not lock):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:False\nOutputted:{}".format(lock))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occured:")
    print(e)
    failures = failures + 1
    
print("Test lock")
try:
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    guiHandler.lock()
    lock = guiHandler.getLock()
    if(lock):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:False\nOutputted:{}".format(lock))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occured:")
    print(e)
    failures = failures + 1
    
print("Test unlock")
try:
    tests = tests + 1
    guiHandler = GUIHandler.getInstance()
    guiHandler.lock()
    guiHandler.unlock()
    lock = guiHandler.getLock()
    if(not lock):
        print("SUCCESS-Correct value outputted")
        successes = successes + 1
    else:
        print("FAILURE-Incorrect value outputted\nExpected:False\nOutputted:{}".format(lock))
        failures = failures + 1
except Exception as e:
    print("FAILURE-An error occured:")
    print(e)
    failures = failures + 1

print("-----------------------") #Spaces out text as we are finished testing
print("-----------------------")
print("Tests: {}".format(tests))
print("Successes: {}".format(successes))
print("Failures: {}".format(failures))