// Copyright (c) 2011 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//console.log('hello owrl', chrome.browserAction)

//chrome.runtime.onInstalled.addListener(function() {
//    console.log('Hello')
//});


chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    console.log('listener')
    chrome.browserAction.setBadgeText({text: "📭"});
})



chrome.browserAction.onClicked.addListener(function (tab) {
//
//  chrome.tabs.executeScript({
//    code: 'document.body.style.backgroundColor="red"'
//  });
//
    chrome.tabs.create({url: 'https://www.filmweb.pl/'})
//    console.log(tab)

})
//
//chrome.browserAction.onClicked.addListener(function (tab) {
//console.log('something, something....')
//    chrome.tabs.create({url: 'rekomendacje.html'})
//})
// Called when the user clicks on the browser action.
//chrome.browserAction.onClicked.addListener(function(tab) {
//  // No tabs or host permissions needed!
//  console.log('Turning ' + tab.url + ' red!');
//  chrome.tabs.executeScript({
//    code: 'document.body.style.backgroundColor="red"'
//  });
//});
