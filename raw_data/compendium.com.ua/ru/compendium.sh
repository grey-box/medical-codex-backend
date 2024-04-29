#!/bin/bash

scrapy runspider compendium.py -o compendium.xml
scrapy runspider compendium.py -o compendium.json
