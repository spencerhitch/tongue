/* Imports */

var escape = require('escape-regexp');
var removeDiacritics = require('diacritics').remove;
var $ = require('jquery');
require('typeahead.js');

/* General */

var titles = {};

var $input = $('#article_input');
var $form = $('#input_form');
var $articles_list = $('#articles_list');

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

$form.submit(function(e) {
  var res = unsanitizeTitle($input.val());
  var new_li = "<li id='" + res + "'>" + $input.val() + " <button>X</button></li>";
  $articles_list.append(new_li);
  $("#" + res + ">button").click(function(e) {
    $("#" + res).remove();
  });
  console.log("Submitted input: ", res);
  $input.typeahead('val', '');
  e.preventDefault();
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

var sanitizeTitle = function(title){
  return title.substring(1,title.length-2).replace(/_/g, " ");
}

var unsanitizeTitle = function(title){
  return title.replace(/ /g, "_");
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
      key = sanitizeTitle(key);
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
