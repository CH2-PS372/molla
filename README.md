# Molla

## **Notes**

Supaya bisa run di vm ada yang beberapa code yang diubah:

- capstone_text_extracting.py

  ### **Kenapa diubah?**
  Struktur folder diubah, gambar untuk diekstrak diambil dari folder ```./images/```.     
  Image path folder tidak terbaca walaupun sudah mengikuti path linux di vm.
   
  Before:
  ```python
  image_folder_path = r'C:\Users\HP ZBOOK\Downloads\capstone'
  filenames = os.listdir(image_folder_path)
  ```
  After:
  ```py
  image_folder_path = os.path.join(os.path.dirname(__file__), "images")
  filenames = os.listdir(image_folder_path)
  ```
## **API Contract**
### **Quiz**


**GET /quiz**
---
  Get uuid, kalimat bahasa inggris, bahasa indonesia, dan kalimat yang diacak.
* **URL Params**  
  Required: ```language = [string]``` 'indonesia/inggris'
* **Data Params**  
  None
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
  * **Code:** 200  
  **Content:**  
  ```
  {
      "question_id": "<random-uuid>",
      "sentence": {
          "correct_translation": "Beritahu saya kenapa dia menangis.",
          "original_sentence": "Tell me why he is crying.",
          "shuffled_sentence": "me crying. is he why Tell"
      }
  }
  ```

**POST /quiz**
----
  Evaluate jawaban user dan return hasilnya ``` true ``` atau ```false```
* **URL Params**  
  None
* **Data Params**  
  ```
  {
      question_id: "<random-uuid>",
      user_answer: "Tell me why he is crying"
  }
  ```
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
  * **Code:** 200  
    **Content:**  
  ```
  {
    result: true
  }
  ```

* **Error Response:**


  * **Code:** 404  
  **Content:** `{ "error": "Invalid question_id: <random-uuid>" }`
---
### **Qeustions**

**GET /questions**
---
  Mendapatkan list berupa question_id dan jawabannya.
* **URL Params**  
  None
* **Data Params**  
  None
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
  * **Code:** 200  
  **Content:**  
  ```
  {
    "question_data": {
        "74484732-27ce-4484-8307-4d818d9a8433": "Are humans fish?",
        "e0382723-6c01-45ac-85d2-c0fb3e4800c1": "This area is rich in marine products.",
        "f474f3b5-55f3-40b5-9fe2-a984f9ffed61": "This insect is so tiny."
    }
  }
  ```
  **DELETE /questions**
  ---
  Menghapus data question berdasarkan id
* **URL Params**  
  Required: ```question_id = [string]``` 
* **Data Params**
  None
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
  * **Code:** 200  
    **Content:**  
  ```
  {
    "question_id": "e0382723-6c01-45ac-85d2-c0fb3e4800c1",
    "status": "deletion success"
  }
  ```
* **Error Response:**
  * **Code:** 404  
  **Content:** `{ "error": "Invalid question_id: <random-uuid>" }`  
