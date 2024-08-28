/**
 * client.js
 * Your main client script. Listen to and alter the DOM here aswell as send and receive data to iPlug.
 */

function SendTestBinaryData() {
  let uint8 = new Uint8Array([0, 0, 0, 0]);
  uint8.fill(4, 1, 3);
  var bin = String.fromCharCode.apply(null, uint8);
  SAMFUI(3, -1, window.btoa(bin));
}

function SendTestMIDIData() {
  SMMFUI(0x90, 60, 0x7f);
  setTimeout(function(){
    SMMFUI(0x90, 60, 0x00);
  }, 1000);
}

function OnParamChange(param, value) {
  if(param == 0) {
    document.getElementById("gain_knob").value = value * 100;
  }
}

function OnControlChange(ctrlTag, value) {
  // if(ctrlTag == 0) {
  //   document.getElementById("meter").value = value;
  // }
  console.log(`Tag: ${ctrlTag} Value: ${value}`);
}

function onLoad() {
  document.getElementById("gain_knob").addEventListener('input', function(e) {
                                                      SPVFUI(0, e.target.value/100.)
                                                      });
}