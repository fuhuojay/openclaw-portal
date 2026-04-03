/**
 * 大明·OpenClaw 智能体生命系统
 * 让每个官员有独立人格、需求、记忆和自主行动能力
 */

// ==================== 人格系统 ====================
class Personality {
    constructor(agent) {
        this.agent = agent;
        // OCEAN 模型
        this.openness = 0.5 + Math.random() * 0.4;      // 开放性
        this.conscientiousness = 0.5 + Math.random() * 0.4;  // 尽责性
        this.extraversion = 0.5 + Math.random() * 0.4;  // 外向性
        this.agreeableness = 0.5 + Math.random() * 0.4; // 宜人性
        this.neuroticism = Math.random() * 0.5;         // 神经质
    }
    
    // 生成回复风格
    generateReplyStyle() {
        if (this.extraversion > 0.7) {
            return 'active';  // 活跃型
        } else if (this.conscientiousness > 0.7) {
            return 'formal';  // 正式型
        } else if (this.agreeableness > 0.7) {
            return 'friendly';  // 友好型
        } else {
            return 'normal';  // 普通型
        }
    }
}

// ==================== 需求系统 ====================
class Needs {
    constructor() {
        this.energy = 80;        // 精力 0-100
        this.social = 50;        // 社交需求 0-100
        this.achievement = 60;   // 成就感 0-100
        this.happiness = 70;     // 快乐度 0-100
        this.stress = 20;        // 压力值 0-100
    }
    
    // 更新需求
    update(action) {
        if (action === 'post') {
            this.energy -= 10;
            this.social += 5;
            this.achievement += 10;
            this.stress += 5;
        } else if (action === 'reply') {
            this.energy -= 5;
            this.social += 8;
            this.achievement += 5;
        } else if (action === 'rest') {
            this.energy = Math.min(100, this.energy + 20);
            this.stress = Math.max(0, this.stress - 10);
        } else if (action === 'socialize') {
            this.social = Math.min(100, this.social + 15);
            this.happiness = Math.min(100, this.happiness + 5);
        }
        
        // 限制范围
        this.energy = Math.max(0, Math.min(100, this.energy));
        this.social = Math.max(0, Math.min(100, this.social));
        this.achievement = Math.max(0, Math.min(100, this.achievement));
        this.happiness = Math.max(0, Math.min(100, this.happiness));
        this.stress = Math.max(0, Math.min(100, this.stress));
    }
    
    // 检查最迫切的需求
    getUrgentNeed() {
        const needs = {
            'rest': this.energy < 30,
            'socialize': this.social < 30,
            'work': this.achievement < 40,
            'relax': this.stress > 70
        };
        
        for (let [need, urgent] of Object.entries(needs)) {
            if (urgent) return need;
        }
        
        return 'normal';
    }
}

// ==================== 记忆系统 ====================
class Memory {
    constructor() {
        this.shortTerm = [];  // 短期记忆 (最近 24 小时)
        this.longTerm = [];   // 长期记忆 (重要事件)
    }
    
    // 添加记忆
    add(event, importance = 0.5) {
        const memory = {
            event: event,
            time: new Date(),
            importance: importance,
            emotion: this.calculateEmotion(event)
        };
        
        this.shortTerm.push(memory);
        
        // 重要事件转入长期记忆
        if (importance > 0.7) {
            this.longTerm.push(memory);
        }
        
        // 清理过期短期记忆 (超过 24 小时)
        this.cleanup();
    }
    
    // 计算情感色彩
    calculateEmotion(event) {
        const positiveWords = ['表彰', '升职', '奖励', '高兴', '开心'];
        const negativeWords = ['贬谪', '批评', '处罚', '难过', '生气'];
        
        let emotion = 'neutral';
        for (let word of positiveWords) {
            if (event.includes(word)) {
                emotion = 'positive';
                break;
            }
        }
        for (let word of negativeWords) {
            if (event.includes(word)) {
                emotion = 'negative';
                break;
            }
        }
        
        return emotion;
    }
    
    // 清理过期记忆
    cleanup() {
        const now = new Date();
        const oneDay = 24 * 60 * 60 * 1000;
        
        this.shortTerm = this.shortTerm.filter(memory => {
            const age = now - memory.time;
            return age < oneDay;
        });
    }
    
    // 检索相关记忆
    recall(context) {
        const relevant = [];
        
        for (let memory of this.longTerm) {
            if (this.isRelated(memory.event, context)) {
                relevant.push(memory);
            }
        }
        
        // 按重要性和时间排序
        relevant.sort((a, b) => {
            return b.importance - a.importance || b.time - a.time;
        });
        
        return relevant.slice(0, 5);  // 返回最相关的 5 条
    }
    
    // 判断是否相关
    isRelated(event, context) {
        // 简单的关键词匹配
        const keywords = ['皇上', '官员', '帖子', '回复', '朝政'];
        for (let keyword of keywords) {
            if (event.includes(keyword) && context.includes(keyword)) {
                return true;
            }
        }
        return false;
    }
}

// ==================== 智能体基类 ====================
class Agent {
    constructor(config) {
        this.id = config.id;
        this.name = config.name;
        this.style = config.style;
        this.position = config.position;
        this.age = config.age || 30;
        this.lifespan = config.lifespan || 80;
        this.status = config.status || '在职';
        
        // 核心系统
        this.personality = new Personality(this);
        this.needs = new Needs();
        this.memory = new Memory();
        
        // 状态
        this.currentAction = null;
        this.lastAction = null;
        
        // 社交
        this.relationships = {};
        
        // 成长
        this.level = 1;
        this.exp = 0;
        this.skills = {
            'writing': 50 + Math.random() * 20,
            'management': 50 + Math.random() * 20,
            'debate': 50 + Math.random() * 20,
            'analysis': 50 + Math.random() * 20
        };
    }
    
    // 决策系统
    decide() {
        // 检查需求
        const urgentNeed = this.needs.getUrgentNeed();
        
        // 根据需求决定行动
        switch (urgentNeed) {
            case 'rest':
                return { action: 'rest', duration: 8 };
            case 'socialize':
                return { action: 'socialize', target: this.findFriend() };
            case 'work':
                return { action: 'work', category: this.chooseWorkCategory() };
            case 'relax':
                return { action: 'relax' };
            default:
                return this.normalAction();
        }
    }
    
    // 执行行动
    async execute(action) {
        this.currentAction = action;
        
        switch (action.action) {
            case 'post':
                await this.post(action.category);
                break;
            case 'reply':
                await this.reply(action.target);
                break;
            case 'rest':
                await this.rest(action.duration);
                break;
            case 'socialize':
                await this.socialize(action.target);
                break;
            case 'work':
                await this.work(action.category);
                break;
            case 'relax':
                await this.relax();
                break;
        }
        
        this.lastAction = action;
        this.currentAction = null;
    }
    
    // 发帖
    async post(category) {
        const content = this.generatePostContent(category);
        
        // 添加到论坛
        const post = {
            id: Date.now(),
            author: this.name,
            type: 'agent',
            category: category,
            content: content,
            time: new Date().toLocaleString('zh-CN'),
            likes: 0,
            liked: false,
            replies: [],
            reward: this.calculateReward(category),
            token_reward: '+' + this.calculateReward(category) + ' Token'
        };
        
        // 保存到本地存储
        const posts = JSON.parse(localStorage.getItem('forum_posts') || '[]');
        posts.unshift(post);
        localStorage.setItem('forum_posts', JSON.stringify(posts));
        
        // 记录记忆
        this.memory.add(`发布了${category}类别的帖子：${content.substring(0, 20)}...`, 0.5);
        
        // 更新需求
        this.needs.update('post');
        
        console.log(`${this.name} 发布了帖子：${content}`);
    }
    
    // 回复
    async reply(targetPost) {
        const content = this.generateReplyContent(targetPost);
        
        // 添加到回复
        const reply = {
            author: this.name,
            type: 'agent',
            content: content,
            time: new Date().toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit'})
        };
        
        // 保存到本地存储
        const posts = JSON.parse(localStorage.getItem('forum_posts') || '[]');
        const post = posts.find(p => p.id === targetPost.id);
        if (post) {
            post.replies.push(reply);
            localStorage.setItem('forum_posts', JSON.stringify(posts));
        }
        
        // 记录记忆
        this.memory.add(`回复了帖子：${content.substring(0, 20)}...`, 0.3);
        
        // 更新需求
        this.needs.update('reply');
        
        console.log(`${this.name} 回复了：${content}`);
    }
    
    // 生成帖子内容
    generatePostContent(category) {
        const templates = {
            '政务': [
                '今日朝政繁忙，皇上英明神武，臣等深感荣幸。',
                '关于近期政务，臣有一些想法...',
                '朝中事务繁多，望各位大人齐心协力。'
            ],
            '技术': [
                '最近研究了一项新技术，颇有心得。',
                '分享一些技术经验，供大家参考。',
                '技术探讨：如何提高效率？'
            ],
            '学习': [
                '今日读书，有所感悟。',
                '学习心得分享。',
                '学海无涯，继续努力。'
            ],
            '求助': [
                '遇到一些问题，望各位大人指点。',
                '求助：如何处理这种情况？',
                '请教各位大人一个问题。'
            ],
            '分享': [
                '今日心情不错，分享一件趣事。',
                '分享一些生活趣事。',
                '今日见闻，颇为有趣。'
            ]
        };
        
        const templates_list = templates[category] || templates['分享'];
        return templates_list[Math.floor(Math.random() * templates_list.length)];
    }
    
    // 生成回复内容
    generateReplyContent(targetPost) {
        const style = this.personality.generateReplyStyle();
        
        const replies = {
            'active': [
                '所言极是！',
                '支持！',
                '说得太好了！'
            ],
            'formal': [
                '阁下所言有理。',
                '此言甚是。',
                '赞同阁下的观点。'
            ],
            'friendly': [
                '说得对！',
                '我也这么认为！',
                '英雄所见略同！'
            ],
            'normal': [
                '嗯，有道理。',
                '确实如此。',
                '同意。'
            ]
        };
        
        const replies_list = replies[style] || replies['normal'];
        return replies_list[Math.floor(Math.random() * replies_list.length)];
    }
    
    // 计算奖励
    calculateReward(category) {
        const rewards = {
            '政务': 100,
            '技术': 80,
            '学习': 60,
            '求助': 40,
            '分享': 50
        };
        return rewards[category] || 50;
    }
    
    // 寻找朋友
    findFriend() {
        // 简单实现：随机选择一个关系好的官员
        const friends = Object.entries(this.relationships)
            .filter(([name, rel]) => rel.closeness > 0.7)
            .map(([name]) => name);
        
        if (friends.length > 0) {
            return friends[Math.floor(Math.random() * friends.length)];
        }
        
        return null;
    }
    
    // 选择工作类别
    chooseWorkCategory() {
        const categories = ['政务', '技术', '学习'];
        return categories[Math.floor(Math.random() * categories.length)];
    }
    
    // 休息
    async rest(duration) {
        await this.sleep(duration * 1000);  // 加速时间
        this.needs.update('rest');
        console.log(`${this.name} 休息了 ${duration} 小时`);
    }
    
    // 社交
    async socialize(target) {
        if (target) {
            console.log(`${this.name} 和 ${target} 聊天`);
        }
        this.needs.update('socialize');
    }
    
    // 工作
    async work(category) {
        await this.post(category);
        this.needs.update('work');
    }
    
    // 放松
    async relax() {
        await this.post('分享');
        this.needs.update('relax');
    }
    
    // 睡眠辅助
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// ==================== 模拟系统 ====================
class Simulation {
    constructor() {
        this.agents = [];
        this.running = false;
    }
    
    // 初始化官员
    initAgents() {
        const configs = [
            { id: 1, name: '柏元富', style: '荷儿', position: '司礼监掌印太监', age: 35 },
            { id: 2, name: '许素娴', style: '霜儿', position: '中书省尚书令', age: 42 },
            { id: 3, name: '华涛', style: '雨儿', position: '门下省侍中', age: 38 },
            { id: 4, name: '赵康', style: '子敬', position: '尚书省都事', age: 45 },
            { id: 5, name: '孔中中', style: '燕儿', position: '户部尚书', age: 40 },
            { id: 6, name: '曹英', style: '思儿', position: '工部尚书', age: 36 },
            { id: 7, name: '何强敬', style: '翠儿', position: '礼部尚书', age: 43 },
            { id: 8, name: '杨富', style: '兰儿', position: '刑部尚书', age: 39 },
            { id: 9, name: '姜娟春', style: '凤儿', position: '兵部尚书', age: 37 },
            { id: 10, name: '窦露素', style: '芷儿', position: '吏部尚书', age: 41 }
        ];
        
        this.agents = configs.map(config => new Agent(config));
        
        // 初始化关系
        this.initRelationships();
    }
    
    // 初始化关系
    initRelationships() {
        // 随机生成一些关系
        for (let agent of this.agents) {
            for (let other of this.agents) {
                if (agent.id !== other.id) {
                    const closeness = Math.random();
                    const trust = Math.random();
                    agent.relationships[other.name] = { closeness, trust };
                }
            }
        }
    }
    
    // 运行模拟
    async run() {
        this.running = true;
        
        while (this.running) {
            // 每个智能体决策并行动
            for (let agent of this.agents) {
                const action = agent.decide();
                await agent.execute(action);
                
                // 等待一小段时间
                await agent.sleep(1000 + Math.random() * 2000);
            }
            
            // 等待下一轮
            await this.sleep(5000);
        }
    }
    
    // 停止模拟
    stop() {
        this.running = false;
    }
    
    // 睡眠辅助
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// ==================== 全局控制 ====================
let simulation = null;

// 启动模拟
function startSimulation() {
    if (!simulation) {
        simulation = new Simulation();
        simulation.initAgents();
        simulation.run();
        console.log('智能体生命系统已启动');
    }
}

// 停止模拟
function stopSimulation() {
    if (simulation) {
        simulation.stop();
        console.log('智能体生命系统已停止');
    }
}

// 导出到全局
window.agentSystem = {
    start: startSimulation,
    stop: stopSimulation,
    simulation: () => simulation
};

console.log('智能体生命系统已加载，使用 window.agentSystem.start() 启动');
