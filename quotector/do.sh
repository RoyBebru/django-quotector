#!/usr/bin/sh

SCRIPT_NAME="$(/usr/bin/basename $0)"
SCRIPT_DIR="$(/usr/bin/dirname $0)"

[ -x "$SCRIPT_DIR/mange.py" ] && echo "Absent executable file '$SCRIPT_DIR/manage.py'" > /dev/stderr && exit 1

PART=${SCRIPT_NAME%.sh}

ARGS=
while [ "$PART" != "do" -a -n "$PART" ]; do
    PARG=${PART##*.}
    PART=${PART%.*}
    ARGS="$PARG $ARGS"
done

./manage.py $ARGS
