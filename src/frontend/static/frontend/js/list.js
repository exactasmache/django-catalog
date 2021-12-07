/********************
 * Global variables *
 ********************/
const API_SCHEME = 'http';
const API_HOST = 'localhost:8000';
const API_BASE = `api`;
const API_URL = `${API_SCHEME}://${API_HOST}/${API_BASE}`;
const API_list = 'list';

const BOOKS_PER_PAGE = 3;


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


function renderButtons(prev_url, next_url) {
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

      renderBookList(data.results);
      renderButtons(data.previous, data.next);
    });
};


/******************
 * Event handlers *
 ******************/
window.addEventListener('load', function () {
  let url = `${API_URL}/${API_list}/all`;
  retrieveListFrom(url);
});
