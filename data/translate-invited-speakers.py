import csv

csv_filename = 'Wormshop 7th Edition Invited Speakers - Sheet1.csv'

def main():
    with open(csv_filename) as csvfile:
        invited = csv.DictReader(csvfile)

        # get the labels on the columns

        # iterate:
        #   construct a string for speakers
        #   convert to valid filename
        #   save to _speakers/...

        # iterate:
        #   construct a string for talks
        #   convert to valid filename invited-???
        #   save to _talks/...


if __name__ == '__main__':
    main()
