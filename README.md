# Query Generator Bot

Ini adalah alat yang menggunakan [Pyrogram](https://docs.pyrogram.org/) untuk mengelola sesi Telegram dan menghasilkan query dari bot. Kode ini berguna untuk berinteraksi dengan bot Telegram melalui API dan menyimpan query ke file json.

## Fitur

- **Tambah Sesi**: Menambahkan sesi Telegram baru.
- **Generate Query**: Menghasilkan query dari bot dan menyimpannya ke `data.json`.
- **Regenerate Query**: Menghasilkan kembali query setiap 6 jam untuk memperbarui informasi.

## Persyaratan

- Python 3.7+
- Pyrogram
- asyncio
- colorama

## Instalasi

1. **Clone repositori ini:**

   ```bash
   git clone https://github.com/0xsyo/query-generator-json.git
   cd query-generator-json

   python3 -m venv venv
   source venv/bin/activate  # Untuk Linux/MacOS
   venv\Scripts\activate     # Untuk Windows

   pip install -r requirements.txt
   python3 main.py
   python main.py



# Konfigurasi:

Buat environment virtual (opsional tetapi disarankan):

Install semua dependensi yang diperlukan:



# Konfigurasi API ID dan API Hash:

Anda harus mendapatkan api_id dan api_hash dari my.telegram.org.

Buka file main.py dan ganti YOUR_API_ID dan YOUR_API_HASH :

    
    api_id = 'YOUR_API_ID'
    api_hash = 'YOUR_API_HASH'



# Pilih opsi:

Opsi 1: Tambah sesi baru.

Opsi 2: Generate query untuk sesi yang ada.

Tambah Sesi:

Jika memilih opsi 1, masukkan nama sesi baru. Sesi ini akan disimpan di folder sessions.

# Generate Query:

Jika memilih opsi 2, Anda akan diminta untuk memasukkan:

Username bot (contoh: tabizoobot)

Request URL Header Bot (contoh: https://app.tabibot.com)

Setelah Anda mengisi informasi tersebut, program akan menghasilkan query dan menyimpannya di data.json. Query akan di-regenerate setiap 6 jam.

# Catatan
Jika Anda menjalankan opsi 2, program akan terus berjalan dan menghasilkan kembali query setiap 6 jam.
Untuk menghentikan program, gunakan Ctrl + C.
