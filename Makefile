ENV := env

.PHONY: env
env:
	virtualenv $(ENV)
	$(ENV)/bin/pip install -U -r pip.requirements

clean:
	rm -rf $(ENV)

IMG_NAME := sample-scraper

docker-build:
	docker build -t $(IMG_NAME) .

docker-run:
	docker run --rm -t -i $(IMG_NAME)

docker-run-custom:
	docker run --rm -t -i $(IMG_NAME) \
	    -v \
	    https://www.jcrew.com/ru/womens_category/shirtsandtops.jsp \
	    https://www.jcrew.com/ru/womens_category/shirtsandtops/topsblouses/PRDOVR~F2728/F2728.jsp \
	    https://www.ulmart.ru/catalog/communicators \
	    https://www.ulmart.ru/goods/3851637 \
	    "https://www.amazon.com/New-Used-Textbooks-Books/b/ref=sv_b_5?ie=UTF8&node=465600" \
	    "https://www.amazon.com/Effective-Java-2nd-Joshua-Bloch/dp/0321356683/ref=pd_bxgy_14_img_3"
