# USAGE: The first argument is "dis" or "hw". The second argument is the number.
#
# This is a Python script that generates .tex content files from JSON files.
#
# 1. Read the JSON file, which contains a list of questions.
# 2. From a Jinja2 template, generate the .tex source file by inserting each question in an "\input{}" command.
# 3. Each template corresponds to one generated .tex file.

import sys
import json
import jinja2

template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(
  block_start_string = '\BLOCK{',
  block_end_string = '}',
  variable_start_string = '\VAR{',
  variable_end_string = '}',
  comment_start_string = '\#{',
  comment_end_string = '}',
  line_statement_prefix = '%%',
  line_comment_prefix = '%#',
  trim_blocks = True,
  autoescape = False,
  loader = template_loader
)

assignment_type = sys.argv[1]
number = sys.argv[2]
base_dir = f'src/{assignment_type}'

file_name = f'{base_dir}/{assignment_type}{number}.json'
with open(file_name, 'r') as data_file:
    data_dict = json.load(data_file)

problem_src = "src/problems"
data_dict['questions'] = map(lambda question : f'{problem_src}/{question}', data_dict['questions'])

# raw_questions reads the actual TeX file in order to generate the source TeX file. This is possible because the
# questions and solutions live in separate .tex files now.
def load_question(question):
    with open(f'{question}.tex', 'r') as f:
        return f.read()
raw_questions = map(load_question, data_dict['questions'])

# The suffixes refer to the templates, e.g. "-sol" corresponds to "template-sol.tex.jinja2". For each of the suffixes
# below, we generate a .tex file from a .tex.jinja2 template.
suffixes = ['', '-sol']
if assignment_type == 'hw' or assignment_type == 'practice':
  # For homeworks, we have another template to generate the raw TeX source file.
  suffixes.append('-raw')

for suffix in suffixes:
    file = f'{base_dir}/template{suffix}.tex.jinja2'
    template = template_env.get_template(file)

    # Pass in variables into the templates.
    content = template.render(
        questions=data_dict['questions'],
        raw=raw_questions,
        title=data_dict['title'],
        date=data_dict['date'],
    )

    output_file_name = f'{base_dir}/{assignment_type}{number}{suffix}.tex'
    with open(output_file_name, 'w') as output_file:
        output_file.write(content)

# This generates one .tex file per question in order to automatically generate images.
if assignment_type == 'hw':
    file = f'{base_dir}/template-img.tex.jinja2'
    template = template_env.get_template(file)

    counter = 1
    for question in data_dict['questions']:
        content = template.render(question=question)
        output_file_name = f'{base_dir}/{assignment_type}{number}-img{counter}.tex'
        with open(output_file_name, 'w') as output_file:
            output_file.write(content)

    counter += 1

# TODO:
# Make header and problem titles look like 170
# Incorporate stars for problems
