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

  
