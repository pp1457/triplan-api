# \testing> python3 .\test_process_user_input.py

import os
import sys
import json

# 將 triplan_api/utils/ 加入模組搜尋路徑
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../triplan_api/utils/')))

from process_user_input import process_user_input

# 定義檔案路徑
INPUT_FILE = './user_input'
OUTPUT_FILE = './user_output'

def main():
    # 確保輸出檔案存在或可寫
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return

    # 讀取輸入檔案
    with open(INPUT_FILE, 'r', encoding='utf-8') as infile:
        inputs = infile.readlines()

    # 初始化輸出內容
    outputs = []
    count = 1

    # 處理每個輸入
    for user_input in inputs:
        user_input = user_input.strip()  # 去除換行符號和空白
        if not user_input:
            continue

        try:
            # 呼叫目標函數並轉換為字串
            output = process_user_input(user_input)
            output_str = json.dumps(output, ensure_ascii=False) + '\n'
            outputs.append(output_str)
        except Exception as e:
            # 若處理過程中出現錯誤，記錄錯誤訊息
            outputs.append(f"Error processing input '{user_input}': {str(e)}\n")
        
        print(f"teatcase {count} done.")
        count = count + 1

    # 寫入輸出檔案
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.writelines(outputs)

    print(f"Processing complete.")

if __name__ == '__main__':
    main()
