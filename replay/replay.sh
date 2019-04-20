#!/bin/bash
export PGHOST=prod-redshift-migrate.cwziypt8qrao.us-west-2.redshift.amazonaws.com
export PGPORT=5439
export PGUSER=clicktripz
export PGPASSWORD=kpdI2u3SWwIyx7vB
export PGDATABASE=analytics

./SimpleReplay.sh ordered
#psql -f 20190418/analytics-lambda-loader-29552.sql
