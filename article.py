#!/usr/bin/env python3

import openai
import os
import json
import datetime
import requests
import sys


# get the api key from first input argument
openai_key = sys.argv[1]
print("OpenAI API Key: " + openai_key)

# Set up your OpenAI API key
openai.api_key = openai_key
path = "./content/posts/"
topic = "Technology, DevOps, DevSecOps, SecOps, Microcontrolers, FPV drones, 3D printing, Motorbikes, Engineering Management, Software Engineering, Software Development, Software Architecture, Software Design, Software Testing, Software Quality, Software Security, Software Performance, Infrastracture "


def ai_query(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}], request_timeout=5000)
    answer = response.choices[0].message.content
    return answer


def remove_quotes(string):
    if string.startswith(("'", '"')) and string.endswith(("'", '"')):
        return string[1:-1]
    else:
        return string


def capitalize_first_letter(string):
    words = string.split()
    capitalized_words = [words[0].capitalize()] + [word.lower() for word in words[1:]]
    return ' '.join(capitalized_words)


def remove_empty_lines(string):
    return '\n'.join([line for line in string.split('\n') if line.strip()])


def generate_markdown(title, date, category, tags, sort, article):
    return f'''
---
title: {title}
date: {date}
author: 'gpt-3.5-turbo'
categories: [{category}]
tags: [{tags}]

resources:
  - name: featured-image
    src: featured-image.png
# - name: featured-image-preview
#     src: featured-image-preview.png

draft: false
lightgallery: true
fontawesome: true
linkToMarkdown: true
rssFullText: false

toc:
auto: false
comment:
enable: true
---

<style>
img {{
    box-shadow: inset 10px 10px 60px #fff;
    -moz-border-radius:25px;
    border-radius:10px;
}}
</style>

{sort}

<!--more-->

{article}
'''


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
            print(f"Image saved as {filename}")
    else:
        print(f"Error downloading image: {response.status_code}")


def save_string_to_file(string, filename):
    with open(filename, 'w') as file:
        file.write(string)
        print(f"{len(string)} bytes written to {filename}")


def make_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    print(f"Folder created at {folder_path}")


print("Topic: " + topic)

area_of_interest = ai_query("Give me a random area of interest if I want to learn something new. Keep this area around" + topic + ". Give the area in a sentence with no more than 20 words, ")
area_of_interest = remove_empty_lines(area_of_interest)
print("Area of Interest: " + area_of_interest)

get_title = ai_query("I am interested in " + area_of_interest + ". Give me one random topic of which I can write an article. Give the topic in a sentence with no more than 20 words, ")
get_title = remove_empty_lines(get_title)
get_title = get_title.lstrip()
print("Title:" + get_title)

get_foldername = ai_query("I want to write an article on " + get_title + ". What folder should I choose? Give me a three word linked with an underscore for the folder name. Something very related to the article. ")
get_foldername = remove_empty_lines(get_foldername)
print("Folder: " + get_foldername)

get_category = ai_query("I want to write an article on " + get_title + ". What category should I choose? Give me a single word category. ")
get_category = remove_empty_lines(get_category)
get_category = capitalize_first_letter(get_category).replace(".", "")
print("Category: " + get_category)

get_tags = ai_query("I want to write an article on " + get_title + ". What tags should I choose? Give me a comma separated list of tags.")
get_tags = remove_empty_lines(get_tags)
get_tags = get_tags.lower()
print("Tags: " + get_tags)

get_sort = ai_query("I want to write an article on " + get_title + ". Giveme a small sentence about it that will have some joke in it. ")
get_sort = remove_empty_lines(get_sort)
get_sort = get_sort.lstrip()
print("Sort: " + get_sort)

get_article = ai_query("I need assistance in structuring an article on" + get_title +
                       " within a 1000-word limit using Markdown. Please provide an introduction and conclusion for the article, and break it down into three parts without explicitly labeling them as \"Act 1\", \"Act 2\", and \"Act 3\". Use Markdown to format the article, including headers and lists for each section. Keep the headers short and to the point. ")
# print(get_article)


image_resp = openai.Image.create(prompt="Realistic Image for an article that is related to :" + get_title, n=1, size="1024x1024")
image_url = image_resp["data"][0]["url"]
# print("Image URK:  " + image_url)

print("Generating Markdown file...")
# generate todays date for the article in the format of YYYY-MM-DD
date = datetime.datetime.now().strftime("%Y-%m-%d")
article = generate_markdown(get_title, date, get_category, get_tags, get_sort, get_article)
# print(article)


print("Saving Markdown file...")
make_folder(path + get_foldername.lower().replace(" ", "_"))
save_string_to_file(article, path + get_foldername.lower().replace(" ", "_") + "/" + "index.en.md")
download_image(image_url, path + get_foldername.lower().replace(" ", "_") + "/" + "featured-image.png")
