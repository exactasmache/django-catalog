const API_SCHEME = 'http'
const API_HOST = 'localhost:8000'
const API_BASE = `api`
const API_URL = `${API_SCHEME}://${API_HOST}/${API_BASE}`
const API_list = 'list'

function retrieveList() {
    let listWrapper = document.getElementById("list-wrapper");
    let url = `${API_URL}/${API_list}/`

    fetch(url)
    .then(response => response.json())
    .then(data => {
      console.log("Data", data);
    });
};

retrieveList();
