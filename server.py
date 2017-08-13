from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)


@app.route('/')
def route_index():
    table = get_table_from_file("notes.csv")
    return render_template('list.html', table=table)


@app.route('/new-note')
def route_new_note():
    note_text = None
    if 'note' in session:
        note_text = session['note']
    return render_template('form.html')


@app.route('/edit-note/<story_id>')
def route_edit(story_id):
    cur_story = None
    print("story_id: {}".format(story_id))
    for story in table:
        if story_id == story[0]:
            print('in')
            cur_story = story
    print("cur_story: {}".format(cur_story))
    return render_template('form.html', story=cur_story)


@app.route('/story', methods=['POST'])
def route_save():
    print('POST request received by route_save!')
    table = get_table_from_file("notes.csv")
    print(table)
    story = dict()
    for key in request.form.keys():
        story.update({key: request.form[key]})
    story.update({"id": id_gen()})
    tmp_dict = dict_from_table(table)
    tmp_dict.append(story)
    table = table_from_dict(tmp_dict)
    export_table(table)
    return redirect('/')


@app.route('/story/<story_id>', methods=['POST'])
def route_save_edit(story_id):
    print('POST request received by story edit!')
    table = get_table_from_file("notes.csv")
    keylog = request.form.keys()
    story = dict()
    for key in keylog:
        story.update({key: request.form[key]})
    story.update({"id": story_id})
    tmp_dict = dict_from_table(table)
    for item in tmp_dict:
        if story_id == item['id']:
            for key in story.keys():
                item[key] = story[key]
    table = table_from_dict(tmp_dict)
    export_table(table)
    return redirect('/')


@app.route('/delete-story/<story_id>')
def route_delete(story_id):
    for story in table:
        if story_id == story[0]:
            table.remove(story)
    export_table(table)
    return redirect('/')


def id_gen():
    table = get_table_from_file("notes.csv")
    if len(table) == 0:
        tmp_id = 1
        return str(tmp_id)
    if len(table) == 1:
        tmp_id = int(table[0][0])+1
        return str(tmp_id)
    tmp_id = int(table[0][0])
    for row in table:
        if (int(row[0]) - tmp_id) < 2:
            tmp_id = int(row[0])
        else:
            tmp_id = int(row[0]) - 1
            return str(tmp_id)
    tmp_id += 1
    print(tmp_id)
    return str(tmp_id)


def get_table_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(";") for element in lines]
    return table


def dict_from_table(table):
    list_ = list()
    for line in table:
        dict_ = dict()
        dict_.update({'id': line[0]})
        dict_.update({'story-title': line[1]})
        dict_.update({'user-story': line[2]})
        dict_.update({'acceptance-criteria': line[3]})
        dict_.update({'value': line[4]})
        dict_.update({'estimation': line[5]})
        dict_.update({'status': line[6]})
        list_.insert(int(dict_['id'])-1, dict_)
    return list_


def table_from_dict(dictionary):
    big_list = list()
    for element in dictionary:
        lil_list = list()
        lil_list.append(element['id'])
        lil_list.append(element['story-title'])
        lil_list.append(element['user-story'])
        lil_list.append(element['acceptance-criteria'])
        lil_list.append(element['value'])
        lil_list.append(element['estimation'])
        lil_list.append(element['status'])
        big_list.insert(int(lil_list[0])-1, lil_list)
    return big_list


def export_table(table):
    with open("notes.csv", "w") as file:
        for note in table:
            row = ';'.join(note)
            file.write(row + "\n")


table = get_table_from_file("notes.csv")


if __name__ == "__main__":
    app.secret_key = 'M4zsol4p4tkany'
    app.run(
      debug=True,  # Allow verbose error reports
      port=5000  # Set custom port
      )
