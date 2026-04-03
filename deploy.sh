#!/bin/bash
# 大明·OpenClaw 门户 - GitHub Pages 部署脚本

echo "🏛️  大明·OpenClaw 三省六部制 - GitHub Pages 部署"
echo "================================================"
echo ""

# 检查 Git 仓库
if [ ! -d ".git" ]; then
    echo "❌ 错误：这不是一个 Git 仓库"
    echo "请先运行：git init"
    exit 1
fi

# 添加所有文件
echo "📝 添加文件..."
git add .

# 提交
echo "💾 提交更改..."
git commit -m "自动更新：$(date '+%Y-%m-%d %H:%M:%S')"

# 检查远程仓库
if ! git remote | grep -q "origin"; then
    echo ""
    echo "⚠️  未配置远程仓库"
    echo ""
    echo "请按以下步骤操作："
    echo "1. 访问 https://github.com"
    echo "2. 登录/注册 GitHub 账号"
    echo "3. 点击右上角 + → New repository"
    echo "4. 填写仓库名称：openclaw-portal"
    echo "5. 选择 Public"
    echo "6. 点击 Create repository"
    echo ""
    echo "然后运行："
    echo "git remote add origin https://github.com/你的用户名/openclaw-portal.git"
    echo "git push -u origin main"
    echo ""
    exit 1
fi

# 推送
echo "🚀 推送到 GitHub..."
git push

# 检查推送结果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 部署完成！"
    echo ""
    echo "🌐 访问地址："
    echo "https://你的用户名.github.io/openclaw-portal/"
    echo ""
    echo "📝 注意："
    echo "1. 首次部署需要等待 1-2 分钟"
    echo "2. 在 GitHub 仓库 Settings → Pages 启用 GitHub Pages"
    echo "3. Source 选择 main 分支"
    echo ""
else
    echo ""
    echo "❌ 推送失败"
    echo "请检查网络连接和 GitHub 账号"
    exit 1
fi
