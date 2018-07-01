WORKDIR=/home/justin.bell/chorewheel

. $WORKDIR/sendgrid.env
$WORKDIR/.env/bin/python $WORKDIR/main.py $WORKDIR/housemates.csv >> /tmp/chorewheel.log 2>&1
