# Installation of Sage

http://doc.sagemath.org/html/en/installation/

# Using in PyCharm

- Open Settings > Project Interpreter
- At the top right of the modal window, click on the gear and select "Add..."
- Choose the "System Interpreter at the left side"
- Select the Python interpreter of the SageMath. (Sage 9.2 version case: [Your SageMath folder]/local/bin/python3)

# Using in console Linux

If you already linked your sage into folder that contained in the $PATH enviroment variable, you can simply run the unit test by the following command:
```
sage unit_test.py
```
That command will initiate a python interpreter that already have the correct local packages.

# Docker

The repository contains a small docker image workspace handler tool. To use it first build the docker image with the following command:
```
./build_image.sh sage
```

Then any folder where you call the `docky.sh sage` command and it will create you a workspace and mounts up the actual working directory into the docker image, so you can work on your local machine on the Sage code.

## Troubleshoot

List the folder that should contain the link to the sage.
```
ls /usr/local/bin/|grep sage
```

Check the path enviroment variable, if contains the folder where you added the link of the sage.
```
echo $PATH
```

## Necessary packages for successfull test compilation

### parameterized
This package is used for parameterize unit test cases, allow to add multiple test data for a single test case.

**Installation**: 
```
path/to/sage/python -m pip install parameterized
```