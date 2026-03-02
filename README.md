# YZ
A comprasion command line softwere.

# Commands
## Help
This commands outputs the names of the other Commands with the requiert inputs
### Format:
> yz -help

## Compress
The Compress command takes the input file and the output file.
The Input file can be any text or binary file.
The Output file is where the comprest file is going to get stored.
### Format:
> yz -compress [input file] [output file]

## Decompress
Reverses the compresion algoritham with 0% loss, it takes again an input file and an output file.
The Input file is the privieslie generatet file from **Compress** and the output file is where the output of the decompresion is going to get stored.
### Format:
> yz -decompress [input file] [output file]

## Mode
This can change the mode **Compress** and **Decompress** work in from text to binary.
This must be put infront of **Compress** or **Decompress**, if its not it wont take effect.
### Format:
> yz -mode [text (standard) or binary]
