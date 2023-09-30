from unidic2ud import UniDic2UDEntry


def format_output(entry: UniDic2UDEntry) -> str:
    line_rows = get_line_rows(entry)
    return align_tab_separated_values(line_rows)

def format_output_for_comparing_ignore_space_after_and_features(entry: UniDic2UDEntry) -> str:
    line_rows = get_line_rows(entry)
    line_rows = [line[:-2] for line in line_rows]
    return align_tab_separated_values(line_rows, "＿")


def get_line_rows(entry) -> list[list[str]]:
    output = repr(entry)
    return get_lines_from_output(output)


def get_lines_from_output(output:str) -> list[list[str]]:
    output = output.replace("-", "－")  # use a full width character instead to keep the alignment working.
    lines = output.strip().split('\n')  # Split the multiline string into lines
    lines = [line for line in lines if "\t" in line]  # Skip lines that are not the true output
    line_rows = [line.split('\t') for line in lines]  # Split each line by tab and create a list of lists
    for line in line_rows: line.append(line.pop(5))  # move the features line that often differs to the end.
    return line_rows


def align_tab_separated_values(line_rows: list[list[str]], full_width_separator:str = "　") -> str:
    col_widths = [max(len(str(item)) + 2 for item in col) for col in zip(*line_rows)]  # Find the maximum length for each column

    # Determine the type of space for each column
    space_types = []
    for col in zip(*line_rows):
        if all(all(ord(' ') <= ord(c) <= ord('~') for c in item) for item in col):
            space_types.append(' ')  # ASCII characters
        else:
            space_types.append(full_width_separator)  # Japanese full-width space

    aligned_str = '\n'.join(
        ''.join(f"{item + space_types[i] * (col_widths[i] - len(item))}" for i, item in enumerate(row))
        for row in line_rows)

    return aligned_str