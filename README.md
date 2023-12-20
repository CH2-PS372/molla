## **API Contract**
### **Read Image**

**POST /read_image**
----
  Melakukan text extraction dengan OCR. Mengembalikan `extracted_text` dan `translated_text`
* **URL Params**  
  None
* **Data Params**  
  ```
  {
      image: <file-image>
  }
  ```
* **Headers**  
  Content-Type: multipart/form-data
* **Success Response:**  
  * **Code:** 200  
    **Content:**  
  ```
  {
    extracted_text: "string extracted text goes here",
    translated_text: "string translated text goes here
  }
  ```

* **Error Response:**
  * **Code:** 400  
  **Content:** `{ "error": "No image file provided" }`
---
### **Translate**

**POST /translate**
---
  Mendapatkan hasil terjemahan dari sebuah teks
* **URL Params**  
  None
* **Data Params**
example:  
   ```
  {
      "text": "I just want a better life"
  }
  ```
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
  * **Code:** 200  
  **Content:**  
  ```
  {
    "text": "I just want a better life",
    "translated_text": "Saya hanya ingin hidup yang lebih baik"
  }
  ```
* **Error Response:**
  * **Code:** 400  
  **Content:** `{ "error": "No text provided for translation" }`
