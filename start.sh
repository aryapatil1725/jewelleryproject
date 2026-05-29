#!/bin/bash
cd "jewellery project/jewellery project" && gunicorn app:app --bind 0.0.0.0:$PORT