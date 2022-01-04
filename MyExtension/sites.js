//I consulted the mozilla topSites documentation to learn how to write this code
//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/topSites

function gotSites(sites) {
    var div = document.getElementById('sites');

    let ul = document.createElement('ul');
    for (let site of sites) {
      let li = document.createElement('li');
      let a = document.createElement('a');
      a.href = site.url;
      a.innerText = site.title || site.url;
      li.appendChild(a);
      ul.appendChild(li);
    }

    div.appendChild(ul);
}

var getSites = browser.topSites.get();
getSites.then(gotSites);
