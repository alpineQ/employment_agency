let bgItems = document.querySelectorAll('.bg-light')
let textItems = document.querySelectorAll('.text-dark')
let listGroupItems = document.querySelectorAll('.list-group-item-light')
let tableItems = document.querySelectorAll('.table-light')
let darkTheme = false

var checkRequest = new XMLHttpRequest()
checkRequest.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    if (JSON.parse(checkRequest.responseText)['dark_theme']) {
      recolorPage()
    }
  }
}
checkRequest.open('GET', '/theme/', true)
checkRequest.send()

function recolorPage() {
  if (darkTheme) {
    for (let i = 0; i < bgItems.length; i++) {
      bgItems[i].classList.replace('bg-dark', 'bg-light')
    }
    for (let i = 0; i < textItems.length; i++) {
      textItems[i].classList.replace('text-light', 'text-dark')
    }
    for (let i = 0; i < listGroupItems.length; i++) {
      listGroupItems[i].classList.replace('list-group-item-dark', 'list-group-item-light')
    }
    for (let i = 0; i < tableItems.length; i++) {
      tableItems[i].classList.replace('table-dark', 'table-light')
    }
    darkTheme = false
  } else {
    for (let i = 0; i < bgItems.length; i++) {
      bgItems[i].classList.replace('bg-light', 'bg-dark')
    }
    for (let i = 0; i < textItems.length; i++) {
      textItems[i].classList.replace('text-dark', 'text-light')
    }
    for (let i = 0; i < listGroupItems.length; i++) {
      listGroupItems[i].classList.replace('list-group-item-light', 'list-group-item-dark')
    }
    for (let i = 0; i < tableItems.length; i++) {
      tableItems[i].classList.replace('table-light', 'table-dark')
    }
    darkTheme = true
  }
  document.getElementById('switch-theme').checked = darkTheme
}

function switchTheme() {
  recolorPage()
  var changeRequest = new XMLHttpRequest();
  changeRequest.open("POST", '/theme/', true);
  changeRequest.send('');
}
