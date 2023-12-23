import subprocess
import re

def client(server_ip):
    try:
        command = f"iperf3 -c {server_ip}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        return stdout, stderr
    except subprocess.CalledProcessError as e:
        return None, e.stderr

def parser(output):
    intervals = []
    print(output)
    interval_pattern = re.compile(r'([\d.]+-[\d.]+)\s+sec\s+([\d.]+\s+\w?Bytes)\s+([\d.]+\s+\w?bits/sec)[\s\w]\s+([\d.]+)\s+([\d.]+\s+\w?Bytes)')
    matches = interval_pattern.findall(output.strip())
    for match in matches:
        interval = {
            'Interval': match[0],
            'Transfer': float(match[1].split()[0]),
            'Bitrate': float(match[2].split()[0]),
            'Retr': float(match[3].split()[0]),
            'Cwnd': float(match[4].split()[0])
        }
        intervals.append(interval)
    return intervals

def main():
    server_ip = '192.168.103.10'
    result, error = client(server_ip)

    if error:
        print(error)
    else:
        result_list = parser(result)
        for value in result_list:
            if value['Transfer'] > 2 and value['Bitrate'] > 1:
                print(value)

if __name__ == '__main__': 
    main()
