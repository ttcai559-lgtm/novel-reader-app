# 📱 GitHub Actions 打包APK 详细步骤

## 🎯 方案优势

- ✅ **完全云端构建** - 不需要本地Linux环境
- ✅ **自动化** - 一键触发，自动完成
- ✅ **免费** - GitHub Actions免费额度足够
- ✅ **时间** - 20-30分钟得到APK
- ✅ **简单** - 只需要几个点击

---

## 📋 前提条件

1. **GitHub账号** - 免费注册
2. **项目代码** - 已经准备好（在 `D:\Python_file\APP_Tool`）
3. **10-15分钟操作时间**

---

## 🚀 详细步骤

### 步骤1: 创建GitHub账号（如果没有）

1. 访问: https://github.com/signup
2. 输入邮箱
3. 设置密码
4. 选择用户名
5. 验证邮箱
6. ✅ 完成注册

**⏱️ 用时: 2分钟**

---

### 步骤2: 创建新仓库

1. 登录GitHub后，点击右上角 **"+"** → **"New repository"**

2. 填写信息:
   ```
   Repository name: novel-reader-app
   Description: TXT小说转有声读物 Android APP
   Privacy: ✅ Private (私有，只有你能看到)
   ```

3. **不要勾选** "Add a README file"

4. 点击 **"Create repository"**

5. 记下仓库地址（类似）:
   ```
   https://github.com/你的用户名/novel-reader-app.git
   ```

**⏱️ 用时: 1分钟**

---

### 步骤3: 上传代码到GitHub

**方法A: 使用GitHub Desktop（推荐，图形界面）**

1. 下载GitHub Desktop: https://desktop.github.com/
2. 安装并登录
3. File → Add Local Repository → 选择 `D:\Python_file\APP_Tool`
4. Publish repository
5. ✅ 完成

**方法B: 使用命令行（如果你熟悉Git）**

打开PowerShell:

```powershell
# 进入项目目录
cd D:\Python_file\APP_Tool

# 初始化Git（如果还没有）
git init

# 添加所有文件
git add .

# 创建第一次提交
git commit -m "Initial commit - TXT小说转有声读物APP"

# 关联GitHub仓库（替换成你的仓库地址）
git remote add origin https://github.com/你的用户名/novel-reader-app.git

# 设置主分支
git branch -M main

# 推送代码
git push -u origin main
```

**如果提示需要登录**:
- 使用GitHub用户名和密码
- 或使用Personal Access Token（在GitHub Settings → Developer settings中生成）

**⏱️ 用时: 3-5分钟**

---

### 步骤4: 验证代码已上传

1. 刷新GitHub仓库页面
2. 应该能看到所有文件:
   ```
   novel-reader-app/
   ├── .github/
   │   └── workflows/
   │       └── build-apk.yml  ← 重要！
   ├── mobile_app/
   ├── modules/
   ├── core/
   ├── config/
   └── ...
   ```

3. 确认 `.github/workflows/build-apk.yml` 存在

**⏱️ 用时: 30秒**

---

### 步骤5: 触发APK构建

1. 在GitHub仓库页面，点击 **"Actions"** 标签

2. 如果第一次使用Actions，点击 **"I understand my workflows, go ahead and enable them"**

3. 左侧找到 **"Build Android APK"** 工作流

4. 点击右侧 **"Run workflow"** 按钮

5. 确认分支是 `main`

6. 点击绿色的 **"Run workflow"**

7. 页面会刷新，显示构建任务开始

**⏱️ 用时: 1分钟**

---

### 步骤6: 等待构建完成

1. 可以看到构建进度（黄色圆圈转动）

2. 点击任务查看详细日志

3. 构建过程:
   ```
   ⏳ Checkout code (30秒)
   ⏳ Set up Python (1分钟)
   ⏳ Install system dependencies (5分钟)
   ⏳ Install Python dependencies (3分钟)
   ⏳ Prepare mobile app (30秒)
   ⏳ Build APK (15-20分钟) ← 最慢的步骤
   ⏳ Upload APK (30秒)
   ```

4. **总时间**: 约25-30分钟

5. 完成后显示 ✅ 绿色勾

**⏱️ 用时: 25-30分钟**（自动进行，可以做其他事）

---

### 步骤7: 下载APK

1. 构建完成后，在Actions页面

2. 点击刚才的构建任务

3. 向下滚动到 **"Artifacts"** 部分

4. 点击 **"novelreader-apk"** 下载

5. 下载的是ZIP文件，解压得到:
   ```
   novelreader-1.0.0-debug.apk
   ```

6. 文件大小: 约40-60MB

**⏱️ 用时: 2分钟**

---

### 步骤8: 安装到手机

**方法A: 直接传输**

1. 把APK文件传到手机（微信/QQ/数据线）
2. 手机上找到APK文件
3. 点击安装
4. 如果提示"未知来源"，允许安装
5. ✅ 安装完成

**方法B: ADB安装（如果你有）**

```bash
adb install novelreader-1.0.0-debug.apk
```

**⏱️ 用时: 2分钟**

---

## 📊 时间总结

| 步骤 | 时间 |
|-----|------|
| 1. 创建GitHub账号 | 2分钟 |
| 2. 创建仓库 | 1分钟 |
| 3. 上传代码 | 3-5分钟 |
| 4. 验证代码 | 30秒 |
| 5. 触发构建 | 1分钟 |
| 6. 等待构建 | 25-30分钟（自动） |
| 7. 下载APK | 2分钟 |
| 8. 安装到手机 | 2分钟 |
| **总计** | **~40分钟**（其中25分钟是自动的） |

---

## ❓ 常见问题

### Q1: 构建失败怎么办？

**A**: 点击失败的任务查看日志，常见原因：

- **缺少文件**: 确保 `.github/workflows/build-apk.yml` 存在
- **权限问题**: 确保Actions已启用
- **依赖问题**: 重新触发构建试试

**解决**:
1. 查看错误日志
2. 告诉我错误信息
3. 我帮你修复

---

### Q2: GitHub Actions额度够吗？

**A**: 完全够！

- 免费账号: 每月2000分钟
- 一次构建: 约30分钟
- 可以构建60多次

---

### Q3: 代码安全吗？

**A**: 安全！

- 设置为Private仓库，只有你能看到
- 不会泄露任何信息
- 可以随时删除

---

### Q4: 可以修改APP吗？

**A**: 当然可以！

1. 修改代码
2. `git add .` → `git commit -m "更新"` → `git push`
3. 自动触发新构建
4. 下载新APK

---

### Q5: APK可以分享吗？

**A**: 可以！

- Debug版本可以直接分享给朋友安装
- 如果要发布到应用商店，需要签名

---

## 🎯 快速检查清单

构建前确认：

- [ ] GitHub账号已创建
- [ ] 仓库已创建
- [ ] 代码已上传
- [ ] `.github/workflows/build-apk.yml` 文件存在
- [ ] Actions已启用

全部打勾就可以触发构建了！

---

## 📞 需要帮助？

### 卡在哪一步了？

**步骤1-2**: GitHub操作
- 截图给我，我指导你

**步骤3**: 上传代码
- 告诉我遇到什么问题

**步骤5-6**: 构建失败
- 复制错误日志给我

**步骤8**: 安装问题
- 告诉我手机提示什么

---

## 🎊 开始吧！

**现在就开始第一步**:

1. 访问: https://github.com/signup
2. 或如果已有账号: https://github.com/login

**告诉我你的进度，我全程指导你！🚀**

---

## 📱 预期结果

完成后你将得到:

```
novelreader-1.0.0-debug.apk
├── 大小: 40-60MB
├── 支持: Android 5.0+
└── 功能:
    ✅ TXT导入
    ✅ 8种AI音色
    ✅ 智能章节识别
    ✅ 音频播放器
    ✅ 倍速播放
    ✅ 进度保存
```

**立即在手机上享受有声小说！📱📚🎧**
