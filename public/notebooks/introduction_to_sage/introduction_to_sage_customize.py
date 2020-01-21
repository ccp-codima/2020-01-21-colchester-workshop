#!/usr/bin/env python3
"""
Interactive script to customize the Introduction to Sage notebooks to a
specific workshop.

This takes the workshop title, location, and instructor name(s) as well as URLs
for each, and fills that information into the heading of each of the tutorial
notebooks.
"""

import glob
import json
import sys


NOTEBOOK_PATTERN = 'introduction_to_sage_*.ipynb'


def ask_yesno(question):
    question = question.rstrip(' ?')
    question += ' [(y)es/(n)o]? '
    while True:
        ans = input(question).lower()
        if ans.startswith('y'):
            return True
        elif ans.startswith('n'):
            return False


def dict_slice(d, *keys):
    return tuple(d[k] for k in keys)


def format_instructors(instructors):
    return ', '.join(f"[{ins['name']}]({ins['url']})"
                     for ins in instructors)


def summarize(context):
    workshop, location, instructors = dict_slice(context,
            'workshop', 'location', 'instructors')
    summary = (f"[{workshop['name']}]({workshop['url']})\n"
               f"[{location['name']}]({location['url']})\n"
               f"Instructors: {format_instructors(instructors)}")
    print()
    print(summary)
    print()
    return ask_yesno('Is the previous information correct')


def format_notebook(notebook, context):
    heading = notebook['cells'][0]
    lines = heading['source']

    for idx, line in enumerate(lines):
        lines[idx] = line.format(**context)


def format_notebooks(context):
    context = context.copy()
    context['instructors'] = format_instructors(context['instructors'])
    for filename in glob.glob(NOTEBOOK_PATTERN):
        with open(filename) as fp:
            notebook = json.load(fp)

        # Modifies the JSON in-place
        format_notebook(notebook, context)

        with open(filename, 'w') as fp:
            json.dump(notebook, fp, sort_keys=True, indent=1)
            # The notebooks usually seem to have a trailing newline which
            # json.dump doesn't add by default
            fp.write('\n')


def gather():
    workshop = {}
    workshop['name'] = input('Workshop name: ')
    workshop['url'] = input('Workshop URL: ')

    location = {}
    location['name'] = input('Workshop location: ')
    location['url'] = input('Workshop location URL: ')

    instructors = []
    while True:
        instructor = {}
        instructor['name'] = input('Instructor name: ')
        instructor['url'] = input('Instructor URL: ')
        instructors.append(instructor)
        if not ask_yesno('Add another instructor'):
            break

    return {
        'workshop': workshop,
        'location': location,
        'instructors': instructors
    }


def main():
    while True:
        context = gather()

        if summarize(context):
            format_notebooks(context)
            return


if __name__ == '__main__':
    sys.exit(main())
