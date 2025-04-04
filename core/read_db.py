# # # # import os
# # # # import sqlite3
# # # # import tempfile


# # # # def query_db(db_path, password=None):
# # # #     """
# # # #     执行SQLite查询并返回数据库连接，支持解密SQLCipher加密的数据库

# # # #     :param db_path: SQLite数据库文件路径
# # # #     :param query: SQL查询语句
# # # #     :param password: 可选，解密数据库的密码
# # # #     :return: 连接
# # # #     :raises: 解密失败时抛出异常
# # # #     """
# # # #     temp_path = None
# # # #     conn = None

# # # #     # try:
# # # #     if password is not None:
# # # #         # 读取数据库文件前1024字节和后部数据
# # # #         with open(db_path, "rb") as f:
# # # #             first_1024 = f.read(1024)
# # # #             remaining_data = f.read()

# # # #         # 确定HMAC算法类型
# # # #         hmac_type = "sha1"
# # # #         if b"HMAC_SHA512" in first_1024:
# # # #             hmac_type = "sha512"
# # # #         elif b"HMAC_SHA1" in first_1024:
# # # #             hmac_type = "sha1"

# # # #         # 创建临时文件保存后部数据
# # # #         # TODO: 临时文件路径规范化
# # # #         temp_fd, temp_path = tempfile.mkstemp()
# # # #         os.close(temp_fd)
# # # #         with open(temp_path, "wb") as f_temp:
# # # #             f_temp.write(remaining_data)

# # # #         # 连接临时数据库并设置解密参数
# # # #         conn = sqlite3.connect(temp_path)
# # # #         cursor = conn.cursor()
# # # #         cursor.execute(f"PRAGMA key = {password}")
# # # #         cursor.execute("PRAGMA kdf_iter = 4000")
# # # #         cursor.execute(f"PRAGMA cipher_hmac_algorithm = {hmac_type.upper()}")

# # # #         # 验证解密是否成功
# # # #         cursor.execute("SELECT count(*) FROM sqlite_master")
# # # #         cursor.fetchone()
# # # #     else:
# # # #         # 无密码直接连接原数据库
# # # #         conn = sqlite3.connect(db_path)
# # # #         cursor = conn.cursor()
# # # #     return conn

# # # #     # except Exception as e:
# # # #     #     # 抛出异常供上层处理
# # # #     #     raise Exception(f"数据库操作失败: {str(e)}")

# # # # path=input("请输入数据库路径：")
# # # # password=input("请输入数据库密码：")
# # # # conn=query_db(path,password)
# # # # print("数据库连接成功！")
# # # # print(conn)

# # # import os
# # # import sqlite3
# # # import tempfile

# # # class read_db:
# # #     @staticmethod
# # #     def query_db(db_path, password=None):
# # #         """
# # #         执行SQLite查询并返回数据库连接，支持解密SQLCipher加密的数据库
        
# # #         :param db_path: SQLite数据库文件路径
# # #         :param password: 可选，解密数据库的密码
# # #         :return: 数据库连接对象
# # #         :raises: 解密失败时抛出异常
# # #         """
# # #         temp_path = None
# # #         conn = None
        
# # #         try:
# # #             # 读取数据库文件（跳过前1024字节）
# # #             with open(db_path, "rb") as f:
# # #                 f.seek(1024)  # 跳过前1024字节
# # #                 db_data = f.read()
            
# # #             # 创建临时文件
# # #             temp_fd, temp_path = tempfile.mkstemp()
# # #             os.close(temp_fd)
# # #             with open(temp_path, "wb") as f_temp:
# # #                 f_temp.write(db_data)
            
# # #             # 连接临时数据库
# # #             conn = sqlite3.connect(temp_path)
            
# # #             if password is not None:
# # #                 cursor = conn.cursor()
# # #                 cursor.execute("PRAGMA key = ?", (password,))
# # #                 cursor.execute("PRAGMA kdf_iter = 4000")
# # #                 cursor.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1")
                
# # #                 # 验证解密是否成功
# # #                 cursor.execute("SELECT count(*) FROM sqlite_master")
# # #                 cursor.fetchone()
            
# # #             # 保存临时文件路径以便后续删除
# # #             conn._temp_db_file = temp_path
# # #             return conn
            
# # #         except Exception as e:
# # #             # 清理临时文件
# # #             # if temp_path and os.path.exists(temp_path):
# # #             #     os.unlink(temp_path)
# # #             raise Exception(f"数据库操作失败: {str(e)}")

# # #     @staticmethod
# # #     def close_db(conn):
# # #         """关闭数据库连接并清理临时文件"""
# # #         if conn:
# # #             if hasattr(conn, '_temp_db_file'):
# # #                 try:
# # #                     os.unlink(conn._temp_db_file)
# # #                 except:
# # #                     pass
# # #             conn.close()

# # # # 使用示例
# # # path = input("请输入数据库路径：")
# # # password = input("请输入数据库密码：")
# # # try:
# # #     conn = read_db.query_db(path, password)
# # #     print("数据库连接成功！")
    
# # #     # 执行查询
# # #     cursor = conn.cursor()
# # #     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# # #     print("数据库中的表：", cursor.fetchall())
    
# # # finally:
# # #     if 'conn' in locals():
# # #         read_db.close_db(conn)

# # import os
# # import sqlite3

# # class read_db:
# #     @staticmethod
# #     def query_db(db_path, password=None):
# #         """
# #         执行SQLite查询并返回数据库连接，支持解密SQLCipher加密的数据库
        
# #         :param db_path: SQLite数据库文件路径
# #         :param password: 可选，解密数据库的密码
# #         :return: 数据库连接对象
# #         :raises: 解密失败时抛出异常
# #         """
# #         temp_path = None
# #         conn = None
        
# #         try:
# #             # 获取原始数据库所在目录
# #             db_dir = os.path.dirname(os.path.abspath(db_path))
# #             db_name = os.path.basename(db_path)
            
# #             # 创建临时文件名（在原目录下）
# #             temp_name = f"temp_{db_name}"
# #             temp_path = os.path.join(db_dir, temp_name)
            
# #             # 读取数据库文件（跳过前1024字节）
# #             with open(db_path, "rb") as f:
# #                 f.seek(1024)  # 跳过前1024字节
# #                 db_data = f.read()
            
# #             # 写入临时文件
# #             with open(temp_path, "wb") as f_temp:
# #                 f_temp.write(db_data)
            
# #             # 连接临时数据库
# #             conn = sqlite3.connect(temp_path)
            
# #             if password is not None:
# #                 cursor = conn.cursor()
# #                 cursor.execute("PRAGMA key ="+password)
# #                 cursor.execute("PRAGMA kdf_iter = 4000")
# #                 cursor.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1")
                
# #                 # 验证解密是否成功
# #                 cursor.execute("SELECT count(*) FROM sqlite_master")
# #                 cursor.fetchone()
            
# #             # 保存临时文件路径以便后续删除
# #             conn._temp_db_file = temp_path
# #             return conn
            
# #         except Exception as e:
# #             # 清理临时文件
# #             if temp_path and os.path.exists(temp_path):
# #                 try:
# #                     os.unlink(temp_path)
# #                 except:
# #                     pass
# #             raise Exception(f"数据库操作失败: {str(e)}")

# #     @staticmethod
# #     def close_db(conn):
# #         """关闭数据库连接并清理临时文件"""
# #         if conn:
# #             if hasattr(conn, '_temp_db_file'):
# #                 try:
# #                     os.unlink(conn._temp_db_file)
# #                 except:
# #                     pass
# #             conn.close()

# # # 使用示例
# # if __name__ == "__main__":
# #     path = input("请输入数据库路径：")
# #     password = input("请输入数据库密码(若无密码直接回车)：") or None
    
# #     try:
# #         conn = read_db.query_db(path, password)
# #         print("数据库连接成功！")
        
# #         # 执行查询
# #         cursor = conn.cursor()
# #         cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# #         tables = cursor.fetchall()
# #         print("数据库中的表：")
# #         for table in tables:
# #             print(table[0])
        
# #     except Exception as e:
# #         print(f"错误: {str(e)}")
# #     finally:
# #         if 'conn' in locals():
# #             read_db.close_db(conn)

# import os
# import sqlite3
# import tempfile

# class read_db:
#     @staticmethod
#     def query_db(db_path, password=None):
#         """
#         执行SQLite查询并返回数据库连接，支持解密SQLCipher加密的数据库
        
#         :param db_path: SQLite数据库文件路径
#         :param password: 可选，解密数据库的密码
#         :return: 数据库连接对象
#         :raises: 解密失败时抛出异常
#         """
#         temp_path = None
#         conn = None
        
#         try:
#             # 获取原始数据库所在目录
#             db_dir = os.path.dirname(os.path.abspath(db_path))
#             db_name = os.path.basename(db_path)
            
#             # 创建临时文件名（在原目录下）
#             temp_name = f"temp_{db_name}"
#             temp_path = os.path.join(db_dir, temp_name)
            
#             # 读取数据库文件（跳过前1024字节）
#             with open(db_path, "rb") as f:
#                 f.seek(1024)  # 跳过前1024字节
#                 db_data = f.read()
            
#             # 写入临时文件
#             with open(temp_path, "wb") as f_temp:
#                 f_temp.write(db_data)
            
#             # 连接临时数据库
#             conn = sqlite3.connect(temp_path)
            
#             if password is not None:
#                 cursor = conn.cursor()
#                 # 使用参数化查询避免特殊字符问题
#                 cursor.execute("PRAGMA key = ?", (password,))
#                 cursor.execute("PRAGMA cipher_compatibility = 4")  # 兼容性设置
#                 cursor.execute("PRAGMA kdf_iter = 4000")
#                 cursor.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1")
                
#                 # 验证解密是否成功
#                 try:
#                     cursor.execute("SELECT count(*) FROM sqlite_master")
#                     cursor.fetchone()
#                 except sqlite3.DatabaseError:
#                     raise Exception("解密失败 - 密码错误或数据库损坏")
            
#             # 保存临时文件路径以便后续删除
#             conn._temp_db_file = temp_path
#             return conn
            
#         except Exception as e:
#             # 清理临时文件
#             if temp_path and os.path.exists(temp_path):
#                 try:
#                     os.unlink(temp_path)
#                 except:
#                     pass
#             raise Exception(f"数据库操作失败: {str(e)}")

#     @staticmethod
#     def close_db(conn):
#         """关闭数据库连接并清理临时文件"""
#         if conn:
#             if hasattr(conn, '_temp_db_file'):
#                 try:
#                     os.unlink(conn._temp_db_file)
#                 except:
#                     pass
#             conn.close()

# # 使用示例
# if __name__ == "__main__":
#     path = input("请输入数据库路径：").strip('"')  # 处理可能包含的引号
#     password = input("请输入数据库密码(若无密码直接回车)：") or None
    
#     try:
#         conn = read_db.query_db(path, password)
#         print("数据库连接成功！")
        
#         # 执行查询
#         cursor = conn.cursor()
#         cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#         tables = cursor.fetchall()
#         print("数据库中的表：")
#         for table in tables:
#             print(table[0])
        
#     except Exception as e:
#         print(f"错误: {str(e)}")
#     finally:
#         if 'conn' in locals():
#             read_db.close_db(conn)


import os
import sqlite3
import tempfile
import shutil

class read_db:
    @staticmethod
    def query_db(db_path, password=None):
        """
        执行SQLite查询并返回数据库连接，支持解密SQLCipher加密的数据库
        
        :param db_path: SQLite数据库文件路径
        :param password: 可选，解密数据库的密码
        :return: 数据库连接对象
        :raises: 解密失败时抛出异常
        """
        temp_path = None
        conn = None
        
        try:
            # 获取原始数据库所在目录
            db_dir = os.path.dirname(os.path.abspath(db_path))
            db_name = os.path.basename(db_path)
            
            # 创建临时文件名（在原目录下）
            temp_name = f"temp_{db_name}"
            temp_path = os.path.join(db_dir, temp_name)
            
                        # 读取数据库文件前1024字节和后部数据
            with open(db_path, "rb") as f:
                first_1024 = f.read(1024)
                remaining_data = f.read()

            # 确定HMAC算法类型
            hmac_type = "sha1"
            if b"HMAC_SHA512" in first_1024:
                hmac_type = "HMAC_SHA512"
            elif b"HMAC_SHA1" in first_1024:
                hmac_type = "HMAC_SHA1"

            
            # 复制原始数据库文件（跳过前1024字节）
            with open(db_path, "rb") as src, open(temp_path, "wb") as dst:
                src.seek(1024)  # 跳过前1024字节
                shutil.copyfileobj(src, dst)
            
            # 连接临时数据库
            conn = sqlite3.connect(temp_path)
            
            if password is not None:
                cursor = conn.cursor()
                # 直接拼接密码字符串（注意转义单引号）
                safe_password = password.replace("'", "''")
                cursor.execute(f"PRAGMA key = '{safe_password}'")
                # cursor.execute("PRAGMA cipher_compatibility = 4")
                cursor.execute("PRAGMA kdf_iter = 4000")
                cursor.execute(f"PRAGMA cipher_hmac_algorithm = {hmac_type.upper()}")
                cursor.execute("PRAGMA cipher_page_size = 4096")
                cursor.execute("PRAGMA cipher_default_kdf_algorithm = PBKDF2_HMAC_SHA512")
                cursor.execute("PRAGMA cipher = 'aes-256-cbc'")
                
                # 验证解密是否成功
                try:
                    cursor.execute("SELECT count(*) FROM sqlite_master")
                    cursor.fetchone()
                except sqlite3.DatabaseError as e:
                    raise Exception(f"解密失败 - 密码错误或数据库不兼容: {str(e)}")
            
            # 保存临时文件路径以便后续删除
            conn._temp_db_file = temp_path
            return conn
            
        except Exception as e:
            # 清理临时文件
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except:
                    pass
            raise Exception(f"数据库操作失败: {str(e)}")

    @staticmethod
    def close_db(conn):
        """关闭数据库连接并清理临时文件"""
        if conn:
            if hasattr(conn, '_temp_db_file'):
                try:
                    os.unlink(conn._temp_db_file)
                except:
                    pass
            conn.close()

# 使用示例
if __name__ == "__main__":
    path = input("请输入数据库路径：").strip('"\'')
    password = input("请输入数据库密码(若无密码直接回车)：") or None
    
    try:
        conn = read_db.query_db(path, password)
        print("数据库连接成功！")
        
        # 执行查询
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("数据库中的表：")
        for table in tables:
            print(table[0])
        
    except Exception as e:
        print(f"错误: {str(e)}")
    finally:
        if 'conn' in locals():
            read_db.close_db(conn)