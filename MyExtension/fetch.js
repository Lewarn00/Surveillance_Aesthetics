//I consulted the mozilla storage documentation and example projects to learn how to write this code
//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/storage/StorageArea/get
//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects

function getResults(results){
  let host_results = document.getElementById("hosts");
  let type_results = document.getElementById("types");

  //For next two lines --> https://github.com/mdn/webextensions-examples/blob/master/navigation-stats/popup.js
  let hosts_sorted = Object.keys(results.host).sort((a, b) => (results.host[a] <= results.host[b]));
  let types_sorted = Object.keys(results.type).sort((a, b) => (results.type[a] <= results.type[b]));

  for (let i=0; i < hosts_sorted.length; i++) { 
    if (i < 5) {
      let li1 = document.createElement("li");
      let content1 = document.createTextNode(hosts_sorted[i] + ": " + results.host[hosts_sorted[i]]);
      li1.appendChild(content1);
      host_results.appendChild(li1);

      let li2 = document.createElement("li");
      let content2 = document.createTextNode(types_sorted[i] + ": " + results.type[types_sorted[i]]);
      li2.appendChild(content2);
      type_results.appendChild(li2);
    }
  }
}

var getStored = browser.storage.local.get();
getStored.then(getResults);