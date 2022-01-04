//I consulted the mozilla history and cookies documentation to learn how to write this code
//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/history/getVisits
//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/cookies

function displayWarning(tabs) {
  let tab = tabs.pop();

  var div = document.getElementById('results');
  let h1 = document.createElement('h1');

  var searching = browser.history.getVisits({
      url: tab.url
  });

  searching.then((search) => {
    if (search.length > 100){
      var text = document.createTextNode(tab.url + " is watching you! ");
      h1.appendChild(text);
    }
  });

  var getCookies = browser.cookies.getAll({url: tab.url});
  getCookies.then((cookies) => {
    if (cookies.length > 5){
    var text = document.createTextNode(tab.url + " is studying you! ");
    h1.appendChild(text);
    }
  });

  div.appendChild(h1);
}

function currentTab() {
  return browser.tabs.query({currentWindow: true, active: true});
}
currentTab().then(displayWarning);