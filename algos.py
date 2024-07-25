import json
import logging
import os


def final_new_format(lines):
    pass


def read_file(file_name):
    """
    Reads a file and returns a list of lines.
    :param file_name: name of file to read
    :return: list of lines
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.readlines()


def rm_useless_lines(lines):
    """
    Removes useless lines from a list of lines.
    :param lines: list of lines
    :return: list of important lines
    """
    watermark_to_avoid = ["dreampointech.com"]
    new_lines = []
    for line in lines:
        line = line.strip()
        if "RESULTS:" in line:
            continue
        if "Regist:" in line:
            continue
        if "Results of Successful" in line:
            # TODO: calculate the total number of students who passed here
            # passed += int(line.split()[-1])
            continue
        if ("Page" and "of") in line:
            continue
        if "% Passed" in line:
            continue
        if not line.strip():
            continue
        if "alphabetical order" in line.lower():
            continue
        if line.lower().startswith("subjects:"):
            continue
        if line.strip()[0] == '(' and len(line.strip().split()) == 1:
            continue
        if line[-1] == ')' and len(line.strip().split()) == 1:
            continue
        # if len(line.strip().split()) == 1 and ("-" not in line or "," not in line):
        #     # might cause errors for name with single word
        #     continue
        if line.strip() in watermark_to_avoid:
            continue

        if line.strip().isdigit() and new_lines[-1].strip() and "passed" in new_lines[-1].strip().lower():
            continue

        new_lines.append(line)

    save_temp_file(new_lines)
    return new_lines


def save_temp_file(lines):
    """
    Saves a list of useful lines to a temporary file.
    :param lines: list of lines
    :return: None
    """
    # CREATE A DIRECTORY CALLED OUT IF IT DOESN'T EXIST
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(BASE_DIR, 'out')
    os.makedirs(out_dir, exist_ok=True)

    with open('out/temp.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def fix_lines_technical(lines):
    fixed_lines = []
    skip_ind = set()
    for ind, line in enumerate(lines):
        if ind in skip_ind:
            continue
        if not line.strip():
            continue
        line = line.strip()
        if line[0] == '(':
            line = " ".join(line.split()[1:])
            fixed_lines.append(line)
            continue

        if "Centre No:" in line:
            if "Centre No:" in lines[ind + 1]:
                # no student passed in current center
                continue
            if "Passed" not in lines[ind + 1]:
                # continuation of center name
                line = line + " " + lines[ind + 1].strip()
                fixed_lines.append(line)
                skip_ind.add(ind + 1)
                continue
        if "Single Subjects" in line:
            continue
        if "Passed In" in line:
            # if "Specialty:" in lines[ind + 1]:
            # line = line + " " + lines[ind + 1].strip()
            # skip_ind.add(ind + 1)
            # fixed_lines.append(line)
            continue
        if "Specialty:" in line:
            continue
        fixed_lines.append(line)

    save_fixed_file(fixed_lines)
    return fixed_lines


def fix_lines(lines):
    """
    Fixes lines in a list of lines. removes ( and ) and numbers
    :param lines: list of lines
    :return: list of fixed lines
    """

    skip_ind = set()

    skip_center = False
    fixed_lines = []
    for ind, line in enumerate(lines):
        if ind in skip_ind:
            continue
        if skip_center:
            skip_center = False
            continue
        line = line.strip()

        if line.count('(') > 1:
            p = line.split('(')[-1].split(')')[0]
            logging.warning(f'Line {line} has more than one (')
            if p.isdigit():
                line1 = " ".join(line.split(")")[1].split()[:-1]).strip()
                line2 = line.split(')')[-1].strip()
                fixed_lines.append(line1)
                fixed_lines.append(line2)
                continue

        if line[0] == '(':
            line = " ".join(line.split()[1:])
            fixed_lines.append(line)
            # if ind < len(lines) - 4:
            if (ind < len(lines) - 1) and ("Passed In" in lines[ind + 1]) and (("," or "-") not in line):
                # papers passed comes before
                # could throw a list index out of range error
                # TODO fix this
                fixed_lines.append(lines[ind + 2].strip())
                if len(lines[ind + 3].split()) == 1:
                    # part of the grade continues on third line
                    fixed_lines.append(lines[ind + 3].strip())
                    skip_ind.add(ind + 3)
                fixed_lines.append(lines[ind + 1].strip())

                skip_ind.add(ind + 1)
                skip_ind.add(ind + 2)

            continue

        if line[-1] == ')' and line[-2].isdigit():
            line = " ".join(line.split()[:-1])
            fixed_lines.append(line)

            if len(lines[ind + 1].split()) > 1:
                # papers passed comes before grade. so append grade before papers passed
                fixed_lines.append(lines[ind + 2].strip())
                if len(lines[ind + 3].split()) == 1:
                    # part of the grade continues on third line
                    fixed_lines.append(lines[ind + 3].strip())
                    skip_ind.add(ind + 3)
                fixed_lines.append(lines[ind + 1].strip())

                skip_ind.add(ind + 1)
                skip_ind.add(ind + 2)

            continue

        if "Centre No:" in line:
            # if ind > len(lines) - 2:
            #     continue
            if "Centre No:" in lines[ind + 1]:
                # no student passed in current center
                continue
            if "Passed" not in lines[ind + 1]:
                line = line + " " + lines[ind + 1].strip()
                fixed_lines.append(line)
                # logging.warning(f"Fixed center name: {line} ")
                skip_center = True
                continue

        if "Passed In" in line:
            last = line.split()[-1].strip()
            if last.isdigit():
                # no grade attached to this so no problem
                if len(lines[ind + 1].split()) == 1:
                    # part of the grade continues on third line
                    fixed_lines.append(lines[ind + 1].strip())
                    skip_ind.add(ind + 1)
                fixed_lines.append(line)
                continue
            else:
                pp = " ".join(line.split()[:-1])
                for ind1, l1 in enumerate(lines):
                    if l1.isdigit():
                        continue
                    else:
                        g = last[ind1:]
                        pp = pp + " " + last[:ind1]

                        fixed_lines.append(g)
                        fixed_lines.append(pp)
            continue

        if not line.strip():
            continue

        fixed_lines.append(line)

    save_fixed_file(fixed_lines)
    return fixed_lines


def save_fixed_file(lines):
    """
    Saves a list of fixed lines to a temporary file.
    :param lines: list of lines
    :return: None
    """
    with open('out/fixed.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def seperate_long_name_grade(line):
    for i in range(len(line)):
        if line[i] == "-" and line[i + 2] == ",":
            grade = "".join(line[i - 3:])
            name = "".join(line[:i - 3])

            break
    # print(f"{name} - {grade}")
    return name + " " + grade


def final_fix(lines):
    """
    adds grades to their names
    :param lines:
    :return: grades attached to names
    """

    temp_list = []
    should_build = False
    for i, line in enumerate(lines):
        strip_line = line.replace(" ", "")
        strip_line = strip_line.replace(" ", "")
        split_line = line.split()

        line = line.strip()

        if "Centre No:" in line:
            temp_list.append(line)
            continue
        if "Passed In" in line:
            temp_list.append(line)
            continue

        if should_build:
            # either previos item is a name
            last = split_line[-1]
            if len(split_line) == 1:
                if len(last) > 4 and ("-" not in last or "," not in last):
                    # name continuation
                    last = temp_list[-1]
                    temp_list[-1] = last + " " + line + " "
                    continue
                # grade continuation
                last = temp_list[-1]
                new_line = last + " " + line
                temp_list[-1] = new_line
                should_build = False
                continue
            if ("-" in last and "," in last) and len(split_line) > 1:
                # the name is long ans still has part of the grade
                # seperate the grade from the name
                new_line = seperate_long_name_grade(line)
                last = temp_list[-1]
                temp_list[-1] = last + new_line
                should_build = False
                continue

            if len(strip_line) >= 6:
                # to avoid index error for name continuation that is short
                if ((strip_line[3] == "-") and strip_line[5] == ",") or ((strip_line[2] == "-") and strip_line[
                    4] == ",") or ((strip_line[4] == "-") and strip_line[
                    6] == ","):  # second or for commercial who has 2 subject code
                    # add this grade to the previos item which is the name
                    last = temp_list[-1]
                    temp_list[-1] = last + line
                    should_build = False
                    continue


            else:
                # continuation of name on a new line so add name to previous
                last = temp_list[-1]
                temp_list[-1] = last + " " + line + " "
                # should_build = False
        else:
            if (len(split_line) > 1) and ("-" in split_line[-1]):
                if "," in split_line[-1]:
                    # a name which contains grade
                    temp_list.append(line)
                else:
                    # a name which contains - but no grade
                    temp_list.append(line)
                    should_build = True

            elif len(split_line) == 1 and (("-" in split_line[-1]) or (len(split_line[0]) == 1)):
                if "," not in line and "-" in line and len(line) > 10:
                    # person has single name
                    temp_list.append(line + " ")
                    should_build = True
                    continue
                else:
                    # short continuation of the grade
                    # print(line)
                    last = temp_list[-1]
                    temp_list[-1] = last + line
            else:
                # print(line)
                # it is  name without a grade
                temp_list.append(line + " ")
                should_build = True

    save_final_file(temp_list)
    return temp_list


def save_final_file(lines):
    """
    Saves a list of fixed lines to a temporary file.
    :param lines: list of lines
    :return: None
    """
    with open('out/final.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def is_center(line):
    return "Centre No" in line


def process_center(line):
    split_line = line.strip().split()
    c_number = split_line[2]
    c_name = " ".join(split_line[3:])
    return c_number, c_name


def is_papers_passed(line):
    return "passed in" in line.lower()


def get_papers_passed(line):
    return line.strip().split()[2]


def process_name_grade(line):
    s_grade = line.split()[-1]
    s_name = " ".join(line.split()[:-1])
    return s_name, s_grade


def saveFile(my_json, file_name):
    with open(file_name, "w") as f:
        json.dump(my_json, f)


def encode(grade):
    new_grade = ""
    for i in grade:
        if i in [",", "-"]:
            new_grade += i
        elif i.isalpha():
            new_grade += i
        else:
            new_grade += "-"

    return new_grade
