import flet as ft
import json
import datetime

# Ensure the database file exists with an empty structure if it doesn't
DB_FILE = "data.json"

def sort_by_percentage(match_item):
    return match_item["percentage"]
#needs to be globel so is can get the other users input,
def get_matches(current_user_key):
    
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    
    current_user = data.get(current_user_key)
    if not current_user or "fname" not in current_user:
        return []

    matches = []
    
    for other_user_key, other_user in data.items():
        if other_user_key == current_user_key or "fname" not in other_user:
            continue
            
        score = 0
        max_score = 7
        
        if current_user["age"] == other_user["age"]:
            score += 1
        if current_user["hobby"] == other_user["hobby"]:
            score += 1
        if current_user["job"] == other_user["job"]:
            score += 1
        if current_user["conflict"] == other_user["conflict"]:
            score += 1
        if current_user["weekend"] == other_user["weekend"]:
            score += 1
        if current_user["love_lang"] == other_user["love_lang"]:
            score += 1
        if current_user["gender"] != other_user["gender"]: 
            score += 1
        else:
            score=0
        match_percentage = int((score / max_score) * 100)
        if score != 0 and match_percentage > 30:
            matches.append({
                "username_key": other_user_key,
                "name": f"{other_user['fname']} {other_user['lname']}",
                "age": other_user["age"],
                "gender": other_user["gender"],
                "hobby": other_user["hobby"],
                "job": other_user["job"],
                "location": other_user.get("location", "Not specified"),
                "percentage": match_percentage
            })
    # Sort matches by highest percentage using the standard helper function above
    return sorted(matches, key=sort_by_percentage, reverse=True)


def main(page: ft.Page):
    page.title = "Date and Mate"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.TRANSPARENT
    def question_page(username_key):
        page.decoration = ft.BoxDecoration(
            image = ft.DecorationImage(
                src="pixil-frame-0 (1).png",
                fit= ft.BoxFit.FILL
            )
        )
        page.controls.clear()
        page.floating_action_button = None
        questions_text = [
            "What's your first name?",
            "What's your last name?",
        ]    
        questioncontrols = [
            ft.TextField(label=x, hint_text="Enter your answer",color=ft.Colors.WHITE,bgcolor=ft.Colors.BLACK) for x in questions_text
        ]
        address_control = ft.TextField(
            label="What is your preferred meetup address?", 
            hint_text="e.g., 123 Main St, Ottawa, ON",
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLACK,
        )
        question_dropdown = {
            "What's your age?":["18-25","26-30","31-35","41-45","46-50","51+"],
            "What's your gender?":["Male", "Female", "Non-Binary", "Transgender", "Other", "Perfer Not Say"],
            "What's your fav hobby?":["Creative & Crafting", "Physical & Athletic", "Intellectual & Learning", "Outdoor & Nature", "Food & Drink", "Collecting"],
            "What's your job Status?":["Student", "Unemployed", "Employed", "Retired", "Self-Employed", "Other"],
            "How do you handle conflict?": ["Talk it out immediately","Take space to cool down"],
            "What is your ideal weekend layout?": ["Staying home streaming movies","Going dancing or parting","Learing new stuff","Exploring the oudors"],
            "What is your love language?": ["Quality Time", "Words of Affirmation", "Acts of Service", "Gifts"],
        }
        questioncontrols_dropdowns=[
            ft.Dropdown(
                label=x,
                width=300,
                bgcolor=ft.Colors.BLACK,
                options=[ft.dropdown.Option(y) for y in question_dropdown[x]],
            )for x in question_dropdown
        ]
        data: dict = {}
        def submit(e):
            if not address_control.value or address_control.value.strip() == "":
                page.add(ft.Text("Please fill out your meetup physical address!"))
                page.update()
                return
            with open(DB_FILE, "r") as f:
                data = json.load(f)
            data[username_key].update(
                {
                    "fname": questioncontrols[0].value,
                    "lname": questioncontrols[1].value,
                    "age": questioncontrols_dropdowns[0].value,
                    "gender": questioncontrols_dropdowns[1].value,
                    "hobby": questioncontrols_dropdowns[2].value,
                    "job": questioncontrols_dropdowns[3].value,
                    "conflict": questioncontrols_dropdowns[4].value,
                    "weekend": questioncontrols_dropdowns[5].value,
                    "love_lang": questioncontrols_dropdowns[6].value,
                    "location": address_control.value.strip(),
                    "notifications": data[username_key].get("notifications", [])
                }
            )
            with open(DB_FILE, "w") as f:
                json.dump(data, f, indent=4)
            main_page(username_key)
            page.update()
        las= ft.Button("Submit", on_click=submit)
        
        page.add(
            ft.Container(
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Column(controls=questioncontrols),
                        address_control,
                        ft.Column(controls=questioncontrols_dropdowns),
                        las,
                    ]
                ),
                alignment=ft.Alignment.CENTER
            )            
        )
        page.update()

    def new_user():
        page.controls.clear()
        page.floating_action_button = None
        page.decoration = ft.BoxDecoration(
            image = ft.DecorationImage(
            src="pixil-frame-0.png",
            fit= ft.BoxFit.FILL
            )
        )
        greeting = ft.Text(value="Please register for a new account", size=20)
        username = ft.TextField(label="Name", hint_text="Please enter your user name")
        password = ft.TextField(label="Password", password=True, can_reveal_password=True)
        passwordconfirm = ft.TextField(label="Confirm your Password", password=True, can_reveal_password=True)
        feedback = ft.Text(size=16)
        def register_click(e):
            if password.value == passwordconfirm.value:
                comform_username=True
                data: dict = {}
                with open('data.json', 'r') as f:
                    data = json.load(f)
                for x in data:
                    if x == username.value:
                        comform_username=False
                if comform_username == True:
                    data[username.value] = {"password": password.value}
                    with open('data.json', 'w') as f:
                        json.dump(data, f, indent=4)
                    main_start_page()
                else:
                    feedback.value = ("Username is taken")
            else:
                feedback.value = ("Passwords do not match")
        def go_back(e):
            main_start_page()
        bto = ft.Button("Register", on_click=register_click)
        gbb=ft.Button("Return", on_click=go_back)
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        greeting,
                        username,
                        password,
                        passwordconfirm,
                        feedback,
                        bto,
                        gbb,
                    ]
                ),
                alignment=ft.Alignment.CENTER
            )
        )
        page.update()

    def main_start_page():
        page.decoration = ft.BoxDecoration(
            image = ft.DecorationImage(
            src="pixil-frame-0.png",
            fit= ft.BoxFit.FILL
            )
        )
        page.controls.clear()
        page.floating_action_button = None
        
        greeting = ft.Text(value="Welcome to Date and Mate", size=24, weight=ft.FontWeight.BOLD)
        username = ft.TextField(label="Name", hint_text="Please enter your user name", bgcolor=ft.Colors.BLACK)
        password = ft.TextField(label="Password", password=True, can_reveal_password=True, bgcolor=ft.Colors.BLACK)
        feedback = ft.Text(size=16)
        
        def submit_click(e):
            data: dict = {}
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
            
            # Check if user exists and password matches
            user_entry = data.get(username.value)
            if user_entry and user_entry.get("password") == password.value:
                feedback.value = "Login successful!"
                feedback.color = ft.Colors.GREEN_900
                page.update()
                user_found = True
                if "fname" in user_entry:
                    main_page(username.value)
                else:
                    print("hi")
                    question_page(username.value)
            else:
                feedback.value = "Wrong password"
                feedback.color = ft.Colors.RED_900
        def N_User(e):
            new_user()
        submit_click_button = ft.Button("Log In", on_click=submit_click)
        N_User_button = ft.Button("Register a new account?", on_click=N_User)
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        greeting,
                        username,
                        password,
                        feedback,
                        submit_click_button,
                        N_User_button,
                    ]
                ),
                alignment=ft.Alignment.CENTER,
            )
        )

    def main_page(user):
        page.controls.clear()
        page.floating_action_button = None
        feedback = ft.Text(size=20)
        page.decoration = ft.BoxDecoration(
            image = ft.DecorationImage(
            src="pixil-frame-0 (2).png",
            fit= ft.BoxFit.FILL
            )
        )
        with open(DB_FILE, "r") as f:
            db_data = json.load(f)
        current_user_profile = db_data.get(user, {})
        notifications = current_user_profile.get("notifications", [])
        today = datetime.datetime(year=2025, month=4, day=15)
        date_picker = ft.DatePicker(
            first_date=today,
            last_date=datetime.datetime(year=today.year + 1, month=today.month, day=20),
        )
        page.overlay.append(date_picker)

        def make_meet_click_handler(target_key):
            def on_meet_click(e):
                def handle_date_picked(date_event):
                    if date_picker.value:
                        formatted_date = date_picker.value.strftime('%m/%d/%Y')
                        send_meetup_request(target_key, formatted_date)
                date_picker.on_change = handle_date_picked
                date_picker.pick_date()
            return on_meet_click

        def send_meetup_request(target_user_key,selected_date):
            with open(DB_FILE, "r") as f:
                data = json.load(f)
            
            sender_name = f"{data[user]['fname']} {data[user]['lname']}"
            target_address = data[target_user_key].get("location", "their set address")
            
            notification_msg = f"{sender_name} wants to meet up with you on {selected_date} at your preferred address: {target_address}!"
            
            if "notifications" not in data[target_user_key]:
                data[target_user_key]["notifications"] = []
                
            if notification_msg not in data[target_user_key]["notifications"]:
                data[target_user_key]["notifications"].append(notification_msg)
                
            with open(DB_FILE, "w") as f:
                json.dump(data, f, indent=4)
                
            feedback.value=(f"Meetup request sent for address: {target_address} on {selected_date}")
            page.update()
        
        def go_meet(e):
            page.decoration = ft.BoxDecoration(
                image = ft.DecorationImage(
                src="pixil-frame-0 (4).png",
                fit= ft.BoxFit.FILL
                )
            )
            page.controls.clear()
            
            # Fetch matches for this specific user
            match_list = get_matches(user)
            def dww(e):
                make_meet_click_handler(match["username_key"])
            button_to_go_meet=ft.Button("Send Request to Meet Here",on_click=dww)
            match_cards = []
            if not match_list:
                match_cards.append(ft.Text("No matches found yet! Try again later.", size=16, italic=True))
            else:
                for match in match_list:
                    match_cards.append(
                        ft.Card(
                            content=ft.Container(
                                padding=15,
                                width=350,
                                expand=True,
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text(match["name"], size=20),
                                        ft.Container(
                                            content=ft.Text(f"{match['percentage']}% Match", color=ft.Colors.WHITE, size=12),
                                            bgcolor=ft.Colors.RED_900,
                                            padding=5,
                                        ),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Divider(),
                                    ft.Text(f"Age Group: {match['age']} | Gender: {match['gender']}"),
                                    ft.Text(f"Hobby: {match['hobby']}"),
                                    ft.Text(f"Occupation: {match['job']}"),
                                    button_to_go_meet
                                ])
                            )
                        )
                    )

            def back_to_dashboard(e):
                main_page(user)

            back_btn = ft.Button("Back to Dashboard", on_click=back_to_dashboard)
            
            page.add(
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            ft.Text("Your Top Matches", size=24, weight=ft.FontWeight.BOLD),
                            ft.Column(
                                controls=match_cards,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll=ft.ScrollMode.ALWAYS,
                                expand=True,
                            ),
                            back_btn,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
            page.update()
        def clear_notifications(e):
            with open(DB_FILE, "r") as f:
                data = json.load(f)
            data[user]["notifications"] = []
            with open(DB_FILE, "w") as f:
                json.dump(data, f, indent=4)
            main_page(user)

        notification_controls = []

        if notifications:
            notification_controls.append(ft.Text("Meetups:", size=18, color=ft.Colors.WHITE))
            for note in notifications:
                notification_controls.append(
                    ft.Container(
                        content=ft.Text(note, size=14, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.RED_50,
                        padding=10,
                        border_radius=5,
                        width=350
                    )
                )
            notification_controls.append(ft.TextButton("Clear Notifications", on_click=clear_notifications))
        else:
            notification_controls.append(ft.Text("No new meetup notifications.", size=14))
        def Go_to_Q(e):
            question_page(user)
        retake_quiz_btn = ft.Button("Retake Quiz", on_click=Go_to_Q)
        retake_quiz_btn.data = user 
        def end(e):
            main_start_page()
        end_button = ft.Button("Log out", on_click=end)
        page.add(
            ft.Container(
                expand=True,
                content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Dashboard Main Page", size=30),
                    ft.Divider(),
                    ft.Column(controls=notification_controls, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Divider(),
                    retake_quiz_btn,
                    ft.Button("Meet Up with People", on_click=go_meet),
                    end_button,
                    ],
                ),
                alignment=ft.Alignment.CENTER
            )
        )
        page.update()
    main_start_page()
#with open("data.json", "w") as file:
#    json.dump({}, file)
ft.run(main,assets_dir="assets")