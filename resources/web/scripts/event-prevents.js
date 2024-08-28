/**
 * event-prevents.js
 * Listen to events that should be prevented such as WebView refreshing, context menus, and inspector.
 */

document.addEventListener('contextmenu', (event) => {
  event.preventDefault();
});

document.addEventListener('keydown', function (event) {
  if (event.ctrlKey && event.key === 'r') {
    event.preventDefault();
  }
  if (event.key === 'F5') {
    event.preventDefault();
  }
  if (event.key === 'F12') {
    event.preventDefault();
  }
});