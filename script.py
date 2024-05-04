import os
import json
import sys

input_path = sys.argv[1]
output_path = sys.argv[2]
template_path = sys.argv[3]

print('')
print('Chemin des fichiers .json : ' + input_path)
print('Chemin de sortie : ' + output_path)
print('Fichier de template : ' + template_path + ' chargé')
print('')

arr = [name for name in os.listdir(input_path) if '.json' in name]
template_file = open(template_path, encoding='utf-8')

print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
print('')

for name in arr:

    old_file_path = input_path + name
    new_file_path = output_path + name[0:len(name)-len('.info.json')] + '.nfo'

    json_file = open(old_file_path, encoding='utf8')
    data = json.load(json_file)
    new_file = open(new_file_path, "w", encoding='utf8')

    date_to_str = str(data['upload_date'])
    data['upload_date'] = date_to_str[0:4] + '-' + date_to_str[4:6] + '-' + date_to_str[6:8]

    file_content = ''
    for line in template_file.readlines():
        new_line = ''
        try:
            start = line.index('json_key')
            sub_line = line[start:]
            end = sub_line.index(')') + (len(line) - len(sub_line)) + 1
            key = sub_line[len('json_key('):sub_line.index(')')]
            json_value = data[key]
            new_line = line.replace(line[start:end], json_value)
        except ValueError:
            new_line = line
        file_content += new_line

    new_file.write(file_content)
    new_file.close()
    print(new_file_path + " : FINISHED")
print('')
