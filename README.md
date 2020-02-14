# Houdini Auto-Create Redshift Material
目前設計供夢想動畫公司內部流程使用


## Features
* 自動產生Redshift材質球並連結資料夾路徑內的貼圖


## Getting Started
1. 在 Menu / MoonShine / Auto-create Redshift Material 點選開啟工具視窗

   ![01](https://user-images.githubusercontent.com/42924265/74494847-20b51c80-4f11-11ea-8590-e472e670c279.gif)


* Asset Model :　用 "Select Asset Node" 按鈕選擇當前材質對應的asset模型
 
   ![02](https://user-images.githubusercontent.com/42924265/74496148-c5852900-4f14-11ea-8ada-0dd1d36c49ff.gif)

* Textures Path : 用 "Browse" 按鈕選擇材質貼圖所在路徑資料夾。選擇完後篩選到可以使用的貼圖便會呈現在 "Textures in Folder" 欄位內。預設讀取檔案名稱格式為 `$AssetName.$TextureSetPart.$Channel.$FileType` 。

   ![03](https://user-images.githubusercontent.com/42924265/74496652-50b2ee80-4f16-11ea-84ac-6e3498fcdedc.gif)


* 若檔名格式為其他情況則需勾選 "Custom Name Selection"，手動填入 `$AssetName+$TextureSetPart` 名稱於 "Asset Name and Texture Set"欄位，輸入完後按下 "Reload Textures" 按鈕更新。

   ![04](https://user-images.githubusercontent.com/42924265/74496880-ffefc580-4f16-11ea-88d9-a1a6e052c478.gif)

* Create Shader : 產生材質球於 SOP/obj 階層，並以Asset model名稱命名。

   ![05](https://user-images.githubusercontent.com/42924265/74497117-b9e73180-4f17-11ea-8802-60438426b413.gif)



## Example
範例一 : 貼圖檔名依據 `$AssetName.$TextureSetPart.$Channel.$FileType` 規則 (Ex: car_1.body.BaseColor.png )
1. Asset Model : car_1
2. Textures Path : D:\redshift_shader\asset\car_1\texture\RS_car_1_body
3. Create Shader

範例二 : 貼圖檔名沒有依據 `$AssetName.$TextureSetPart.$Channel.$FileType` 規則 (Ex: car_1_RS_car_body_BaseColor.png )
1. Asset Model : car_1
2. Textures Path : D:\redshift_shader\asset\car_1\texture\RS_car_1_body
3. 勾選 "Custom Name Selection"
4. 在 "Asset Name and Texture Set" 填入 car_1_RS_car_body
5. Reload Textures
6. Create Shader


## 測試環境
* Houdini 18.0.287 / 17.5.425
* Redshift 3.0.13
