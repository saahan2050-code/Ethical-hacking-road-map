"""
Ethical Hacking Roadmap - a Streamlit app powered by Gemini Flash.

Features
- A complete, curated roadmap (works with no API key)
- Progress tracker with downloadable progress file
- AI-personalised study plan (Gemini)
- AI mentor chat (Gemini) that only teaches legal, defensive-minded security
"""

import json
import os

import streamlit as st

# ----------------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Ethical Hacking Roadmap",
    page_icon="🛡️",
    layout="wide",
)

DEFAULT_MODEL = "gemini-2.5-flash"

# ----------------------------------------------------------------------------
# Roadmap data
# ----------------------------------------------------------------------------
ROADMAP = [
    {
        "title": "Phase 0 - Ethics, Law & Mindset",
        "weeks": "1 week",
        "goal": "Understand what you may and may not do before touching any tool.",
        "topics": [
            "What ethical hacking / penetration testing is (and isn't)",
            "Laws: computer misuse laws in your country (e.g. PECA 2016 in Pakistan, CFAA in the US, Computer Misuse Act in the UK)",
            "Scope, rules of engagement and written authorization",
            "Responsible disclosure and bug bounty rules",
            "Build a safe home lab (VirtualBox/VMware, Kali Linux, vulnerable VMs)",
        ],
        "tools": ["VirtualBox", "VMware Workstation Player", "Kali Linux", "Parrot OS"],
        "resources": [
            "TryHackMe - Pre Security path",
            "Cybrary / YouTube intro to ethical hacking",
        ],
        "project": "Set up an isolated lab with Kali Linux + one intentionally vulnerable VM, and write your own 'rules I will follow' document.",
    },
    {
        "title": "Phase 1 - IT & Networking Fundamentals",
        "weeks": "3-4 weeks",
        "goal": "You cannot break (or defend) what you don't understand.",
        "topics": [
            "OSI & TCP/IP models, IP addressing, subnetting",
            "Common protocols: HTTP/S, DNS, DHCP, ARP, FTP, SSH, SMB, SMTP",
            "Routers, switches, firewalls, VPNs, NAT",
            "Windows fundamentals (users, services, registry, Active Directory basics)",
            "Linux fundamentals (filesystem, permissions, processes, package managers)",
            "Command line mastery (Bash, PowerShell)",
        ],
        "tools": ["Wireshark", "Packet Tracer", "Linux terminal", "PowerShell"],
        "resources": [
            "Professor Messer - Network+ videos (free)",
            "OverTheWire: Bandit (Linux wargame)",
            "TryHackMe - Network Fundamentals, Linux Fundamentals",
        ],
        "project": "Capture your own traffic in Wireshark and explain a full DNS lookup and a TCP 3-way handshake.",
    },
    {
        "title": "Phase 2 - Programming & Scripting",
        "weeks": "3-4 weeks",
        "goal": "Automate tasks and read code to find flaws.",
        "topics": [
            "Python basics: data types, loops, functions, files, requests, sockets",
            "Bash scripting for automation",
            "SQL fundamentals",
            "HTML, CSS and JavaScript basics (needed for web security)",
            "Git and GitHub basics",
            "Reading code in C/PHP/Java at a basic level",
        ],
        "tools": ["Python 3", "VS Code", "Git", "Bash"],
        "resources": [
            "Automate the Boring Stuff with Python (free online)",
            "freeCodeCamp - JavaScript & SQL",
            "Codecademy / W3Schools for web basics",
        ],
        "project": "Write a Python script that checks which common ports are open on YOUR OWN lab machine and logs the results.",
    },
    {
        "title": "Phase 3 - Security Fundamentals",
        "weeks": "3 weeks",
        "goal": "Learn the concepts every security professional shares.",
        "topics": [
            "CIA triad, risk, threats, vulnerabilities, attack surface",
            "Cryptography basics: hashing, symmetric/asymmetric, TLS, PKI",
            "Authentication, authorization, password security, MFA",
            "Common attack types at a conceptual level (phishing, malware, DoS, MITM)",
            "Defensive basics: logging, firewalls, IDS/IPS, patching, hardening",
            "Frameworks: MITRE ATT&CK, OWASP, NIST, Cyber Kill Chain",
        ],
        "tools": ["CyberChef", "Hashcat (lab use)", "OpenSSL"],
        "resources": [
            "CompTIA Security+ study material (Professor Messer)",
            "TryHackMe - Introduction to Cyber Security path",
            "MITRE ATT&CK website",
        ],
        "project": "Map one real-world breach (from public write-ups) to MITRE ATT&CK techniques.",
    },
    {
        "title": "Phase 4 - Reconnaissance & Scanning",
        "weeks": "3 weeks",
        "goal": "Learn to map a target's attack surface (only with permission).",
        "topics": [
            "Passive recon / OSINT (WHOIS, DNS, search engines, public records)",
            "Active recon: host discovery, port scanning, service/version detection",
            "Subdomain and directory enumeration",
            "Vulnerability scanning and interpreting results",
            "Enumeration of SMB, FTP, SSH, HTTP services",
        ],
        "tools": ["Nmap", "Amass / Subfinder", "Gobuster / ffuf", "Nessus Essentials / OpenVAS", "Shodan"],
        "resources": [
            "Nmap official book / nmap.org documentation",
            "TryHackMe - Nmap, Network Services rooms",
        ],
        "project": "Fully enumerate a vulnerable lab VM and write a one-page report of its attack surface.",
    },
    {
        "title": "Phase 5 - Web Application Security",
        "weeks": "5-6 weeks",
        "goal": "Web apps are the most common real-world target.",
        "topics": [
            "How web apps, sessions, cookies and APIs work",
            "OWASP Top 10: injection, broken access control, XSS, CSRF, SSRF, misconfigurations",
            "Authentication and session flaws, IDOR",
            "File upload and deserialization issues",
            "API security testing",
            "Secure coding fixes for each vulnerability class",
        ],
        "tools": ["Burp Suite Community", "OWASP ZAP", "SQLMap (lab use)", "Browser DevTools"],
        "resources": [
            "PortSwigger Web Security Academy (free, excellent)",
            "OWASP Juice Shop and DVWA (practice apps)",
            "OWASP Web Security Testing Guide (WSTG)",
        ],
        "project": "Complete 20+ PortSwigger labs and write a clear write-up of one vulnerability with the fix.",
    },
    {
        "title": "Phase 6 - Network & System Pentesting",
        "weeks": "6-8 weeks",
        "goal": "Gain access to systems in a lab and understand how to prevent it.",
        "topics": [
            "Exploitation fundamentals with Metasploit and manual exploits",
            "Password attacks and credential hygiene (in lab)",
            "Linux and Windows privilege escalation",
            "Active Directory basics and common misconfigurations",
            "Pivoting and tunneling concepts",
            "Wireless security fundamentals (own equipment only)",
            "Post-exploitation, persistence concepts and cleanup",
        ],
        "tools": ["Metasploit", "Hydra / John the Ripper", "LinPEAS / WinPEAS", "BloodHound", "Aircrack-ng"],
        "resources": [
            "TryHackMe - Jr Penetration Tester path",
            "Hack The Box Academy",
            "TCM Security - Practical Ethical Hacking (course)",
        ],
        "project": "Fully compromise 5 beginner machines on TryHackMe/HTB and write a professional write-up for each.",
    },
    {
        "title": "Phase 7 - Practice, CTFs & Reporting",
        "weeks": "Ongoing",
        "goal": "Turn knowledge into skill and learn to communicate findings.",
        "topics": [
            "Capture The Flag (CTF) competitions",
            "Methodology: recon -> enumerate -> exploit -> escalate -> report",
            "Writing professional penetration test reports (executive summary, risk rating, remediation)",
            "Note-taking and documentation habits",
            "CVSS scoring and risk communication",
        ],
        "tools": ["Obsidian / CherryTree", "Dradis / Markdown templates", "HackTheBox", "PicoCTF"],
        "resources": [
            "PicoCTF (great for beginners)",
            "OverTheWire wargames",
            "VulnHub and HackTheBox retired machines",
            "CTFtime.org for upcoming competitions",
        ],
        "project": "Play in 3 CTFs and publish a sanitized pentest report sample on GitHub.",
    },
    {
        "title": "Phase 8 - Specialize",
        "weeks": "Ongoing",
        "goal": "Pick a direction that fits your interests.",
        "topics": [
            "Web / API application security",
            "Cloud security (AWS, Azure, GCP)",
            "Mobile security (Android / iOS)",
            "Active Directory and internal network pentesting",
            "Red teaming and adversary emulation",
            "Malware analysis and reverse engineering (defensive)",
            "Blue team: SOC analysis, SIEM, threat hunting, DFIR",
        ],
        "tools": ["Ghidra", "Frida", "ScoutSuite / Prowler", "Splunk / ELK", "Volatility"],
        "resources": [
            "flaws.cloud / flaws2.cloud",
            "OWASP Mobile Security Testing Guide",
            "Hack The Box Pro Labs",
            "Malware Unicorn workshops",
        ],
        "project": "Choose one specialty and build one portfolio project (e.g. a cloud misconfiguration audit of your own account).",
    },
    {
        "title": "Phase 9 - Certifications & Career",
        "weeks": "Ongoing",
        "goal": "Prove your skills and find a job or bug bounty income.",
        "topics": [
            "Entry certs: CompTIA Security+, Google Cybersecurity Certificate",
            "Practical certs: eJPT, PNPT, CEH (Practical)",
            "Advanced certs: OSCP, CRTP, CPTS, OSWE",
            "Bug bounty platforms: HackerOne, Bugcrowd, Intigriti",
            "Building a portfolio: blog, GitHub, write-ups, CVEs",
            "Networking: local security meetups, conferences, LinkedIn, Discord/Reddit communities",
        ],
        "tools": ["HackerOne", "Bugcrowd", "LinkedIn", "GitHub", "Medium / personal blog"],
        "resources": [
            "Official exam objectives for each certification",
            "Bug Bounty Bootcamp (book by Vickie Li)",
            "Local DEF CON / BSides groups",
        ],
        "project": "Publish a portfolio site with at least 5 write-ups and apply to your first bug bounty program or junior role.",
    },
]

ETHICS_RULES = [
    "Only test systems you own or have **written permission** to test.",
    "Stay inside the agreed **scope** - no exceptions.",
    "Never access, copy, change or destroy data you don't need.",
    "Report vulnerabilities **responsibly** and give the owner time to fix them.",
    "Keep client or program information **confidential**.",
    "Practice on legal targets: your own lab, TryHackMe, Hack The Box, PortSwigger, OverTheWire, DVWA, Juice Shop.",
    "Know your local laws - unauthorized access is a crime in almost every country, even 'just to look'.",
]

SYSTEM_PROMPT = """You are "HackMentor", a friendly and practical cybersecurity teacher who helps \
beginners and intermediates learn ETHICAL HACKING and penetration testing.

Rules you must always follow:
1. Teach only legal, authorized, defensive-minded security. Always remind learners to practice \
only on systems they own or have written permission to test (home labs, TryHackMe, Hack The Box, \
PortSwigger Academy, DVWA, Juice Shop, CTFs).
2. Refuse to help with attacking real third-party targets, stealing credentials or data, creating \
deployable malware/ransomware, stalking, doxxing, bypassing a specific person's accounts, or any \
illegal activity. If asked, politely decline and suggest a legal learning alternative.
3. Explain concepts clearly, with the 'why', how the attack works at a conceptual level, and \
how to detect and fix it. For hands-on steps, point to lab environments.
4. Be encouraging, structured and concise. Use headings and bullet points where helpful.
5. Stay on topic: cybersecurity, IT fundamentals, programming for security, certifications and careers. \
Politely redirect off-topic questions.
"""

# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"role": "user"|"assistant", "content": str}
if "custom_plan" not in st.session_state:
    st.session_state.custom_plan = ""


def checkbox_key(phase_idx: int, topic_idx: int) -> str:
    return f"chk_{phase_idx}_{topic_idx}"


def get_progress() -> dict:
    """Return {'done': int, 'total': int, 'phases': [(title, done, total), ...]}."""
    phases = []
    done_all = total_all = 0
    for p_idx, phase in enumerate(ROADMAP):
        total = len(phase["topics"])
        done = sum(
            1 for t_idx in range(total) if st.session_state.get(checkbox_key(p_idx, t_idx), False)
        )
        phases.append((phase["title"], done, total))
        done_all += done
        total_all += total
    return {"done": done_all, "total": total_all, "phases": phases}


# ----------------------------------------------------------------------------
# Gemini helpers
# ----------------------------------------------------------------------------
def get_api_key() -> str:
    """Priority: sidebar input -> Streamlit secrets -> environment variable."""
    typed = st.session_state.get("api_key_input", "").strip()
    if typed:
        return typed
    try:
        secret = st.secrets.get("GEMINI_API_KEY", "")
        if secret:
            return str(secret).strip()
    except Exception:
        pass  # no secrets file present
    return os.environ.get("GEMINI_API_KEY", "").strip()


def call_gemini(contents, system_instruction: str, temperature: float = 0.6) -> str:
    """Call Gemini and return text. Raises RuntimeError with a friendly message on failure."""
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("No Gemini API key found. Add it in the sidebar or in Streamlit secrets.")

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        model = st.session_state.get("model_name", DEFAULT_MODEL).strip() or DEFAULT_MODEL
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=4096,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError(
                "Gemini returned an empty response (it may have been blocked by safety filters). "
                "Try rephrasing your request."
            )
        return text
    except RuntimeError:
        raise
    except Exception as exc:  # network, auth, quota, bad model name, etc.
        raise RuntimeError(f"Gemini request failed: {exc}") from exc


def build_chat_contents(history):
    """Convert our chat history into Gemini 'contents' (roles: user / model)."""
    from google.genai import types

    contents = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
    return contents


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.title("🛡️ Ethical Hacking Roadmap")
    st.caption("Learn legally. Hack responsibly.")

    st.subheader("⚙️ Gemini settings")
    st.text_input(
        "Gemini API key",
        type="password",
        key="api_key_input",
        help="Get a free key at https://aistudio.google.com/apikey. "
        "On Streamlit Cloud you can store it in Secrets instead.",
    )
    st.text_input(
        "Model name",
        value=DEFAULT_MODEL,
        key="model_name",
        help="Any Gemini Flash model, e.g. gemini-2.5-flash",
    )
    if get_api_key():
        st.success("API key detected ✅")
    else:
        st.info("No key yet - the roadmap works without one; AI tabs need it.")

    st.divider()
    prog = get_progress()
    pct = prog["done"] / prog["total"] if prog["total"] else 0
    st.subheader("📈 Your progress")
    st.progress(pct, text=f"{prog['done']} / {prog['total']} topics ({pct:.0%})")

    st.divider()
    st.warning("⚠️ Only practice on systems you own or have written permission to test.")

# ----------------------------------------------------------------------------
# Main content
# ----------------------------------------------------------------------------
st.title("🛡️ Ethical Hacking: Complete Learning Roadmap")
st.write(
    "A step-by-step path from absolute beginner to job-ready ethical hacker, "
    "with an AI mentor to personalise your journey."
)

tab_road, tab_progress, tab_plan, tab_chat, tab_ethics = st.tabs(
    ["🗺️ Roadmap", "✅ Progress", "🎯 My AI Plan", "💬 AI Mentor", "⚖️ Ethics & Law"]
)

# ---- Roadmap tab -----------------------------------------------------------
with tab_road:
    st.subheader("The roadmap")
    st.caption("Tick topics as you learn them - your progress is tracked in the next tab.")
    for p_idx, phase in enumerate(ROADMAP):
        with st.expander(f"{phase['title']}  •  ⏱️ {phase['weeks']}", expanded=(p_idx == 0)):
            st.markdown(f"**🎯 Goal:** {phase['goal']}")
            st.markdown("**📚 Topics to learn**")
            for t_idx, topic in enumerate(phase["topics"]):
                st.checkbox(topic, key=checkbox_key(p_idx, t_idx))
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🧰 Tools**")
                st.markdown("\n".join(f"- {t}" for t in phase["tools"]))
            with col2:
                st.markdown("**🔗 Resources**")
                st.markdown("\n".join(f"- {r}" for r in phase["resources"]))
            st.info(f"🛠️ **Mini-project:** {phase['project']}")

# ---- Progress tab ----------------------------------------------------------
with tab_progress:
    st.subheader("Your progress")
    prog = get_progress()
    pct = prog["done"] / prog["total"] if prog["total"] else 0
    st.metric("Overall completion", f"{pct:.0%}", f"{prog['done']} of {prog['total']} topics")
    st.progress(pct)

    for title, done, total in prog["phases"]:
        st.write(f"**{title}**")
        st.progress(done / total if total else 0, text=f"{done}/{total}")

    if pct == 1:
        st.balloons()
        st.success("You completed the whole roadmap! Time to go for certifications and real-world projects.")

    report = {
        "overall_percent": round(pct * 100, 1),
        "phases": [{"phase": t, "done": d, "total": n} for t, d, n in prog["phases"]],
    }
    st.download_button(
        "⬇️ Download progress (JSON)",
        data=json.dumps(report, indent=2),
        file_name="ethical_hacking_progress.json",
        mime="application/json",
    )
    st.caption("Note: progress lives in your browser session. Download it to keep a record.")

# ---- AI plan tab -----------------------------------------------------------
with tab_plan:
    st.subheader("Get a personalised study plan")
    with st.form("plan_form"):
        c1, c2 = st.columns(2)
        with c1:
            level = st.selectbox(
                "Your current level",
                ["Complete beginner", "Know some IT / programming", "Intermediate (some security experience)"],
            )
            hours = st.slider("Hours you can study per week", 2, 40, 10)
            weeks = st.slider("Plan length (weeks)", 4, 52, 16)
        with c2:
            goal = st.selectbox(
                "Main goal",
                [
                    "Get a junior pentester / security job",
                    "Bug bounty hunting",
                    "Pass a certification (e.g. CEH, eJPT, OSCP)",
                    "Become a SOC analyst / blue teamer",
                    "Learn for personal interest / protect my own systems",
                ],
            )
            background = st.text_area(
                "Your background (optional)",
                placeholder="e.g. I know basic Python, studying BS Computer Science, have no Linux experience...",
            )
        submitted = st.form_submit_button("✨ Generate my plan", type="primary")

    if submitted:
        prompt = (
            f"Create a personalised ethical hacking study plan.\n"
            f"- Current level: {level}\n- Goal: {goal}\n- Available time: {hours} hours/week\n"
            f"- Plan length: {weeks} weeks\n- Background: {background or 'not provided'}\n\n"
            "Format the answer in Markdown with: (1) a short summary of the approach, "
            "(2) a week-by-week (or block-by-block) schedule with specific topics, free resources "
            "(TryHackMe, PortSwigger, HTB Academy, OverTheWire, etc.) and one small hands-on exercise per block, "
            "(3) milestones/checkpoints, (4) recommended certifications at the right time, "
            "(5) common mistakes to avoid. Emphasise legal practice environments only."
        )
        try:
            with st.spinner("Building your plan..."):
                st.session_state.custom_plan = call_gemini(prompt, SYSTEM_PROMPT, temperature=0.5)
        except RuntimeError as err:
            st.error(str(err))

    if st.session_state.custom_plan:
        st.markdown(st.session_state.custom_plan)
        st.download_button(
            "⬇️ Download plan (Markdown)",
            data=st.session_state.custom_plan,
            file_name="my_ethical_hacking_plan.md",
            mime="text/markdown",
        )

# ---- Chat tab --------------------------------------------------------------
with tab_chat:
    st.subheader("Ask HackMentor")
    st.caption("Ask about concepts, tools, labs, certifications or careers. Legal and ethical learning only.")

    if st.button("🗑️ Clear chat"):
        st.session_state.chat_history = []
        st.rerun()

    if not st.session_state.chat_history:
        st.info(
            "Try: *What is SQL injection and how do I prevent it?* • "
            "*Explain Nmap scan types* • *What should I learn before OSCP?*"
        )

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask your ethical hacking question...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    contents = build_chat_contents(st.session_state.chat_history[-20:])
                    answer = call_gemini(contents, SYSTEM_PROMPT)
                st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except RuntimeError as err:
                st.error(str(err))
                # drop the unanswered user message so history keeps alternating roles
                st.session_state.chat_history.pop()

# ---- Ethics tab ------------------------------------------------------------
with tab_ethics:
    st.subheader("The ethical hacker's code")
    for rule in ETHICS_RULES:
        st.markdown(f"- {rule}")
    st.error(
        "Unauthorized access to computer systems is illegal and can lead to fines, "
        "prison and a permanent career ban. This app is for education only."
    )
    st.subheader("Legal places to practice")
    st.markdown(
        "- [TryHackMe](https://tryhackme.com)\n"
        "- [Hack The Box](https://www.hackthebox.com)\n"
        "- [PortSwigger Web Security Academy](https://portswigger.net/web-security)\n"
        "- [OverTheWire](https://overthewire.org/wargames/)\n"
        "- [PicoCTF](https://picoctf.org)\n"
        "- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)\n"
        "- [VulnHub](https://www.vulnhub.com)"
    )
