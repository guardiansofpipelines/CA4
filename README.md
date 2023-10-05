[![main workflow](https://github.com/guardiansofpipelines/CA4/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/guardiansofpipelines/CA4/actions/workflows/main.yml)
# CA4

## For Windows
### create a virtual environment
```bash
python -m venv venv_name
```
### set execution policy
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
### activate the virtual environment
```bash
source venv_name/Scripts/activate
```
### Create requirements.txt 
```bash
touch requirements.txt
```
### Add the following to requirements.txt
```
black
pytest
```
### run makefile
```bash
make install
```
### run tests
```bash
make test
```
### run lint
```bash
make lint
```
