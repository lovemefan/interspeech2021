# -*- coding: utf-8 -*-
# @Time  : 2021/9/1 21:45
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : classify.py
import json
import re

from tqdm import tqdm


def save2json():
    inter_speech = dict()
    with open("../data/session.txt", encoding='utf-8') as f:
        for line in f:
            session, topic = line.strip().split(';')
            inter_speech[topic] = {"session": session.strip()}
            # print(inter_speech)

            session_paper = dict()
            with open("../data/paper.txt", encoding='utf-8') as papers:
                for paper in papers:
                    session_id, paper_name, uri = paper.strip().split("|")
                    paper_name = f"{paper_name}|{uri.replace('/IS2021/HTML/AUTHOR', '/papers')}"
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
                 inter_speech[key]["papers"] = sorted(session_paper[value['session']], key=lambda x: x['id'])


    with open("../data/interspeech2021.json", 'w', encoding='utf-8') as f:
        json.dump(inter_speech, f, ensure_ascii=False)


def save_treemap():
    with open("../data/interspeech2021.json", encoding='utf-8') as f:
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
    with open("../data/interspeech2021-tree_map.json", 'w', encoding='utf-8') as f:
        json.dump(_map, f, ensure_ascii=False)


def generate_paper_list():
    count = 0
    papers_uri = set()
    with open("../data/paper.txt", 'w', encoding='utf-8') as paper_file:
        with open("../data/WELCOME.HTM", "r", encoding="utf-8") as file:
            pattern = re.compile(".*?IS\d+\.PDF.*?$", re.I)
            for line in tqdm(file):
                is_paper = pattern.match(line)
                if is_paper:
                    uri = re.findall("/IS2021/HTML/AUTHOR/IS\d+.PDF", line)[0]
                    if uri not in papers_uri:
                        papers_uri.add(uri)
                        info = re.findall("\[\[.*?\]\]", line)[0].replace("[", "").replace("]", "")
                        session, paper_name = info.split("|")

                        # 细分session
                        session = session.replace('&amp', '').replace(";", '')
                        session = re.split("(\d+)", session)

                        session[2] = ' '
                        session = "".join(session)

                        paper_name = paper_name.split("—")[-1].strip()
                        paper_file.write(f"{session}|{paper_name}|{uri}\n")
                        count += 1
                        # print(count)



if __name__ == '__main__':
    generate_paper_list()
    save2json()
    save_treemap()
