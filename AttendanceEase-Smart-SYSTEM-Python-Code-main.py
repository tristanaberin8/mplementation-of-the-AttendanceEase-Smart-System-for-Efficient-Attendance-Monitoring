import datetime
import random

users = {}
attendance = []

print("=======================================")
print("Welcome to Attendance Monitoring System")
print("=======================================")

while True:
    print("\n=== AttendanceEase Smart System ===")
    print("Main Menu:")
    print("1. Add User")
    print("2. View All Users")
    print("3. Edit User")
    print("4. Simulate Scan (Log Attendance)")
    print("5. View Attendance Today")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        while True:
            while True:
                name = input("Enter name: ").strip()
                if name.lower() in [n.lower() for n in users.values()]:
                    print("This name is already used. Please try again.")
                elif name == "":
                    print("Name cannot be empty. Try again.")
                else:
                    break

            uid = str(random.randint(100000, 999999))
            users[uid] = name
            print(f"Completed! New User added: {name} (ID: {uid})")

            while True:
                again = input("Add another user? (y/n): ").lower()
                if again == "y":
                    break
                elif again == "n":
                    print("Returning to main menu...")
                    break
                else:
                    print("Invalid input! Please enter 'y' or 'n'. Try again.")
                    continue
            if again == "n":
                break

    elif choice == "2":
        if not users:
            print("No users yet.")
        else:
            print("\nRegistered Users:")
            for uid, name in users.items():
                print(f"- {name} (ID: {uid})")


    elif choice == "3":
        while True:
            uid = input("Enter user ID to edit: ")
            if uid in users:
                while True:
                    new_name = input("Enter new name: ").strip()
                    if new_name.lower() in [n.lower() for n in users.values() if n != users[uid]]:
                        print("This name is already used by another user. Try again.")
                    elif new_name == "":
                        print("Name cannot be empty. Try again.")
                    else:
                        break
                users[uid] = new_name
                print("Successful! User info updated.")
            else:
                print("!!! User ID not found, please try again.")

            while True:
                again = input("Edit another user? (y/n): ").lower()
                if again == "y":
                    break
                elif again == "n":
                    print("Returning to main menu...")
                    break
                else:
                    print("Invalid input! Please enter 'y' or 'n'. Try again.")
                    continue
            if again == "n":
                break


    elif choice == "4":
        while True:
            uid = input("Scan User ID (enter ID): ").strip()
            if uid in users:
                tz_offset = datetime.timezone(datetime.timedelta(hours=8))
                now = datetime.datetime.now(tz=tz_offset)

                attendance.append({
                    "uid": uid,
                    "name": users[uid],
                    "time_24": now.strftime("%H:%M:%S"),
                    "time_display": now.strftime("%I:%M %p"),
                    "date": now.strftime("%Y-%m-%d"),
                })
                print(f"Done! Attendance recorded for {users[uid]} at {now.strftime('%I:%M %p')}.")
            else:
                print("OOOPS Unknown card! Please register first.")

            while True:
                again = input("Scan another user? (y/n): ").lower()
                if again == "y":
                    break
                elif again == "n":
                    print("Returning to main menu...")
                    break
                else:
                    print("Invalid input! Please enter 'y' or 'n'. Try again.")
                    continue
            if again == "n":
                break


    elif choice == "5":

        cutoff_time_str = input("Enter cutoff time (e.g., 08:00 AM or 01:30 PM): ").strip()

        try:
            cutoff_time = datetime.datetime.strptime(cutoff_time_str, "%I:%M %p").time()
        except ValueError:
            print("Invalid time format! Use HH:MM AM/PM.")
            continue

        today = datetime.date.today().strftime("%Y-%m-%d")

        while True:
            print("\nBy status?")
            print("Options: all / present / late / absent")
            filter_choice = input("Enter filter: ").lower().strip()

            if filter_choice.lower() in ["all", "present", "late", "absent"]:
                break
            else:
                print("Invalid input! Please enter only: all, present, late, or absent.")

        print(f"\nAttendance for {today}:")
        found_any = False

        for uid, name in users.items():

            user_entry = None
            for entry in attendance:
                if entry["uid"] == uid and entry["date"] == today:
                    user_entry = entry
                    break

            if user_entry:
                entry_time = datetime.datetime.strptime(user_entry["time_24"], "%H:%M:%S").time()
                status = "Present" if entry_time <= cutoff_time else "Late"
                time_str = user_entry["time_display"]
            else:
                status = "Absent"
                time_str = "----"

            if filter_choice != "all" and filter_choice != status.lower():
                continue

            print(f"- {name} ({uid}) - {today} - {time_str} - {status}")
            found_any = True

        if not found_any:
            print("No records match this filter.")

    elif choice == "6":
        print("Exiting... Goodbye!")
        break

    else:
        print("Invalid choice, please try again.")