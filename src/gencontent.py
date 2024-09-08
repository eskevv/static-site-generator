import os
from markdown_block import markdown_to_html_node

def generate_pages_recursive(from_path:str, template_path:str, dest_path:str):
  print(f" * {from_path} {template_path} -> {dest_path}")
  if not os.path.isfile(from_path):
    for i in os.listdir(from_path):
      src_p = os.path.join(from_path, i) 
      dest_p =  os.path.join(dest_path, i)
      generate_pages_recursive(src_p, template_path, dest_p) 
    return
  
  dest_path = dest_path.replace(".md", ".html")

  from_file = open(from_path, "r")
  markdown_content = from_file.read()
  from_file.close()

  template_file = open(template_path, "r")
  template = template_file.read()
  template_file.close()

  node = markdown_to_html_node(markdown_content)
  html = node.to_html()

  title = extract_title(markdown_content)
  template = template.replace("{{ Title }}", title)
  template = template.replace("{{ Content }}", html)

  dest_dir_path = os.path.dirname(dest_path)
  if dest_dir_path != "":
    os.makedirs(dest_dir_path, exist_ok=True)
  to_file = open(dest_path, "w")
  to_file.write(template)


def extract_title(md):
  lines = md.split("\n")
  for line in lines:
    if line.startswith("# "):
      return line[2:]
  raise ValueError("No title found")
