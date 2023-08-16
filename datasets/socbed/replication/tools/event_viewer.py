import argparse
import json
from prettyprinter import cpprint
from termcolor import colored
from sys import exit

cur_entry_nr = 0
event_amount = 0
all_events = initial_events = []
options = {
    "view": "all"
}


def main():
    args = parse_args()
    with open(args.filename, "r") as jsonl_file:
        events = list(jsonl_file)

    console(events)


def parse_args():
    parser = argparse.ArgumentParser(description="View event and relevant fields")
    parser.add_argument("filename", help="JSONL file containing alerts. Top level field 'metadata' should exist.")
    return parser.parse_args()


def console(events):
    global event_amount, cur_entry_nr, all_events, initial_events
    event_amount = len(events)
    initial_events = events.copy()
    all_events = events
    do_print = True
    view_changed = False

    while True:
        if view_changed:
            events = get_new_view()
            view_changed = False

        current_event = events[cur_entry_nr]

        if do_print:
            print_event(json.loads(current_event))

        user_in = input("(P)revious | (N)ext | (J)ump | (E)dit | (O)ptions | (S)ave & Quit | (Q)uit\n"
                        "Choose action: ").lower()
        match user_in:
            case "p":
                do_print = set_next_event(cur_entry_nr - 1)
            case "n":
                do_print = set_next_event(cur_entry_nr + 1)
            case "j":
                do_print = set_next_event(-9999)
            case "e":
                do_print = view_changed = edit_event(current_event)
            case "o":
                do_print = view_changed = set_options()
            case "s":
                save_and_exit()
            case "q":
                exit_app()
            case _:
                print(colored("Invalid input", "red"))
                do_print = False


def print_event(event):
    for key in event.keys():
        print(colored(40 * "~" + f" {key.upper()}", "blue"))
        cpprint(event[key])
    print(colored("\n" + 70 * "=" + "\n", "blue"))
    print(colored("Ground truth values:", "green"))
    if "mitreattack" in event["metadata"] and event["metadata"]["mitreattack"]:
        ground_truth = event["metadata"]["mitreattack"]
        for tactic, techniques in ground_truth.items():
            print(f"Tactic \"{tactic}\" with technique(s) {techniques}")
    else:
        print("Not set!")
    if "comment" in event["metadata"]:
        print(colored("\nAdded comment:\n", "green") + f"{event['metadata']['comment']}")
    print(colored("\n" + 70 * "=" + "\n", "blue"))
    print(f"You are viewing event {cur_entry_nr + 1} out of {event_amount}\n")


def set_next_event(target):
    global cur_entry_nr, event_amount
    if target == -9999:
        try:
            target = int(input("Jump to: ")) - 1
        except ValueError:
            print(colored("Invalid input", "red"))
            return False
    if not (0 <= target < event_amount):
        print(colored("TARGET ENTRY NR IS OUT OF BOUNDS", "red"))
        return False
    cur_entry_nr = target
    return True


def set_options():
    global options
    user_in = input("Which events should be shown?\n"
                    "(T)rue positives | (F)alse positives | (A)ll\n"
                    "Choose type: ").lower()
    match user_in:
        case "t":
            options["view"] = "True"
        case "f":
            options["view"] = "False"
        case "a":
            options["view"] = "all"
        case _:
            print(colored("Invalid input", "red"))
            return False
    return True


def edit_event(edited_event):
    global all_events
    index = all_events.index(edited_event)
    edited_event = json.loads(all_events[index])

    if "mitreattack" not in edited_event["metadata"]:
        edited_event["metadata"]["mitreattack"] = {}

    while True:
        print(colored("\n" + 70 * "=" + "\n", "blue"))
        print(colored("Current tactics/techniques:", "green"))
        for tactic, techniques in edited_event["metadata"]["mitreattack"].items():
            print(f"{tactic} - {techniques}")
        if "comment" in edited_event["metadata"]:
            print(colored("Added comment:\n", "green") + f"{edited_event['metadata']['comment']}\n")
        user_in = input("(A)dd tactic | (R)emove tactic | (C)omment | (F)inish\n"
                        "Choose action: ").lower()

        match user_in:
            case "a":
                new_tactic = input("New tactic name: ")
                new_techniques = input(f"Techniques for tactic {new_tactic} (comma-separated, e.g. 'T1,T2,T3'): ").split(",")
                edited_event["metadata"]["mitreattack"][new_tactic] = new_techniques
            case "r":
                try:
                    delete_key = input("Which tactic to delete: ")
                    del edited_event["metadata"]["mitreattack"][delete_key]
                except KeyError:
                    print("Tactic not present, can't delete.")
            case "c":
                edited_event["metadata"]["comment"] = ""
                comment = input("Enter command that should be attached to this event (empty to remove):\n")
                if comment:
                    edited_event["metadata"]["comment"] = comment
                else:
                    del edited_event["metadata"]["comment"]
            case "f":
                break
            case _:
                print(colored("Invalid input", "red"))

    all_events[index] = json.dumps(edited_event) + "\n"
    return True


def get_new_view():
    global options, event_amount, cur_entry_nr, all_events
    view = options["view"]
    if view == "all":
        event_amount = len(all_events)
        return all_events
    new_events = []
    for event in all_events:
        json_event = json.loads(event)
        if str(json_event["metadata"]["misuse"]) == view:
            new_events.append(event)
    old_event_amount = event_amount
    event_amount = len(new_events)
    if old_event_amount != event_amount:
        cur_entry_nr = 0
    return new_events


def save_and_exit():
    global all_events

    while True:
        filename = input("Save file as: ")
        if filename:
            break
        else:
            print(colored("Filename cannot be empty", "red"))

    with open(filename, "w") as file:
        for event in all_events:
            file.write(event)
    print(f"Saved file as {filename}. Goodbye.")
    exit(0)


def exit_app():
    global all_events, initial_events
    if initial_events != all_events:
        while True:
            decision = input("You have made changes! Are you sure you want to quit (N/y)?: ").lower()
            match decision:
                case "n":
                    return
                case "":
                    return
                case "y":
                    exit(0)
                case _:
                    print(colored("Invalid input", "red"))

    exit(0)


if __name__ == '__main__':
    main()
