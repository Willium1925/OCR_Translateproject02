package org.example.ocrtranslateproject02;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

@RestController
@CrossOrigin // 允許前端跨域請求
public class OcrController {

    @PostMapping("/upload")
    public String uploadImage(@RequestParam("file") MultipartFile file) {
        // 圖片儲存資料夾（絕對路徑，依照你的電腦調整）
        String uploadDir = "D:/FCU/code/AI/final02/uploadtemp/";

        // 確保資料夾存在
        File dir = new File(uploadDir);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        // 產生隨機檔名，避免檔案名稱衝突
        String newFileName = UUID.randomUUID().toString() + ".png";
        File destFile = new File(uploadDir, newFileName);

        try {
            // 將上傳檔案儲存到指定位置
            file.transferTo(destFile);

            // 指定 Anaconda 環境內的 Python 路徑與 Python 腳本
            String pythonPath = "C:/Users/GIGABYTE/.conda/envs/ocr_translate02/python.exe";
            String scriptPath = "D:/FCU/code/AI/final02/translate_module.py";

            // 呼叫 Python 程式
            ProcessBuilder pb = new ProcessBuilder(
                    pythonPath,
                    scriptPath,
                    destFile.getAbsolutePath()
            );

            pb.environment().put("PYTHONIOENCODING", "utf-8"); // Java 端 ProcessBuilder 設定環境變數強制 Python 用 UTF-8
            //pb.redirectErrorStream(true); // 合併標準錯誤與標準輸出


            Process process = pb.start();

            // 讀取 Python 標準輸出
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8));
            StringBuilder resultBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                resultBuilder.append(line).append("\n");
            }

            // 讀取標準錯誤（如果需要）
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream(), StandardCharsets.UTF_8));
            StringBuilder errorBuilder = new StringBuilder();
            String errorLine;
            while ((errorLine = errorReader.readLine()) != null) {
                errorBuilder.append(errorLine).append("\n");
            }

            // 等待 Python 程式執行結束
            int exitCode = process.waitFor();

            // 如果非 0，表示執行失敗，回傳錯誤訊息
            if (exitCode != 0) {
                return "Python 程式執行失敗，錯誤代碼：" + exitCode + "\n訊息：" + resultBuilder;
            }

            // 成功，回傳 OCR 翻譯結果
            return resultBuilder.toString();

        } catch (Exception e) {
            e.printStackTrace();
            return "伺服器發生錯誤：" + e.getMessage();
        }
    }
}
