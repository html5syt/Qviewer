import base64
import json
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Union
import blackboxprotobuf
import threading
import sqlite3
import os
import tempfile
import methods as mt

# class Load():


class Read_DB:
    def query_db_decrypted(self,db_path, query):
        """
        执行SQLite查询并将结果转换为字典列表，自动尝试用Protobuf解析字节类型字段

        :param db_path: SQLite数据库文件路径
        :param query: SQL查询语句
        :return: 包含结果字典的列表，键为列名
        """
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(query)

            # 获取列名信息
            columns = [col[0] for col in cursor.description] if cursor.description else []
            results = []

            # 遍历所有结果行
            for row in cursor.fetchall():
                processed_row = {}
                for idx, value in enumerate(row):
                    col_name = columns[idx]

                    # 处理字节类型字段
                    if isinstance(value, bytes):
                        try:
                            # 尝试Protobuf解码
                            decoded, _ = blackboxprotobuf.decode_message(value)
                            processed_row[col_name] = decoded
                        except Exception as e:
                            # 解析失败保留原始值
                            print(e)
                            processed_row[col_name] = value
                    else:
                        processed_row[col_name] = value

                results.append(processed_row)

            return results
        finally:
            conn.close()

    # TODO:解密SQLCipher加密的数据库

    def query_db(self, db_path, query, password=None):
        """
        执行SQLite查询并将结果转换为字典列表，支持解密SQLCipher加密的数据库

        :param db_path: SQLite数据库文件路径
        :param query: SQL查询语句
        :param password: 可选，解密数据库的密码
        :return: 包含结果字典的列表，键为列名
        :raises: 解密失败时抛出异常
        """
        temp_path = None
        conn = None

        try:
            if password is not None:
                # 读取数据库文件前1024字节和后部数据
                with open(db_path, 'rb') as f:
                    first_1024 = f.read(1024)
                    remaining_data = f.read()

                # 确定HMAC算法类型
                hmac_type = 'sha1'
                if b'HMAC_SHA512' in first_1024:
                    hmac_type = 'sha512'
                elif b'HMAC_SHA1' in first_1024:
                    hmac_type = 'sha1'

                # 创建临时文件保存后部数据
                temp_fd, temp_path = tempfile.mkstemp()
                os.close(temp_fd)
                with open(temp_path, 'wb') as f_temp:
                    f_temp.write(remaining_data)

                # 连接临时数据库并设置解密参数
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                cursor.execute("PRAGMA key = ?", (password,))
                cursor.execute("PRAGMA kdf_iter = 4000")
                cursor.execute(f"PRAGMA cipher_hmac_algorithm = {hmac_type.upper()}")

                # 验证解密是否成功
                cursor.execute("SELECT count(*) FROM sqlite_master")
                cursor.fetchone()
            else:
                # 无密码直接连接原数据库
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

            # 执行查询并处理结果
            cursor.execute(query)
            columns = [col[0] for col in cursor.description] if cursor.description else []
            results = []

            for row in cursor.fetchall():
                processed_row = {}
                for idx, value in enumerate(row):
                    col_name = columns[idx]
                    if isinstance(value, bytes):
                        try:
                            decoded, _ = blackboxprotobuf.decode_message(value)
                            processed_row[col_name] = decoded
                        except Exception as e:
                            print(f"Protobuf解码失败: {e}")
                            processed_row[col_name] = value
                    else:
                        processed_row[col_name] = value
                results.append(processed_row)

            return results

        except Exception as e:
            # 抛出异常供上层处理
            raise Exception(f"数据库操作失败: {str(e)}")

        finally:
            # 清理资源
            if conn:
                conn.close()
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    def recursive_process(
        self,data: Union[dict, list], lock: threading.Lock
    ) -> Union[dict, list]:
        """
        递归地处理字典或列表中的字节字符串。
        """
        # 复制结构，避免修改原数据
        new_data = data.copy() if isinstance(data, dict) else list(data)

        # 处理字典
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, bytes):
                    # 替换字节字符串
                    new_data[key] = self.process_byte_string(value, lock)
                elif isinstance(value, (dict, list)):
                    # 递归处理子结构
                    new_data[key] = self.recursive_process(value, lock)

        # 处理列表
        elif isinstance(data, list):
            for i, value in enumerate(data):
                if isinstance(value, bytes):
                    # 替换字节字符串
                    new_data[i] = self.process_byte_string(value, lock)
                elif isinstance(value, (dict, list)):
                    # 递归处理子结构
                    new_data[i] = self.recursive_process(value, lock)

        return new_data

    def process_byte_string(self,byte_str: bytes, lock: threading.Lock) -> str:
        """
        处理字节字符串，按照要求转换。
        """
        try:
            # 1. 尝试 UTF-8 解码
            try:
                utf8_result = byte_str.decode("utf-8")
                return utf8_result
            except UnicodeDecodeError:
                # 如果 UTF-8 解码失败，尝试 ProtoBuf 解码
                try:
                    decoded_message, _ = blackboxprotobuf.decode_message(byte_str)
                    return f"ProtoBuf decoded: {json.dumps(decoded_message)}"
                except:
                    # ProtoBuf 解码失败，转为 Base64 编码
                    base64_result = base64.b64encode(byte_str).decode("utf-8")
                    return base64_result
        finally:
            pass

    def process_data_multithread(self,data: list, num_threads: int = 5) -> list:
        """
        使用多线程递归处理数据。
        """
        lock = threading.Lock()
        results = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # 将数据拆分为多个子任务
            futures = []
            for chunk in data:
                future = executor.submit(self.recursive_process, chunk, lock)
                futures.append(future)

            # 收集结果
            for future in futures:
                results.append(future.result())

        return results

    def read_db(self):
        """
        读取数据库文件，并将结果转换为字典列表，自动尝试用Protobuf解析字节类型字段。
        """
        db_path = input("输入解密后的nt_msg相对于运行目录的路径：")
        group_list = input("请输入需要导出的群号，多个群号用空格分隔：").split()
        start_time_in = input("请输入开始时间（格式：2021-09-01 00:00:00）：")
        time_arr = time.strptime(start_time_in, "%Y-%m-%d %H:%M:%S")
        start_time = time.mktime(time_arr)  # 时间戳
        end_time_in = input("请输入结束时间（格式：2021-09-01 00:00:00）：")
        time_arr = time.strptime(end_time_in, "%Y-%m-%d %H:%M:%S")
        end_time = time.mktime(time_arr)  # 时间戳
        results = self.query_db(
            db_path,
            f"""SELECT *
    FROM group_msg_table
    WHERE "40050" <> 0
    AND "40050" >= {int(start_time)}
    AND "40050" < {int(end_time)}
    AND "40021" IN ('{"','".join(map(str, group_list))}')
    ORDER BY "40050" ;""",
        )

        results1 = self.process_data_multithread(results)

        with open(f"{'+'.join(map(str, group_list))}--S{start_time_in.replace(':', ';')}--E{end_time_in.replace(':', ';')}.json", "w") as f:
            json.dump(results1, f, ensure_ascii=False, indent=4)
