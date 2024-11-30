---
marp: true
theme: gaia
class:
  - invert
paginate: true
style: |
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap');
  section {
    font-family: 'Noto Sans TC', sans-serif;
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
  .columns-center {
    place-items: center;
  }
  img[alt="遊戲截圖"] {
    width: 100%;
    max-height: 500px;
    object-fit: contain;
  }
  .split-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
    margin-top: -1rem;
  }
  .split-list h4 {
    margin-top: 0;
    font-size: 0.9em;
  }
  .split-list ul {
    font-size: 0.8em;
    padding-left: 1.2em;
  }
---

# 🐍 重新定義經典遊戲

### 一段關於貪食蛇的故事

---

# 40年的經典遊戲

### 從街機到智慧手機

- 1976年街機遊戲 Blockade
- 1998年 Nokia 3310 最經典版本
- 2023年仍在 Google、Discord 流行

---

# 為什麼長青不衰？

### 簡單而不簡單

- 規則簡單，策略豐富
- 考驗反應力與決策
- 最佳的程式入門專案

---

# 我們的創新

<div class="columns">
<div>

### 保留經典，加入新意

<div class="split-list">
<div>

#### 遊戲體驗
- 流暢的操控方式
- 特殊食物系統
- 即時音效回饋

</div>
<div>

#### 技術突破
- 模組化設計
- 完整測試覆蓋
- AI 輔助開發

</div>
</div>

</div>
<div class="columns-center">

![遊戲截圖](./screenshot.png)

</div>
</div>

---

# 開源的魅力

### 集體智慧的結晶

```python
class SnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.food = FoodSystem()
        self.power_ups = PowerUpManager()
```

---

# 一起來玩吧！

### 新手也能輕鬆上手

- 簡單的安裝步驟
- 清晰的程式架構
- 完整的開發文件

---

# 加入開發

### 從這裡開始

1. Fork 專案開始
2. 挑選感興趣的任務
3. 提交你的第一個改進

---

# 展望未來

### 更多可能性

- 多人對戰模式
- AI 對戰系統
- 全球排行榜
- 跨平台支援

---

# 立即行動

- GitHub: [https://github.com/hlb/snake](https://github.com/hlb/snake)
- Star 支持我們
- Fork 開始貢獻

---

# 讓我們一起

### 重新定義經典，創造未來 

🐍 × 💻 × 🌟
