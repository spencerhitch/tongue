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
var articles = {}

var $generateButton = $('#generate_button');

$input.on("keyup", function(e) {
  if ($input.val().length >= 2 && Object.keys(titles).length == 0) {
    var alpha = $input.val().substring(0,2).toLowerCase();
    var url = 'static/js/en_es/' + alpha + ".json";
    $.getJSON(url, function(data) {
      titles = data;
      loadInput();
      update();
    });
  } else if ($input.val().length < 2) {
    titles = {};
    resetInput();
  } else {
    update();
  }
});

$form.submit(function(e) {
  e.preventDefault();
  var title = "" 
  if ($(".tt-hint").val()){
    title =  $(".tt-hint").val();
  } else {
    title = $(".tt-suggestion").first().text();
  }
  if (isMatchingTitle(title)) {
    target_title = titles[unsanitizeTitle(title)];
    console.log(target_title);
    $input.typeahead('val', '');
    $.ajax({
      url: '/addArticle',
      data: {
        title: target_title
      },
      type: 'POST',
      success: function(r){
        articles[title] = r;
        addListItem(title);
      },
      error: function(e){
        console.log(e);
      }
    });
  } 
});

$generateButton.click(function (e) {
  $.ajax({
    url: '/generate',
    data: {
      articles: JSON.stringify(articles)
    },
    type: 'POST',
    success: function(r) {
      console.log(r);
//      listGeneratedWords(r);
    },
    error: function(e) {
      console.log(e);
    }
  });
});

var isMatchingTitle = function(title) {
  if (title.length > 0) return true;
  else return false;
}

var addListItem = function(title) {
  var id = stripTitle(title);
  var li = "<li id='" + id + "'>" + title + " <button>X</button></li>";
  $articles_list.append(li);
  $("#" + id + ">button").click(function(e) {
    $("#" + id).remove();
  });
}

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
  return title.replace(/_/g, " ");
}

var unsanitizeTitle = function(title){
  return title.replace(/ /g, "_");
}

var stripTitle = function(title){
  title = title.replace(/ /g, "_");
  return title.replace(/[.,\/#!$%\^&\*;:{}=\-`~()]/g, "")
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
//    cb(equalMatches.concat(startMatches));
  };
}

var resetInput = function() {
  $input.typeahead('destroy');
  $input.focus();
}
