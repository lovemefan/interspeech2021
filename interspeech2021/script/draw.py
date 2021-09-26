# -*- coding: utf-8 -*-
# @Time  : 2021/9/2 10:27
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : draw.py
import json

from pyecharts.charts import Pie, TreeMap, Bar, WordCloud
import pyecharts.options as opts
from pyecharts.faker import Faker


def draw_pie():
    with open("../data/interspeech2021.json", 'r', encoding='utf-8') as f:
        interspeech: dict = json.loads(f.read())


    interspeech_inner = {}

    for key, value in interspeech.items():
        if interspeech_inner.get(key.split(':')[0], None):
            interspeech_inner[key.split(':')[0]] += len(value['papers'])
        else:
            interspeech_inner[key.split(':')[0]] = 0
            interspeech_inner[key.split(':')[0]] += len(value['papers'])

    inner_x_data = interspeech_inner.keys()
    inner_y_data = interspeech_inner.values()

    inner_data_pair = [list(z) for z in zip(inner_x_data, inner_y_data)]

    outer_x_data = interspeech.keys()
    outer_y_data = [len(value['papers']) for value in interspeech.values()]
    outer_data_pair = [list(z) for z in zip(outer_x_data, outer_y_data)]

    (
        Pie(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add(
            series_name="访问来源",
            data_pair=inner_data_pair,
            radius=[0, "30%"],
            label_opts=opts.LabelOpts(position="inner"),
        )
            .add(
            series_name="访问来源",
            radius=["40%", "55%"],
            data_pair=outer_data_pair,
            # label_opts=opts.LabelOpts(
            #     position="outside",
            #     formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            #     background_color="#eee",
            #     border_color="#aaa",
            #     border_width=1,
            #     border_radius=4,
            #     rich={
            #         "a": {"color": "#999", "lineHeight": 22, "align": "center"},
            #         "abg": {
            #             "backgroundColor": "#e3e3e3",
            #             "width": "100%",
            #             "align": "right",
            #             "height": 22,
            #             "borderRadius": [4, 4, 0, 0],
            #         },
            #         "hr": {
            #             "borderColor": "#aaa",
            #             "width": "100%",
            #             "borderWidth": 0.5,
            #             "height": 0,
            #         },
            #         "b": {"fontSize": 16, "lineHeight": 33},
            #         "per": {
            #             "color": "#eee",
            #             "backgroundColor": "#334455",
            #             "padding": [2, 4],
            #             "borderRadius": 2,
            #         },
            #     },
            # ),
        )
            .set_global_opts(legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"))
        #     .set_series_opts(
        #     tooltip_opts=opts.TooltipOpts(
        #         trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        #     )
        # )
            .render("nested_pies.html")
    )


def draw_treemap():
    with open("../data/interspeech2021-tree_map.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    (
        TreeMap(init_opts=opts.InitOpts(width="1900px", height="890px"))
            .add(
            series_name="option",
            data=data["children"],
            visual_min=500,
            leaf_depth=1,
            # 标签居中为 position = "inside"
            label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(
                title="Interspeech 2021 论文分布", subtitle="2021/9/2", pos_left="leafDepth"
            ),
        )
            .render("../../docs/Interspeech2021.html")
    )


def draw_bar():
    with open("../data/interspeech2021-tree_map.json", 'r', encoding='utf-8') as f:
        data: dict = json.load(f)["children"]

    bar_data = []
    for item in data:
        bar_data.append((item["name"], item["value"]))
    # data of top 10
    bar_data = sorted(bar_data, key=lambda x: x[1])[-10:]

    x_data = []
    y_data = []
    for item in bar_data:
        x_data.append(item[0])
        y_data.append(item[1])

    c = (
        Bar(init_opts=opts.InitOpts(width="2400px", height="890px"))
            .add_xaxis(x_data)
            .add_yaxis("论文数量", y_data, gap="50%")
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title="interspeech top 10 session"))
            .reversal_axis()
            .render("interspeech2021_bar.html")
    )

def draw_session_pie(session):
    asr_topic = []
    with open("../data/interspeech2021-tree_map.json", 'r', encoding='utf-8') as f:
        data: dict = json.load(f)["children"]
        for item in data:
            if item["name"] == session:
                asr_data = item["children"]
                for topic in asr_data:
                    asr_topic.append([topic["name"], topic["value"]])


    c = (
        Pie(init_opts=opts.InitOpts(width="3000px", height="1500px"))
            .add(
            "",
            asr_topic,
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-富文本示例"))
            .render(f"../../docs/interspeech_{session}.html")
    )


def draw_session_cloud(session: str):
    words = {}
    with open("../../docs/asr_paer", 'w', encoding='utf-8') as asr:
        with open("../data/interspeech2021-tree_map.json", 'r', encoding='utf-8') as f:
            data: dict = json.load(f)["children"]
            for item in data:
                if item["name"] == session:
                    asr_data = item["children"]
                    for topic in asr_data:
                        for paper in topic["children"]:
                            asr.writelines(paper["name"] + '\n')
                            delete_words = ['for', 'and', 'of', 'with', 'in', 'a', 'on', 'using', 'to', 'the'
                                            'the', 'by']
                            for word in paper["name"].split():
                                if word.lower() not in delete_words:
                                    if words.get(word, None):
                                        words[word] += 1
                                    else:
                                        words[word] = 1

    data: [] = sorted([(key, value) for key, value in words.items()], key=lambda x: x[1])
    data.reverse()
    data = data[:50]



    (
        WordCloud(init_opts=opts.InitOpts(width="3000px", height="3000px"))
            .add(series_name="热点分析", data_pair=data, word_size_range=[60, 660])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=25)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
            .render(f"{session}_wordcloud.html")
    )

if __name__ == '__main__':
    draw_treemap()
    # draw_session_pie("Speech Synthesis")
    # draw_session_pie("Topics in ASR")
    # draw_session_cloud("Topics in ASR")
    # draw_session_cloud("Speech Synthesis")
