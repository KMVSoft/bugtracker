var DOM = (typeof(document.getElementById) != 'undefined');

function setHomePage(objSrc, language) {
  if ((navigator.appName == "Microsoft Internet Explorer") && (parseInt(navigator.appVersion) >= 4)) {
    objSrc.style.behavior='url(#default#homepage)';
    objSrc.setHomePage('http://www.fsvps.ru');
  } else {
    wopen(
      "/fsvps-docs/"+language+"/homepage.html",
      null, 
      500, 
      450
    );
  }
}


function addBookmark(url, title){
  if ((navigator.appName == "Microsoft Internet Explorer") && (parseInt(navigator.appVersion) >= 4)) {
    window.external.AddFavorite(url,title);
  } else if (navigator.appName == "Netscape") {
    window.sidebar.addPanel(title,url,"");
  } else {
    alert("Press CTRL-D (Netscape) or CTRL-T (Opera) to bookmark");
  }
}


function hideShow(id) {
  var el = document.getElementById(id);
  if (el.style.display == 'none') 
    el.style.display = 'block';
  else 
    el.style.display = 'none';
};


function mailPage() {
  mail_str = "mailto:?subject=%CE%F4%E8%F6%E8%E0%EB%FC%ED%FB%E9%20%F1%E0%E9%F2%20%D0%EE%F1%F1%E5%EB%FC%F5%EE%E7%ED%E0%E4%E7%EE%F0%E0";
  mail_str += "&body=%CE%E1%F0%E0%F2%E8%F2%E5%20%E2%ED%E8%EC%E0%ED%E8%E5";
  mail_str += ". " + location.href;
  location.href = mail_str;
}


function checkElement(id) {
   document.getElementById(id).checked = true;
}


function checkBox(id) {
   flag = document.getElementById(id).checked;
   if(flag) {
      document.getElementById(id).checked = false;
   } else {
      document.getElementById(id).checked = true;
   }
}


function checkAll(Element,Name) {
  if (DOM) {
    thisCheckBoxes = Element.parentNode.parentNode.parentNode.getElementsByTagName('input');
    for (i = 1; i < thisCheckBoxes.length; i++) {
      if (thisCheckBoxes[i].name == Name){
        thisCheckBoxes[i].checked = Element.checked;        
      }
    }
  }
}


function wopen(url, name, w, h) {
  // Fudge factors for window decoration space.
  // In my tests these work well on all platforms & browsers.
  w += 32;
  h += 96;
  wleft = (screen.width - w) / 2;
  wtop = (screen.height - h) / 2;
  // IE5 and other old browsers might allow a window that is
  // partially offscreen or wider than the screen. Fix that.
  // (Newer browsers fix this for us, but let's be thorough.)
  if (wleft < 0) {
    w = screen.width;
    wleft = 0;
  }
  if (wtop < 0) {
    h = screen.height;
    wtop = 0;
  }
  var win = window.open(url,
    name,
    'width=' + w + ', height=' + h + ', ' +
    'left=' + wleft + ', top=' + wtop + ', ' +
    'location=no, menubar=no, ' +
    'status=no, toolbar=no, scrollbars=yes, resizable=no');
  // Just in case width and height are ignored
  win.resizeTo(w, h);
  // Just in case left and top are ignored
  win.moveTo(wleft, wtop);
  win.focus();
}


function expandMultiTags(Tgs, VsblTgs) {
  var tags = document.getElementById(Tgs);
  var visibleTags = document.getElementById(VsblTgs);
  var alwaysContain = false;
  
  for(i = 0; i < visibleTags.length; i++) {
    if(visibleTags.options[i].text == comboBox.getComboText()) alwaysContain = true;
  }
  
  if(!alwaysContain) {
    var oOption = document.createElement("option");
    var selectedText = comboBox.getComboText();
    var selectedValue = comboBox.getSelectedValue();
    oOption.appendChild(document.createTextNode(selectedText));
    if(selectedValue == null || selectedValue == "") oOption.setAttribute("value", selectedText)
    else oOption.setAttribute("value", selectedValue);
    visibleTags.appendChild(oOption);
    var hOption = document.createElement("option");
    hOption.appendChild(document.createTextNode(selectedText));
    if(selectedValue == null || selectedValue == "") hOption.setAttribute("value", selectedText)
    else hOption.setAttribute("value", selectedValue);
    hOption.setAttribute("selected", true);
    tags.appendChild(hOption);
  }
}


function narrowMultiTags(Tgs, VsblTgs){
  var visibleTags = document.getElementById(VsblTgs);
  var tags = document.getElementById(Tgs);
  for(i = 0; i < visibleTags.length; i++){
    if(visibleTags.options[i].selected){
      var selectedValue = visibleTags.options[i].value;
      visibleTags.remove(i);
      for(j = 0; j < tags.length; j++){
        if(tags.options[j].value == selectedValue) tags.remove(i);
      }
    }
  }
}


function selectOptionByValue(selObj, val) {
  var A = selObj.options, L = A.length;
  while(L){
    if (A[--L].value == val){
      selObj.selectedIndex = L;
      L = 0;
    }
  }
}


function checkFileSize(el, maxSize, message) {
  var files = el.files;
  if (files) {
    for (var i=0; i<files.length; i++) {
      if (files[i].size > maxSize) {
        alert(message);
        el.value = "";
      }
    }
  }
}


var fileFieldCount = 1;

function addFileField() {
  var fields = $('#attachments_fields');
  if (fields.children().length >= 10) return false;
  
  fileFieldCount++;
  var newFileField = fields.children(":first").clone();
  newFileField.find('input.file').attr("name", "attachments[" + fileFieldCount + "][file]");
  newFileField.find('input.file').val("");
  newFileField.find('input.description').attr("name", "attachments[" + fileFieldCount + "][description]");
  newFileField.find('input.description').val("");
  fields.append(newFileField);
}


function removeAttachmentField(el) {
  var fields = $('#attachments_fields');
  var s = $(el).parent();
  if (fields.children().length > 1) {
    s.remove();
  }
}


function deleteAttachment(attachmentId, el){
  if (confirm('Вы действительно хотите выполнить удаление?')) {
    var s = $(el).parent();
    jQuery.ajax({
      url: '/fsvps/admin/deleteAttachment',
      data: {'id': attachmentId},
      dataType : "json",
      success: function (data, textStatus) {s.hide("fast");},
    });
  }
};

function checkQuestion(messageId, id){
  if (confirm('Вы действительно хотите опубликовать?')) {

    jQuery.ajax({
      url: '/fsvps/admin/ereception/checkMessage',
      data: {'id': messageId},
      dataType : "json",
      success: function (data, textStatus) {$(id).html('<span style="color: green; font-weight: bold;">Опубликовано</span>');}
    });
  }
};