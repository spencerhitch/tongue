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
  var input_value = $input.val();
  console.log(input_value);
  if (input_value.length == 2) {
    var alpha = $input.val().toLowerCase();
    var url = 'static/js/en_es/' + alpha + ".json";
    $.getJSON(url, function(data) {
      titles = data;
      loadInput();
      update();
    });
  }
});

var update = function() {
  articleName = decodeURIComponent(window.location.hash.substring(1));
  if (articleName) {
    $input.typeahead('val', articleName);
    $input.blur();
  } else {
    $input.typeahead('val', '');
    $input.focus();
  }
}

window.onhashchange = update;

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

  $input.bind('typeahead:select', function(e, articleName) {
    if (articleName == decodeURIComponent(window.location.hash.substring(1))) {
      $input.blur();
    } else {
      window.location.hash = '#' + encodeURIComponent(articleName);
    }
  });
}

var inputMatcher = function(strs) {
  return function findMatches(q, cb) {
    var equalRegex = new RegExp('^' + escape(removeDiacritics(q)) + '$', 'i');
    var startRegex = new RegExp('^' + escape(removeDiacritics(q)), 'i');
    var substrRegex = new RegExp(escape(removeDiacritics(q)), 'i');

    var equalMatches = [];  // Equal to
    var startMatches = [];  // Starts with
    var substrMatches = []; // Substring of

    $.each(strs, function(i, str) {
      if (equalRegex.test(removeDiacritics(str))) {
        equalMatches.push(str);
      } else if (startRegex.test(removeDiacritics(str))) {
        startMatches.push(str);
      } else if (substrRegex.test(removeDiacritics(str))) {
        substrMatches.push(str);
      }
    });

    cb(equalMatches.concat(startMatches).concat(substrMatches));
  };
}
