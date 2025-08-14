import shutil
import os

from website_functions import generate_page, copy_contents, extract_title, generate_pages_recursive

def main():
    dir_source = "./static"
    dir_destination = "./public"
    copy_contents(dir_source, dir_destination)
    generate_pages_recursive('./content', 'template.html', './public')








if __name__ == '__main__':
    main()
