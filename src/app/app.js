/* eslint-disable require-jsdoc */

function showPipeline() {
  console.log('show pipeline');
  document.querySelector('#map').setAttribute('style', 'display:none');
  document.querySelector('#pipeline').removeAttribute('style');
  document
    .querySelectorAll('nav button')
    .forEach(e => e.classList.remove('active'));
  document
    .querySelector('nav button[route="pipeline"]')
    .classList.add('active');
}

function showMap() {
  console.log('show map');
  document.querySelector('#pipeline').setAttribute('style', 'display:none');
  document.querySelector('#map').removeAttribute('style');
  document
    .querySelectorAll('nav button')
    .forEach(e => e.classList.remove('active'));
  document.querySelector('nav button[route="map"]').classList.add('active');
}

function render(spec) {
  // palette mapped to
  // statuses = ['NEEDED', 'NOT_AVAILABLE', 'PENDING', 'INCLUDED']
  // const colors = ['#feedde', '#fdd0a2', '#fd8d3c', '#a63603'];
  const colors = ['#fdae6b', '#c6dbef', '#3182bd', '#08519c'];
  vega.scheme('custom', colors);
  const view = new vega.View(vega.parse(spec), {
    renderer: 'svg',
    container: '#view',
    hover: true,
  });
  return view.runAsync();
}

function initialize() {
  fetch('/spec.json')
    .then(res => res.json())
    .then(spec => render(spec))
    .catch(err => console.error(err));
}

document.addEventListener('DOMContentLoaded', initialize);
