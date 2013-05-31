function expColl(id) {
  var ele = document.getElementById(id);
  if (ele.style.display != 'none')
      ele.style.display = 'none';
  else
      ele.style.display = 'block';
}

function toggleConj(id) {
    var button = document.getElementById(id).childNodes[0].innerHTML = 'blah';
    //var ele = document.getElementById(id);
    //var temp = ele.text;
    //ele.text = ele.getAttribute("repltext");
    //ele.setAttribute("repltext", temp);
    //console.log(temp);
}

