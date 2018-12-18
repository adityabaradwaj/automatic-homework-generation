# Automatic Content Generation Repository

This repository's purpose is to make document generation easier for CS170 staff. This includes homeworks, discussion worksheets, practice worksheets (for practice exams or guerilla sections) and exams. At a high level, here is how the process works:
- The `src` folder contains the LaTeX files for the problems and solutions. This is where you will add new problems.
- You can specify the problems you want to put on a homework/worksheet using a JSON file. You can also specify things like title/due date/etc here.
- The `Makefile` organizes various scripts that are used to cut-and-paste the relevant LaTeX files into a single file, and render that file as a PDF using `pdflatex`.

# Acknowledgements

This is a modified version of the `materials` repo originally created by Alvin Wan and Sinho Chewi for CS 70's materials. The Makefile and much of the documentation remains intact from the old version. This repo was adapted for CS 170 and CS 188 by Aditya Baradwaj. Changes in this version include:
- Rewriting `generate.py` in Python, in order to remove the dependence on Ruby, as well as to make the repo easier to understand and edit for new TAs (who are likely more familar with Python). Jinja2 replaces Erubis as the templating package used.
- Addition of the `make publish` function, which allows staff to automatically post homework threads to Piazza. The `publish.py` script uploads the generated homework images to Imgur, and uses the unofficial Piazza API to post them.
- The `.sty` files and template files have been modified to fit CS 170's LaTeX style for homework and discussion.


# Installation

Clone the repository.

```
git clone https://github.com/Berkeley-CS170/course-materials.git
```

Check if you have TeX installed.

```
tex --version
```

If not, install TeX [from source](https://www.tug.org/begin.html), **OR** by running the following to install Homebrew and then install TeX using it.

```
brew install tex
```

You will also need Python >=3.6 installed. The `generate.py` script uses f-strings, and it will not work with any Python version before 3.6. In addition, you will need to install the Jinja2 package for Python:

```
pip install Jinja2
```

# How to Use

All commands are available via `make`. If for some reason, `make` is not installed on your OS, check the `Makefile` for the bash commands.

## Creating Documents

We support a workflow which produces the `.tex` files from templates. The templates are located at `src/[category]/template.tex.jinja2` and `src/[category]/template-sol.tex.jinja2`. In order to make the actual documents, the only documents you need to edit are: a JSON file containing the data for a document, and the `.tex` files for the problems themselves. If at any point you find that you require some Latex package or wish to define your own commands/environments, include those in `cs170.sty`.

Here, we will create a new document of the form `[category][num]`. This may be a discussion or homework; for simplicity, let us consider a document `dis03b`.

First, navigate to `src/dis/`, and make a file called `dis03b.json`.

```
cd src/dis
touch dis03b.json
```

Open up `dis03b.json` using a text editor of your choice. If you are unfamiliar with JSON format, don't worry: the basics are simple. Here is an example:

```
{
  "questions": [
    "asymptoticnotation/analyze-running-time"
  ],
  "title": "DIS 01"
}
```

The fields are documented below:
* `questions`: A comma-separated list of the problems, found in the directory `src/problems`.
* `title`: This will appear in the header of the document.

Browse through problems in `src/problems/`, and add problems to the `questions` field.

## Adding Questions

The question file starts with the command `\question`. You are free to include whatever you want afterwards. Example:

```
\question{Algorithm Design}

Design an algorithm to...
```

The solution file should be wrapped in the `solution` environment. Example:

```
\begin{solution}

The algorithm proceeeds by...

\end{solution}
```

The templating engine assumes that solutions are wrapped in the `\begin{solution} ... \end{solution}` environment. If this is not the case, you will have to reformat the problems in that way in order for it to work.

Also, you can use the following environment for first-level subparts of a problem:
```
\begin{subparts}
\subpart Part 1
\subpart Part 2
end{subparts}
```


## Rendering Document

First, navigate to the root directory of this repo. In other words `pwd` should end with `/Berkeley-CS70`.

Then, to render an assignment, use `make [category] n=[number]`.
The following are valid categories:

- `dis`
- `hw`
- `practice`

For example, to make Discussion 3, use

```
make dis n=03
```

> **Note**: We have not yet run sanity checks against all of the LaTeX files. Some of them may contain random `\fi`s, misplaced curly braces, undefined control sequences, or otherwise incorrect syntax. Common mishaps include:
>
> - misplaced: `\fi`s, without an `\ifsolution` (remove both)
> - undefined: `\qitem`, which should be renamed to `\Part`
> - extra: `\end{enumerate}` or `\end{document}`
>
> Additionally, some files may contain multiple `\Question`s. This occurs when two problems are given the same title, to let us resolve duplicates easier. If they are the same, feel free to delete one copy. If they are different, feel free to split them up into multiple files.

This will create two PDF files:

- `rendered/dis03/dis03b.pdf`
- `rendered/dis03/dis03b-sol.pdf`

What's going on when you run the command?
- First, the Ruby script `generate.rb` is run to generate the `.tex` files from the JSON data file, along with the embedded Ruby template files (files ending with `.tex.jinja2`). (After rendering, you should find the generated `.tex` files in `src/[category]`.
- Then, the generated `.tex` files are compiled into `.pdf` files, and dumped into the `rendered` directory.

## Viewing Problems

What if you want to view all of the problems in the repository? Run:

    python3 update-directory.py
    make practice n=0

This will generate a (massive) PDF document containing all of the problems in the repository. If you would like to limit the PDF file to only include certain directories, such as `asymptoticnotation` and `divideandconquer`, run:

    python3 update-directory.py asymptoticnotation divideandconquer
    make practice n=0

## Generating Image Files

After running `make hw n=[number]` as above, the command `make img n=[number]` will generate PNG image files, also in the `rendered` directory. To use this feature, you must have ImageMagick installed (see the requirements above).

## Posting to Piazza

After making the image files, you can post to Piazza. Make sure to first set the configuration in `config.json`. Following that, you can type `make publish n=[number] test=true` to post to the `test_nid` Piazza defined in `config.json`. To post to `client_id` Piazza, run `make publish n=[number] test=false`.

# Why Templating?

This problem creation setup solves a few problems that were present in the old workflow.

The most important feature is separation of problems into dedicated problem files. Before this, our worksheets were primarily created by copy-pasting latex code from previous semesters' worksheets. Not only does this lead to unnecessary code duplication, it is also more tedious and prone to errors with package imports/command definitions/etc. 

By creating problem and solution templates and forcing the user to create worksheets using a JSON file, we end up reducing things like ad-hoc command/enviroment definitions getting placed in the worksheet's latex file. These kinds of temporary fixes build up over time, and end up leaving a lot of dead code (just look at any of our past HW or discussion worksheets). With this setup, the only way to import packages or define new commands is through the `cs170.sty` file, which puts all the important stuff in one well-organized place.
