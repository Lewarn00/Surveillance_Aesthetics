//I consulted the mozilla history documentation to learn how to write this code
//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/history/getVisits

function gotVisits(visits) {
  var div = document.getElementById('visits');
  let h = document.createElement('h3');
  let content = document.createTextNode("You have visited this site " + visits.length + " times");
  h.appendChild(content);
  div.appendChild(h);
  let p = document.createElement('p');
  for (let i=0; i < visits.length; i++){
    if (i < 31){
      let content1 = document.createTextNode("    " + new Date(visits[i].visitTime));
      p.appendChild(content1);
    }
  }
  div.appendChild(p);
}

//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/history/getVisits
function findVisits(pre_visits) {
  if (pre_visits.length) {
    var foundVisits = browser.history.getVisits({
      url: pre_visits[0].url
    });
    foundVisits.then(gotVisits);
  }
}

function display(tabs) {
  let tab = tabs.pop();

  var searching = browser.history.search({
  text: tab.url,
  startTime: 0,
  maxResults: 1
  });

  searching.then(findVisits);
}

function currentTab() {
  return browser.tabs.query({currentWindow: true, active: true});
}
currentTab().then(display);
