# ics2toodledo
Convert ICS files into ToodleDo CVS import files.

## Sample Call

The following call will convert all entries in the file `/some/dir/my_calendar.ics` into the CSV file
`/some/dir/toodledo.csv` which can be uploaded into Toodledo. All alarms will be shifted to the day before
(`--delta -1`) their respective events at 10 PM (`--due-time 22:00`). All events will be put into the folder `Private`
and be tagged with `Household`.

    icstoodleso.pl --folder Private \
                   --tag Household \
                   --priority high \
                   --due-time 22:00 \
                   --delta -1 \
                   /some/dir/my_calendar.ics \
                   /some/dir/toodledo.csv
                   

## Where To Obtain the ICS Files...

* Bonn, Germany:  https://www.bonnorange.de/abfuhrtermine.html

## Continuous Integration Status Overview

| Status | Master | 
|:------ |:------ |
| Snyk Vulnerability | <a href="https://snyk.io/test/github/marcus67/ics2toodledo?targetFile=requirements.txt"><img src="https://snyk.io/test/github/marcus67/ics2toodledo/badge.svg?targetFile=requirements.txt" alt="Known Vulnerabilities" data-canonical-src="https://snyk.io/test/github/marcus67/little_brother?targetFile=requirements.txt" style="max-width:100%;"></a>

Note: The vulnerability status is derived from the Python PIP packages found in `requirement.txt` which is in itself
is generated from `pip3 freeze`.
