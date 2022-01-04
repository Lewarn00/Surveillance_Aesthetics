//I consulted the mozilla cookies documentation and example projects to learn how to write this code
//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/history/getVisits
//https://github.com/mdn/webextensions-examples/tree/master/list-cookies

function displayCookies(tabs) {
  let tab = tabs.pop();

  function gotCookies(cookies){
    var div = document.getElementById('title');    
    let h = document.createElement('h2');
    var text = document.createTextNode(tab.title + " is using " + cookies.length + " cookies");
    h.appendChild(text);
    div.appendChild(h);
  } 
  
  var getCookies = browser.cookies.getAll({url: tab.url});
  getCookies.then(gotCookies);
}

function currentTab() {
  return browser.tabs.query({currentWindow: true, active: true});
}
currentTab().then(displayCookies);