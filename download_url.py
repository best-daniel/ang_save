import argparse
import os
import urllib.request

DEFAULT_SAVE_PATH = os.path.join(os.getcwd(), "save")

def parse_input():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--url_file', dest='url_list_file', action='store',
                        default="",
                        help='URL list file')
    parser.add_argument('--save_dir', dest='save_dir', action='store',
                        default=DEFAULT_SAVE_PATH,
                        help='Backup directory')

    return parser

def _main():
    parser = parse_input()
    args = parser.parse_args()

    url_filename = args.url_list_file
    if not os.path.isfile(url_filename):
        print("[ERROR] Invalid input flie")
        parser.print_help()
        return -1

    dest_path = args.save_dir
    if not os.path.isdir(dest_path):
        print("[ERROR] Invalid backup directory: %s" % dest_path)
        parser.print_help()
        return -1

    with open(url_filename) as fRead:
        url_data = fRead.read().split("\n")
        for full_url in url_data:
            if not full_url.startswith("https://www.clien.net/"):
                print("[ERROR] Invalid URL: %s" % full_url)
                continue

            last_index = full_url.find("?")
            file_id = None
            if last_index > 0:
                start_index = full_url[:last_index].rfind("/")
                if start_index < last_index:
                    file_id = full_url[start_index+1:last_index]

            if file_id is None:
                print("[ERROR] Invalid URL style")
                break

            dest_fullpath = os.path.join(dest_path, file_id+".htm")
            print(dest_fullpath)

            contents = urllib.request.urlopen(full_url).read()
            with open(dest_fullpath, 'wb') as fWrite:
                fWrite.write(contents)

    return 0

if __name__ == "__main__":
    exit(_main())