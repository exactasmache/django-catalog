/********************
 * Global variables *
 ********************/
const API_SCHEME = 'http';                                  // API scheme
const API_HOST = 'localhost:8000';                          // API host and port
const API_BASE = `api`;                                     // API basename
const API_URL = `${API_SCHEME}://${API_HOST}/${API_BASE}`;  // API baseUrl

const API_list = 'list';                                    // Endpoint that retrieves the
// list of books
const API_similars = 'similars';                            // Endpoint that retrieves the
// similar for a given book

const SEARCH_KEYWORD = 'search';                            // Keyword for the freetext search
const KEYWORDS_KEYWORD = 'keyword';                         // Keyword to search by keyword

/********************
 *     Functions    *
 ********************/

/**
 * Generates the html with the list of books.
 * 
 * @param {List} books 
 */
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
      <div id="book-row-${i}" class="book-wrapper book-pointer flex-wrapper">
        <div style="flex:3">
          <span id="book-title-${i}" class="book-pointer">${books[i].title}</span>
        </div>
        <div style="flex:3">
          <span id="book-author-${i}" class="book-pointer">${books[i].author}</span>
        </div>
        <div style="flex:1">
          <span id="book-date-${i}" class="book-pointer">${books[i].date_of_publication}</span>
        </div>
      </div>
    `;

    listWrapper.innerHTML += item;
  }

  for (i in books) {
    let book = document.getElementById(`book-row-${i}`);
    let id = books[i].id

    book.addEventListener('click', () => {
      let search_text = document.getElementById("search-input");
      search_text.value = '';
      setSelected(id);

      let url = `${API_URL}/${API_similars}/${id}`;
      retrieveListFrom(url);
    });
  }
}

/**
 * Shows the details for the book with id='id' by showing
 * an html into the div with id #selected-wrapper.
 * It also adds event listeners to the keywords in order
 * to allow searching by them.
 * 
 * @param {String} id : id of the selected book.
 */
async function setSelected(id) {
  let selected = document.getElementById('selected-wrapper');

  if (id == null) {
    selected.innerHTML = "";
    return;
  }

  let url = `${API_URL}/${API_list}/${id}`;
  let data;
  try {
    let response = await fetch(url);
    data = await response.json();
  } catch (error) {
    console.log(error);
    return;
  }

  if (data === undefined) return;

  innerHtml = `
    <h4 class="details-title">Book details</h4>
      <div class="book-wrapper flex-wrapper">
        <div style="flex:3">
          <p class="selected-header">Title</p>
          <p class="selected-header">${data.title}</p>
        </div>
        <div style="flex:2">
          <p class="selected-header">Author</p>
          <p>${data.author}</p>
        </div>
        <div style="flex:3">
          <p class="selected-header">Published in</p>
          <p>${data.date_of_publication}</p>
        </div>
        <div style="flex:4">
          <p class="selected-header">Keywords</p>
          <div id="book_keywords">
  `;

  keywords = data.keywords.split(', '); 
  for (k of keywords) {
    innerHtml += `<p id="keyword-${k}">${k}</p>`
  }

  innerHtml += `
          </div>
        </div>
      </div>
    <h7 class="suggestion-title">You may also be interested in...</h7>
  `;

  selected.innerHTML = innerHtml;

  for (k of keywords) {
    let key_html = document.getElementById(`keyword-${k}`);
    let k_url = `${API_URL}/${API_list}/?${KEYWORDS_KEYWORD}=${k}`;
    
    key_html.addEventListener('click', () => {
      retrieveListFrom(k_url)
    });
  }
}

/**
 * Adds functionality to the pagination buttons. When an 'url' is given, 
 * it adds a listener that handles the 'click' event calling the 
 * 'retriveListFrom' function with the url. When the 'url' is null, the 
 * button is disabled.
 * 
 * @param {Element} btn : Button to add the listener to.
 * @param {String} url  : String pointing to the next/previous page.
 */
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

/**
 * Renders and configures the pagination buttons in order to call the links
 * received as parameters. 
 * 
 * @param {String} prev_url : Link to previous page
 * @param {String} next_url : Link to next page
 */
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

/**
 * Renders the book list and configure the pagination buttons with the received
 * data and links.
 * 
 * @param {Object} results    : List of books as Jsons
 * @param {String} previous   : Link to previous page (or null)
 * @param {String} next       : Link to next page (or null)
 */
function configureContainer(results, previous, next) {
  renderBookList(results);
  renderPaginationButtons(previous, next);
}

/**
 * Generates the list with all the books for a given url.
 * 
 * @param {String} url : Endpoint that returns a list and two links (possible null).
 *                        
 */
function retrieveListFrom(url) {

  let response = fetch(url);

  response.catch(error => console.log(error));

  response
    .then(response => response.json())
    .then(data => {
      if (data === undefined) return;

      configureContainer(data.results, data.previous, data.next);
    })
    .catch(error => console.log(error));
};

/**
 * Adds an event listener to the search button. When clicked it asks the server
 * for the list of books that matches the entered text. If no text it retrieves
 * all the books.
 */
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
    setSelected(null);
  });
}

/******************
 * Event handlers *
 ******************/
/**
 * When the page is loaded it retrieves the list of all books and
 * configures dynamically the event handler for the search button.
 */
window.addEventListener('load', function () {
  let url = `${API_URL}/${API_list}`;
  retrieveListFrom(url);
  configureSearchButton();
});
