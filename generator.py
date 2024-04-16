import mysql.connector

# Menghubungkan ke database
conn = mysql.connector.connect(
    host="localhost", # Your Hostname
    user="root", # Your MySQL Username
    password="", # Your MySQL Password 
    database="techsmart" # Your Database Name
)

# Membuat objek cursor untuk mengeksekusi perintah SQL
cursor = conn.cursor()

# Membuat tabel
def create_table():
    table_name = input("Masukkan nama tabel: ")
    column_count = int(input("Masukkan jumlah kolom: "))
    
    columns = []
    primary_key = None
    foreign_keys = []
    for i in range(column_count):
        column_name = input(f"Masukkan nama kolom ke-{i+1}: ")
        column_type = input(f"Masukkan tipe data untuk kolom {column_name} (misalnya VARCHAR(50)): ")
        is_primary_key = input(f"Apakah kolom {column_name} adalah primary key? (y/n): ").lower()
        if is_primary_key == 'y':
            primary_key = column_name
        columns.append(f"`{column_name}` {column_type} NOT NULL")

        foreign_key_input = input(f"Apakah kolom {column_name} adalah foreign key? (y/n): ")
        if foreign_key_input.lower() == 'y':
            referenced_table = input(f"Masukkan nama tabel yang dirujuk: ")
            referenced_column = input(f"Masukkan nama kolom di tabel {referenced_table}: ")
            foreign_keys.append((column_name, referenced_table, referenced_column))
    
    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
    create_table_query += ",\n".join(columns)
    if primary_key:
        create_table_query += f",\nPRIMARY KEY (`{primary_key}`)"
    if foreign_keys:
        foreign_key_queries = [f"FOREIGN KEY (`{fk[0]}`) REFERENCES `{fk[1]}`(`{fk[2]}`)" for fk in foreign_keys]
        create_table_query += ",\n" + ",\n".join(foreign_key_queries)
    create_table_query += "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"
    
    print("Query SQL:")
    print(create_table_query)  # Cetak query SQL
    cursor.execute(create_table_query)
    print("Tabel berhasil dibuat")


# Menambahkan data ke tabel
def insert_data():
    # Menampilkan daftar tabel
    list_tables()
    
    # Memilih tabel
    table_name = input("Masukkan nama tabel: ")
    
    # Mendapatkan daftar kolom dari tabel
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    column_names = [column[0] for column in columns]

    # Menampilkan daftar kolom
    print("Daftar kolom dalam tabel:")
    for i, column_name in enumerate(column_names, start=1):
        print(f"{i}. {column_name}")

    # Meminta input nilai untuk setiap kolom
    values = []
    for column_name in column_names:
        value = input(f"Masukkan nilai untuk kolom {column_name}: ")
        values.append(value)

    # Membuat string query SQL untuk memasukkan data
    insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s']*len(values))})"

    # Menjalankan query SQL
    print("Query SQL:")
    # Mengganti placeholder %s dengan nilai yang dimasukkan
    insert_query = insert_query.format(*values)
    print(insert_query)  # Cetak query SQL
    cursor.execute(insert_query, values)
    conn.commit()
    print("Data berhasil ditambahkan")


def view_table(table_name):
    # Mendapatkan struktur kolom dari tabel
    describe_query = f"DESCRIBE `{table_name}`"
    cursor.execute(describe_query)
    columns = cursor.fetchall()

    print(f"\nStruktur kolom tabel {table_name}:")
    for column in columns:
        print(column[0], "-", column[1])

    # Mendapatkan data dari tabel
    select_query = f"SELECT * FROM `{table_name}`"
    cursor.execute(select_query)
    records = cursor.fetchall()

    if records:
        print("\nIsi tabel:")
        for record in records:
            print(record)
    else:
        print(f"Tabel {table_name} kosong")


# Melihat isi database
def view_database():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        select_query = f"SELECT * FROM `{table_name}`"
        print("Query SQL:")
        print(select_query)  # Cetak query SQL
        cursor.execute(select_query)
        records = cursor.fetchall()
        if records:
            print(f"Isi tabel {table_name}:")
            for record in records:
                print(record)
        else:
            print(f"Tabel {table_name} kosong")
        print()  # Membuat baris kosong antara setiap tabel

# Mencetak daftar tabel yang ada dalam database
def list_tables():
    show_tables_query = "SHOW TABLES"
    print("Query SQL:")
    print(show_tables_query)  # Cetak query SQL
    cursor.execute(show_tables_query)
    tables = cursor.fetchall()
    print("Daftar tabel dalam database:")
    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table[0]}")


# Fungsi untuk menghapus data dari tabel
def delete_data():
    # Menampilkan daftar tabel
    list_tables()
    
    # Memilih tabel
    table_name = input("Masukkan nama tabel: ")

    # Menampilkan struktur dan isi tabel yang dipilih
    view_table(table_name)

    # Meminta ID data yang akan dihapus
    record_id = input("Masukkan ID data yang akan dihapus: ")

    # Membuat query SQL untuk menghapus data
    delete_query = f"DELETE FROM {table_name} WHERE id = %s"

    # Menjalankan query SQL
    print("Query SQL:")
    print(delete_query)  # Cetak query SQL
    cursor.execute(delete_query, (record_id,))
    conn.commit()
    print("Data berhasil dihapus")


# Menghapus tabel dari database
def drop_table():
    # Menampilkan daftar tabel
    list_tables()
    
    # Memilih tabel
    table_name = input("Masukkan nama tabel yang akan dihapus: ")

    # Membuat query SQL untuk menghapus tabel
    drop_table_query = f"DROP TABLE IF EXISTS {table_name}"

    # Menjalankan query SQL
    print("Query SQL:")
    print(drop_table_query)  # Cetak query SQL
    cursor.execute(drop_table_query)
    conn.commit()
    print("Tabel berhasil dihapus")



# Pilihan menu
def menu():
    print("=============== WELCOME TO MYSQL BUILDER ===============")
    print("Menu:")
    print("1. Tambah Tabel")
    print("2. Hapus Tabel")
    print("3. Tambah Data")
    print("4. Hapus Data")
    print("5. Lihat Isi Tabel")
    print("6. Lihat Isi Database")
    print("7. List Tabel")
    print("0. Keluar")

# Program Utama
try:
    while True:
        menu()
        choice = input("Pilih menu: ")

        if choice == '1':
            create_table()
        elif choice == '4':
            delete_data()
        elif choice == '3':
            insert_data()
        elif choice == '2':
            drop_table()
        elif choice == '5':
            list_tables()
            table_name = input("Masukkan nama tabel: ")
            view_table(table_name)
        elif choice == '6':
            view_database()
        elif choice == '7':
            list_tables()
        elif choice == '0':
            break
        else:
            print("Pilihan tidak valid.")

except mysql.connector.Error as error:
    print("Error:", error)

finally:
    # Menutup cursor dan koneksi
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Koneksi ditutup")
