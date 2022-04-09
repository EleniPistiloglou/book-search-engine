// https://www.gutenberg.org/cache/epub/67449/pg67449.txt
/*
console.log("calling function");
var req = new XMLHttpRequest();
console.log("craeting request");
req.open('GET', 'https://www.gutenberg.org/cache/epub/67449/pg67449.txt', false);

req.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
req.setRequestHeader("Access-Control-Allow-Origin", "*");

console.log("sending request");
req.send("http://127.0.0.1");
if(req.status == 200) {
  // alert(req.responseText);
  console.log("got answer");
  console.log(req.responseText);
} else console.log("ERROR");
*/

/*
>>> import requests
>>> from bs4 import BeautifulSoup

>>> getpage= requests.get('http://www.learningaboutelectronics.com/Articles/')

>>> getpage_soup= BeautifulSoup(getpage.text, 'html.parser')

>>> print(getpage_soup.prettify())
*/