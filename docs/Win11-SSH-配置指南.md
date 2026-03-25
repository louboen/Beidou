# 🔧 Win11 SSH 远程连接配置指南

**创建日期**: 2026-03-22  
**适用场景**: 从 Linux 服务器通过 SSH 连接 Windows 11 设备

---

## 📋 概述

本指南记录如何在一台 Windows 11 设备上配置 OpenSSH Server，实现从 Linux 服务器的免密码 SSH 连接。

### 环境信息
| 项目 | 配置 |
|------|------|
| **目标系统** | Windows 11 (Microsoft 账户) |
| **SSH 服务器** | Windows OpenSSH Server |
| **认证方式** | SSH 密钥（ED25519） |
| **网络** | Tailscale (`100.64.0.0/24`) |

---

## 🚀 快速开始

### 步骤 1：在 Win11 上启用 SSH

**以管理员身份运行 PowerShell**，执行：

```powershell
# 下载并执行启用脚本
$url = "https://raw.githubusercontent.com/louboen/openclaw-backup/main/scripts/enable-ssh-win11.ps1"
$output = "$env:USERPROFILE\Desktop\enable-ssh-win11.ps1"
Invoke-WebRequest -Uri $url -OutFile $output
.\enable-ssh-win11.ps1
```

或从飞书文档复制脚本：https://feishu.cn/docx/VfaFdianiotaW3xgfG4cCmzInih

---

### 步骤 2：生成 SSH 密钥对

**在 Linux 服务器上执行**：

```bash
# 生成 ED25519 密钥对
ssh-keygen -t ed25519 -f ~/.ssh/win11-key -N "" -C "linux-to-win11"

# 查看公钥
cat ~/.ssh/win11-key.pub
```

---

### 步骤 3：配置 Win11 公钥认证

**在 Win11 上以管理员身份运行 PowerShell**：

```powershell
# 1. 设置公钥（替换为你的公钥内容）
$pubKey = "ssh-ed25519 AAAA... 你的公钥 ... user@host"
$authFile = "C:\ProgramData\ssh\administrators_authorized_keys"

# 2. 创建/更新 authorized_keys 文件
Set-Content -Path $authFile -Value $pubKey -Encoding ASCII

# 3. 设置严格权限
$acl = New-Object System.Security.AccessControl.FileSecurity
$acl.SetAccessRuleProtection($true, $false)
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule("SYSTEM", "FullControl", "Allow")))
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule("Administrators", "FullControl", "Allow")))
Set-Acl -Path $authFile -AclObject $acl

# 4. 重启 SSH 服务
Restart-Service sshd

# 5. 验证
Write-Host "✅ 配置完成" -ForegroundColor Green
Get-Content $authFile
Get-Acl $authFile | Format-Table Owner, AccessToString
```

---

### 步骤 4：测试连接

**在 Linux 服务器上执行**：

```bash
# 测试连接
ssh -i ~/.ssh/win11-key loubo@100.64.0.2 "whoami && hostname"

# 预期输出：
# boen-book\loubo
# Boen-Book
```

---

## 🔍 故障排除

### 问题 1：Permission denied (publickey)

**原因**: 公钥文件权限不正确

**解决**:
```powershell
# 重新设置权限（管理员 PowerShell）
$acl = New-Object System.Security.AccessControl.FileSecurity
$acl.SetAccessRuleProtection($true, $false)
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule("SYSTEM", "FullControl", "Allow")))
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule("Administrators", "FullControl", "Allow")))
Set-Acl -Path "C:\ProgramData\ssh\administrators_authorized_keys" -AclObject $acl
Restart-Service sshd
```

---

### 问题 2：Connection refused

**原因**: SSH 服务未运行

**解决**:
```powershell
# 检查服务状态
Get-Service sshd

# 启动服务
Start-Service sshd

# 设置开机自启
Set-Service -Name sshd -StartupType Automatic
```

---

### 问题 3：密钥生成失败（选项 N 错误）

**原因**: Windows 版 ssh-keygen 参数格式不同

**正确格式**:
```powershell
# Windows PowerShell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\id_ed25519" -N ""

# 注意：-N "" 之间有空格
```

---

### 问题 4：Microsoft 账户无法设置密码

**原因**: Microsoft 账户不能用 `net user` 修改密码

**解决**:
- 使用 SSH 密钥认证（推荐）
- 或使用 Microsoft 账户密码（不是 PIN 码）登录

---

## 📚 关键知识点

### Windows SSH 特殊要求

1. **管理员账户** 必须使用 `C:\ProgramData\ssh\administrators_authorized_keys`
   - 普通用户才用 `C:\Users\<user>\.ssh\authorized_keys`

2. **权限要求极其严格**
   - 只能有 SYSTEM 和 Administrators 组权限
   - 不能有用户个人权限
   - 不能有继承权限

3. **空密码登录被禁止**
   - Windows OpenSSH 默认禁止空密码
   - 即使配置 `PermitEmptyPasswords yes` 也可能不生效
   - 建议始终使用密钥认证

---

### SSH 配置文件位置

| 文件 | 路径 | 用途 |
|------|------|------|
| sshd_config | `C:\ProgramData\ssh\sshd_config` | SSH 服务器配置 |
| administrators_authorized_keys | `C:\ProgramData\ssh\administrators_authorized_keys` | 管理员公钥 |
| authorized_keys | `C:\Users\<user>\.ssh\authorized_keys` | 普通用户公钥 |

---

## 🔐 安全建议

1. **使用 ED25519 密钥** —— 比 RSA 更安全、更快速
2. **定期轮换密钥** —— 建议每 6-12 个月
3. **限制 SSH 访问** —— 使用防火墙或 Tailscale ACL
4. **监控登录日志** —— 定期检查 `Get-EventLog -LogName System -Source sshd`

---

## 📎 相关资源

- **启用脚本**: https://github.com/louboen/openclaw-backup/blob/main/scripts/enable-ssh-win11.ps1
- **飞书文档**: https://feishu.cn/docx/VfaFdianiotaW3xgfG4cCmzInih
- **记忆文件**: `memory/2026-03-22.md`
- **长期记忆**: `MEMORY.md`

---

## 📝 配置检查清单

- [ ] OpenSSH Server 已安装
- [ ] SSH 服务正在运行
- [ ] SSH 服务开机自启
- [ ] 公钥已添加到 `administrators_authorized_keys`
- [ ] 文件权限正确（SYSTEM + Administrators only）
- [ ] 防火墙规则已配置（端口 22）
- [ ] 测试连接成功

---

*文档维护：司南 🧭*  
*最后更新：2026-03-22 21:43*
