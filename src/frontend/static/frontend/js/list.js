/********************
 * Global variables *
 ********************/
const API_SCHEME = 'http';
const API_HOST = 'localhost:8000';
const API_BASE = `api`;
const API_URL = `${API_SCHEME}://${API_HOST}/${API_BASE}`;
const API_list = 'list';

const BOOKS_PER_PAGE = 3;
const SEARCH_KEYWORD = 'search'


/********************
 *     Functions    *
 ********************/

function renderBookList(books) {
  let listWrapper = document.getElementById("list-wrapper");

  listWrapper.innerHTML =
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
}


function setBtnUrl(btn, url) {
  if (url != null) {
    btn.addEventListener('click', () => retrieveListFrom(url));
    btn.disabled = false;
    btn.classList.add('btn-primary');
  } else {
    btn.disabled = true;
    btn.classList.add('btn-secondary');
  }
}


function renderPaginationButtons(prev_url, next_url) {
  let btnsWrapper = document.getElementById("pagination-wrapper");
  let buttons = `
    <button id="pag-prev">&laquo; Previous</button>
    <button id="pag-next">Next &raquo;</button>
  `;
  btnsWrapper.innerHTML = buttons;

  let prev_btn = document.getElementById("pag-prev");
  let next_btn = document.getElementById("pag-next");

  setBtnUrl(prev_btn, prev_url);
  setBtnUrl(next_btn, next_url);
}


function configureContainer(data) {
  renderBookList(data.results);
  renderPaginationButtons(data.previous, data.next);
}

/**
 * Generate the list with all the books.
 */
function retrieveListFrom(url) {

  let response = fetch(url);

  response.catch(error => console.log(error));

  response
    .then(response => response.json())
    .then(data => {
      if (data === undefined) return;

      configureContainer(data);
    });
};


function configureSearchButton() {
  let search_btn = document.getElementById("search-btn");
  let search_text = document.getElementById("search-input");

  search_btn.addEventListener('click', () => {
    let url = `${API_URL}/${API_list}`;
    if (search_btn.value == null) {
      retrieveListFrom(url);
    } else {
      url += `/?${SEARCH_KEYWORD}=${search_text.value}`;
      retrieveListFrom(url);
    }
  });
}

/******************
 * Event handlers *
 ******************/
window.addEventListener('load', function () {
  let url = `${API_URL}/${API_list}`;
  retrieveListFrom(url);
  configureSearchButton();
});
