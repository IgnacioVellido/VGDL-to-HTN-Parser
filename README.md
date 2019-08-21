# antlr-vgdl
ANTLR4 grammar definition for VGDL language and transformation in a HPDL domain.

## Installation
See the [Wiki](https://github.com/IgnacioVellido/antlr-vgdl/wiki) for installation instructions (ANTLR and Java).

## Usage
Having set up everything, to compile the grammar:
```batch
> make.bat build
```

And to transform in a HPDL domain:

```batch 
> make.bat run <VGDL file> [ouput file]
```