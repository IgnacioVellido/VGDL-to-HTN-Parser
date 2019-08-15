# antlr-vgdl
ANTLR4 grammar definition for VGDL language.

## Installation
See the [Wiki](https://github.com/IgnacioVellido/antlr-vgdl/wiki) for installation instructions.

## Usage
Having set up everything, you can put (in the command prompt):
```batch
> make.bat buildrun basicGame
```

Or, for a visual representation of the parsed tree:

```batch 
> make.bat buildgrun basicGame
```

For testing a specific rule:
```batch
> make.bat <option> <rule name> <vgdl-file>
```

You can find a list of available options in the [Wiki](https://github.com/IgnacioVellido/antlr-vgdl/wiki/Make-options)