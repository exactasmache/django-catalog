# Django-catalog

Simple website that manages a database of books and authors using the latest stable version of Django and SQLite as a database.

- Every author has these attributes: first name, last name, date of birth.
- Every book has these attributes: title, date of publication, author.
- Books are categorized by keywords to facilitate navigation and discovery.
- The Django admin should be enabled, allowing you to manage books and authors.
- The frontend:
  - Shows a list of all the available books with their author, sorted by book title by default.
  - Allows searching by free text, matching by both book title and author. The search does not reload the whole page, only the results' area is updated.
  - Paginates the books list with 10 results per page.
  - Allows filtering and search books through the categorization system previously mentioned.
  - Has a recommendation system that for a given suggests similar books you may be interested in.

## Installation
Create a virtual environment and activate it:
```
python3 -m venv ./venv
. venv/bin/activate
```
Install _Django_, its _Rest-Framework_ and _Decouple_:
```
pip install Django djangorestframework python-decouple
```
Otherwise, you can install everything from the file _requirements.txt_
```
pip install -r requirements.txt
```
Create an _.env_ file and store the _SECRET KEY_:
```
echo SECRET_KEY = 'mySecretKey'" >> .env
echo "DEBUG = False" >> .env
```

## Usage

The server listen the _localhost:8000_ by default by executing the following commands:
```
cd src
python manage.py runserver
```

When started and whenever the _Search_ button is pressed with not input in the search field, the main window list all the books paginated with 10 results per page.
To see the details of a particular book just click on its row. The table is automatically filled by similar books. By clicking in the keywords, the system retrieves all books with those keywords.
