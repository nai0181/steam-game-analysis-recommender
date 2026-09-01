# Data Schema

本文档用于统一项目中的公共数据字段、数据类型和文件格式。

如需修改公共字段，请先在组内沟通确认，避免不同模块之间出现数据格式不一致的问题。

## 1. 数据文件

### games.csv

保存 Steam 游戏基础信息。

建议位置：

`data/raw/games.csv`

清洗后的版本：

`data/processed/cleaned_games.csv`

### reviews.csv

保存 Steam 用户评论数据。

建议位置：

`data/raw/reviews.csv`

清洗后的版本：

`data/processed/cleaned_reviews.csv`

---

## 2. games.csv 字段规范

| 字段名             | 类型    | 是否必填 | 说明                   |      |
| --------------- | ----- | ---- | -------------------- | ---- |
| `appid`         | int   | 是    | Steam 游戏唯一编号         |      |
| `name`          | str   | 是    | 游戏名称                 |      |
| `price`         | float | 否    | 游戏价格，统一保存为数值         |      |
| `release_date`  | str   | 否    | 游戏发行日期               |      |
| `developer`     | str   | 否    | 游戏开发商                |      |
| `genres`        | str   | 否    | 游戏类型，多项使用 `          | ` 分隔 |
| `tags`          | str   | 否    | Steam 游戏标签，多项使用 `    | ` 分隔 |
| `positive_rate` | float | 否    | 游戏好评率，统一使用 0～1 之间的小数 |      |
| `review_count`  | int   | 否    | 游戏评论总数               |      |

示例：

```
appid,name,price,release_date,developer,genres,tags,positive_rate,review_count
12345,Game A,99.0,2024-01-01,Studio A,Action|RPG,Open World|Souls-like,0.95,50000
```

---

## 3. reviews.csv 字段规范

| 字段名           | 类型    | 是否必填 | 说明                |
| ------------- | ----- | ---- | ----------------- |
| `appid`       | int   | 是    | 对应游戏的 Steam AppID |
| `review_id`   | str   | 是    | 评论唯一编号            |
| `review_text` | str   | 是    | 评论正文              |
| `voted_up`    | bool  | 是    | 是否推荐，True 表示推荐    |
| `playtime`    | float | 否    | 玩家游戏时长，统一以小时为单位   |
| `timestamp`   | str   | 否    | 评论发布时间            |

示例：

```
appid,review_id,review_text,voted_up,playtime,timestamp
12345,review_001,Very good game,True,120.5,2026-08-30
12345,review_002,Poor optimization,False,8.2,2026-08-30
```

---

## 4. 公共关联字段

`appid` 是整个项目中最重要的关联字段。

游戏基础信息、评论数据、聚类结果、推荐结果和前端展示都优先通过 `appid` 关联。

例如：

`games.csv`

```
appid = 12345
name = Game A
```

`reviews.csv`

```
appid = 12345
review_text = Very good game
```

表示该评论属于 Game A。

除非组内统一修改，否则不要自行把 `appid` 改成：

* `game_id`
* `id`
* `steam_id`
* 其他名称

---

## 5. 多值字段规范

`genres` 和 `tags` 可能包含多个值。

统一使用 `|` 分隔。

正确示例：

```
Action|RPG|Adventure

Open World|Souls-like|Dark Fantasy
```

不要不同成员分别使用逗号、斜杠、分号等不同方式。

---

## 6. 数值字段规范

### price

统一保存为数值，例如：

```
99.0
```

不要保存为：

```
￥99
99元
$9.99
```

如果存在货币差异，应在数据清洗阶段统一。

### positive_rate

统一使用 0～1 的小数。

例如：

```
0.95
```

表示 95%。

不要部分数据使用 `95`，另一部分使用 `0.95`。

### playtime

统一使用“小时”作为单位。

例如：

```
120.5
```

表示 120.5 小时。

---

## 7. 缺失值规范

数据缺失时，不要随意填写：

```
无
暂无
-
unknown
0
```

如果确实没有该数据，则保持为空。

在 pandas 中可以统一处理为 `NaN`。

特别注意：

`price = 0`

和

`price 缺失`

含义不同。

不要为了避免空值而随意填 0。

---

## 8. 原始数据与清洗数据

目录统一为：

```
data/
├── raw/
│   ├── games.csv
│   └── reviews.csv
├── processed/
│   ├── cleaned_games.csv
│   └── cleaned_reviews.csv
└── sample/
```

### raw

保存从 Steam 获取的原始数据，不直接覆盖。

### processed

保存经过缺失值处理、重复值处理、类型转换、字符串清洗等操作后的数据。

### sample

保存小规模测试数据，供其他成员开发和联调。

---

## 9. CSV 文件规范

所有 CSV 文件统一：

* 使用 UTF-8 编码
* 第一行为字段名
* 不额外保存 pandas index
* 字段名使用英文
* 字段名统一小写
* 多个单词使用下划线连接

正确：

```
release_date
review_count
positive_rate
```

不建议：

```
ReleaseDate
reviewCount
Positive Rate
```

---

## 10. 公共字段修改规则

如果需要：

* 增加字段
* 删除字段
* 修改字段名
* 修改单位
* 修改数据格式

请先在组内说明。

确认后再：

1. 修改本文件
2. 修改对应代码
3. 通知会使用该字段的成员

不要个人直接修改公共数据结构。

---

## 11. 模块输入输出约定

### 数据采集模块

输出：

`games.csv`

`reviews.csv`

### 评论分类模块

输入：

`review_text`

输出：

* 预测结果
* 推荐 / 不推荐

### 聚类模块

输入：

`cleaned_games.csv`

输出至少包含：

* `appid`
* `cluster`

### 推荐模块

输入：

* `cleaned_games.csv`
* 用户选择的 `appid`

输出至少包含：

* 推荐游戏 `appid`
* 相似度
* 推荐排名

### 前端模块

通过 `appid` 和各模块标准输出进行数据展示。

---

## 12. GitHub 数据提交规则

GitHub 中不要直接提交过大的原始数据文件。

仓库主要保留：

* 小规模示例数据
* 数据字段说明
* 数据处理代码
* 必要运行示例

例如：

```
data/sample/games_sample.csv
data/sample/reviews_sample.csv
```

大规模原始数据根据实际情况另行共享。

---

## 13. 当前项目数据流

```
Steam
  ↓
数据采集
  ↓
raw 数据
  ↓
数据清洗
  ↓
processed 数据
  ↓
├── EDA / K-Means
├── 评论分类
└── 推荐算法
  ↓
Streamlit 前端
```

整个流程尽量始终保留 `appid`，作为不同模块之间关联游戏的统一标识。
