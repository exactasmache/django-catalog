const API_SCHEME = 'http';
const API_HOST = 'localhost:8000';
const API_BASE = `api`;
const API_URL = `${API_SCHEME}://${API_HOST}/${API_BASE}`;
const API_list = 'list';

/**
 * Generate the list with all the books.
 * TODO: Use pagination.
 */
function retrieveList() {
    let listWrapper = document.getElementById("list-wrapper");
    let url = `${API_URL}/${API_list}/all`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
      let books = data.results;
      console.log(books);
      listWrapper.innerHTML += 
      `<div id="books-header" class="book-header-wrapper flex-wrapper">
        <div style="flex:3">
          <span class="books-header"">Title</span>
        </div>
        <div style="flex:3">
          <span class="books-header">Author</span>
        </div>
        <div style="flex:1">
          <span class="books-header">Publication date</span>
        </div>
      </div>`;

      for (i in books) {
        let item = `
          <div id="book-row-${i}" class="book-wrapper flex-wrapper">
            <div style="flex:3">
              <span class="book-title">${books[i].title}</span>
            </div>
            <div style="flex:3">
              <span class="book-title">${books[i].author}</span>
            </div>
            <div style="flex:1">
              <span class="book-title">${books[i].date_of_publication}</span>
            </div>
          </div>
        `;

        listWrapper.innerHTML += item;
      }
    });
};

window.addEventListener('load', function () {
  retrieveList();
});
