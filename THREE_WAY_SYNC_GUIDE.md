# 三方同步工作流程指南

## 🔄 仓库关系说明

```
原始源代码(sansan0/TrendRadar) ←───┐
                                    │
                                    ├── 获取更新
                                    │
你的Fork(moyu-good/TrendRadar) ←───┤
                                    │
                                    └── 推送更改
                                    
本地仓库(你的电脑)
```

## 📋 当前配置状态

### ✅ 已配置
- **原始源代码**: `upstream` → https://github.com/sansan0/TrendRadar.git
- **你的Fork**: `origin` → https://github.com/moyu-good/TrendRadar.git
- **本地环境**: Python 3.12 + UV包管理器
- **邮件配置**: 1249510763@qq.com (已配置)
- **AI功能**: 已集成AI增强报告生成

### 🎯 工作流程

#### 1. 日常开发流程
```powershell
# 1. 获取原始源代码最新更新
git fetch upstream

# 2. 合并原始代码更新（如果有）
git merge upstream/master

# 3. 处理你的本地更改
git add .
git commit -m "你的更改描述"

# 4. 推送到你的Fork
git push origin master
```

#### 2. 使用自动同步脚本
```powershell
# 运行三方同步脚本
.\sync-three-way.ps1
```

#### 3. 手动同步特定部分
```powershell
# 只同步原始代码更新
git fetch upstream
git merge upstream/master

# 只推送你的更改到Fork
git push origin master

# 查看更新历史
git log upstream/master --oneline -10  # 原始代码最近10次提交
git log origin/master --oneline -10    # 你的Fork最近10次提交
```

## 🔧 配置验证

### 检查远程仓库
```powershell
git remote -v
# 应该显示：
# origin  https://github.com/moyu-good/TrendRadar.git (fetch)
# origin  https://github.com/moyu-good/TrendRadar.git (push)
# upstream        https://github.com/sansan0/TrendRadar.git (fetch)
# upstream        https://github.com/sansan0/TrendRadar.git (push)
```

### 检查当前分支
```powershell
git status
# 应该显示在 master 分支
```

## 🚀 功能测试

### 测试本地运行
```powershell
C:\Users\12495\.local\bin\uv run python main.py
```

### 测试AI邮件发送
```powershell
C:\Users\12495\.local\bin\uv run python send_ai_report_email.py
```

### 检查GitHub Actions状态
访问：https://github.com/moyu-good/TrendRadar/actions

## ⚠️ 注意事项

### 冲突处理
如果原始代码和你的修改有冲突：
1. Git会提示冲突文件
2. 手动编辑冲突文件解决冲突
3. `git add .` 然后 `git commit` 完成合并

### 备份策略
- 重要更改前创建分支：`git branch backup-日期`
- 定期推送到你的Fork保持备份

### 保持同步频率
建议定期运行同步脚本：
- 开发前：获取最新原始代码
- 开发后：推送你的更改
- 每周：完整三方同步

## 📞 支持

### 检查workflow运行状态
```powershell
# 查看workflow历史
gh run list --repo=moyu-good/TrendRadar

# 查看最新workflow状态
gh run view --repo=moyu-good/TrendRadar --web
```

### 查看日志文件
- 本地日志：`trendradar.log`
- GitHub Actions日志：在Actions页面查看

现在你的TrendRadar项目已经完美配置了三方同步机制！🎉

你可以：
- ✅ 获取原始源代码的最新功能
- ✅ 保持你自己的配置和修改
- ✅ 推送到你的Fork进行备份
- ✅ 享受AI增强的新闻分析功能
- ✅ 每天早上9点收到邮件推送