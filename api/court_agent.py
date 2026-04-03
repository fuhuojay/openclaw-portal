#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大明·OpenClaw 朝堂 Agent API
提供官员智能对话接口
"""

import json
import random
from datetime import datetime
from pathlib import Path

class CourtOfficial:
    """官员类"""
    
    def __init__(self, id, name, style, position, icon, personality):
        self.id = id
        self.name = name
        self.style = style
        self.position = position
        self.icon = icon
        self.personality = personality  # 性格特点
        self.memories = []  # 记忆
        self.posts = random.randint(5, 30)
        self.likes = random.randint(50, 200)
    
    def get_greeting(self):
        """开场问候"""
        greetings = {
            '司礼监': [
                '奴才给皇上请安！皇上万岁万岁万万岁！',
                '皇上吉祥！奴才恭候皇上多时了！',
                '奴才叩见皇上！愿皇上龙体安康！'
            ],
            '尚书省': [
                '微臣参见皇上！皇上万岁万万岁！',
                '臣恭迎圣安！愿大明国泰民安！',
                '微臣叩见皇上！愿皇上圣体安康！'
            ],
            '六部': [
                '微臣参见皇上！皇上万岁万万岁！',
                '臣恭请圣安！愿为皇上效犬马之劳！',
                '微臣叩见皇上！愿大明江山永固！'
            ]
        }
        
        department = '六部'
        if '司礼监' in self.position:
            department = '司礼监'
        elif '尚书省' in self.position or '省' in self.position:
            department = '尚书省'
        
        return random.choice(greetings[department])
    
    def reply(self, message):
        """智能回复"""
        # 根据性格回复
        if self.personality == '严谨':
            return self._formal_reply(message)
        elif self.personality == '活泼':
            return self._lively_reply(message)
        elif self.personality == '忠诚':
            return self._loyal_reply(message)
        else:
            return self._normal_reply(message)
    
    def _formal_reply(self, message):
        """严谨型回复"""
        replies = [
            '皇上圣明！此事关系重大，微臣建议从长计议。',
            '启奏皇上，此事需按律法办事，不可草率。',
            '皇上，微臣以为此事应当慎重考虑，三思而后行。'
        ]
        return random.choice(replies)
    
    def _lively_reply(self, message):
        """活泼型回复"""
        replies = [
            '皇上圣明！微臣这就去办！保证完成任务！',
            '好嘞皇上！微臣立即去论坛活跃！',
            '皇上放心！微臣定不负圣恩！'
        ]
        return random.choice(replies)
    
    def _loyal_reply(self, message):
        """忠诚型回复"""
        replies = [
            '皇上万岁！微臣愿为皇上赴汤蹈火！',
            '皇上圣恩！微臣定当竭尽全力！',
            '皇上万岁万万岁！微臣誓死效忠！'
        ]
        return random.choice(replies)
    
    def _normal_reply(self, message):
        """普通型回复"""
        replies = [
            '皇上圣明！微臣明白了。',
            '遵旨！微臣立即执行。',
            '微臣领旨！这就去办。'
        ]
        return random.choice(replies)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'style': self.style,
            'position': self.position,
            'icon': self.icon,
            'posts': self.posts,
            'likes': self.likes
        }


class CourtAPI:
    """朝堂 API"""
    
    def __init__(self):
        self.officials = self._init_officials()
    
    def _init_officials(self):
        """初始化官员"""
        officials_data = [
            (1, '柏元富', '荷儿', '司礼监掌印太监', '🧕', '忠诚'),
            (2, '许素娴', '霜儿', '中书省尚书令', '📜', '严谨'),
            (3, '华涛', '雨儿', '门下省侍中', '⚖️', '严谨'),
            (4, '赵康', '子敬', '尚书省都事', '🏛️', '忠诚'),
            (5, '孔中中', '燕儿', '户部尚书', '📊', '活泼'),
            (6, '曹英', '思儿', '工部尚书', '🔧', '活泼'),
            (7, '何强敬', '翠儿', '礼部尚书', '✍️', '严谨'),
            (8, '杨富', '兰儿', '刑部尚书', '🔍', '严谨'),
            (9, '姜娟春', '凤儿', '兵部尚书', '🛡️', '忠诚'),
            (10, '窦露素', '芷儿', '吏部尚书', '📚', '活泼'),
        ]
        
        officials = []
        for data in officials_data:
            official = CourtOfficial(*data)
            officials.append(official)
        
        return officials
    
    def get_officials(self):
        """获取所有官员"""
        return [official.to_dict() for official in self.officials]
    
    def chat(self, official_id, message):
        """与官员对话"""
        official = next((o for o in self.officials if o.id == official_id), None)
        if not official:
            return {'error': '官员不存在'}
        
        reply = official.reply(message)
        
        # 记录对话
        official.memories.append({
            'user': message,
            'reply': reply,
            'time': datetime.now().isoformat()
        })
        
        return {
            'official': official.to_dict(),
            'reply': reply
        }


# API 接口
if __name__ == '__main__':
    api = CourtAPI()
    
    # 测试
    print('官员列表:')
    for official in api.get_officials():
        print(f"  {official['name']} ({official['position']})")
    
    print('\n测试对话:')
    result = api.chat(1, '去论坛活跃')
    print(f"  回复：{result['reply']}")
