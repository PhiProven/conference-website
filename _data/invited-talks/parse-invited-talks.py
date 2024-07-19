import csv
import os.path
import re
import sys
import urllib.request


csv_filename = 'Wormshop 7th Edition Invited Speakers - Sheet1.csv'
sheet_export_url = 'https://docs.google.com/spreadsheets/d/1DtVh5k8sN_gMZaYPgJ-LFFapAP1z7knAh3swxIEaGtQ/export?format=csv&id=1DtVh5k8sN_gMZaYPgJ-LFFapAP1z7knAh3swxIEaGtQ&gid=0'


def prompt_choice(prompt_string, default_yes=True, exit_on_no=False):
    choice_string = "[Y/n]" if default_yes else "[y/N]"
    print(prompt_string, choice_string, end='\t')
    answer = input()
    if (answer == '' and default_yes) or answer.lower() == 'y':
        return True
    else:
        if exit_on_no:
            sys.exit(0)
        else:
            return False

def main():
    if prompt_choice("Download sheet?", default_yes=False):
        download_google_sheet()
    if prompt_choice("Print list of speakers for front page?", default_yes=False):
        csv_to_invited_speakers_list(prefix='  - ')
    if prompt_choice("Export to _speakers/?", default_yes=False):
        csv_to_speakers()
    if prompt_choice("Export to _talks/?", default_yes=False):
        csv_to_talks()


def download_google_sheet():
    print("Downloading...")
    try:
        urllib.request.urlretrieve(sheet_export_url, csv_filename)
        print("Done!")
    except Exception as err:
        print("Could not export sheet!")
        print(err)


def csv_to_invited_speakers_list(prefix=''):
    with open(csv_filename) as csvfile:
        invited_reader = csv.DictReader(csvfile)
        invited = list(invited_reader)

        for speaker in invited:
            speaker_string = prefix
            if speaker['Website'] == 'N/A':
                speaker_string += speaker['Name']
            else:
                speaker_string += "[{Name}]({Website} \"{Name}\")".format(**speaker)
            if speaker['Tutorial?'] == 'Yes':
                speaker_string += " (Tutorial)"
            speaker['string'] = speaker_string

        for speaker in sorted(invited, key=lambda x: get_name_transliteration(x['Last name'])):
            # print(get_name_transliteration(speaker['Last name']))
            print(speaker['string'])


def csv_to_speakers():
    with open(csv_filename) as csvfile:
        invited_reader = csv.DictReader(csvfile)
        invited = list(invited_reader)

        for speaker in invited:
            speaker_md = '\n'.join([
                "---",
                "name: {Name}",
                "first_name: {First name}",
                "last_name: {Last name}"
            ])
            if speaker['Website'] != 'N/A':
                speaker_md = '\n'.join([speaker_md] + [
                    "links:",
                    "  - name: Website",
                    "    absolute_url: {Website}",
                    "    icon: house-user",
                ])
            speaker_md = '\n'.join([speaker_md] + [
                "---",
                ""
            ])

            speaker_md = speaker_md.format(**speaker)
            filename_speaker_md = get_valid_filename(speaker['Name']) + '.md'
            filename_speaker_md = filename_speaker_md.lower()

            with open('../../_speakers/invited/' + filename_speaker_md, 'w') as speaker_file:
                speaker_file.write(speaker_md)


def csv_to_talks():
    with open(csv_filename) as csvfile:
        invited_reader = csv.DictReader(csvfile)
        invited = list(invited_reader)

        for speaker in invited:
            talk_md = '\n'.join([
                "---",
                "name: {Title}",
                "speakers:",
                "  - {Name}",
                "categories:",
                "  - Invited Talks",
            ])
            if speaker['Tutorial?'] == "Yes":
                talk_md = '\n'.join([talk_md] + [
                    "  - Tutorials"
                ])
            talk_md = '\n'.join([talk_md] + [
                "katex: true",
            ])
            if '$' in speaker['Title']:
                talk_md = '\n'.join([talk_md] + [
                    "mathjax: true",
                ])
            talk_md = '\n'.join([talk_md] + [
                "---",
                ""
            ])

            if speaker['Title'] == "":
                speaker['Title'] = "(To Be Announced)"
                # speaker['Title'] = "\"TBA: invited talk by " + speaker['Name'] + "\""

            talk_md = talk_md.format(**speaker)

            if speaker['Abstract'] != "":
                if os.path.isfile(speaker['Abstract']):
                    with open(speaker['Abstract'], 'r') as abstract_md:
                        abstract = abstract_md.read()
                        talk_md += "\n" + abstract + "\n"
                else:
                    print("File does not exist!", speaker['Abstract'])

            filename_talk_md = "invited-" + get_valid_filename(speaker['Name']) + '.md'
            filename_talk_md = filename_talk_md.lower()

            with open('../../_talks/invited/' + filename_talk_md, 'w') as talk_file:
                talk_file.write(talk_md)


# See: https://github.com/django/django/blob/main/django/utils/text.py
def get_valid_filename(name):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "", s)
    if s in {"", ".", ".."}:
        raise SuspiciousFileOperation("Could not derive file name from '%s'" % name)
    return s


# See: https://stackoverflow.com/questions/70683722/convert-non-standard-latin-characters-in-a-string-to-standard-ones
def get_name_transliteration(name):
    table = str.maketrans("ł", "l")
    formatted_name = name.lower().translate(table)
    return formatted_name


if __name__ == '__main__':
    main()
