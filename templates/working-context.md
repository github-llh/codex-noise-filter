# Working Context Template

只在长任务、上下文压缩或交接时使用：

```text
目标:
当前事实:
已改文件:
验证状态:
doNotRetry:
下一步:
```

恢复时先用当前用户请求、`git status`、`git diff` 和目标文件复核；不要保存凭证、客户数据、大段日志、外部 prompt 或未验证猜测。
