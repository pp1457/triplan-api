# \triplan-api> python3 -m testing.test_process_user_input

from triplan_api.utils import process_user_input as p

import os

# 定義檔案路徑
INPUT_FILE = './testing/user_input'
OUTPUT_FILE = './testing/user_output'

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
            continue  # 跳過空輸入

        try:
            # 呼叫目標函數並取得結果
            result_dict = p.process_user_input(user_input)
            output = "[ " + p.activity_to_text(result_dict, 1) + " ]"
            for option in range(2, 7):
                output = output + " " + "[ " + p.activity_to_text(result_dict, option)+ " ]"
            
            output = output + "\n"
            outputs.append(output)
        except Exception as e:
            # 若處理過程中出現錯誤，記錄錯誤訊息
            outputs.append(f"Testcase {count} Error: {str(e)}\n")

        print(f"Testcase {count} done.")
        count += 1

    # 寫入輸出檔案
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.writelines(outputs)


    print(f"Processing complete.")

if __name__ == '__main__':
    main()
