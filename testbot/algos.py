import json
import sys

sys.path.append("../testbot")
from perform_test import perform_test_o


def main():
    with open("output/ALG2022/lines.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open("output/ALG2022/names.txt", 'r', encoding='utf-8') as f:
        names = f.readlines()

    process_data(lines, names)


def is_name_and_grade(line):
    line = line.strip()
    return len(line.split()) > 1 and "-" in line and "," in line


def is_only_name(line):
    line = line.strip()
    last = line.split()[-1]
    return "-" not in last and "," not in last


def fix_names(names):
    temp_list = []
    skips = set()
    print("len(names): " + str(len(names)))
    for ind, line in enumerate(names):
        if not line.strip():
            continue
        line = line.strip()
        if ind in skips:
            continue

        if is_name_and_grade(line):
            temp_list.append(line)

        elif is_only_name(line):
            next1 = ind + 1
            grade = names[next1]
            temp_list.append(line + " " + grade)
            skips.add(next1)

    return temp_list


def process_data(lines, names):
    centers = {}
    current_center = ""
    for line in lines:
        line = line.strip()
        if line.lower().startswith("centre"):
            centers[line] = []
            current_center = line
            continue

        if not current_center:
            continue

        centers[current_center].append(line)

    with open("output/ALG2022/centerNameNumber.json", 'w') as f:
        json.dump(centers, f, indent=2)

    names = fix_names(names)
    for name in names:
        if len(name.split()) == 1:
            print("ERROR: Grade not found for name: " + name)

    with open("output/ALG2022/names_grades.txt", 'w', encoding='utf-8') as f:
        for name in names:
            f.write(name + "\n")

    json_builder = []
    e1 = True
    e2 = True
    for name in names:
        center = ""
        for center_key, center_value in centers.items():
            a = " ".join(name.split()[:-1])
            if len(a.split()) == 1:
                if e1:
                    print("WARNING: Name has just one word. Might cause incorrect data. Crosscheck: " + a)
                    e1 = False
            for v in center_value:
                if a in v:
                    center = center_key
                    break
        if not center:
            print("WARNING: Center not found for name: " + name)

            for center_key, center_value in centers.items():
                a = name.split()[-1]
                for v in center_value:
                    if a in v:
                        center = center_key
                        if e2:
                            print("WARNING: Center found for name using grade. Crosscheck: " + name)
                            e2 = False
                        break

        if not center:
            print("WARNING: Center not found for name: " + name)
            exit(-1)

        try:
            center.split()[2]
        except:
            print("ERROR: incorrect center format: " + center + " for " + name)
            exit(-1)

        student_data = {
            "center_name": " ".join(center.split()[3:]),
            "center_number": center.split()[2],
            "level": "ALG",
            "year": "2022",
            "papers_passed": name.split()[-1].count("-"),
            "student_name": " ".join(name.split()[:-1]),
            "student_grades": name.split()[-1]
        }

        json_builder.append(student_data)

    perform_test_o(json_builder)



if __name__ == '__main__':
    main()
