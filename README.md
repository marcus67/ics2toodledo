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
                   

## Where to the ICS Files...

* Bonn, Germany:  https://www.bonnorange.de/abfuhrtermine.html