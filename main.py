import json

from algos import read_file, rm_useless_lines, fix_lines, final_fix, is_center, process_center, is_papers_passed, \
    get_papers_passed, process_name_grade, saveFile, encode, fix_lines_technical
from finsal_test_o import perform_test_o

level = "ALT"
year = "2022"
file_name = 'alt2022.txt'
save_name = "out/ALT2022_FINAL.txt"


def main():
    lines = read_file(file_name)
    lines = rm_useless_lines(lines)
    lines = fix_lines(lines) if level[-1] == "G" else fix_lines_technical(lines)
    lines = final_fix(lines)

    center_no = center_name = papers_passed = ""
    json_builder = []

    for line_ind, line in enumerate(lines):
        if is_center(line):
            center_no, center_name = process_center(line)
        elif is_papers_passed(line):
            papers_passed = get_papers_passed(line)
        else:
            name, grade = process_name_grade(line)
            grade = encode(grade)
            student_data = {
                "center_name": center_name,
                "center_number": center_no,
                "level": level,
                "year": year,
                "papers_passed": papers_passed if level[-1] == "G" else grade.count("-"),
                "student_name": name,
                "student_grades": grade
            }

            json_builder.append(student_data)

    perform_test_o(json_builder)
    saveFile(json.dumps(json_builder), save_name)


if __name__ == '__main__':
    main()
