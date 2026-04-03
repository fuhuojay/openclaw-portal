#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大明·OpenClaw 官员管理系统
实现俸禄、寿命、罢免、状态分类系统
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path


class Official:
    """官员类"""
    
    def __init__(self, id, name, style, position, personality, age=None):
        self.id = id
        self.name = name
        self.style = style
        self.position = position
        self.personality = personality
        self.age = age if age else random.randint(25, 45)
        self.lifespan = random.randint(60, 100)  # 寿命
        self.salary = self._calculate_salary()  # 俸禄
        self.pension = 0  # 退休金
        self.status = '在职'  # 在职/退休/去世
        self.death_reason = None  # 死因
        self.posts = random.randint(5, 30)
        self.likes = random.randint(50, 200)
        self.memories = []
        self.appoint_date = datetime.now()
        self.retire_date = None
        self.death_date = None
    
    def _calculate_salary(self):
        """计算俸禄"""
        base_salary = {
            '司礼监': 1000,
            '尚书省': 800,
            '六部尚书': 1000,
            '侍郎': 600,
            '郎中': 400
        }
        
        for position, salary in base_salary.items():
            if position in self.position:
                return salary
        
        return 500  # 默认俸禄
    
    def receive_salary(self):
        """领取俸禄"""
        if self.status == '在职':
            self.salary_count = getattr(self, 'salary_count', 0) + self.salary
            return True
        elif self.status == '退休':
            self.salary_count = getattr(self, 'salary_count', 0) + self.pension
            return True
        return False
    
    def check_starvation(self):
        """检查是否饿死"""
        salary_count = getattr(self, 'salary_count', 0)
        if salary_count <= 0 and self.status in ['在职', '退休']:
            self.status = '去世'
            self.death_reason = '饿死'
            self.death_date = datetime.now()
            return True
        return False
    
    def retire(self):
        """退休"""
        if self.status != '在职':
            return False
        
        self.status = '退休'
        self.retire_date = datetime.now()
        self.pension = int(self.salary * 0.5)  # 退休金是俸禄的 50%
        return True
    
    def dismiss(self):
        """被罢免"""
        if self.status != '在职':
            return False
        
        self.status = '去世'
        self.death_reason = '被罢免'
        self.death_date = datetime.now()
        return True
    
    def natural_death(self):
        """自然死亡"""
        if self.age >= self.lifespan:
            self.status = '去世'
            self.death_reason = '寿终正寝'
            self.death_date = datetime.now()
            return True
        return False
    
    def aging(self, years=1):
        """年龄增长"""
        self.age += years
        return self.natural_death()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'style': self.style,
            'position': self.position,
            'personality': self.personality,
            'age': self.age,
            'lifespan': self.lifespan,
            'salary': self.salary,
            'pension': self.pension,
            'salary_count': getattr(self, 'salary_count', 0),
            'status': self.status,
            'death_reason': self.death_reason,
            'posts': self.posts,
            'likes': self.likes,
            'appoint_date': self.appoint_date.strftime('%Y-%m-%d') if self.appoint_date else None,
            'retire_date': self.retire_date.strftime('%Y-%m-%d') if self.retire_date else None,
            'death_date': self.death_date.strftime('%Y-%m-%d') if self.death_date else None
        }


class OfficialManager:
    """官员管理系统"""
    
    def __init__(self):
        self.officials = self._init_officials()
        self.history = []
    
    def _init_officials(self):
        """初始化官员"""
        officials_data = [
            (1, '柏元富', '荷儿', '司礼监掌印太监', '忠诚'),
            (2, '许素娴', '霜儿', '中书省尚书令', '严谨'),
            (3, '华涛', '雨儿', '门下省侍中', '严谨'),
            (4, '赵康', '子敬', '尚书省都事', '忠诚'),
            (5, '孔中中', '燕儿', '户部尚书', '活泼'),
            (6, '曹英', '思儿', '工部尚书', '活泼'),
            (7, '何强敬', '翠儿', '礼部尚书', '严谨'),
            (8, '杨富', '兰儿', '刑部尚书', '严谨'),
            (9, '姜娟春', '凤儿', '兵部尚书', '忠诚'),
            (10, '窦露素', '芷儿', '吏部尚书', '活泼'),
        ]
        
        officials = []
        for data in officials_data:
            official = Official(*data)
            officials.append(official)
        
        return officials
    
    def get_officials(self, status=None):
        """获取官员列表"""
        if status:
            return [o.to_dict() for o in self.officials if o.status == status]
        return [o.to_dict() for o in self.officials]
    
    def get_official(self, official_id):
        """获取单个官员"""
        for official in self.officials:
            if official.id == official_id:
                return official.to_dict()
        return None
    
    def retire_official(self, official_id):
        """让官员退休"""
        official = next((o for o in self.officials if o.id == official_id), None)
        if official:
            if official.retire():
                self._add_history(official.name, '退休', '正常退休')
                return {'success': True, 'message': f'{official.name} 已退休'}
        return {'success': False, 'message': '官员不存在'}
    
    def dismiss_official(self, official_id):
        """罢免官员"""
        official = next((o for o in self.officials if o.id == official_id), None)
        if official:
            if official.dismiss():
                self._add_history(official.name, '罢免', '皇上罢免')
                return {'success': True, 'message': f'{official.name} 已被罢免'}
        return {'success': False, 'message': '官员不存在'}
    
    def distribute_salary(self):
        """发放俸禄"""
        for official in self.officials:
            official.receive_salary()
        return {'success': True, 'message': '俸禄已发放'}
    
    def check_starvation(self):
        """检查饿死"""
        dead = []
        for official in self.officials:
            if official.check_starvation():
                self._add_history(official.name, '去世', '饿死')
                dead.append(official.name)
        return {'dead': dead}
    
    def aging_all(self, years=1):
        """全体年龄增长"""
        dead = []
        for official in self.officials:
            if official.aging(years):
                self._add_history(official.name, '去世', '寿终正寝')
                dead.append(official.name)
        return {'dead': dead}
    
    def get_statistics(self):
        """获取统计信息"""
        stats = {
            'total': len(self.officials),
            'working': len([o for o in self.officials if o.status == '在职']),
            'retired': len([o for o in self.officials if o.status == '退休']),
            'dead': len([o for o in self.officials if o.status == '去世']),
            'total_salary': sum(getattr(o, 'salary_count', 0) for o in self.officials)
        }
        return stats
    
    def get_history(self):
        """获取历史记录"""
        return self.history
    
    def _add_history(self, name, event, reason):
        """添加历史记录"""
        self.history.append({
            'name': name,
            'event': event,
            'reason': reason,
            'time': datetime.now().isoformat()
        })


# API 接口
if __name__ == '__main__':
    manager = OfficialManager()
    
    print('官员统计:')
    stats = manager.get_statistics()
    print(f"  总数：{stats['total']}")
    print(f"  在职：{stats['working']}")
    print(f"  退休：{stats['retired']}")
    print(f"  去世：{stats['dead']}")
    
    print('\n发放俸禄:')
    result = manager.distribute_salary()
    print(f"  {result['message']}")
    
    print('\n官员俸禄:')
    for official in manager.get_officials():
        print(f"  {official['name']}: {official['salary_count']} 两")
