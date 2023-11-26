# ScriptSheet
[[ScriptSheet|scriptsheet.py]] is a rudimentary Python script to convert a set of annotations made by the [Annotator](https://github.com/elias-sundqvist/obsidian-annotator) plugin to a [markdownEos](https://github.com/stark-illuminations/markdownEos)-ready cuelist. It does not require access to the script, just the markdown file used to edit it.

## Known Issues
---
- ScriptSheet is incompatible with [Linter](https://github.com/platers/obsidian-linter) for Obsidian, as Linter often causes problems with Annotator. Disable Linter in the Obsidian vault used for scripts.
- ScriptSheet does not differentiate between Annotations and Highlights. A highlighted section will be inserted as a cue with no information other than a cue line.

## Installation
---
ScriptSheet is a one-file script, requires no dependencies, and is provided without any supplementary materials. Download the file from this repository and run!

## Getting Started
---
To use ScriptSheet, your script must be annotated with Annotator, and all cue data you want to be inserted into the final table must be included in the "comment" section. The highlighted text will be used as the Cue Line, and all properly-prefixed (see [Options](#Options) for more info) will be inserted under the appropriate header.

ScriptSheet does not currently utilize tags, page notes, or any Annotator features beyond basic annotation.

For safety, do not use the original markdown file used to annotate the script. While ScriptSheet only reads the file, Annotator is picky about formatting, and any human tampering risks Annotator being unable to re-open your annotations.

### Basic Use

Run the script by running `$ python scriptsheet.py path/to/source/file path/to/output/file`. The path to the output file can be any blank .md or .txt file.

After running, the table in the output file may be inserted into another markdown file, or used on its own for markdownEos.

### Options

ScriptSheet supports custom prefixes for any header. These prefixes are not case sensitive, and may have one space after them. They must be at the beginning of a new line in the comment. The below table includes the command line option, the name of the option, the default value, and examples.

*Note*: The "Block" and "Mark" options will accept any value. MarkdownEos will treat any value in these cells as a "yes".

| Option | Name    | Default | Examples                                             |
| ------ | --- | ------- | ---------------------------------------------------- |
| `--q`  | Cue Number    | Q       | Q3 \| Q 4.9 \| q931                                  |
| `--i`  | Time    | I       | I1/2 \| i 9                                          |
| `--l`  | Label    | Label:  | Label: Spot Center \| LABEL:Blackout                 |
| `--n`  | Notes    | Notes:  | Notes: Fix shutter cuts                              |
| `--s`  | Scene    | Scene:  | Scene: Act 1, Scene 9 \| Scene:#19 - Moonlight Tango |
| `--m`  | Mark    | M       | MX \| M X \| m Mark                                  |
| `--b`  | Block    | B       | BX \| B X \| b Block                                 |
| `--f`  | Follow    | F       | F10 \| F 3.5 \| f1.2                                 |
| `--x`  | Execute    | X       | XMacro 13 \| X Snapshot 201 \| x Cue 2/19            |

