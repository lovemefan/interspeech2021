# -*- coding: utf-8 -*-
# @Time  : 2021/9/1 21:45
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : classify.py
import json
import re


def save2json():
    inter_speech = dict()
    with open("session.txt", encoding='utf-8') as f:
        for line in f:
            session, topic = line.strip().split(';')
            inter_speech[topic] = {"session": session.strip()}
            # print(inter_speech)

            session_paper = dict()
            with open("paper.txt", encoding='utf-8') as papers:
                for paper in papers:
                    session_id, paper_name = paper.strip().split("|")
                    if len(session_id.split()) == 2:
                        session, id = session_id.split()
                        session = session.strip()
                    else:
                        session, id = session_id, None

                    if session_paper.get(session, None):
                        session_paper[session].append({"id": int(id), "name": paper_name})
                    else:
                        session_paper[session] = []
                        session_paper[session].append({"id": int(id), "name": paper_name})

            for key, value in inter_speech.items():
                 inter_speech[key]["papers"] = sorted(session_paper[value['session']], key = lambda x: x['id'])


    with open("interspeech2021.json", 'w', encoding='utf-8') as f:
        json.dump(inter_speech, f, ensure_ascii=False)


def save_treemap():
    with open("interspeech2021.json", encoding='utf-8') as f:
        interspeech:dict = json.load(f)

    tree_map = []
    children = {}
    _map = dict()
    _map["name"] = "tree map"
    _map["value"] = 0

    for key, value in interspeech.items():

        if len(key.split(":")) == 2:
            if children.get(key.split(":")[0].strip(), None):
                children[key.split(":")[0].strip()]["children"].append({"name": key.strip(), "children": [{"name": paper["name"]} for paper in value["papers"]]})
            else:
                children[key.split(":")[0].strip()] = {}
                children[key.split(":")[0].strip()]["children"] = []
                children[key.split(":")[0].strip()]["children"].append({"name": key.strip(), "children": [{"name": paper["name"]} for paper in value["papers"]]})
        else:
            children[key.strip()] = {}
            children[key.strip()]["children"] = []
            children[key.strip()]["children"].append({"name": key.strip(), "children": [{"name": paper["name"]} for paper in value["papers"]]})

    _map["children"] = [{"name": key.strip(), "children": value["children"]} for key, value in children.items()]

    # add value
    def add_value(data: dict):
        if not data.get("children", None):
            data['value'] = 1
            return 1

        count = 0
        for item in data["children"]:
            count += add_value(item)

        data["value"] = count
        return count


    add_value(_map)
    with open("interspeech2021-tree_map.json", 'w', encoding='utf-8') as f:
        json.dump(_map, f, ensure_ascii=False)

    123

# def temp():
#     with open("paper.txt", 'r', encoding='utf-8') as papers:
#         text = papers.read()
#         text = re.sub(r'-(\d)\s', r" \1", text)
#     with open("paper.txt", 'w', encoding='utf-8') as papers:
#         papers.write(text)

if __name__ == '__main__':
    save2json()
    save_treemap()
