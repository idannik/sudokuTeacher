/* Project specific Javascript goes here. */
"use strict";

document.addEventListener("DOMContentLoaded", function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    window.focus_cell = {
        index: -1,
        row: -1,
        col: -1
    };

    const query_soduko_cell = (id, square, cell) => {
        return document.querySelector(`div.square:nth-child(${square}) > div:nth-child(${cell})`);
    }

    const get_cell_according_to_row_and_col = (row, col, id) => {
        const square = Math.floor(row / 3) * 3 + Math.floor(col / 3) + 1
        const cell = (row % 3) * 3 + col % 3 + 1
        return query_soduko_cell(id, square, cell)
    }

    const no_focus_on_cell = () => {
        return window.focus_cell.index === -1 && window.focus_cell.row === -1 && window.focus_cell.col === -1
    }

    const get_focus_cell = () => {
        return get_cell_according_to_row_and_col(window.focus_cell.row, window.focus_cell.col, window.focus_cell.index)
    };

    const unfocus_old_cell = () => {
        if (no_focus_on_cell()) {
            return
        }

        let div = get_focus_cell()
        if (div) {
            div.style.backgroundColor = ""
        }
        focus_cell.index = -1
        focus_cell.row = -1
        focus_cell.col = -1
    };


    const set_div_pencil_mode = (div, pencil_mode) => {
        if (div.pencil_mode !== pencil_mode) {
            div.textContent = ""
        }
        div.pencil_mode = pencil_mode;
        let color = 'moccasin'
        let fontSize = ''
        let fontWeight = ''
        if (div.pencil_mode) {
            color = 'paleturquoise'
            fontSize = '175%'
            fontWeight = 'bold'
        }
        div.style.backgroundColor = color
        div.style.fontSize = fontSize
        div.style.fontWeight = fontWeight
    }

    const init_cell_on_click = () => {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                let div = get_cell_according_to_row_and_col(i, j, 0)
                if (div) {
                    div.onclick = (event) => {
                        if (!event.target.disabled) {
                            unfocus_old_cell()
                            window.focus_cell.index = 0;
                            window.focus_cell.row = i;
                            window.focus_cell.col = j;

                            set_div_pencil_mode(event.target, event.altKey);
                        }
                    }
                    div.onkeypress = (event) => {
                        let target = event.target
                        if (!target.disabled) {
                            if (event.key >= 1 && event.key <= 9) {
                                const key = event.key
                                if (target.pencil_mode) {
                                    const numbers = target.textContent.split(" ")
                                    const idx = numbers.findIndex(x => x === key)
                                    if (idx === -1) {
                                        numbers.push(key)
                                        numbers.sort()
                                    } else {
                                        numbers.splice(idx, 1)
                                    }
                                    target.textContent = numbers.join(" ")
                                } else {
                                    target.textContent = event.key
                                }
                            }
                        }
                    }

                }
            }
        }
    }
    init_cell_on_click()


    function get_board() {
        let board = []
        for (let id = 0; id < 1; id++) {
            for (let i = 0; i < 9; i++) {
                let row = []
                for (let j = 0; j < 9; j++) {
                    let div = get_cell_according_to_row_and_col(i, j, id)
                    let val = div.textContent
                    if (val === '' || div.pencil_mode) {
                        row[j] = 0
                    } else {
                        row[j] = parseInt(val)
                    }

                }
                board[i] = row
            }
        }
        return board;
    }

    document.querySelector("#fill-pencil-marks-btn").onclick = function () {
        let board = get_board();
        fetch_for_django("#fill-pencil-marks-btn", {"board" : board})
    }

    document.querySelector("#suggest-btn").onclick = function () {
        let board = get_board();
        fetch_for_django("#suggest-btn", {"board" : board})
    }
    const stripTrailingSlash = (str) => {
        return str.endsWith('/') ?
            str.slice(0, -1) :
            str;
    };

    function get_url_for_fetch(selector) {
        const data_url = document.querySelector(selector).attributes['data-url']
        return new URL(stripTrailingSlash(data_url.baseURI) + data_url.value);
    }

    async function fetch_for_django(selector, data={}) {
        let url = get_url_for_fetch(selector);
        const request = new Request(
            url,
            {headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/json'}}
        );
        const json = await fetch(request, {
            body: JSON.stringify(data),
            method: 'POST',
            mode: 'same-origin'  // Do not send CSRF token to another domain.
        }).then(res => res.json());
        update_board(json)
    }

    document.querySelector("#load-btn").onclick = async function () {
        await fetch_for_django("#load-btn");
    }


    const update_board = (message) => {
        const board = message['board']
        const id = message["id"]
        const pencil_marks = message['pencil_marks']
        console.log(pencil_marks)
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                let div = get_cell_according_to_row_and_col(i, j, id)
                if (div) {
                    if (board[i][j] > 0) {
                        set_div_pencil_mode(div, false)
                        div.textContent = board[i][j]
                        div.disabled = true
                        div.style.backgroundColor = "lightgray"
                        div.pencil_mode = false
                    } else {
                        div.textContent = ""
                        div.disabled = false
                        if (pencil_marks && pencil_marks[i][j]) {
                            set_div_pencil_mode(div, true)
                            let numbers = pencil_marks[i][j]
                            console.log(numbers)
                            numbers.sort()
                            div.textContent = numbers.join(" ")
                        } else {
                            div.pencil_mode = false
                        }
                        div.style.backgroundColor = ''
                    }

                }

            }
        }
    };
});
