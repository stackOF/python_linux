import datetime
import subprocess
from subprocess import Popen
import psutil


def get_users_and_process():
    """Get all users, all process, all users process"""
    # Users
    u = Popen("sed 's/:.*//' /etc/passwd", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    all_users = u[0].decode('UTF-8').replace('\n', ', ')
    print(f"All systems users: {all_users}")

    # Process
    p = Popen("ps -A | wc -l", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    run_process = p[0].decode('UTF-8')
    print(f"Run process: {run_process}")

    # Users processes
    users_processes_list = ''
    for user in all_users.replace(',', ' ').split():
        command_str = f"ps U {user} | wc -l"
        up = Popen(command_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        uses_processes = f"{user}: {up[0].decode('UTF-8')}"
        users_processes_list = users_processes_list + uses_processes
    print(f"Users process: \n{users_processes_list}")

    # Total memory used
    total_mem = psutil.virtual_memory().used / 1024**2
    print(f"Total memory used: {total_mem}")

    # Total cpu used
    total_cpu = psutil.cpu_percent(interval=0.1)
    print(f"Total cpu used: {total_cpu}")

    # Top %mem process
    m = Popen("ps -eo cmd --sort -%mem | head -n 2 | tail -n 1", stdout=subprocess.PIPE,
              stderr=subprocess.PIPE, shell=True).communicate()
    top_mem = m[0][:20].decode('UTF-8')
    print(f"The most memory used process: {top_mem}")

    # Top CPU used
    ps = Popen("ps -eo cmd --sort -%cpu | head -n 2 | tail -n 1", stdout=subprocess.PIPE,
               stderr=subprocess.PIPE, shell=True).communicate()
    top_pr = ps[0][:20].decode('UTF-8')
    print(f"The most CPU used process: {top_pr}")

    # Export data to file
    f = open(f"{datetime.datetime.now().strftime('%d-%m-%Y-%H:%M')}-scan.txt", "w")
    f.write("System status report: \n")
    f.write(f"All systems users: {all_users} \n")
    f.write(f"Run process: {run_process} \n")
    f.write(f"Users process: \n{users_processes_list}")
    f.write("... \n")
    f.write(f"Total memory used: {total_mem} \n")
    f.write(f"Total cpu used: {total_cpu} \n")
    f.write(f"The most memory used process: {top_mem} \n")
    f.write(f"The most CPU used process: {top_pr} \n")


if __name__ == '__main__':
    pass
    get_users_and_process()
