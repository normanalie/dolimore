#!/bin/bash
source venv/bin/activate
flask db upgrade
exec waitress-serve --listen=*:5000 dolimore:app