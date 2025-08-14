mport subprocess

def get_system_users():
    with open("/etc/passwd", "r") as f:
        return [line.split(":")[0] for line in f]

def get_duplicate_uids():
    uids = subprocess.getoutput("cut -d: -f3 /etc/passwd | sort | uniq -d")
    return uids.splitlines()

def check_ssh_failed_attempts():
    result = subprocess.getoutput("journalctl -u ssh | grep 'Failed password'")
    return result.splitlines()

def check_mfa():
    config = subprocess.getoutput("cat /etc/ssh/sshd_config | grep -i 'AuthenticationMethods'")
    return config.strip()

def main():
    print("🧑‍💻 Usuarios del sistema:")
    for user in get_system_users():
        print(f" - {user}")

    print("\n⚠️ UIDs duplicados (cuentas compartidas):")
    duplicates = get_duplicate_uids()
    if duplicates:
        print("\n".join(duplicates))
    else:
        print("No se encontraron.")

    print("\n🚨 Intentos fallidos de acceso SSH:")
    for line in check_ssh_failed_attempts()[:10]:
        print(f" {line}")

    print("\n🔐 MFA configurado:")
    mfa = check_mfa()
    print(mfa if mfa else "No configurado")

if __name__ == "__main__":
    main()