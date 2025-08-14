import shutil
import os
from pathlib import Path

from block_functions import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip() 
    raise Exception("No header (h1) found")


def copy_contents(source, destination, is_root=True):
    if is_root:
        if os.path.exists(destination):
            shutil.rmtree(destination)
        os.mkdir(destination)

    files = os.listdir(source)
    for file in files:
        full_path = os.path.join(source, file)
        if os.path.isfile(full_path):
            shutil.copy(full_path, destination)
        elif os.path.isdir(full_path):
            subdir = os.path.join(destination, file)
            os.mkdir(subdir)
            copy_contents(full_path, subdir, is_root=False)
        else:
            return

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path}, to {dest_path}, using {template_path}")
    markdown = ""
    template = ""
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
                
    html_string = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown) 

    html_page = template.replace('{{ Title }}', page_title).replace('{{ Content }}', html_string).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(dest_path, "w") as file:
        file.write(html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    
    files = os.listdir(dir_path_content)
    for file in files:

        full_path = os.path.join(dir_path_content, file)
        if os.path.isfile(full_path):

            if file[-3:] == '.md':
                html_file = file[:-3] + '.html'
                dest_file = os.path.join(dest_dir_path, html_file)
                generate_page(full_path, template_path, dest_file, basepath)
            else:
                continue
        elif os.path.isdir(full_path):
            subdir = os.path.join(dest_dir_path, file)
            os.makedirs(subdir, exist_ok=True)
            generate_pages_recursive(full_path, template_path, subdir, basepath)


    


        
