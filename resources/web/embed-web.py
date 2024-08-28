'''
  embed-web.py
  author: Cole P. Mangio
  description: bundles all web assets and scripts into a single embedding to load into iPlug2's webview as a base64 encoded data URI.
    This script is run during the pre-build event through the (pre-build.bat) script
'''

import os
import mimetypes
import base64
import re
import sys
import zlib

# Filled with the tuple (file_path, mime_type, data_uri)
resource_data = []

relative_directory = "./"
if len(sys.argv) > 1:
  relative_directory = sys.argv[1]

# This function is for string vs base64 data based on mime types. If is image etc, we want to store base64, not string. If text or script, we want a string of its content.
def get_mime_type(file_path):
  mime_type, _ = mimetypes.guess_type(relative_directory + file_path)
  if (mime_type == None): 
    print("WARNING: Cannot identify mime type for: " + file_path)
  return mime_type

def is_text_or_script_file(file_path):
  mime_type = get_mime_type(file_path)
  # List of MIME types that are considered text or script
  text_or_script_mime_types = [
    'text/plain',       # .txt files
    'text/html',        # .html files
    'text/css',         # .css files
    'application/javascript',  # .js files
    'application/json', # .json files
    'application/xml',  # .xml files
  ]
  if mime_type:
    if mime_type.startswith('text/') or mime_type in text_or_script_mime_types:
      return True
    else:
      return False
  else:
    return False

def get_relative_resource_paths():
  relative_paths = []
  for dirpath, _, filenames in os.walk(relative_directory):
    for filename in filenames:
      # Get the relative file path
      relative_path = os.path.relpath(os.path.join(dirpath, filename), relative_directory)
      # Replace backslashes with forward slashes
      relative_path = relative_path.replace(os.sep, '/')
      relative_paths.append(relative_path)
  # Ignore these files
  if('embeds/EmbeddedWeb.h' in relative_path):
    relative_paths.remove('embeds/EmbeddedWeb.h')
  relative_paths.remove('embed-web.py')
  return relative_paths

def get_base64_data_uri(file_path):
  with open(relative_directory + "\\" + file_path, 'rb') as file:
    binary_data = file.read()
    base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')
  return f"data:{get_mime_type(file_path)};base64,{base64_encoded_data}"

def string_to_base64_data_uri(string_content, mime_type):
  binary_data = string_content.encode('utf-8')
  base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')
  return f"data:{mime_type};base64,{base64_encoded_data}"

# Retrieve all files and populate the resources array. Non-script assets will have their data immediately converted into a data URI.
def populate_resources(file_path):
  is_str_content = is_text_or_script_file(file_path)
  data_uri = None
  if (not is_str_content):
    data_uri = get_base64_data_uri(file_path)
  resource_data.append((
    file_path,
    get_mime_type(file_path),
    data_uri,
  ))

def replace_pattern_data_uri(search_string, data_uri, string_content):
  escaped_pattern = re.escape(search_string)
  # Regular expression to find the search string anywhere within quotes or backticks
  pattern = re.compile(rf'(["\'`])([^"\']*?{escaped_pattern}[^"\']*?)\1')
  def replace_with_data_uri(match):
    return f'{match.group(1)}{data_uri}{match.group(1)}'
  modified_content = pattern.sub(replace_with_data_uri, string_content)
  return modified_content

def encode_resources_into_scripts():
  final_html_resource = None # Will eventually have its encoded data uri
  # Iterate through all script resources other than index.html (we do this last)
  for index, resource in enumerate(resource_data):
    script_path, script_mime_type, _ = resource
    if is_text_or_script_file(script_path) and script_path != 'index.html':
      script_content = ""
      with open(relative_directory + "\\" + script_path, 'r') as file:
        script_content = file.read()
      # Replace paths as their uri instead
      for asset in resource_data:
        asset_path, _, asset_data_uri = asset
        if not is_text_or_script_file(asset_path):
          found = asset_path in script_content
          script_content = replace_pattern_data_uri(
            asset_path,
            asset_data_uri,
            script_content
          )
          if found:
            print(f"Encoded '{asset_path}' into '{script_path}'")
      resource_data[index] = (
        script_path,
        script_mime_type,
        string_to_base64_data_uri(
          script_content, 
          script_mime_type
      ))
      print(f"Finished encoding resources for '{script_path}'")
  # Encode all script/non-script resources into the index.html
  print("COMMENCING ENCODING FOR INDEX.HTML")
  for index, resource in enumerate(resource_data):
    script_path, script_mime_type, _ = resource
    if(script_path == 'index.html'):
      html_content = ""
      with open(relative_directory + "\\" + script_path, 'r') as file:
        html_content = file.read()
      for encoded_asset in resource_data:
        asset_path, _, asset_data_uri = encoded_asset
        if(asset_path != 'index.html'):
          found = asset_path in html_content
          html_content = replace_pattern_data_uri(
            asset_path,
            asset_data_uri,
            html_content
          )
          if found:
            print(f"Encoded '{asset_path}' into '{script_path}'")
      resource_data[index] = (
        script_path,
        script_mime_type,
        string_to_base64_data_uri(
          html_content,
          script_mime_type 
        )
      )
      final_html_resource = resource_data[index]
      print(f"Finished encoding resources for '{script_path}'")
  print("RESOURCES ENCODED SUCCESSFULLY")
  return final_html_resource

def split_string_every_n(input_string, n=1000):
  return [input_string[i:i + n] for i in range(
    0, len(input_string), n
  )]

def generate_embedded_web(index_content):
  directory = relative_directory + '\\' + 'embeds'
  embed_file_name = 'EmbeddedWeb.h'
  if not os.path.exists(directory):
    os.makedirs(directory)
  file_path = os.path.join(directory, embed_file_name)
  chunked_array = split_string_every_n(index_content)  
  chunked_content = ""
  for chunk in chunked_array:
    chunked_content += f'"{chunk}"\n'
  header_content = f"""
    #ifndef EMBEDDED_WEB_H
    #define EMBEDDED_WEB_H
    #include <iostream>
    namespace EmbeddedWeb {{
      const std::string WebContent = {chunked_content};
    }}
    #endif // EMBEDDED_WEB_H
  """
  with open(file_path, 'w') as file:
    file.write(header_content)
  print(f"Header file '{embed_file_name}' has been generated successfully in the 'embeds' directory.")

def main():
  # Add additional mime types here if some mime types aren't being detected
  mimetypes.add_type('font/ttf', '.ttf');
  for path in get_relative_resource_paths():
    populate_resources(path)
  encoded_html = encode_resources_into_scripts()
  for resource in resource_data:
    print(resource[0] + " | " + resource[1] + " | " + str(resource[2])[:100].replace('\n', '') + "\n")
  generate_embedded_web(encoded_html[2])

main()