async function get_page_info() {
  const response = await fetch('/get_page_info', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
  });
  const text = await response.text();
  try {
    const json = JSON.parse(text);
    return json;
  }
  catch (e) {
    return { title: "WebRemote" };
  }
}

async function macro_info_request(id) {
  const response = await fetch('/get_macro_info', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: "macro=" + id
  });
  const text = await response.text();
  try {
    const json = JSON.parse(text);
    return json;
  }
  catch (e) {
    return { name: "", color: "" };
  }
}

function macro_request(id) {
  fetch('/request', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'macro=' + id
  });
}

async function initPage() {

  const page_info = await get_page_info();
  document.title = page_info.title;
  const mainBody = document.getElementById("mainBody");
  mainBody.style.backgroundColor = page_info.background;

  // Now load button grid
  const buttonGrid = document.getElementById('buttonGrid');
  // Clear any existing content
  buttonGrid.innerHTML = '';

  const rows = page_info.rows;
  const cols = page_info.columns;
  // Create the grid of buttons
  for (let i = 0; i < rows; i++) {
    const row = document.createElement('div');
    row.classList.add('row');

    for (let j = 0; j < cols; j++) {
      const col = document.createElement('div');
      col.classList.add('col-sm', "d-flex", "justify-content-center"); // Adjust column width as needed
      const button = document.createElement('button');
      const button_index = `${j},${i}`;
      const json = await macro_info_request(button_index);

      button.classList.add('btn', 'btn-primary', 'square-btn');
      button.textContent = `${json.name}`;
      button.style.backgroundColor = (json.color == "" ? page_info.default_button_color : json.color);
      button.onclick = function () {
        macro_request(button_index);
      };

      col.appendChild(button);
      row.appendChild(col);
    }

    buttonGrid.appendChild(row);
  }
}