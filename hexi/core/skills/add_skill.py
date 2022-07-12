import json
import os


def load_skills():
    with open("skills.json", "r") as jsonfile:
        return json.load(jsonfile)


def save_skill(skills):
    with open("skills.json", "w") as outfile:
        json.dump(skills, outfile, indent=4, ensure_ascii=False, sort_keys=True)


def get_inputs():
    skill_name = input("Enter skill name: ")

    print("Enter commands to envoke the skill, enter q when done:")
    commands = []
    while True:
        out = input().lower()
        if out == "q":
            break
        else:
            commands.append(out)

    return skill_name, commands


def generate_folder(skill_name):
    os.mkdir(skill_name)
    with open(f'{skill_name}/run.py', 'a') as runfile:
        runfile.write("# import interfaces here\n\n# entry point of skill\ndef start():\n    pass\n")


def main():
    skills = load_skills()

    skill_name, commands = get_inputs()
    if skill_name in skills.keys():
        print("Skill with that name already exists")
        quit()

    skills[skill_name] = {
            "commands": commands,
            "script": f'{skill_name}/'
            }

    save_skill(skills)

    generate_folder(skill_name)

    print("\nSkill added!")


if __name__ == "__main__":
    main()
