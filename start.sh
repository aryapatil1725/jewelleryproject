#!/bin/bash
cd "jewellery project/jewellery project" || exit 1
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
gunicorn app:app --bind 0.0.0.0:$PORT
 +++++++ REPLACE
