def greater_than_four(my_json):
    for name in my_json:
        grade = name["student_grades"]
        split_grade = grade.split()
        if len(split_grade) >= 1:
            pass
        else:
            print("no greater than or equal 4")
            print(name)


def contains_dash(my_json):
    for name in my_json:
        grade = name["student_grades"]
        strip_grade = grade.replace(" ", "")
        # if strip_grade[-2] == "-":
        #     pass
        # else:
        #     print("no dash found at end")
        #     print(name)
        # if int(name['papers_passed']) != strip_grade.count('-'):
        #     print()

        if strip_grade[-2] == "-":  # second ooption for subjects with 2 codes
            pass
        else:
            print("no dash found at begining")
            # print(name)
            print(strip_grade)


def check_type_papers_passed(my_json):
    for name in my_json:
        papers_passed = name["papers_passed"]
        try:
            type(int(papers_passed)) == int
        except:
            print("papers passed is not a number")
            print(name)


def check_type_center_number(my_json):
    for name in my_json:
        center_number = name["center_number"]
        try:
            type(int(center_number)) == int
        except:
            print("Center number is not a number")
            print(name)


def check_name_dash(my_json):
    for item in my_json:
        if "-" in item['student_name']:
            print(item)


def check_duplicate(my_json):
    count = 0
    seen = set()
    dupes = []
    for item in my_json:
        new_item = item["student_name"] + item["center_number"]
        if new_item not in seen:
            seen.add(new_item)
        else:
            dupes.append(new_item)

    if dupes:
        print("duplicates found")
        print(dupes)


def check_papers_passed(my_json):
    for item in my_json:
        if int(item["papers_passed"]) == item["student_grades"].count("-"):
            pass
        else:
            print("number of papers passed not equal to number of grades")
            print(item)


def check_student_in_correct_center(my_json):
    for item_ind, item in enumerate(my_json):
        try:
            pass
        except:
            continue


def grades_have_dash(my_json):
    for line in my_json:
        split_grade = line["student_grades"].split()
        for grade in split_grade:
            if "-" in grade:
                pass
            else:
                print("not all grades have dash")
                print(line)


def center_test(my_json):
    for ind, line in enumerate(my_json):
        if ind < 1:
            continue
        cur_center = int(line['center_number'])
        # if cur_center == 11467:
        #     print(line['student_name'])
        #     continue
        prev_line = my_json[ind - 1]
        prev_center = int(prev_line['center_number'])
        # we have changed center
        if cur_center > prev_center:
            # check that number of papers is greater than previous
            if int(line['papers_passed']) < int(prev_line['papers_passed']):
                print("first papers passed for center is less than last for previous center")
                print(line)


def test2019(my_json):
    with open('names.txt', 'r') as f:
        names = f.readlines()

    new_names = []
    for name in names:
        name = name.strip()
        if name[0] == '(' and len(name.split()) > 1:
            # print(name)
            if '-' in name:
                # print(name.split(')')[-1].split('-')[0][:-3])
                new_names.append(name.split(')')[-1].split('-')[0][:-3].strip())
                continue

            else:
                new_names.append(name.split(')')[-1].strip())
                continue
        if name[0] == '(' and len(name.split()) == 1:
            continue
        if 'Passed' in name or 'RESULTS' in name or ('Page' in name and 'of' in name):
            continue

        if '-' in name and ',' in name:
            continue
        new_names.append(name)

    center_names = list(filter(lambda x: x['center_number'] == '11467', my_json))
    # print(len(center_names), len(new_names))

    for name1, name2 in zip(new_names, center_names):
        print(f"{name1} -- {name2['student_name']}")


def perform_test_o(my_json):
    greater_than_four(my_json)
    contains_dash(my_json)
    check_type_papers_passed(my_json)
    check_type_center_number(my_json)
    check_papers_passed(my_json)
    grades_have_dash(my_json)
    # check_name_dash(my_json)
    check_duplicate(my_json)
    # center_test(my_json)
    # check_student_in_correct_center(my_json)

    # test2019(my_json)
