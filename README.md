# Pac-Man, by Andrea Oliveri

## Project Overview

The goal of the project is to implement a Pac-Man game in Python.

**This project was done for recreational and learning purposes, and is not, nor it was at any time, meant for commercial purposes.**

## Repository Structure

This directory contains the following files and directories:

* [**pacman.py**](pacman.py): Main Python script used to run the game.
* [**src**](src): Directory collecting all additional Python scripts and custom packages needed to run the game.
* [**assets**](assets): Audio and image files used in the game. 
* [**pacman.spec**](pacman.spec): Pyinstaller specification file needed to package the game into a single executable.
* [**README.md**](README.md): The Readme file you are currently reading.


## Getting Started

### 0) Python Environment

The Python enviroment used for this project was kept as simple as possible to prevent the size of the executable from increasing too much.

An environment containing the required packages with compatible versions can be created as follows:

```bash
conda create -n pacman python=3.13.5
conda activate pacman
pip install pyglet==2.1.6
```

Optionally, to package the game into an executable, Pyinstaller also needs to be installed into the environment:

```bash
pip install pyinstaller==6.15.0
```

### 1) Run

To run the Python script, simply activate the correct conda environment and, from the same directory as the [**pacman.py**](pacman.py) file run:

```bash
python pacman.py
```


### 2) Generate executable

To generate a single executable containing the whole game and all assets, simply activate the correct conda environment and, from the same directory as the [**pacman.spec**](pacman.spec) file run:

```bash
pyinstaller pacman.spec
```

After running this command, the executable should appear inside a folder named **dist**, and can be moved anywhere freely. Another folder named **build** will also be generated. Feel free to delete both folders after generating the executable. 