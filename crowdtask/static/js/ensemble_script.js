$title = [
  'Content & Organization','Language use','Machanics','Others'
]

$order = getParameterByName('order');
$version = 0;
if($order == 'HML') $str = 0;
else if($order == 'LMH') $str = 2;
else $str = -1;
$txt = getParameterByName('txt');
$json = getParameterByName('json');
//$txt = getQueryVariable('txt');
//$json = getQueryVariable('json');
$timer = 0; // seconds to count down
$revisionArray = new Array();
window.setInterval(everysecond, 1000);
everysecond();

// if($txt>0) readTextFile($txt);
// else readTextFile("/static/feedback-data/doc_origin.docx.txt");
// if($json>0) readJson($json);
// else readJson("/static/feedback-data/doc_mod.json");


var content = $("#article_content").attr("content");
var json_content = $("#feedback_content").attr("content");

loadText(content);
loadJSON(json_content);


function disable(e){
  console.log(e);
  e.setAttribute("class",'ui disabled button');
  if(e.innerHTML==='Reject') {
    console.log("reject");
    e.previousSibling.setAttribute("class",'ui disabled button');
  }
  else if(e.innerHTML==='Accept') {
    console.log("accept");
    e.nextSibling.setAttribute("class",'ui disabled button');
  }
  e.parentNode.previousSibling.setAttribute('style',"background-color: LightGray;");
  e.parentNode.previousSibling.setAttribute('result',e.innerHTML);
  e.parentNode.previousSibling.setAttribute('action_time',$timer);// TODO: Save $time 
  
}

function finish(){
  console.log("Finish");
  $('#reminder-check').modal('hide');
  //return 0;

  var results = new Array();
  $(".feedback").each(function(i, val){
    var item_result = $(this).find(".title").attr("result");
    var rating = $(this).find(".title .rating .active").length;
    var action_time = $(this).find(".title").attr("action_time");
    var action = (typeof item_result === "undefined" ? "None" : item_result);

    var item = {
      "id": i,
      "type_name": $title[ parseInt($(this).attr("type_id")) ],
      "type_id": $(this).attr("type_id"),
      "rating": rating,
      "action": action,
      "action_time": action_time
    }
    results.push(item);
  });

  //save the last revision content
  $("#revision_content").attr('action_time',$timer);// TODO: Save $time 
  var revision_data = {
    "revision_content": $("#revision_content").val(),
    "revision_time": $("#revision_content").attr("action_time")
  }
  $revisionArray.push(revision_data);


  $.ajax({
      type: "POST",
      url: "/api/add_revision",
      data: {
          "article_id": $("#article_id").attr("content"),
          "created_user": $("#create_user").attr("content"),
          "feedback_id": $("#feedback_id").attr("content"),
          "feedback_content": JSON.stringify(results),
          "revision_content": JSON.stringify($revisionArray),
          "duration_time": $timer,

          "verified_string": $("#verified_string").attr("content"),
          "feedback_order": $order
      },
      dataType: 'json', 
      
      success: function(data) {
          if(data['success'] == 1){
            window.location = "/success?verified_string="+$("#verified_string").attr("content")+"&flow="+$('#experiment_flow').attr("content")+"&user="+$('#create_user').attr("content");
          }
      },
      beforeSend: function(){
          $('#loading-image').show();
      },
      complete: function(){
          $('#loading-image').hide();
                      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
          alert("Error");    
      }
  });
  
}

function nextstage(){
  $('#reminder-check').modal('hide');

  if($order == "HML"){
    
    $(".feedback[type_id="+$str+"]").hide(); //hide feedback

    //clear up text
    mod_list = $('span.mod_'+$str);
    for(i=0;i<mod_list.length;i++){
        //mod_list[i].setAttribute('style','background-color: White;');
        mod_list[i].setAttribute('style','background-color: White;');
    }
    $('.ins.mod_'+$str).hide();
    $(".del-text.mod_"+$str).attr('style','background-color:#fff; text-decoration:none;color:#000;');

    //show feedback at the next stage
    $(".del-text.mod_"+($str+1)).attr('style','text-decoration:line-through; color:#f00;');
    $('.ins.mod_'+($str+1)).show();
    $(".feedback[type_id="+($str+1)+"]").show();
    mod_list = $('span.mod_'+($str+1));
    for(i=0;i<mod_list.length;i++){
        e = mod_list[i];
        if(!e.getAttribute('class')) continue
        else if(e.getAttribute('class').includes('mod_0')){
          e.setAttribute('style','background-color: #ccf2ff ;');
        }
        else if(e.getAttribute('class').includes('mod_1')){
          e.setAttribute('style','background-color: #ebf5d6 ;');
        }
        else if(e.getAttribute('class').includes('mod_2')){
          e.setAttribute('style','background-color: #ffcce6 ;');
        }
        // if(!e.getAttribute('class')) continue
        // else if($str != -1){
        //   if(e.getAttribute('class').includes('mod_0') && $str==0)
        //     e.setAttribute('style','background-color: #ccf2ff ;');
        //   else if(e.getAttribute('class').includes('mod_1') && $str==1)
        //     e.setAttribute('style','background-color: #ebf5d6 ;');
        //   else if(e.getAttribute('class').includes('mod_2') && $str==2)
        //     e.setAttribute('style','background-color: #ffcce6 ;');
        // }else{
        //   if(e.getAttribute('class').includes('mod_0'))
        //     e.setAttribute('style','background-color: #ccf2ff ;');
        //   else if(e.getAttribute('class').includes('mod_1'))
        //     e.setAttribute('style','background-color: #ebf5d6 ;');
        //   else if(e.getAttribute('class').includes('mod_2'))
        //     e.setAttribute('style','background-color: #ffcce6 ;');
        // }
    }
    $str++;
    $version++;

    document.getElementById('version').innerHTML = $version;

    if($version>2){
      btn = document.getElementById('btn_next');
      btn.innerHTML='Finish';

      var btn2 = document.getElementById('go-to-next');
      btn2.innerHTML='Finish';
      btn2.setAttribute('onclick','finish()');
    }
  }else if($order == "LMH"){

    $(".feedback[type_id="+$str+"]").hide();
    mod_list = $('span.mod_'+$str);
    for(i=0;i<mod_list.length;i++){
        mod_list[i].setAttribute('style','background-color: White;');
    }
    $('.ins.mod_'+$str).hide();
    $(".del-text.mod_"+$str).attr('style','background-color:#fff; text-decoration:none;color:#000;');
    
    $(".del-text.mod_"+($str-1)).attr('style','text-decoration:line-through; color:#f00;');
    $('.ins.mod_'+($str-1)).show();
    $(".feedback[type_id="+($str-1)+"]").show();
    mod_list = $('span.mod_'+($str-1));
    for(i=0;i<mod_list.length;i++){
        e = mod_list[i];
        if(!e.getAttribute('class')) continue
        else if(e.getAttribute('class').includes('mod_0')){
          e.setAttribute('style','background-color: #ccf2ff ;');
        }
        else if(e.getAttribute('class').includes('mod_1')){
          e.setAttribute('style','background-color: #ebf5d6 ;');
        }
        else if(e.getAttribute('class').includes('mod_2')){
          e.setAttribute('style','background-color: #ffcce6 ;');
        }
        // if(!e.getAttribute('class')) continue
        // else if($str != -1){
        //   if(e.getAttribute('class').includes('mod_0') && $str==0)
        //     e.setAttribute('style','background-color: #ccf2ff ;');
        //   else if(e.getAttribute('class').includes('mod_1') && $str==1)
        //     e.setAttribute('style','background-color: #ebf5d6 ;');
        //   else if(e.getAttribute('class').includes('mod_2') && $str==2)
        //     e.setAttribute('style','background-color: #ffcce6 ;');
        // }else{
        //   if(e.getAttribute('class').includes('mod_0'))
        //     e.setAttribute('style','background-color: #ccf2ff ;');
        //   else if(e.getAttribute('class').includes('mod_1'))
        //     e.setAttribute('style','background-color: #ebf5d6 ;');
        //   else if(e.getAttribute('class').includes('mod_2'))
        //     e.setAttribute('style','background-color: #ffcce6 ;');
        // }
    }
    $str--;
    $version++;
    document.getElementById('version').innerHTML = $version;

    if($version>2){
      btn = document.getElementById('btn_next');
      btn.innerHTML='Finish';

      var btn2 = document.getElementById('go-to-next');
      btn2.innerHTML='Finish';
      btn2.setAttribute('onclick','finish()');
    }

  }else{
    btn = document.getElementById('btn_next');
    btn.innerHTML='Finish';
    var btn2 = document.getElementById('go-to-next');
    btn2.innerHTML='Finish';
    btn2.setAttribute('onclick','finish()');
  }

  //save revision content
  $("#revision_content").attr('action_time',$timer);// TODO: Save $time 
  var revision_data = {
    "revision_content": $("#revision_content").val(),
    "revision_time": $("#revision_content").attr("action_time")
  }
  $revisionArray.push(revision_data);

  // if($str>2 || $str<0){
  //   finish();
  //   return 0;
  // }
  // if($str==2){
  //   btn = document.getElementById('btn_next')
  //   btn.innerHTML='Finish';
  //   btn.parentNode.setAttribute('onclick','finish()');
  // }
  // mod_list = document.getElementsByClassName('mod_'+($str-1));
  // for(i=0;i<mod_list.length;i++){
  //     if(mod_list[i].getAttribute('class').includes('title'))
  //       mod_list[i].style.display = 'none';
  //     else {
  //       mod_list[i].setAttribute('style','background-color: White;');
  //     }
  // }
  // mod_list = document.getElementsByClassName('mod_'+$str);
  // for(i=0;i<mod_list.length;i++){
  //     e = mod_list[i];
  //     if(!e.getAttribute('class')) continue
  //     else if(e.getAttribute('class').includes('mod_0'))
  //       e.setAttribute('style','background-color: #ccf2ff ;');
  //     else if(e.getAttribute('class').includes('mod_1'))
  //       e.setAttribute('style','background-color: #ebf5d6 ;');
  //     else if(e.getAttribute('class').includes('mod_2'))
  //       e.setAttribute('style','background-color: #ffcce6 ;');
  // }
  // document.getElementById('version').innerHTML = ++$str;
}

function everysecond(){
  /*if($timer%60<10)
    document.getElementById('clock').innerHTML = Math.floor($timer/60)+' min 0'+$timer%60+' sec';
  else {
    document.getElementById('clock').innerHTML = Math.floor($timer/60)+' min '+$timer%60+' sec';
  }
  if($timer==0){
    nextstage();
  }
  else
    $timer--;
  */
  document.getElementById('clock').innerHTML = Math.floor($timer/60)+' min '+$timer%60+' sec';
  $timer++;
}

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

function getQueryVariable(variable)
{
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    if(pair[0] == variable){return pair[1];}
  }
  return(-1);
}
function addText(i,c){
  e = document.createElement('span');
  e.setAttribute('id',i);
  e.innerHTML = c;
  return e;
}
function addIns(i){
  e = document.createElement('span');
  e.setAttribute('class',"ins ins_"+i);
  e.setAttribute('i_start',i);
  e.innerHTML = '';
  return e; 
}
function display(txt)
{
    var text = txt.split('\n');
    var index = 1,start_row = 0;
    document.getElementById('title').innerHTML = '';
    document.getElementById('content').innerHTML = '';

    while(!text[start_row]) {
      start_row += 1;
    }
    for(i=0;i< text[start_row].length;i++){
      e = addText(index,text[start_row][i]);
      document.getElementById('title').appendChild(e);
      index += 1;
    }
    for (i = start_row+1; i < text.length; i++){
      for(j = 0; j < text[i].length; j++){
        e = addText(index,text[i][j]);
        document.getElementById('content').appendChild(e);
        document.getElementById('content').appendChild(addIns(index));
        index += 1;
      }
      document.getElementById('content').innerHTML += '<br>';
    }
}
function addElement(type, id, inner){
   e = document.createElement(type);
   e.setAttribute("class", id);
   e.innerHTML = inner;
   return e;
}

function addMod(uid, id, e_type, i_s, i_e, e_title, hist, comment, visibility){
  new_e = document.createElement("div");
  new_e.setAttribute("class", 'mod '+e_type+' title '+e_type+"_styled "+e_title);
  new_e.setAttribute("i_start", i_s);
  new_e.setAttribute("i_end", i_e);
  new_e.setAttribute("e_id", e_type[4]);

  
  if(e_type==='mod_0')
    new_e.innerHTML += $title[0]+' #'+id;
  else if(e_type==='mod_1')
    new_e.innerHTML += $title[1]+' #'+id;
  else if(e_type==='mod_2')
    new_e.innerHTML += $title[2]+' #'+id;
  else
    new_e.innerHTML += $title[3]+' #'+id;
  new_e.appendChild(addElement("div",'ui huge star rating',''));

  new_e_2 = document.createElement("div");
  new_e_2.setAttribute("class", 'mod content '+e_title);
  new_e_2.setAttribute("i_start", i_s);
  new_e_2.setAttribute("i_end", i_e);
  new_e_2.setAttribute("e_id", e_type[4]);

  comment = comment.replace(new RegExp('\n','g'), '<br>');
  new_e_2.appendChild(addElement('p','',e_title+' '+hist+'.<br>'+comment));

  // if(e_title==='Comment'){
  //   btn = addElement('button','ui primary button','Solved');
  //   btn.setAttribute("onclick", "disable(this)");
  //   new_e_2.appendChild(btn);
  // }
  // else {
  //   btn_1 = addElement('button','ui primary button','Accept');
  //   btn_1.setAttribute("onclick", "disable(this)");
  //   btn_2 = addElement('button','ui primary button','Reject');
  //   btn_2.setAttribute("onclick", "disable(this)");
  //   new_e_2.appendChild(btn_1);
  //   new_e_2.appendChild(btn_2);
  // }
  
  btn_1 = addElement('button','ui primary button','Accept');
  btn_1.setAttribute("onclick", "disable(this)");
  btn_2 = addElement('button','ui primary button','Reject');
  btn_2.setAttribute("onclick", "disable(this)");
  new_e_2.appendChild(btn_1);
  new_e_2.appendChild(btn_2);

  // if(!visibility){
  //   new_e.style.display = 'none';
  //   new_e_2.style.display = 'none';
  // }

  if(e_title == "Insert"){
    var ins_ele = $(".ins_"+(i_s-1));
    ins_ele.html("&nbsp;&nbsp;");
    ins_ele.addClass("ins-text");
    ins_ele.addClass(e_type);
  }
  for(i=i_s;i<=i_e;i++){
    var e = document.getElementById(i.toString());
      // e.setAttribute('class',e_type);
    if(e==null) continue;
    
    if(e_title == "Delete") e.setAttribute("class","del-text "+e_type);
    else if(e_title == "Replace") e.setAttribute("class","del-text "+e_type);
    else if(e_title == "Comment") e.classList.add(e_type);

    if(!visibility){
        e.setAttribute('style','background-color: white;');
    }
  }   
  
  


  var new_item = document.createElement("div");
  
  new_item.setAttribute("id",'feedback_'+uid);
  new_item.setAttribute("class",'feedback');
  new_item.setAttribute("type_id",e_type[4])
  new_item.appendChild(new_e);
  new_item.appendChild(new_e_2);

  if(!visibility){
    new_item.style.display = 'none';
  }
  document.getElementById('history').appendChild(new_item);
  //document.getElementById('history').appendChild(new_e);
  //document.getElementById('history').appendChild(new_e_2);

  
}

function loadText(text)
{
    display(text);
}
function loadJSON(jsonData){
    var json = $.parseJSON(jsonData);
    k = [1,1,1];
    num = 0;
    for(j = 0;j<json.length;j++){
        e = json[j];
        index = parseInt(e['modifier'][4]);
        if(e['mod_type']){
          if($str != -1) {
            visibility = (index==$str);
            //var ind_start = isInt(e['index_start']) ? e['index_start'] : parseInt(e['index_start']);
            //var ind_end = isInt(e['index_end']) ? e['index_end'] : parseInt(e['index_end']);
            addMod(num++, k[index]++,e['modifier'],e['index_start'],e['index_end'],e['mod_type'],e['mod_history'],e['mod_comment'],visibility);
          }else{
            addMod(num++, k[index]++,e['modifier'],e['index_start'],e['index_end'],e['mod_type'],e['mod_history'],e['mod_comment'],true);
          }
          // addMod(num++, k[index]++,e['modifier'],e['index_start'],e['index_end'],e['mod_type'],e['mod_history'],e['mod_comment'],false);
        }
    }
    if($str == -1){
      btn = document.getElementById('btn_next');
      btn.innerHTML='Finish';

      var btn2 = document.getElementById('go-to-next');
      btn2.innerHTML='Finish';
      btn2.setAttribute('onclick','finish()');
    }
    else {
      document.getElementById('version').innerHTML = ++$version;
    }
  
  h = $('#origin').height()-60;
  document.getElementById('history').setAttribute('style','height: '+h+'px;');

  $("span.ins").hide();
  if($str == -1){
    $(".mod_0").attr('style','background-color: #ccf2ff ;');
    $(".mod_1").attr('style','background-color: #ebf5d6 ;');
    $(".mod_2").attr('style','background-color: #ffcce6 ;');
    $("span.ins").show();
  }else{
    $(".del-text").attr('style','background-color:#fff; text-decoration:none;color:#000;');
    if($str == 0){
      $(".del-text.mod_0").attr('style','text-decoration:line-through; color:#f00;');
      $(".mod_0").attr('style','background-color: #ccf2ff ;');
      $(".ins.mod_0").show();
    }
    else if($str == 1){
      $(".del-text.mod_1").attr('style','text-decoration:line-through; color:#f00;');
      $(".mod_1").attr('style','background-color: #ebf5d6 ;');
      $(".ins.mod_1").show();
    }
    else if($str == 2){
      $(".del-text.mod_2").attr('style','text-decoration:line-through; color:#f00;');
      $(".mod_2").attr('style','background-color: #ffcce6 ;');
      $(".ins.mod_2").show();
    }
  }

}

function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                display(allText);
            }
        }
    }
    rawFile.send(null);
}

function readJson(file)
{

  $.getJSON(file, function(json) {
    k = [1,1,1];
    num = 0;
    for(j = 0;j<json.length;j++){
        e = json[j];
        //var ind_start = isInt(e['index_start']) ? e['index_start'] : parseInt(e['index_start']);
        //var ind_end = isInt(e['index_end']) ? e['index_end'] : parseInt(e['index_end']);
        index = parseInt(e['modifier'][4]);
        if(e['mod_type']){
          if($str>2 || $str<0){
            addMod(num++, k[index]++,e['modifier'],e['index_start'],e['index_end'],e['mod_type'],e['mod_history'],e['mod_comment'],true);
          }
          else {
            visibility = (index==$str || $str>2 || $str==-1);
            addMod(num++, k[index]++,e['modifier'],e['index_start'],e['index_end'],e['mod_type'],e['mod_history'],e['mod_comment'],visibility);
          }
        }
    }
    if($str>=2 || $str<0){
      btn = document.getElementById('btn_next');
      btn.innerHTML='Finish';

      var btn2 = document.getElementById('go-to-next');
      btn2.innerHTML='Finish';
      btn2.setAttribute('onclick','finish()');
    }
    else {
      document.getElementById('version').innerHTML = ++$str;
    }
  });
  h = $('#origin').height()-60;
  document.getElementById('history').setAttribute('style','height: '+h+'px;');
}

// function canvas_arrow(context, fromx, fromy, tox, toy){
//   size = 5;
//   context.save();
//   context.beginPath();
//   context.moveTo(fromx,fromy-size);
//   context.lineTo(fromx,fromy+size);
//   context.lineTo(tox, fromy);
//   context.closePath();
//   context.fill();
//   context.restore();
// }

function drawArrow(a_x,a_y,b_x,b_y){
  a_x = parseInt(a_x);
  b_x = parseInt(b_x);
  a_y = parseInt(a_y);
  b_y = parseInt(b_y);
  var p = {
      x: a_x < b_x ? a_x : b_x,
      x1: a_x > b_x ? a_x : b_x,
      y: a_y < b_y ? a_y : b_y,
      y1: a_y > b_y ? a_y : b_y
  };
  var c = $('<canvas/>').attr({
      'width': p.x1 - p.x +20,
      'height': p.y1 - p.y +100
  }).css({
      'position': 'absolute',
      'left': p.x,
      'top': p.y + 25,
      'z-index': 2
  }).appendTo($('body table'))[0].getContext('2d');

  // draw line
  c.strokeStyle = '#DB0A79';
  c.lineWidth = 2;
  // canvas_arrow(c,b_x-10 - p.x,b_y-10 - p.y,b_x - p.x,b_y-10 - p.y);
  c.moveTo(a_x - p.x,    a_y - p.y);
  c.lineTo(a_x - p.x,    a_y+10 - p.y);
  c.lineTo(b_x-10 - p.x,    a_y+10 - p.y);
  c.lineTo(b_x-10 - p.x,    b_y-10 - p.y);
  // c.quadraticCurveTo(a_x - p.x,a_y - p.y+100,b_x - p.x,b_y-10 - p.y);
  c.stroke();

}
var $middle_x = Math.floor(document.getElementById('history').offsetLeft);
// Hover on text
$("#origin").on("mouseover", "span", function () {
  var $t = $(this);
  var $id = parseInt($t.attr('id'));
  var $this_list = [];

  if($t.hasClass("ins")){
    if(!$t.hasClass('loc-hovered')){
      $t.addClass('loc-hovered');
    }
  }else{
    if($str != -1){
      //var $this_list = document.getElementsByClassName('mod mod_'+$str);
      $this_list = document.querySelectorAll('.mod.mod_'+$str+':not(.Insert)');
    }else{
      $this_list = document.querySelectorAll('.mod:not(.Insert)');
      //var $this_list = document.getElementsByClassName('mod');
    }

    for(i=0;i<$this_list.length;i++){
      var i_s = parseInt($this_list[i].getAttribute('i_start'));
      var i_e = parseInt($this_list[i].getAttribute('i_end'));
      
      
      if(i_s<= $id && i_e>= $id){
        // $this_list[i].setAttribute('style',"background-color: White;");
        $this_list[i].parentNode.classList.add('feedback-hovered');
        // $this_list[i].classList.toggle('active');
        for(i_x=i_s;i_x<=i_e;i_x++){
          // document.getElementById(i_x).setAttribute('style','background-color: LightGray;');
          if(!document.getElementById(i_x).classList.contains('loc-hovered')){
            document.getElementById(i_x).classList.add('loc-hovered');
            
          }
          
        }
      }
    }
  }

  
});
$("#origin").on("click", "span.ins", function () {
  var $t = $(this);
  var $id = parseInt($t.attr('i_start'))+1;

  if($str != -1){
    $this_list = document.querySelectorAll('.mod.mod_'+$str+".Insert");
  }else{
    $this_list = document.querySelectorAll('.mod.Insert');
  }

  for(i=0;i<$this_list.length;i++){
    var i_s = parseInt($this_list[i].getAttribute('i_start'));
    var i_e = parseInt($this_list[i].getAttribute('i_end'));

    if(i_s<= $id && i_e>= $id){
        var current = $t.hasClass('loc-selected');
        
        if(!current){
          $('.loc-selected').removeClass('loc-selected');
          $('.feedback-selected').removeClass('feedback-selected');
          // $this_list[i].parentNode.classList.remove('feedback-selected');
        }
        for(i_x=i_s;i_x<=i_e;i_x++){
          if(current){
            $this_list[i].parentNode.classList.remove('feedback-selected');
            $t.removeClass('loc-selected');
          }
          else{
            $this_list[i].parentNode.classList.add('feedback-selected');
            $t.addClass('loc-selected');
          }
        }

        $offset = $('#'+i_s).offset();
        $history = $('#history');

        document.getElementById('history').scrollTop = ($this_list[i].offsetTop - $offset.top +20);
        drawArrow($offset.left, $offset.top,$this_list[i].offsetLeft+$history.offset().left,
          $this_list[i].offsetTop+$history.offset().top - $history.scrollTop());
        
        break;
    }
  }
});
$("#origin").on("click", "span:not('.ins')", function () {
  var $t = $(this);
  var $id = parseInt($t.attr('id'));

  
  // if($str != -1){
  //   var $this_list = $('.mod_'+$str);
  // }else{
  //   var $this_list = $('.mod');
  // }

  if($str != -1){
    //var $this_list = document.getElementsByClassName('mod mod_'+$str);
    $this_list = document.querySelectorAll('.mod.mod_'+$str+':not(.Insert)');

  }else{
    $this_list = document.querySelectorAll('.mod:not(.Insert)');
    //var $this_list = document.getElementsByClassName('mod');
  }
  
  for(i=0;i<$this_list.length;i++){
    var i_s = parseInt($this_list[i].getAttribute('i_start'));
    var i_e = parseInt($this_list[i].getAttribute('i_end'));

    if(i_s<= $id && i_e>= $id){
        var current = document.getElementById(i_s).classList.contains('loc-selected');

        if(!current){
          $('.loc-selected').removeClass('loc-selected');
          $('.feedback-selected').removeClass('feedback-selected');
          // $this_list[i].parentNode.classList.remove('feedback-selected');
        }
        if($t.hasClass('loc-selected')){
          $('.loc-selected').removeClass('loc-selected');
          $('.feedback-selected').removeClass('feedback-selected');
        }else{
          $('.loc-hovered').addClass('loc-selected');
          $('.feedback-hovered').addClass('feedback-selected');  
        }

        $offset = $('#'+i_s).offset();
        $history = $('#history');

        document.getElementById('history').scrollTop = ($this_list[i].offsetTop - $offset.top +20);
        drawArrow($offset.left, $offset.top,$this_list[i].offsetLeft+$history.offset().left,
          $this_list[i].offsetTop+$history.offset().top - $history.scrollTop());
        
        break;
    }
  }
  

});
$("#origin").on("mouseleave", "span", function () {
  $('canvas').remove();
  var $t = $(this);
  var $id = parseInt($t.attr('id'));
  // if($str != -1){
  //   // var $this_list = document.getElementsByClassName('mod mod_'+($str-1));
  //   var $this_list = document.getElementsByClassName('mod mod_'+$str);
  // }else{
  //   var $this_list = document.getElementsByClassName('mod');
  // }

  if($t.hasClass("ins")){
    if($t.hasClass('loc-hovered')){
      $t.removeClass('loc-hovered');
    }
  }else{
    if($str != -1){
      //var $this_list = document.getElementsByClassName('mod mod_'+$str);
      $this_list = document.querySelectorAll('.mod.mod_'+$str+':not(.Insert)');
    }else{
      $this_list = document.querySelectorAll('.mod:not(.Insert)');
      //var $this_list = document.getElementsByClassName('mod');
    }

    for(i=0;i<$this_list.length;i++){
      var e = $this_list[i];
      var i_s = parseInt(e.getAttribute('i_start'));
      var i_e = parseInt(e.getAttribute('i_end'));
      if(i_s<= $id && i_e>= $id){
        e.setAttribute('style',"background-color: none;");
        $this_list[i].parentNode.classList.remove('feedback-hovered');
        // $this_list[i].classList.toggle('active');

        for(i_x=i_s;i_x<=i_e;i_x++){
          // document.getElementById(i_x).setAttribute('style',"background-color: none;");
          if(document.getElementById(i_x).classList.contains('loc-hovered'))
            document.getElementById(i_x).classList.remove('loc-hovered');
        }
      }
    }
  }

  
});

// Hover on history
$('#history').on("mouseover", ".mod", function () {
  
  var $t = $(this);
  var i_s = parseInt($t.attr('i_start')), i_e = parseInt($t.attr('i_end'));
  var index = Math.floor((i_s+i_e)/2 );
  for(i=i_s;i<=i_e;i++){
    document.getElementById(i).setAttribute('style','background-color: LightGray;');
  }
});

$('#history').on("mouseleave", ".mod", function () {
  $('canvas').remove();
  var $t = $(this);
  

  var i_s = parseInt($t.attr('i_start')), i_e = parseInt($t.attr('i_end'));
  for(i=i_s;i<=i_e;i++){
    e = document.getElementById(i)
    if(!e.getAttribute('class')) continue
    else if($str != -1){
      if(e.getAttribute('class').includes('mod_0') && $str==0)
        e.setAttribute('style','background-color: #ccf2ff ;');
      else if(e.getAttribute('class').includes('mod_1') && $str==1)
        e.setAttribute('style','background-color: #ebf5d6 ;');
      else if(e.getAttribute('class').includes('mod_2') && $str==2)
        e.setAttribute('style','background-color: #ffcce6 ;');
    }else{
      if(e.getAttribute('class').includes('mod_0'))
        e.setAttribute('style','background-color: #ccf2ff ;');
      else if(e.getAttribute('class').includes('mod_1'))
        e.setAttribute('style','background-color: #ebf5d6 ;');
      else if(e.getAttribute('class').includes('mod_2'))
        e.setAttribute('style','background-color: #ffcce6 ;');
    }

  }
});

// $(document).ready(function(){
    // All your normal JS code goes in here
    // $(".rating").rating();
    // $(".accordion").accordion();
// });
