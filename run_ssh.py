import paramiko
import sys
import time

def run_ssh_command(host, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {host}:{port} as {username}...")
        client.connect(hostname=host, port=port, username=username, password=password)
        print(f"Executing command: {command}")
        
        # Need to request a PTY for some commands like apt-get that might otherwise fail or buffer weirdly
        # But wait, paramiko exec_command runs in a single session.
        # It's better to use invoke_shell for complex scripts, but exec_command is simpler for one-offs.
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        
        # Wait for the command to finish and print output
        exit_status = stdout.channel.recv_exit_status()
        
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        
        print("--- STDOUT ---")
        import sys; sys.stdout.buffer.write(out.encode('utf-8'))
        print("--- STDERR ---")
        print(err)
        print(f"--- EXIT STATUS: {exit_status} ---")
        
    except Exception as e:
        print(f"Failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_ssh.py <command>")
        sys.exit(1)
        
    cmd = " ".join(sys.argv[1:])
    run_ssh_command("103.97.127.34", 2018, "root", "kA0P74Ygdb", cmd)
