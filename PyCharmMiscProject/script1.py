#Strict TPS (HTTP Strict Transport Security (HSTS))
#Forces the browser to use HTTPS instead of HTTP
#Prevents attackers from downgrading
import base64
#Content security policy
#Controls what content is allowed to load on the website
#Helps prevent XSS attacks


#X frame options
#Stops your website from loading inside an iframe
#Protects against clickjacking

#X content type options
#Tells the browser not to guess the file type (no MIME sniffing)
#Prevents malicious files from being executed incorrectly

#Referrer Policy
#Controls how much information is shared when a user clicks a links
#Helps protect user privacy and sensitive data


#Permissions Policy
#Controls access to browser features like camera, microphone, location
#Prevents unwanted use of sensitive device features

import socket
import ssl
import http.client
from urllib.parse import urlparse  # To parse URLs
from datetime import datetime # For certificate expiry handling

#list of important security headers to check
SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy" ,
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy"
]

#------------------------------------------------------
#Resolve domain name to IP address
#------------------------------------------------------
def resolve_host (host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except Exception as e:
        return f"DNS resolution failed: {e}"

#------------------------------------------------------
#Check if a specific port is open on the target host
#------------------------------------------------------
def check_port (host, port, timeout=3):
    try:
        #Try to create a TCP connection
        with socket.create_connection((host, port), timeout=timeout):
            return True #Port is open
    except Exception:
        return False

#------------------------------------------------------
#Get TLS/SSL certificate details from the server
#------------------------------------------------------
def get_tls_info (host, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()

                not_after = cert.get('notAfter')
                expiry = None
                day_left = None

                if not_after:
                    expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                    days_left = (expiry - datetime.utcnow()).days

                subject = dict(x[0] for x in cert.get("subject", []))
                issuer = dict(x[0] for x in cert.get("issuer", []))

                return {
                    "tls_version": version,
                    "cipher": cipher,
                    "subject_cn": subject.get("commonName", "Unknown"),
                    "issuer_cn": issuer.get("commonName", "Unknown"),
                    "expiry": expiry.isoformat() if expiry else None,
                    "days_left": days_left,
                }

    except Exception as e:
        return f"error: {e}"

#------------------------------------------------------
#Send HTTP/HTTPS request retrieve headers
#------------------------------------------------------

def get_http_headers(url):
    try:
        parsed = urlparse(url)

        # Determine scheme(http or https)
        scheme = parsed.scheme or "https"
        host = parsed.netloc or parsed.path
        path = parsed.path if parsed.netloc else "/"

        if not path:
            path = "/"

        # Choose correct connection type
        if scheme == "https":
            conn = http.client.HTTPSConnection(host, timeout=5)

        else:
            conn = http.client.HTTPConnection(host, timeout=5)

        # Send GET request
        conn.request("GET", path, headers={
            "User-Agent": "AuthorizedSecurityAudit/1.0"})

        response = conn.getresponse()
        # Convert headers to dictionary
        headers = dict(response.getheaders())
        conn.close()

        return {"status": response.status, "headers": headers}

    except Exception as e:
        return {"error": str(e)}



#
# Analyze presence of secuirty headers
#

def analyze_security_headers(headers):
    findings = []
    for header in SECURITY_HEADERS:
        if header in headers:
            findings.append(f"[OK] {header}: {headers[header]}")
        else    :
            findings.append(f"[MISSING] {header}")

    return findings

#
#   Main audit function for a single target
#


def audit_target(target):
# Ensure target has a scheme

    if not target.startswith("http://") and not target.startswith("https://"):
        url = f"https://{target}"
    else:
        url = target

    parsed = urlparse(url)
    host = parsed.netloc or parsed.path
    print("=" * 69)
    print(f"Target: {target}")
    print("=" * 69)


# Step 1 DNS Resolution

    ip = resolve_host(host)
    print(f"Resolved IP: {ip}")
# Step 2 Port checks

    port_80 = check_port(host, "80")
    port_443 = check_port(host, "443")
    print(f"Port 80 open : {port_80}")
    print(f"Port 443 open : {port_443}")

# Step 3 TLS Inspection
    if port_443:
        tls_info = get_tls_info(host)
        print("\n[TLS INFO]")

        if "error" in tls_info:
            print(f"TLS check failed: {tls_info['error']}")

        else:
            for key, value in tls_info.items():
                print(f"{key}: {value}")

            # Warn if certificate is about to expire
            if tls_info.get("days_left") is not None and tls_info["days_left"] < 30:
                print("[WARNING] Certificate expires in less than 30 days")

    # Step 4 HTTP Header analysis

    http_info = get_http_headers(url)
    print("\n[HTTP/HTTPS INFO]")
    if "error" in http_info:
        print(f"HTTP check failed: {http_info['error']}")

    else:
        print(f"HTTP status: {http_info['status']}")
        findings = analyze_security_headers(http_info['headers'])

        for line in findings:
            print(line)

        # Check if server reveals its identity

        server = http_info['headers'].get("server")
        if server:
            print(f"[INFO] Server: {server}")

        else:
            print(f"[OK] Server header not exposed")


# Entry point of the script
#
def main():
    print("=" * 69)
    print("Authorized Network Security Audit Tool")
    print("Use only on systems you own or are permitted to test.\n")
    # Take multiple targets as inputs
    targets = input("Enter target hosts or URLs (comma separated): ").split(",")

    for target in targets:
        target = target.strip()

        if target:
            audit_target(target)

main()


























