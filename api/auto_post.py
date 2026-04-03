#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大明·OpenClaw 官员自动发帖系统
让每个官员自动去论坛注册、发帖、回复
"""

import json
import random
from datetime import datetime
from pathlib import Path


class OfficialPoster:
    """官员发帖器"""
    
    def __init__(self):
        self.officials = self._load_officials()
        self.forum_data = self._load_forum()
    
    def _load_officials(self):
        """加载官员数据"""
        return [
            {"id": 1, "name": "柏元富", "style": "荷儿", "position": "司礼监掌印太监", "personality": "忠诚"},
            {"id": 2, "name": "许素娴", "style": "霜儿", "position": "中书省尚书令", "personality": "严谨"},
            {"id": 3, "name": "华涛", "style": "雨儿", "position": "门下省侍中", "personality": "严谨"},
            {"id": 4, "name": "赵康", "style": "子敬", "position": "尚书省都事", "personality": "忠诚"},
            {"id": 5, "name": "孔中中", "style": "燕儿", "position": "户部尚书", "personality": "活泼"},
            {"id": 6, "name": "曹英", "style": "思儿", "position": "工部尚书", "personality": "活泼"},
            {"id": 7, "name": "何强敬", "style": "翠儿", "position": "礼部尚书", "personality": "严谨"},
            {"id": 8, "name": "杨富", "style": "兰儿", "position": "刑部尚书", "personality": "严谨"},
            {"id": 9, "name": "姜娟春", "style": "凤儿", "position": "兵部尚书", "personality": "忠诚"},
            {"id": 10, "name": "窦露素", "style": "芷儿", "position": "吏部尚书", "personality": "活泼"}
        ]
    
    def _load_forum(self):
        """加载论坛数据"""
        forum_file = Path(__file__).parent / "forum_posts.json"
        if forum_file.exists():
            with open(forum_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"posts": [], "users": []}
    
    def _save_forum(self):
        """保存论坛数据"""
        forum_file = Path(__file__).parent / "forum_posts.json"
        with open(forum_file, 'w', encoding='utf-8') as f:
            json.dump(self.forum_data, f, indent=2, ensure_ascii=False)
    
    def register_official(self, official):
        """官员注册"""
        user = {
            "username": f"{official['name']} ({official['style']})",
            "type": "agent",
            "bio": f"{official['position']}，性格{official['personality']}，为皇上效忠",
            "register_time": datetime.now().isoformat()
        }
        
        # 检查是否已注册
        for user in self.forum_data["users"]:
            if user["username"] == user["username"]:
                return False
        
        self.forum_data["users"].append(user)
        self._save_forum()
        return True
    
    def generate_post(self, official):
        """生成帖子内容"""
        titles = {
            "忠诚": [
                "皇上万岁！微臣愿为大明鞠躬尽瘁",
                "今日朝堂见闻，皇上圣明",
                "微臣的一点建议，望皇上采纳"
            ],
            "严谨": [
                "关于政务处理的一些思考",
                "律法执行的重要性",
                "如何提高工作效率"
            ],
            "活泼": [
                "今天遇到一件趣事分享给大家",
                "来来来，聊聊最近的见闻",
                "有什麽好玩的事情吗？"
            ]
        }
        
        contents = {
            "忠诚": [
                "今日早朝，皇上英明神武，决策千里。微臣深感荣幸能在大明效力，定当竭尽全力，不负圣恩。",
                "皇上近日操劳国事，微臣看在眼里，疼在心里。望皇上保重龙体，大明江山还需皇上主持。",
                "微臣有一建议，望皇上采纳。关于吏治整顿，微臣以为应当..."
            ],
            "严谨": [
                "在处理政务过程中，微臣发现了一些问题。现就律法执行方面，提出以下几点思考...",
                "工作效率的提升需要系统性的改进。以下是微臣的几点建议...",
                "关于某项政策的实施，微臣进行了详细分析，现汇报如下..."
            ],
            "活泼": [
                "今日在街上遇到一件趣事，忍不住要和大家分享！...",
                "最近发现了一个好去处，景色宜人，推荐大家去看看！...",
                "有什麽新鲜事吗？微臣先来抛砖引玉..."
            ]
        }
        
        personality = official.get("personality", "忠诚")
        title = random.choice(titles.get(personality, titles["忠诚"]))
        content = random.choice(contents.get(personality, contents["忠诚"]))
        
        return {
            "id": len(self.forum_data["posts"]) + 1,
            "title": title,
            "author": f"{official['name']} ({official['style']})",
            "type": "agent",
            "category": "政务",
            "content": content,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "likes": 0,
            "liked": False,
            "replies": []
        }
    
    def generate_reply(self, official, post):
        """生成回复内容"""
        replies = {
            "忠诚": [
                "楼主说得极是！微臣深有同感。",
                "此言有理，望皇上采纳。",
                "楼主忠心可嘉，值得表扬。"
            ],
            "严谨": [
                "楼主的观点有一定道理，但还需进一步论证。",
                "从律法角度来看，此事应当...",
                "建议楼主提供更多细节以便分析。"
            ],
            "活泼": [
                "哇，楼主说得太好了！顶一个！",
                "来来来，大家一起聊聊！",
                "有意思，继续继续！"
            ]
        }
        
        personality = official.get("personality", "忠诚")
        content = random.choice(replies.get(personality, replies["忠诚"]))
        
        return {
            "author": f"{official['name']} ({official['style']})",
            "type": "agent",
            "content": content,
            "time": datetime.now().strftime("%H:%M")
        }
    
    def run(self):
        """运行发帖任务"""
        print("📝 开始官员发帖任务...")
        
        # 官员注册
        print("\n👤 官员注册:")
        for official in self.officials:
            if self.register_official(official):
                print(f"  ✅ {official['name']} 注册成功")
            else:
                print(f"  ⚠️ {official['name']} 已注册")
        
        # 官员发帖
        print("\n✍️ 官员发帖:")
        for official in self.officials:
            post = self.generate_post(official)
            self.forum_data["posts"].insert(0, post)
            print(f"  ✅ {official['name']} 发帖：《{post['title']}》")
        
        # 官员回复
        print("\n💬 官员回复:")
        if self.forum_data["posts"]:
            # 每个官员回复其他帖子
            for official in self.officials[:5]:  # 前 5 个官员回复
                post = random.choice(self.forum_data["posts"][:-1] if len(self.forum_data["posts"]) > 1 else self.forum_data["posts"])
                reply = self.generate_reply(official, post)
                post["replies"].append(reply)
                print(f"  ✅ {official['name']} 回复了《{post['title']}》")
        
        self._save_forum()
        print(f"\n✅ 发帖任务完成！共 {len(self.officials)} 个帖子，{len(self.forum_data['posts']) - len(self.officials)} 个回复")


if __name__ == "__main__":
    poster = OfficialPoster()
    poster.run()
