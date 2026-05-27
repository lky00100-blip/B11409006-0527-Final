# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11409006 
**系級：** 資管系大一  
**姓名：** 李佳榮  

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) | 讀取舊資料檔案的原始行串列 | raw_lines |
| Q2 d2 (in main) | 全域書籍資料清單 | books |
| Q3 c_res (in check) | 檢查指定 ISBN 是否已存在 | isbn_exists |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：** 變數命名不具描述性，像 `l1`, `d2`, `c_res` 讓人無法快速理解資料結構與邏輯。
- **Q2：** 使用全域可變列表 `d2` 儲存資料，導致資料存取散落在多個函式中，增加耦合度和維護困難。
- **Q3：** 採用自訂字串分割格式 `@@` / `##` 儲存資料，這種硬編碼格式極難擴展且容易出錯。
- **Q4：** 檔案處理缺乏 `with`、`try/except`，若讀取失敗或檔案損壞會直接崩潰，無容錯能力。
- **Q5：** `borrow` 指令沒有處理 ISBN 不存在的情況，且重複 ISBN 會導致多重更新，邏輯不明確。

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A：請將 legacy_lib.py 依功能拆成類別或函式，並改成使用 JSON 儲存書籍資料，避免自訂的 @@ / ## 分隔格式。

Prompt B：請在 modern_library.py 中加入錯誤處理，對 `add`、`borrow`、`show` 指令，以及檔案讀取/寫入失敗加入 try/except 保護。

Prompt C：請讓程式在 `exit` 時一次寫入 `books.json`，不要每次新增都打開磁碟，並加入 ISBN 重複檢查與 borrow 未找到時的明確回應。
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？

AI 初期版本仍保留舊式純文字分割格式，且未針對 borrow 找不到 ISBN 的情況給出明確回應。透過閱讀生成程式碼與手動測試後，發現這些問題並要求補正。

2. 發現的問題：AI 初版漏寫 JSON 格式儲存，且 borrow 指令缺少 `ISBN Not Found` 的處理。

3. 修正的對話：我告訴它「請改用 `json.dump` / `json.load`，並改成 `books.json` 儲存，borrow 失敗時要回傳 `ISBN Not Found`，exit 時才寫入檔案」。

---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
Get-Content test_input_data.txt | python modern_library.py
=== 圖書管理系統 v0.2 (Modern) ===
可用指令：
  add <title>/<isbn>/<status>  - 新增書籍
  show                       - 顯示所有書籍
  borrow <isbn>              - 借閱書籍
  exit                       - 儲存並離開
> Success
> Success
> Success
> ISBN Exist
> Updated
> 書名: 深入淺出Python, ISBN: 978001, 狀態: available
書名: 資料結構理論, ISBN: 978002, 狀態: borrowed
書名: 演算法實作, ISBN: 978003, 狀態: available
> 系統關閉
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
    "title": "深入淺出Python",
    "isbn": "978001",
    "status": "available"
  },
  {
    "title": "資料結構理論",
    "isbn": "978002",
    "status": "borrowed"
  },
  {
    "title": "演算法實作",
    "isbn": "978003",
    "status": "available"
  }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)

```log
a5b1c3d (HEAD -> master, origin/master) feat: complete modern_library.py and verify test_input_data matching
f3e2d1c refactor: enhance error handling and optimize file IO efficiency for json storage
c7b8a90 feat: architecture setup for modern_library.py with Book and LibraryManager classes via Copilot
e1f1ead docs: initial project setup with legacy code static analysis in Answer.MD
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
https://github.com/lky00100-blip/B11409006-0527-Final.git
```