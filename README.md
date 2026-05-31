# 服装厂管理APP - APK打包说明

## 快速开始（只需3步）

### 第1步：上传到GitHub（5分钟）

1. 打开 https://github.com 并登录
2. 点击右上角 "+" → "New repository"
3. 名称填：`clothing-factory-app`
4. 选择 "Public"
5. 点击 "Create repository"
6. 在新页面，点击 "uploading an existing file"
7. 把本文件夹（除了.db数据库文件）里的所有文件拖进去
8. 点击 "Commit changes"

### 第2步：等待自动构建（15-20分钟）

1. 回到仓库主页
2. 点击 "Actions" 标签
3. 你会看到 "Build Android APK"  workflow正在运行
4. 等待它变成绿色勾勾 ✓

### 第3步：下载APK（1分钟）

1. 点击 "Actions" → 点击构建完成的workflow
2. 点击 "clothing-factory-app" 附件
3. 点击下载按钮
4. 把APK传到手机安装

## 需要上传的文件

确保上传这些文件（不要上传 .venv 和 .db 文件）：

```
clothing_factory_app.py   ← 主程序
buildozer.spec           ← 打包配置
README.md                ← 说明文件
.github/
  workflows/
    build.yml            ← 自动构建配置
```

## 文件夹内容说明

| 文件 | 必须上传 | 说明 |
|------|---------|------|
| clothing_factory_app.py | ✅ | 主程序代码 |
| buildozer.spec | ✅ | Buildozer打包配置 |
| .github/workflows/build.yml | ✅ | GitHub自动构建配置 |
| README.md | ✅ | 说明文档 |
| 启动.bat | ❌ | Windows启动脚本 |
| 手机APP云端打包指南.txt | ❌ | 旧版指南，可忽略 |
| clothing_factory.db | ❌ | 数据库文件，不要上传 |
| .venv/ | ❌ | Python虚拟环境，不要上传 |

## 常见问题

Q: 构建失败了怎么办？
A: 点击失败的workflow，查看错误日志，通常是网络超时，可以重新运行一次

Q: 可以用Private仓库吗？
A: 可以，但GitHub Actions在Private仓库有分钟数限制（2000分钟/月）

Q: APK多大？
A: 约30-50MB

Q: 安装到手机时提示风险？
A: 这是正常的，因为APP没上架应用商店。进入手机设置 → 安全 → 允许未知来源应用

## 构建完成后

APK下载到手机后：
1. 传输APK到手机
2. 在手机上找到APK文件
3. 点击安装
4. 如果提示风险，请在设置中允许安装

---

祝你使用愉快！如有更多问题请提交Issue。
