import os
import wikipediaapi
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        wiki_wiki = wikipediaapi.Wikipedia('en')
        person = request.form["person"]
        person_page = wiki_wiki.page(person)
        summary = person_page.summary
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(summary),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(person):
    return f"""read the following summary and tell me the persons age in the following format: Alive, age, date of birth, 
    however they may not be alive, so you need to read the dates carefully and
    determine if there is a date of death. If you see two dates that means they have died
    for example if you see something like this: (May 17, 1956 – January 9, 2022), that means they died jan 9th 2022.
    after you analyze the summary give me the date of death in the following format: Deceased, age, time of death
    {person}"""
