#!/usr/bin/env python

"""
Connect via SSH using paramiko to get information from
the Linux machine and print it to the screen.
"""

import time
import paramiko

# Function to open connection and send a command
def send_cmd(conn, command):

    conn.send(command + "\n")
    time.sleep(1.0)

# Funtion to decode the byte string as UTF-8.
def get_output(conn):

    return conn.recv(65535).decode("utf-8")


def main():

    host_dict = {
        "Hostname01": "df -h ",
        "Hostname02": "df -h ",
    }

    for hostname, cmd in host_dict.items():
        conn_params = paramiko.SSHClient()
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn_params.connect(
            hostname=hostname,
            port=22,
            username="username",
            password="password",
            look_for_keys=False,
            allow_agent=False,
        )

        # Get an interactive shell and wait a bit for the prompt to appear
        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f"Logged into {get_output(conn).strip()} successfully")

        # Iterate over the list of commands, sending each one in series
        # The final command in the list is the OS-specific VRF "show" command
        commands = [
            "uname -a",
            "uptime",
            cmd,
        ]
        for command in commands:

            send_cmd(conn, command)
            print(get_output(conn))

        # Close session when we are done
        conn.close()


if __name__ == "__main__":
    main()
