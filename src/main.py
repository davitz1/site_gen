import shutil
import os
import sys

from website_functions import generate_page, copy_contents, extract_title, generate_pages_recursive

def main():
    dir_source = "./static"
    dir_destination = "./docs"
 
    basepath =  '/'
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if not basepath.endswith('/'):
        basepath = basepath + '/'

    copy_contents(dir_source, dir_destination)
    generate_pages_recursive('./content', 'template.html', './docs', basepath)







if __name__ == '__main__':
    main()
