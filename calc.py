FILENAME = "students.txt"
students = []

# ---------- LOAD ----------
try:
    with open(FILENAME, "r") as f:
        for line in f:
            sid, name, dept, subs = line.strip().split("|")
            subject_list = []
            for s in subs.split(","):
                sub, mark = s.split(":")
                subject_list.append((sub, int(mark)))

            students.append({
                "id": sid,
                "name": name,
                "dept": dept,
                "subjects": subject_list
            })
except FileNotFoundError:
    pass


# ---------- SAVE ----------
def save_data():
    with open(FILENAME, "w") as f:
        for s in students:
            subs = ",".join([f"{sub}:{mark}" for sub, mark in s["subjects"]])
            f.write(f"{s['id']}|{s['name']}|{s['dept']}|{subs}\n")


# ---------- CALCULATIONS ----------
def total_marks(s):
    return sum(mark for _, mark in s["subjects"])

def average_marks(s):
    return total_marks(s) / len(s["subjects"])


# ---------- MENU ----------
while True:
    print("\n--- STUDENT MANAGEMENT SYSTEM (PRO) ---")
    print("1. Add Student")
    print("2. View All Students")
    print("3. View Student Report")
    print("4. Rank Students")
    print("5. Update Student")
    print("6. Delete Student")
    print("7. Save & Exit")

    choice = input("Enter choice: ")

    # ---------- ADD ----------
    if choice == "1":
        sid = input("Student ID: ")
        name = input("Name: ")
        dept = input("Department: ")

        n = int(input("Number of subjects: "))
        subjects = []

        for i in range(n):
            sub = input(f"Subject {i+1} name: ")
            mark = int(input("Mark: "))
            subjects.append((sub, mark))

        students.append({
            "id": sid,
            "name": name,
            "dept": dept,
            "subjects": subjects
        })

        print("Student added ✅")

    # ---------- VIEW ALL ----------
    elif choice == "2":
        if not students:
            print("No records ❌")
        for s in students:
            print(s["id"], s["name"], s["dept"])

    # ---------- REPORT ----------
    elif choice == "3":
        sid = input("Enter Student ID: ")
        for s in students:
            if s["id"] == sid:
                print("\n--- STUDENT REPORT ---")
                print("ID:", s["id"])
                print("Name:", s["name"])
                print("Department:", s["dept"])

                for sub, mark in s["subjects"]:
                    print(sub, ":", mark)

                print("Total:", total_marks(s))
                print("Average:", round(average_marks(s), 2))
                break
        else:
            print("Student not found ❌")

    # ---------- RANKING ----------
    elif choice == "4":
        ranked = sorted(students, key=average_marks, reverse=True)

        print("\n--- RANK LIST ---")
        rank = 1
        for s in ranked:
            print(rank, s["id"], s["name"], round(average_marks(s), 2))
            rank += 1

    # ---------- UPDATE ----------
    elif choice == "5":
        sid = input("Student ID to update: ")
        for s in students:
            if s["id"] == sid:
                s["name"] = input("New Name: ")
                s["dept"] = input("New Department: ")
                print("Updated ✅")
                break
        else:
            print("Student not found ❌")

    # ---------- DELETE ----------
    elif choice == "6":
        sid = input("Student ID to delete: ")
        for s in students:
            if s["id"] == sid:
                students.remove(s)
                print("Deleted ✅")
                break
        else:
            print("Student not found ❌")

    # ---------- EXIT ----------
    elif choice == "7":
        save_data()
        print("Data saved 📁 Exiting 👋")
        break

    else:
        print("Invalid choice ❌")