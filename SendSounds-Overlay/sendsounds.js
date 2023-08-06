let evt = new Event('click');

$(document).ready(function () {
  if (typeof API_Key === 'undefined') {
    $('body').html(
      '<div><br></div>' +
        "<div id='error' class='ui negative message'>" +
        "<h1 style='text-align: center;'> No API Key found!</h1>" +
        '<p style=\'text-align: center; color: black;\'>Right-click on the script in Streamlabs Chatbot and select "Insert API Key"</p>' +
        '</div>'
    );
    $('body').css({ 'background-color': '#1b1c1d' });
    $('#error').css({
      'max-width': '80%',
      'margin-left': 'auto',
      'margin-right': 'auto',
    });
  } else {
    connectWebsocket();
    document.addEventListener('click', function () {
      console.log('A click as forced by a virtual event');
    });
  }
});

function connectWebsocket() {
  var socket = new WebSocket('ws:127.0.0.1:3337/streamlabs');
  socket.onopen = function (message) {
    var auth = {
      author: 'von_Schappler',
      website: 'http://rebrand.ly/vonWebsite',
      api_key: API_Key,
      events: ['EVENT_SENDSOUNDS'],
    };
    socket.send(JSON.stringify(auth));
  };
  socket.onclose = function () {
    socket = null;
    setTimeout(connecWebsocket, 10000);
  };
  socket.onmessage = function (message) {
    console.log(message);
    var msg = JSON.parse(message.data);
    if (msg.event == 'EVENT_SENDSOUNDS') {
      soundData = JSON.parse(msg.data);
      document.dispatchEvent(evt);
      processData(soundData);
    }
  };
}

function processData(info) {
  var sfx = info.audio;
  var sfxAudio = new Audio(sfx);
  sfxAudio.play();
  sfxAudio.volume = info.volume / 100;
  sfxAudio.onended = function () {
    sfxAudio.src = '';
  };
}
