#pragma once

#include "IPlug_include_in_plug_hdr.h"
#include "Oscillator.h"
#include "Smoothers.h"

using namespace iplug;

const int kNumPresets = 3;

enum EParams
{
  kGain = 0,
  kNumParams
};

enum EMsgTags
{
  kMsgTagButton1 = 0,
  kMsgTagButton2 = 1,
  kMsgTagButton3 = 2,
  kMsgTagBinaryTest = 3
};

enum EControlTags
{
  kCtrlTagAudioVisualizer = 0,
};

class IPlugWebEmbed final : public Plugin
{
public:
  IPlugWebEmbed(const InstanceInfo& info);
  
  void ProcessMidiMsg(const IMidiMsg& msg) override;
  void OnReset() override;
  void OnIdle() override;
  bool OnMessage(int msgTag, int ctrlTag, int dataSize, const void* pData) override;
  void OnParamChange(int paramIdx) override;
  void ProcessBlock(sample** inputs, sample** outputs, int nFrames) override;

private:
  sample lastAudioSample;
  void SendAudioDataToWebView();
  FastSinOscillator<sample> mOscillator {0., 440.};
  LogParamSmooth<sample, 1> mGainSmoother;
};
