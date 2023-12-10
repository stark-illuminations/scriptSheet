# Convert PDF annotations made by the Obsidian "Annotator" plugin to
# a Markdown table

import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument("source", help="The source file. A .md file.")
parser.add_argument("dest", help="The dest file. A .md file.")
parser.add_argument(
    "--q",
    help="The prefix for cues in comments. \
    Defaults to 'Q'.",
)
parser.add_argument(
    "--i",
    help="The prefix for times in comments \
    Defaults to 'I'.",
)
parser.add_argument(
    "--l",
    help="The prefix for labels in comments \
    Defaults to 'Label:'.",
)
parser.add_argument(
    "--n",
    help="The prefix for labels in comments \
    Defaults to 'Notes:'.",
)
parser.add_argument(
    "--s",
    help="The prefix for scenes in comments \
    Defaults to 'Scene:'.",
)
parser.add_argument(
    "--m",
    help="The prefix for marks in comments \
    Defaults to 'M'.",
)
parser.add_argument(
    "--b",
    help="The prefix for blocks in comments \
    Defaults to 'B'.",
)
parser.add_argument(
    "--f",
    help="The prefix for follows in comments \
    Defaults to 'F'.",
)
parser.add_argument(
    "--x",
    help="The prefix for executes in comments \
    Defaults to 'X'.",
)


args = parser.parse_args()


def split_annotations(lines):
    # Convert all lines from the source file into individual annotations

    annotations = []
    current_annotation = []
    in_block_quote = False

    # Loop through full file
    for i, line in enumerate(lines):
        # Start a new annotation if we aren't in one
        if not in_block_quote:
            if line[0] == ">":
                in_block_quote = True
                current_annotation.append(line)

        # Append to the curent annotation until it ends
        if in_block_quote:
            if line[0] == ">":
                current_annotation.append(line)
            else:
                # When we reach the end of the annotation, append to the output
                in_block_quote = False
                annotations.append(current_annotation)
                current_annotation = []

    return annotations


def process_cues(
    annotations,
    cue_prefix,
    time_prefix,
    label_prefix,
    notes_prefix,
    scene_prefix,
    mark_prefix,
    block_prefix,
    follow_prefix,
    execute_prefix,
):
    # Convert a list of block-quote annotations into a cuelist table
    cue_table = [
        "| Cue Number | Time | Cue Line | Label | Notes | Scene | Mark | Block | Follow | Execute |\n",
        "| ---------- | ---- | -------- | ----- | ----- | ----- | ---- | ----- | ------ | ------- |\n",
    ]
    json_cues = []
    current_line = ["| "]

    # Pull the JSON data from each annotation and convert it to a dict
    for i, annotation in enumerate(annotations):
        # Work with individual cues

        for j, line in enumerate(annotation):
            if line[1] == "{":
                cue_json = json.loads(line[1:].strip())
                json_cues.append(cue_json)

    # Process the dicts and convert them to cue lines
    for i, cue in enumerate(json_cues):
        # Pull cue comments and convert them to useful data
        cue_comment = cue["text"]
        cue_comment = cue_comment.split("\n")

        cue_text = ""
        cue_number = ""
        cue_time = ""
        cue_label = ""
        cue_notes = ""
        cue_scene = ""
        cue_mark = ""
        cue_block = ""
        cue_follow = ""
        cue_execute = ""

        for j, comment in enumerate(cue_comment):
            if comment.lower().startswith(cue_prefix.lower()) or comment.startswith(
                cue_prefix.lower() + " "
            ):
                cue_number = comment[len(cue_prefix) :]

            if comment.lower().startswith(time_prefix.lower()) or comment.startswith(
                time_prefix.lower() + " "
            ):
                cue_time = comment[len(time_prefix) :]

            if comment.lower().startswith(label_prefix.lower()) or comment.startswith(
                label_prefix.lower() + " "
            ):
                cue_label = comment[len(label_prefix) :]

            if comment.lower().startswith(notes_prefix.lower()) or comment.startswith(
                notes_prefix.lower() + " "
            ):
                cue_notes = comment[len(notes_prefix) :]

            if comment.lower().startswith(scene_prefix.lower()) or comment.startswith(
                scene_prefix.lower() + " "
            ):
                cue_scene = comment[len(scene_prefix) :]

            if comment.lower().startswith(mark_prefix.lower()) or comment.startswith(
                mark_prefix.lower() + " "
            ):
                cue_mark = comment[len(mark_prefix) :]

            if comment.lower().startswith(block_prefix.lower()) or comment.startswith(
                block_prefix.lower() + " "
            ):
                cue_block = comment[len(block_prefix) :]

            if comment.lower().startswith(follow_prefix.lower()) or comment.startswith(
                follow_prefix.lower() + " "
            ):
                cue_follow = comment[len(follow_prefix) :]

            if comment.lower().startswith(execute_prefix.lower()) or comment.startswith(
                execute_prefix.lower() + " "
            ):
                cue_execute = comment[len(execute_prefix) :]

        # Get the cue line from the annotation since it's buried in the JSON
        for j, line in enumerate(cue):
            # The cue text has the only "==" highlight in the annotation
            split_line = line.split("==")

            if len(split_line) > 1:
                # Cue text found
                cue_text = split_line[1]

        # Assemble the new table line
        current_line.append(cue_number + " | ")
        current_line.append(cue_time + " | ")
        current_line.append(cue_text + " | ")
        current_line.append(cue_label + " | ")
        current_line.append(cue_notes + " | ")
        current_line.append(cue_scene + " | ")
        current_line.append(cue_mark + " | ")
        current_line.append(cue_block + " | ")
        current_line.append(cue_follow + " | ")
        current_line.append(cue_execute + " |\n")

        finished_line = "".join((str(x) for x in current_line))

        cue_table.append(finished_line)
        current_line = ["| "]

    table_string = "".join((str(x) for x in cue_table))

    return table_string


def convert_file(args):
    # Main function. Converts the source file to an MD table.
    source_file = args.source
    dest_file = args.dest

    # Confirm that file exists
    try:
        with open(source_file, "r") as file:
            lines = file.readlines()

    except FileNotFoundError:
        print("Source file does not exist or path is incorrect.")
        quit()

    # Set prefixes
    cue_prefix = args.q

    if cue_prefix is None:
        cue_prefix = "Q"

    time_prefix = args.i

    if time_prefix is None:
        time_prefix = "I"

    label_prefix = args.l

    if label_prefix is None:
        label_prefix = "Label:"

    notes_prefix = args.n

    if notes_prefix is None:
        notes_prefix = "Notes:"

    scene_prefix = args.s

    if scene_prefix is None:
        scene_prefix = "Scene:"

    mark_prefix = args.m

    if mark_prefix is None:
        mark_prefix = "M"

    block_prefix = args.b

    if block_prefix is None:
        block_prefix = "B"

    follow_prefix = args.f

    if follow_prefix is None:
        follow_prefix = "F"

    execute_prefix = args.x

    if execute_prefix is None:
        execute_prefix = "X"

    # Split the file into individual annotations by block quote
    annotations = split_annotations(lines)

    # Convert the annotations into a markdown table cuelist
    md_table = process_cues(
        annotations,
        cue_prefix,
        time_prefix,
        label_prefix,
        notes_prefix,
        scene_prefix,
        mark_prefix,
        block_prefix,
        follow_prefix,
        execute_prefix,
    )

    with open(dest_file, "w") as file:
        file.write(md_table)


if __name__ == "__main__":
    convert_file(args)
