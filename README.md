# django-catalog

Simple website that manages a database of books and authors using the latest stable version of Django and SQLite as a database.

- Every author has these attributes: first name, last name, date of birth.
- Every book has these attributes: title, date of publication, author.
- Books need to be categorized somehow to facilitate navigation and discovery.
- The Django admin should be enabled, allowing you to manage books and authors.
- The frontend:
  - Shows a list of all the available books with their author, sorted by book title by default.
  - Allows to search by freetext, matching by both book title and author. The search should not reload the whole page, only the results area should be updated.
  - Paginates the books list with 10 results per page.
  - Allows to filter and search books through the categorization system previously mentioned.
  - Has a recommendation system that for a given suggests similar books you may be interested in.
