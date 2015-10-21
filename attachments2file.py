#!/usr/bin/env python3.4
'''
Usage as script:
attachments2file file1[ file2[...fileN]..]
'''
import email
import sys
import os


def header2str(str):
    if str:
        str = email.header.decode_header(str)
        encoding = str[0][1]
        str = str[0][0]
        if encoding:
            str = str.decode(encoding)
           
    return str


def print_msg(msg):
    for part in msg.walk():
        if  part.get_content_maintype() == 'text':
            print(part.get_payload())        
            continue
    
def attachments2file(msg, dir_out='.'):
    '''
    Takes message, extracts attachments and saves them to directory
    '''
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        filename = header2str(part.get_filename())
        if not filename:
            continue
        if not os.path.isdir(dir_out):
            try:
                os.mkdir(dir_out)
            except FileExistsError:
                print('Can\'t make dir to output attachments')
                return
        full_path = os.path.join(dir_out, filename)
        for count in range(1, 1000):
            if os.path.isfile(full_path):
                full_path = os.path.join(dir_out, '{:04d}_'.format(count)+filename)
        with open(full_path, 'wb') as fp:
            fp.write(part.get_payload(decode=True))
        print("\nAttachment {} is saved".format(full_path))


def main():
    if len(sys.argv) == 1:
        sys.exit('Usage: attachments2file file1[ file2[...fileN]..]')
    for arg in sys.argv[1:]:
        with open(arg) as body_f:
            msg = email.message_from_file(body_f)
        attachments2file(msg, 'attachments')


if __name__ == '__main__':
    main()
