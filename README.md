# transformations2log

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/danilown/transformations2log.svg)](https://github.com/danilown/transformations2log/blob/main/LICENSE)
[![Python application](https://github.com/danilown/transformations2log/actions/workflows/python-app.yml/badge.svg)](https://github.com/danilown/transformations2log/actions/workflows/python-app.yml)

A simple package to extract `torchvision` transformations used during training and testing.

If you need something to keep track of the transformations / augmentations you used to train a given model this package is for you.

It reads your training script and extracts **all** transformations you used in it.

## Requirements

This package doesn't require any extra packages and should run on every setup with `python >= 3.6`.

If you want to call this package from the CLI, installing `pyyaml` through `pip` is recommended, but not necessary.

## Package Installation

If you want to use this function, you have two options:

A) Simply copy and paste it into your project;

B) Or install it through `pip` following the command bellow:

``` bash
pip install git+git://https://github.com/danilown/transformations2log#egg=transformations2log
```

Then, using it is as simples as:

```python
from transformations2log import transformations2log
```

> **Note 1**: As noted by [David Winterbottom](https://codeinthehole.com/tips/using-pip-and-requirementstxt-to-install-from-the-head-of-a-github-branch/), if you freeze the environment to export the dependencies, note that this will add the specific commit to your requirements, so it might be a good idea to delete the commit ID from it.
> ___
> **Note 2**: Due to the simplicity of this "package", this installation method was preferred over the more traditional [PyPI](https://pypi.org/).

## Usage

The following examples are going to show how you could use this package.

Image you have a set of transformations within `training_script.py` like the following:

``` python
...

train_transforms = transforms.Compose(
    [
        transforms.CenterCrop(10),
        transforms.PILToTensor(), # inline comment within the list
        # transforms.ConvertImageDtype(torch.float),
        transforms.RandomResizedCrop(SIZE, scale=(0.08, 1.0)),
        # comment within the list
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

test_transforms = transforms.Compose(
    [
        transforms.CenterCrop(10),
        transforms.PILToTensor(),
        transforms.ConvertImageDtype(torch.float),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ]
)

...
```

You can extract the transformations from this script from the command line:

```shell
python -m transformations2log training_script.py > transformations.yml
```

and get something like this in it (if you installed `pyyaml`):

```yaml
0:
- transforms.CenterCrop(10)
- transforms.PILToTensor()
- transforms.RandomResizedCrop(SIZE,scale=(0.08,1.0))
- transforms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225])
1:
- transforms.CenterCrop(10)
- transforms.PILToTensor()
- transforms.ConvertImageDtype(torch.float)
- transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225))
```

**note** that the indexes indicate the order of the transformations within the script.

you can also give the found transformations names:

```shell
python -m transformations2log training_script.py -n train test > transformations.yml
```

and get something like this in it (if you installed `pyyaml`):

```yaml
test:
- transforms.CenterCrop(10)
- transforms.PILToTensor()
- transforms.ConvertImageDtype(torch.float)
- transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225))
train:
- transforms.CenterCrop(10)
- transforms.PILToTensor()
- transforms.RandomResizedCrop(SIZE,scale=(0.08,1.0))
- transforms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225])
```

or you could add the following imports to `training_script.py`:

```python
import os
from transformations2log import transformations2log
...
```

and later in the script call the function:

```python
...
transformations = transformations2text(os.path.realpath(__file__))
# transformations = [
#   [
#       'transforms.CenterCrop(10)', 
#       'transforms.PILToTensor()', 
#       'transforms.RandomResizedCrop(SIZE,scale=(0.08,1.0))', 
#       'transforms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225])'
#   ], 
#   [
#       'transforms.CenterCrop(10)', 
#       'transforms.PILToTensor()', 
#       'transforms.ConvertImageDtype(torch.float)', 
#       'transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225))'
#   ]
#]
...
```

The extracted transformations are in the same order as in `training_script.py`, so `transformations[0]` will contain the list of transformations used for training and `transformations[1]` will contain the ones used for testing.

If you want, you can substitute variables with their actual value. That, until now, has to be indicated manually for each variable, so if we want to replace the variable `SIZE` for its actual value, lets say `(224,224)`, you add this when calling the function:

```python
transformations = transformations2text(
                        os.path.realpath(__file__),
                        transforms2replace=[("SIZE", "(224,224)")]
                    )
# transformations = [
#   [
#       'transforms.CenterCrop(10)', 
#       'transforms.PILToTensor()', 
#       'transforms.RandomResizedCrop((224,224),scale=(0.08,1.0))', 
#       'transforms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225])'
#   ], 
#   [
#       'transforms.CenterCrop(10)', 
#       'transforms.PILToTensor()', 
#       'transforms.ConvertImageDtype(torch.float)', 
#       'transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225))'
#   ]
#]
```


## Contributing

It is recommended for you to install the following packages:

```python
flake8>=4.0.1
black>= 22.1.0
isort>=5.10.1
```

If you plan to submit a [PR](https://github.com/danilown/transformations2log/pulls), to facilitate my life and yours, run the following commands and fix the errors / warnings **before** pushing your code:

```shell
black --exclude test/resources .

isort --skip test/resources/ .

flake8 . --count --select=E9,F63,F7,F82 --exclude test/resources,transformations2log/__init__.py --show-source --statistics

flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --exclude test/resources,transformations2log/__init__.py --statistics
```

In order to run the tests, just run:

```shell
python -m unittest
```

**OR** you could simply run the `quick_checkup.sh` script, which will run all these commands automatically for you.

## Support

If you would like to see a new functionality, have a suggestion on how to make the documentation clearer or report a problem, you can open an [issue](https://github.com/danilown/transformations2log/issues/new) here on Github or send me an e-mail danilownunes@gmail.com.
