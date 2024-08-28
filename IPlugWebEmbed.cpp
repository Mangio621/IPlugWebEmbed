#include "IPlugWebEmbed.h"
#include "IPlug_include_in_plug_src.h"
#include "IPlugWebEmbedUtils.h"

// Embed
#include "resources/web/embeds/EmbeddedWeb.h"
#include <tuple>
#include <fstream>
#include <sstream>

IPlugWebEmbed::IPlugWebEmbed(const InstanceInfo& info)
: Plugin(info, MakeConfig(kNumParams, kNumPresets))
{
  GetParam(kGain)->InitGain("Gain", 100, 0, 200);
  SetEditorSize(350, 600); // Set inital window width and height here.
  mEditorInitFunc = [&]() {
    /*
      Note that you need to create the GetWebViewWindow function in IPlugWebView.cpp
      wil::com_ptr<ICoreWebView2> IWebView::GetWebViewWindow() { return mWebViewWnd; }
    */
    MangioLoadURI(
      GetWebViewWindow(),
      EmbeddedWeb::WebContent
    ); 
    EnableScroll(false);
  };
  MakePreset("One", 100);
  MakePreset("Two", 50);
  MakePreset("Three", 25); 
}

void IPlugWebEmbed::OnReset()
{
  auto sr = GetSampleRate();
  mOscillator.SetSampleRate(sr);
  mGainSmoother.SetSmoothTime(20., sr);
}

bool IPlugWebEmbed::OnMessage(int msgTag, int ctrlTag, int dataSize, const void* pData)
{
  // Uncomment if you want functionality to resize the window.
  /*if (msgTag == kMsgTagButton1)
    Resize(512, 335);
  else if (msgTag == kMsgTagButton2)
    Resize(1024, 335);
  else if (msgTag == kMsgTagButton3)
    Resize(1024, 768);*/
  if (msgTag == kMsgTagBinaryTest)
  {
    auto uint8Data = reinterpret_cast<const uint8_t*>(pData);
    DBGMSG("Data Size %i bytes\n", dataSize);
    DBGMSG("Byte values: %i, %i, %i, %i\n", uint8Data[0], uint8Data[1], uint8Data[2], uint8Data[3]);
  }

  return false;
}

void IPlugWebEmbed::SendAudioDataToWebView()
{
  std::stringstream script;
  script << "OnAudioSample(" << lastAudioSample << ");";
  EvaluateJavaScript(script.str().c_str());
}

void IPlugWebEmbed::OnIdle()
{
 /* SendControlValueFromDelegate(kCtrlTagMeter, )*/
  auto test = IDLE_TIMER_RATE;
  SendAudioDataToWebView();
}

void IPlugWebEmbed::OnParamChange(int paramIdx) { DBGMSG("Cole gain %f\n", GetParam(paramIdx)->Value()); }

void IPlugWebEmbed::ProcessMidiMsg(const IMidiMsg& msg)
{
  TRACE;
  msg.PrintMsg();
  SendMidiMsg(msg);
}


void IPlugWebEmbed::ProcessBlock(sample** inputs, sample** outputs, int nFrames)
{
  const double gainPercent = GetParam(kGain)->Value() / 100;
  for (int s = 0; s < nFrames; s++)
  {
    outputs[0][s] = inputs[0][s] * gainPercent;
    outputs[1][s] = inputs[1][s] * gainPercent;
  }
  sample monoSample = (outputs[0][0] + outputs[1][0]) / 2; 
  lastAudioSample = monoSample;
}

