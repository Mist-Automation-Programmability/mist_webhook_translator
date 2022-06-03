#!/bin/bash

cd src_angular/
ng build --deploy-url static/
rm ../src/static/*.js
cp dist/webhook-translator/* ../src/static
cp dist/webhook-translator/index.html ../src/templates
cd ..