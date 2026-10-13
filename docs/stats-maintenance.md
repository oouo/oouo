# GitHub 统计卡维护手册

## 当前架构

个人主页不在访问时请求统计服务。README 使用相对路径加载仓库内的两张 SVG：

- `assets/github-stats-dark.svg`：深色模式，`tokyonight` 主题
- `assets/github-stats-light.svg`：浅色模式，`default` 主题

`.github/workflows/update-stats.yml` 每天拉取一次新卡片，完整校验两张 SVG 后才一起替换并提交。更新失败时，仓库里的上一版有效卡片保持不变，因此主页展示不受统计服务临时故障影响。

统计区保留可折叠结构，但使用 `<details open>` 让卡片在个人页首屏默认可见。

```text
定时或手动触发
  → 检查仓库活动，必要时提交保活
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

公开仓库连续 60 天没有仓库活动时，GitHub 会自动停用定时工作流。工作流运行本身不能替代仓库活动。为避免统计长期不变或接口长期故障导致停用，下载前检查最新提交时间；超过 30 天时，机器人推送一次空的维护提交。它不修改统计卡，也不把后续下载失败标记为成功。已有近期提交时不产生额外提交。

不要把 README 改回动态统计链接，也不要改用公共的 `github-readme-stats.vercel.app` 实例。GitHub 会正确解析 README 中的相对图片路径；将生成后的 SVG 存进仓库，也避免了每次浏览主页都依赖外部统计接口。

## 更新保护

工作流只会在两张卡片全部通过以下检查后安装新文件：

1. HTTP 请求成功，响应类型为 SVG。
2. 先检查服务错误卡片，提取 SVG 中的具体错误写入日志和运行摘要；HTTP 200 不代表返回了有效统计。
3. 文件不少于 1000 字节，并且 XML 根节点是 `<svg>`。
4. 包含 stars、commits、PR、issues 和 contributions 等预期字段。
5. 不包含 `<script>`、`<foreignObject>` 或内联事件处理器。

先下载到临时目录、后同时安装是关键约束。任何一张卡片失败，都不能覆盖现有资源。

## 故障排查

按这个顺序处理：

1. 查看 **Update GitHub stats** 对应失败运行的日志，确定失败发生在下载、校验、提交还是推送阶段。
2. 直接请求自托管接口，检查 HTTP 状态、`Content-Type`、响应大小和 SVG 内容。
3. 如果接口本身失败，再检查自托管部署、GitHub Token、限流和上游 API 状态。
4. 如果工作流成功但页面仍旧，确认提交已进入默认分支，并检查 README 的相对路径与文件名。

这套架构不再依赖外部统计图片的浏览器缓存。不要通过添加随机查询参数或频繁改文件名来“清缓存”；应先确认仓库中的 SVG 是否已经更新。

### Token 权限错误与 60 天停用

`Resource not accessible by personal access token` 表示统计服务的 GitHub Token 无权读取请求的资源，不足以据此认定 Token 已过期。服务把 GraphQL 错误包装成 HTTP 200 的小型 SVG；旧版工作流先检查大小，因此日志只显示 `unexpectedly small`，没有显示权限错误。

Vercel 项目的 `PAT_1` 用来读取统计数据，工作流的 `GITHUB_TOKEN` 用来提交卡片，两者独立。修正 Actions 的 `contents: write` 或重复重跑不能修复服务端 Token。

如果 Vercel 运行日志中的错误路径是 `user.repositories.nodes.*.stargazers`，应检查统计服务的 GraphQL 查询。旧查询 `stargazers { totalCount }` 请求了 Star 用户列表，即使只使用其中的数量，也可能被细粒度 Token 的访问检查拒绝。统计只需要数量时，使用仓库的 `stargazerCount` 标量，并同步分页停止条件与 Star 汇总逻辑。现有 Token 已具备正确的仓库只读权限时，应先修正查询。

恢复顺序：

1. 在统计服务的 Vercel 项目中检查生产环境 `PAT_1`，按部署版本的要求核对 Token 的资源范围、只读权限和有效期，并查看 GraphQL 错误路径。若有多个 `PAT_*`，逐一检查。不要把 Token 写进仓库或运行日志。
2. 修正配置后重新部署，再请求深浅两种主题，确认响应包含正常统计字段，而不是错误卡。
3. 若工作流状态为 `disabled_inactivity`，在 Actions 页面启用 **Update GitHub stats**，再手动执行一次。已停用的工作流不能靠自己的保活步骤恢复。
4. 确认工作流成功且两张卡片一起更新，再检查主页。

## 修改后的本地检查

在提交前至少执行：

```bash
ruby -ryaml -e 'YAML.load_file(".github/workflows/update-stats.yml")'
xmllint --noout assets/github-stats-dark.svg assets/github-stats-light.svg
git diff --check
```

同时确认 README 保留 `<details open>`，继续使用 `<picture>` 提供深浅两套资源，并且两张 SVG 总是成对更新。

回归测试直接执行工作流中的 Bash 脚本，以本地响应夹具和本地 Git 远端验证错误卡诊断、所有原有校验、失败时保留两张旧卡，以及 30 天保活阈值。需要 Python、PyYAML、Bash 和 Git：

```bash
python -B -m unittest discover -s tests -v
```

## 参考资料

- [GitHub：README 中的相对链接和图片路径](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub：使用默认展开的折叠区块](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
- [github-readme-stats：使用 GitHub Actions 生成静态 SVG](https://github.com/anuraghazra/github-readme-stats)
- [GitHub：公开仓库 60 天无活动时停用定时工作流](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)
- [github-readme-stats：自托管 Token 权限配置](https://github.com/anuraghazra/github-readme-stats#first-step-get-your-personal-access-token-pat)
- [GitHub 社区：stargazers 查询被拒绝时改用 stargazerCount](https://github.com/orgs/community/discussions/202883)
