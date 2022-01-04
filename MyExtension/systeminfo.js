//I consulted the mozilla runtime documentation to learn how to write this code
//https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/runtime/getPlatformInfo

function gotPlatformInfo(info) {
  var div = document.getElementById('system-info');
  let p = document.createElement('p');
  let content = document.createTextNode("Operating system: " + info.os + " | Architecture: " + info.arch);
  p.appendChild(content);

  div.appendChild(p);
}

var getInfo = browser.runtime.getPlatformInfo();
getInfo.then(gotPlatformInfo);