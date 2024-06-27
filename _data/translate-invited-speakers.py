import csv
import re


csv_filename = 'Wormshop 7th Edition Invited Speakers - Sheet1.csv'

def main():
    csv_to_invited_speakers_list()


def csv_to_invited_speakers_list():
    with open(csv_filename) as csvfile:
        invited_reader = csv.DictReader(csvfile)
        invited = list(invited_reader)

        for speaker in invited:
            speaker_string = ""
            if speaker['Website'] == 'N/A':
                speaker_string = speaker['Name']
            else:
                speaker_string = "[{Name}]({Website} \"{Name}\")".format(**speaker)
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
                    "    absolute_url: {Website}"
                ])
            speaker_md = '\n'.join([speaker_md] + [
                "---",
                ""
            ])

            speaker_md = speaker_md.format(**speaker)
            filename_speaker_md = get_valid_filename(speaker['Name']) + '.md'
            filename_speaker_md = filename_speaker_md.lower()

            with open('../_speakers/' + filename_speaker_md, 'w') as speaker_file:
                speaker_file.write(speaker_md)

        for speaker in invited:
            talk_md = '\n'.join([
                "---",
                # "name: {Title}",
                "name: Talk by {Name}",
                "speakers:",
                "  - {Name}",
                "categories:",
                "  - Invited Talks"
            ])
            if speaker['Tutorial?'] == "Yes":
                talk_md = '\n'.join([talk_md] + [
                    "  - Tutorials"
                ])
            talk_md = '\n'.join([talk_md] + [
                "---",
                ""
            ])

            talk_md = talk_md.format(**speaker)
            filename_talk_md = "Invited-" + get_valid_filename(speaker['Name']) + '.md'
            filename_talk_md = filename_talk_md.lower()

            with open('../_talks/' + filename_talk_md, 'w') as talk_file:
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
