# Simple scraper

Could be run either with docker or locally with python


## Using Docker

Build

    make build-docker

Run

    docker run --rm -t -i sample-scraper \
        https://www.jcrew.com/ru/womens_category/shirtsandtops/topsblouses/PRDOVR~F2728/F2728.jsp

or

    make docker-run-custom

## Using local Python

Requirements

* python 2.7
* lxml

Build

    make env

Run

    source env/bin/activate
    ./src/runner.py -v https://www.jcrew.com/ru/womens_category/shirtsandtops/topsblouses/PRDOVR~F2728/F2728.jsp
