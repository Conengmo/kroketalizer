import json
import os.path
import random

from dotenv import dotenv_values
from flask import render_template, request, jsonify, Response, stream_with_context
from openai import OpenAI

from . import app
from .cache import get_body_from_cache
from .converter import convert, names
from .scrape import get_content


@app.route("/")
def index():
    body = get_body_from_cache()

    context = get_content(body)

    context = convert(context)

    return render_template('index.html', **context)


@app.route('/colofon')
def colofon():
    return render_template('colofon.html')


@app.route('/chat', methods=['POST'])
def chat():
    return stream_with_context(iter_chat_response())


def iter_chat_response():
    data = request.get_json()

    message_history = data.get('messageHistory', [])

    prompt = (
        "Speel de rol van snackbareigenaar, Piet van het Kroketgebouw. "
        "Blijf in karakter. Praat erg kortaf en plat. "
        "Gebruik NOOIT meer dan twee zinnen. Gebruik GEEN uitroeptekens. "
        "Verweef verwijzingen naar klassieke muziek in je tekst. "
    )
    if len(message_history) > 0 and message_history[0]["role"] == "user":
        # gebruiker stelt een vraag
        pass
    else:
        prompt += (
            "Stel je voor en stel de gebruiker een absurde open vraag, meer niet. "
            "Gebruik het antwoord om advies te geven welk gerecht van een snackbar "
            "bij die gebruiker past. "
        )

    print(prompt)

    api_key = dotenv_values()['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        stream=True,
        messages=[
            {"role": "system", "content": prompt},
            *message_history
        ]
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield content
