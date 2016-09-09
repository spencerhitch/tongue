/* Imports */

var escape = require('escape-regexp');
var removeDiacritics = require('diacritics').remove;
var $ = require('jquery');
require('typeahead.js');

/* General */

var titles = {};

var $input = $('#interaction input');
var $articles_list = $('#articles-list');

$input.on("keyup", function(e) {
  if ($input.val().length >= 2 && Object.keys(titles).length == 0) {
    console.log("if: ", $input.val());
    var alpha = $input.val().substring(0,2).toLowerCase();
    var url = 'static/js/en_es/' + alpha + ".json";
    $.getJSON(url, function(data) {
      titles = data;
      loadInput();
      update();
    });
  } else if ($input.val().length < 2) {
    console.log("else if: ", $input.val());
    titles = {};
    resetInput();
  } else {
    update();
  }
});

var update = function() {
  $input.typeahead('val', $input.val());
  $input.focus();
}

/* Input */

var loadInput = function() {
  $input.typeahead({
    hint: true,
    highlight: true,
    minLength: 2
  },
  {
    title: 'titles',
    source: inputMatcher(titles)
  });
}

var key_sanitizer = function(key){
  return key.substring(1,key.length-2).replace(/_/g, " ");
}

var inputMatcher = function(strs) {
  return function findMatches(q, cb) {
    var equalRegex = new RegExp('^' + escape(removeDiacritics(q)) + '$', 'i');
    var startRegex = new RegExp('^' + escape(removeDiacritics(q)), 'i');
    var substrRegex = new RegExp(escape(removeDiacritics(q)), 'i');

    var equalMatches = [];  // Equal to
    var startMatches = [];  // Starts with
    var substrMatches = []; // Substring of

    $.each(strs, function(key, value) {
      key = key_sanitizer(key);
      if (equalRegex.test(removeDiacritics(key))) {
        equalMatches.push(key);
      } else if (startRegex.test(removeDiacritics(key))) {
        startMatches.push(key);
      } else if (substrRegex.test(removeDiacritics(key))) {
        substrMatches.push(key);
      }
    });

    cb(equalMatches.concat(startMatches).concat(substrMatches));
  };
}

var resetInput = function() {
  $input.typeahead('destroy');
  $input.focus();
}
