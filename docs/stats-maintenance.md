# GitHub 统计卡维护手册

## 当前架构

个人主页不在访问时请求统计服务。README 使用相对路径加载仓库内的两张 SVG：

- `assets/github-stats-dark.svg`：深色模式，`tokyonight` 主题
- `assets/github-stats-light.svg`：浅色模式，`default` 主题

`.github/workflows/update-stats.yml` 每天拉取一次新卡片，完整校验两张 SVG 后才一起替换并提交。更新失败时，仓库里的上一版有效卡片保持不变，因此主页展示不受统计服务临时故障影响。

统计区保留可折叠结构，但使用 `<details open>` 让卡片在个人页首屏默认可见。

```text
定时或手动触发
  → 自托管统计服务
  → 临时目录下载深色、浅色 SVG
  → 完整性与安全校验
  → 同时替换仓库内资源
  → GitHub Actions 机器人提交
  → README 按系统主题读取本地资源
```

## 数据源与调度

- 唯一数据源：`https://github-readme-stats.uuuuo.com/api`
- 定时任务：每天北京时间 08:08，即 UTC 00:08
- 手动任务：GitHub 仓库的 **Actions → Update GitHub stats → Run workflow**
- 动画保持关闭，减少静态文件中的无意义变化

不要把 README 改回动态统计链接，也不要改用公共的 `github-readme-stats.vercel.app` 实例。GitHub 会正确解析 README 中的相对图片路径；将生成后的 SVG 存进仓库，也避免了每次浏览主页都依赖外部统计接口。

## 更新保护

工作流只会在两张卡片全部通过以下检查后安装新文件：

1. HTTP 请求成功，响应类型为 SVG。
2. 文件不少于 1000 字节，并且 XML 根节点是 `<svg>`。
3. 包含 stars、commits、PR、issues 和 contributions 等预期字段。
4. 不包含服务错误卡片的已知文案。
5. 不包含 `<script>`、`<foreignObject>` 或内联事件处理器。

先下载到临时目录、后同时安装是关键约束。任何一张卡片失败，都不能覆盖现有资源。

## 故障排查

按这个顺序处理：

1. 查看 **Update GitHub stats** 对应失败运行的日志，确定失败发生在下载、校验、提交还是推送阶段。
2. 直接请求自托管接口，检查 HTTP 状态、`Content-Type`、响应大小和 SVG 内容。
3. 如果接口本身失败，再检查自托管部署、GitHub Token、限流和上游 API 状态。
4. 如果工作流成功但页面仍旧，确认提交已进入默认分支，并检查 README 的相对路径与文件名。

这套架构不再依赖外部统计图片的浏览器缓存。不要通过添加随机查询参数或频繁改文件名来“清缓存”；应先确认仓库中的 SVG 是否已经更新。

## 修改后的本地检查

在提交前至少执行：

```bash
ruby -ryaml -e 'YAML.load_file(".github/workflows/update-stats.yml")'
xmllint --noout assets/github-stats-dark.svg assets/github-stats-light.svg
git diff --check
```

同时确认 README 保留 `<details open>`，继续使用 `<picture>` 提供深浅两套资源，并且两张 SVG 总是成对更新。

## 参考资料

- [GitHub：README 中的相对链接和图片路径](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub：使用默认展开的折叠区块](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
- [github-readme-stats：使用 GitHub Actions 生成静态 SVG](https://github.com/anuraghazra/github-readme-stats)
