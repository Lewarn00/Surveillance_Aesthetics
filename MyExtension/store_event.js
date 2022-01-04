//I consulted the mozilla webNavigation documentation and example projects to learn how to write this code
//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/webNavigation/onCommitted

function gotResults(results) {
  results = {
      host: {},
      type: {},
    };

  const filter = {
  url:
  [
    {schemes: ["http", "https"]}
  ]
  }

  function gotEvent(event) {
      let transitionType = event.transitionType;
      results.type[transitionType] = results.type[transitionType] || 0;
      results.type[transitionType] = results.type[transitionType] + 1;
      browser.storage.local.set(results);

      let url = new URL(event.url);
      results.host[url.hostname] = results.host[url.hostname] || 0;
      results.host[url.hostname] = results.host[url.hostname] + 1;

      browser.storage.local.set(results);
  }

  browser.webNavigation.onCommitted.addListener(gotEvent, filter);

}


var getStored = browser.storage.local.get();
getStored.then(gotResults);