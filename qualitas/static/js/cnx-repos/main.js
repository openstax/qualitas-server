

const repo = 'openstax/tutor-js';

const tags_url = 'https://api.github.com/repos/' + repo + '/tags';


function appendVersionLink(el, versionNum, url){
  let link = document.createElement('');
  link.innerHTML = versionNum;
  link.setAttribute('target', '_blank');
  link.setAttribute('href', url);
  document.getElementById(el).appendChild(link);
}

function makeXHR(url, method) {


}

function updateTagsAndPyPi() {
  let repos = [
    'Connexions//webview'
  ]


}
