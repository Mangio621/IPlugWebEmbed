#pragma once
#include <iostream>
#include <fstream>
#include <codecvt>

void MangioLoadURI(
  wil::com_ptr<ICoreWebView2> webViewWindow,
  std::string htmlDataUri) {
  std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
  webViewWindow->Navigate(converter.from_bytes(htmlDataUri).c_str());
}