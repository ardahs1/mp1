import flet as ft
import os
import json
class person:
    def __init__(self,name,age,gender,hobby,job):
        self.name=name
        self.age=age
        self.gender=gender
        self.hobby=hobby
        self.job=job
def main(page:ft.Page):
    page.title = "Date and Mate"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    def question_page():
        page.controls.clear()
        questions = [
            "What's you name?",
            "What's your age?",
            "What's your gender?",
            "What's your fav hobby?",
            "What's your job"
        ]
        questioncontrols= [
            ft.TextField(label= x, hint_text = "Enter your answer") for x in questions
        ]
        def submit(e):
            data = []
            with open("data.json", "r") as f:
                data=json.load(f)
            new_person = {}
            for x in range(len(questions)):
                new_person[questions[x]] = questioncontrols[x].value
            data.append(new_person)
            with open("data.json", "w") as f:
                json.dump(data, f)
            page.floating_action_button = ft.FloatingActionButton(content = "Submit",on_click = submit)
        page.add(
            ft.Container(
                content=ft.Column(
                    controls = questioncontrols
                ),
                alignment=ft.Alignment.CENTER,
            )            
        )
    '''
    def display_info():
        page.controls.clear()
        page.floating_action_button = None
        selection = ft.TextField(label = "Name", hint_text="Whose info do you want to check?")
        name = ft.Text(value = "Name: ")
        age = ft.Text(value = "Age: ")
        gender= ft.Text(value = "Gender: ")
    '''
    def new_user():
        page.controls.clear()
        page.floating_action_button = None
        greeting = ft.Text(value="Please register for a new account")
        username = ft.TextField(label = "Name", hint_text="Please enter your user name")
        password = ft.TextField(label = "Password", password=True,can_reveal_password=True)
        passwordconfirm = ft.TextField(label = "Confirm your Password", password=True,can_reveal_password=True)
        feedback = ft.Text(size=16)
        def register_click(e):
            if password.value == passwordconfirm.value:
                comform_username=True
                data: dict = {}
                with open('data.json', 'r') as f:
                    data = json.load(f)
                for x in data:
                    if x == username.value:
                        comform_username==False
                if comform_username == True:
                    data[username.value] = password.value
                    with open('data.json', 'w') as f:
                        json.dump(data, f)
                    main_page()
                else:
                    feedback.value = ("Username is taken")
            else:
                feedback.value = ("Passwords do not match")
        page.floating_action_button = ft.FloatingActionButton("Proceed", on_click=register_click)
        page.add(
            ft.Container(
                expand = True,
                content = ft.Column(
                    controls = [
                        greeting,
                        username,
                        password,
                        passwordconfirm,
                        feedback
                    ]
                )
            )
        )
    def main_page():
        greeting = ft.Text(value="Hello")
        username = ft.TextField(label = "Name", hint_text="Please enter your user name")
        password = ft.TextField(label = "Password", password=True,can_reveal_password=True)
        feedback = ft.Text(size=16)
        def submit_click(e):
            collected_name = username.value
            collected_password = password.value
            info = {}
           
            with open("data.json", 'r') as f:
                info = json.load(f)
            if info[username.value] == password.value:
                print("Login successfully")

            for x in info:
                if (collected_name == x and collected_password == info[x]):
                    feedback.value = "password collected successfully, going into the next page"
                    feedback.color = ft.Colors.GREEN_900
                    question_page()
                #notice here!!! If the username and password is correct
                #we will call the question_page function which initializes a new page.
            else:
                feedback.value = "Wrong password"
                feedback.color = ft.Colors.RED_900
        def N_User(e):
            new_user()
        submit_click_button = ft.Button("Log In", on_click=submit_click)
        N_User_button = ft.Button("regester?", on_click=N_User)
        page.add(
            ft.Container(
                expand=True,
                content=ft.Column(
                    controls = [
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
    main_page()

ft.run(main)