import paramiko
import subprocess
import pytest

server_ip = '192.168.103.10'
password = 'vm'
username = 'vm'

@pytest.fixture(scope='function')
def server(request):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(server_ip, username=username, password=password)
        print(f"Підключено до серверу {server_ip}")
    except Exception as e:
        raise Exception(f"Не вдалося підключитися до серверу {server_ip}: {e}")

    try:
        command = "iperf3 -s -D"
        stdin, stdout, stderr = ssh.exec_command(command)
        print(f"Iperf сервер піднято на сервері {server_ip}")
    except Exception as e:
        raise Exception(f"Помилка при піднятті iperf сервера: {e}")

    def fin():
        try:
            command = "pkill iperf"
            stdin, stdout, stderr = ssh.exec_command(command)
            print(f"Iperf сервер зупинено на сервері {server_ip}")
        except Exception as e:
            print(f"Помилка при зупиненні iperf сервера: {e}")

        ssh.close()
        print(f"SSH-підключення закрито")

    request.addfinalizer(fin)

    return ssh


@pytest.fixture(scope='function')
def client(server):
    try:
        command = f"iperf3 -c {server_ip}"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        raise Exception(f"Помилка при виконанні iperf: {e}")
    except Exception as e:
        raise Exception(f"Невідома помилка: {e}")