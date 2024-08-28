/**
 * network-hub.js
 * Abstracts functions that are called by the iPlug Backend.
 * Delegate refers to backend: WebViewEditorDelegate.h (these are where the functions are called)
 * however, you can call these functions (or your own functions) from iPlug via the EvaluateJavaScript() function
 * e.g EvaluateJavaScript("SCVFD(0, 4)");
 */

function OnAudioSample(audioSample) {
  updateVisualizerData(audioSample);
}

// On Parameter Value From Delegate
function SPVFD(paramIdx, val) {
//  console.log("paramIdx: " + paramIdx + " value:" + val);
  OnParamChange(paramIdx, val);
}

// On Control Value From Delegate
function SCVFD(ctrlTag, val) {
  OnControlChange(ctrlTag, val);
//  console.log("SCVFD ctrlTag: " + ctrlTag + " value:" + val);
}

// On Control Message From Delegate
function SCMFD(ctrlTag, msgTag, dataSize, msg) {
  //  var decodedData = window.atob(msg);
  console.log("SCMFD ctrlTag: " + ctrlTag + " msgTag:" + msgTag + " msg:" + msg);
}

// On Arbitrary Message From Delegate
function SAMFD(msgTag, dataSize, msg) {
  //  var decodedData = window.atob(msg);
  console.log("SAMFD msgTag:" + msgTag + " msg:" + msg);
}

// On Send Midi Message From Delegate
function SMMFD(statusByte, dataByte1, dataByte2) {
  console.log("Got MIDI Message" + status + ":" + dataByte1 + ":" + dataByte2);
}

// On Sysex Message From Delegate
function SSMFD(offset, size, msg) {
  console.log("Got Sysex Message");
}

// FROM UI
// data should be a base64 encoded string
function SAMFUI(msgTag, ctrlTag = -1, data = 0) {
  var message = {
    "msg": "SAMFUI",
    "msgTag": msgTag,
    "ctrlTag": ctrlTag,
    "data": data
  };
  
  IPlugSendMsg(message);
}

function SMMFUI(statusByte, dataByte1, dataByte2) {
  var message = {
    "msg": "SMMFUI",
    "statusByte": statusByte,
    "dataByte1": dataByte1,
    "dataByte2": dataByte2
  };
  
  IPlugSendMsg(message);
}

// data should be a base64 encoded string
function SSMFUI(data = 0) {
  var message = {
    "msg": "SSMFUI",
    "data": data
  };
  
  IPlugSendMsg(message);
}

function EPCFUI(paramIdx) {
  var message = {
    "msg": "EPCFUI",
    "paramIdx": paramIdx,
  };
  
  IPlugSendMsg(message);
}

function BPCFUI(paramIdx) {
  var message = {
    "msg": "BPCFUI",
    "paramIdx": paramIdx,
  };
  
  IPlugSendMsg(message);
}

function SPVFUI(paramIdx, value) {
  var message = {
    "msg": "SPVFUI",
    "paramIdx": paramIdx,
    "value": value
  };

  IPlugSendMsg(message);
}
