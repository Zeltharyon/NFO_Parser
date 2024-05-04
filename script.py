import os
import json
from pathlib import Path

projectDir = str(Path(__file__).parent).replace('\\', '/')
valid_templates = ["tvshow", "movie", "series"]
failed_files = []

input_path = input("Enter INPUT path : ")
output_path = input("Enter OUTPUT path : ")
template = input("Enter TEMPLATE (tvshow (default), movie, series) : ")
delete_original_file = input("Delete original file? (y/N) : ")
deletion_selected = False
if template == '':
    template = 'tvshow'
if input_path[len(input_path) - 1] != '/':
    input_path = input_path + '/'
if output_path[len(output_path) - 1] != '/':
    output_path = output_path + '/'
if delete_original_file == 'y':
    deletion_selected = True

if os.path.isdir(input_path) and os.path.isdir(output_path):

    template_path = projectDir + '/templates/' + template + '.nfo'

    if template in valid_templates and os.path.isfile(template_path):

        print('')
        print('Chemin des fichiers .json : ' + input_path)
        print('Chemin de sortie : ' + output_path)
        print('Fichier de template : ' + template_path + ' chargé')
        print('')

        arr = [name for name in os.listdir(input_path) if '.json' in name]
        template_file = open(template_path, encoding='utf-8')
        template_lines = template_file.readlines()

        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('')

        for name in arr:

            try:
                old_file_path = input_path + name
                new_file_path = output_path + name[0:len(name) - len('.info.json')] + '.nfo'

                json_file = open(old_file_path, encoding='utf8')
                data = json.load(json_file)
                new_file = open(new_file_path, "w", encoding='utf8')
                file_content = ''

                date_to_str = str(data['upload_date'])
                try:
                    data['playlist_index'] = str(data['playlist_index'])
                except KeyError:
                    data['playlist_index'] = '1'
                data['upload_date'] = date_to_str[0:4] + '-' + date_to_str[4:6] + '-' + date_to_str[6:8]

                for line in template_lines:
                    new_line = ''
                    if 'json_keys' in line:
                        while 'json_keys' in line:
                            start = line.index('json_keys')
                            sub_line = line[start:]
                            end = sub_line.index(')') + (len(line) - len(sub_line)) + 1
                            key = sub_line[len('json_keys('):sub_line.index(')')]
                            json_values = list(data[key])
                            lines = []
                            if len(json_values) > 3:
                                json_values = json_values[0:3]
                            for val in json_values:
                                ln = line.replace(line[start:end], val)
                                file_content += ln
                            line = ''
                    elif 'json_key' in line:
                        while 'json_key' in line:
                            start = line.index('json_key')
                            sub_line = line[start:]
                            end = sub_line.index(')') + (len(line) - len(sub_line)) + 1
                            key = sub_line[len('json_key('):sub_line.index(')')]
                            json_value = data[key]
                            line = line.replace(line[start:end], json_value)
                        file_content += line
                    else:
                        file_content += line

                new_file.write(file_content)
                new_file.close()
                if deletion_selected:
                    os.remove(old_file_path)
                print(new_file_path + " : FINISHED")
            except KeyError:
                failed_files.append(name)

        print('')
        if len(failed_files) > 0:
            print("Some files were rejected : ")
            for file_name in failed_files:
                print('- ' + file_name)
    else:
        print("No valid template entered, end of process")

else:
    print("No valid paths entered, end of process")
