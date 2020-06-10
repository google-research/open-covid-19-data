// Copyright 2020 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

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
  spec.width = Math.floor(window.innerWidth * 0.95);
  spec.height = Math.floor(window.innerHeight * 0.75);
  // palette mapped to
  // statuses = ['NEEDED', 'NOT_AVAILABLE', 'PENDING', 'INCLUDED']
  const colors = ['#fdae6b', '#c6dbef', '#3182bd', '#08519c'];
  vega.scheme('custom', colors);
  const view = new vega.View(vega.parse(spec), {
    renderer: 'svg',
    container: '#view',
    hover: true,
    loader: vega.loader({target: '_blank'})
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
