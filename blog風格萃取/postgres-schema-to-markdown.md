---
title: postgres schema to markdown
date: 2026-05-06 09:08:45
tags:
---
&nbsp;
<!-- more -->

被抓來救火, 對方給我一個 mssql 的 word 資料字典, 結果上線的程式是 postgres
欄位名稱跟實際 db 的名稱也有所出入
研究一下總共有 1xx 張 table 導致丟進去 AI 沒辦法得到精準的校正, AI 會遺漏欄位
後來請 AI 產出這段 sql 撈出全部的 table 還有詳細欄位 屬性

```sql
SELECT
    t.table_name AS "資料表名稱",
    c.column_name AS "欄位名稱",
    pd.description AS "中文名稱/描述",
    -- 修正後的資料型態顯示邏輯
    CASE
        WHEN c.data_type = 'character varying' THEN
            'character varying' || COALESCE('(' || c.character_maximum_length || ')', '')
        WHEN c.data_type = 'character' THEN
            'character' || COALESCE('(' || c.character_maximum_length || ')', '')
        WHEN c.data_type = 'numeric' THEN
            'numeric' || COALESCE('(' || c.numeric_precision || ',' || c.numeric_scale || ')', '')
        WHEN c.data_type = 'USER-DEFINED' THEN
            c.udt_name -- 處理自定義型態
        ELSE
            c.data_type
    END AS "資料型態",
    c.is_nullable AS "是否允許空值",
    CASE
        WHEN pk.column_name IS NOT NULL THEN 'P'
        ELSE ''
    END AS "索引/P"
	--,COALESCE(c.column_default, '') AS "預設值"
FROM
    information_schema.tables t
JOIN
    information_schema.columns c ON t.table_name = c.table_name AND t.table_schema = c.table_schema
LEFT JOIN
    pg_catalog.pg_class cl ON cl.relname = t.table_name
LEFT JOIN
    pg_catalog.pg_namespace ns ON ns.oid = cl.relnamespace AND ns.nspname = t.table_schema
LEFT JOIN
    pg_catalog.pg_description pd ON pd.objoid = cl.oid AND pd.objsubid = c.ordinal_position
-- 查詢主鍵資訊
LEFT JOIN (
    SELECT
        kcu.table_name,
        kcu.column_name,
        kcu.table_schema
    FROM
        information_schema.table_constraints tc
    JOIN
        information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
    WHERE
        tc.constraint_type = 'PRIMARY KEY'
) pk ON pk.table_name = t.table_name AND pk.column_name = c.column_name AND pk.table_schema = t.table_schema
WHERE
    t.table_schema = 'yourschema'
    AND t.table_type = 'BASE TABLE'
ORDER BY
    t.table_name,
    c.ordinal_position;
```

這段則是將欄位註記採用 json 更新至 postgres, json 會有 `中文名稱` `欄位範例` 兩個屬性

```
DO $$
DECLARE
    r RECORD;
    v_new_comment TEXT;
BEGIN
    FOR r IN
        SELECT
            cols.table_schema,
            cols.table_name,
            cols.column_name,
            pd.description as current_comment
        FROM
            information_schema.columns cols
        JOIN
            pg_catalog.pg_class pc ON pc.relname = cols.table_name
        JOIN
            pg_catalog.pg_namespace pn ON pn.oid = pc.relnamespace AND pn.nspname = cols.table_schema
        LEFT JOIN
            pg_catalog.pg_description pd ON pd.objoid = pc.oid AND pd.objsubid = cols.ordinal_position
        WHERE
            cols.table_schema = 'yourschema'
    LOOP
        -- 檢查是否已經是 JSON 格式，若不是才進行轉換
        IF r.current_comment IS NULL OR r.current_comment NOT LIKE '{%' THEN
            -- 構造 JSON：{"中文名稱": "...", "欄位範例": ""}
            v_new_comment := json_build_object(
                '中文名稱', COALESCE(r.current_comment, r.column_name),
                '欄位範例', ''
            )::text;

            -- 執行更新指令
            EXECUTE format('COMMENT ON COLUMN %I.%I.%I IS %L',
                r.table_schema, r.table_name, r.column_name, v_new_comment);
        END IF;
    END LOOP; -- 修正處：這裡應為 END LOOP;
END $$;
```

最後再用以下程式碼將 csv 轉為 markdown

```python
import csv
import json
import sys

def convert():
    tables = {}
    with open('完整table.csv', mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader) # skip header
        for row in reader:
            if len(row) < 6: continue
            table_name, col_name, desc_json_str, data_type, nullable, index_p = row
            
            if table_name not in tables:
                tables[table_name] = []
            
            # Parse JSON in 中文名稱/描述
            try:
                desc_json = json.loads(desc_json_str)
                chinese_name = desc_json.get('中文名稱', '')
                example = desc_json.get('欄位範例', '')
            except:
                chinese_name = desc_json_str
                example = ''
                
            tables[table_name].append({
                'col_name': col_name,
                'chinese_name': chinese_name,
                'data_type': data_type,
                'example': example,
                'index': index_p
            })

    output = []
    for table_name, columns in tables.items():
        output.append(f'### 資料表: {table_name}')
        output.append('| 欄位名稱 | 中文名稱 | 資料型態 | 欄位範例 | 索引 |')
        output.append('| :--- | :--- | :--- | :--- | :--- |')
        for col in columns:
            # Handle potential pipes in data
            c_name = str(col['col_name']).replace('|', '\\|')
            zh_name = str(col['chinese_name']).replace('|', '\\|')
            d_type = str(col['data_type']).replace('|', '\\|')
            ex = str(col['example']).replace('|', '\\|')
            idx = str(col['index']).replace('|', '\\|')
            output.append(f'| {c_name} | {zh_name} | {d_type} | {ex} | {idx} |')
        output.append('\n')
    
    with open('完整table.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

if __name__ == "__main__":
    convert()

```
