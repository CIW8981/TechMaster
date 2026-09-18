---
title: "Ansible - First Principles Understanding"
description: "Essential questions to deeply understand Ansible from first principles with examples and metaphors"
tags:
  - ansible
  - configuration-management
  - automation
  - infrastructure-as-code
  - devops
difficulty: beginner
last_updated: "2026-07-22"
---

# Understanding Ansible from First Principles

---

## Q1: What problem does Ansible solve?

**Metaphor**: Imagine you're a restaurant chain owner with 50 locations. Every kitchen must have the same equipment, same recipes posted on the wall, same hygiene rules. You could fly to each restaurant and set it up by hand — but what happens when a recipe changes? You fly to all 50 again?

**Answer**: Ansible solves the problem of **configuring and maintaining many servers in a consistent, repeatable way**.

Without Ansible, you SSH into each server manually:

```bash
# Do this on server 1, then server 2, then server 3...
ssh admin@server1
sudo apt update
sudo apt install nginx
sudo systemctl enable nginx
sudo cp my-config /etc/nginx/nginx.conf
sudo systemctl restart nginx
```

Problems with this:

- **Doesn't scale** — 5 servers is tedious, 500 is impossible
- **Error-prone** — Did you forget a step on server 37?
- **Not reproducible** — New team member can't replicate your setup
- **Drift** — Over time, servers become snowflakes (each slightly different)

Ansible lets you **declare what you want once**, and it makes all servers match:

```yaml
- hosts: webservers
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present

    - name: Deploy config
      copy:
        src: nginx.conf
        dest: /etc/nginx/nginx.conf
      notify: restart nginx

  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
```

---

## Q2: What does "idempotent" mean, and why is it the most important concept?

**Metaphor**: A light switch is idempotent — pressing "ON" when it's already on changes nothing. But a **door lock that toggles** is NOT idempotent — turning the key once locks it, turning it again unlocks it. You can't safely say "turn the key" without knowing the current state.

**Answer**: Idempotent means **running the same operation multiple times produces the same result as running it once**.

This is dangerous (NOT idempotent):

```bash
echo "127.0.0.1 myapp" >> /etc/hosts   # Run 3 times = 3 duplicate lines!
```

This is safe (idempotent):

```yaml
- name: Add hosts entry
  lineinfile:
    path: /etc/hosts
    line: "127.0.0.1 myapp"
    state: present
# Run 100 times — still only one line. Ansible checks first, acts only if needed.
```

**Why it matters**: You must be able to re-run your automation safely at any time — after a failure, after a network hiccup, on a schedule, or just to enforce compliance. If it's not idempotent, re-running causes damage.

---

## Q3: Why is Ansible agentless, and why does that matter?

**Metaphor**: Think of two ways to manage employees.

- **Agent-based** (Chef/Puppet): You install a "supervisor" in every office who checks headquarters every 30 minutes for new instructions. You must hire, train, and maintain all these supervisors.
- **Agentless** (Ansible): You just call each office directly when you have instructions. No permanent staff needed on-site.

**Answer**: Ansible uses **SSH** (already present on every Linux server) to connect, push tasks, execute them, and disconnect. Nothing is installed on managed servers.

```
┌─────────────────┐         SSH          ┌──────────────────┐
│  Control Node   │ ───────────────────→  │  Managed Server  │
│  (your laptop)  │   Copies module,      │  (just needs     │
│  Has: Ansible,  │   executes it,        │   SSH + Python)  │
│  Python         │   gets result back    │                  │
└─────────────────┘                       └──────────────────┘
```

**Why this matters**:

| Concern | Agent-based | Agentless (Ansible) |
|---------|-------------|---------------------|
| Setup on new server | Install + configure agent | Nothing (SSH exists) |
| Agent crashes | Server stops getting updates | N/A — no agent to crash |
| Security surface | Extra daemon listening | No extra ports open |
| Maintenance | Update agents across fleet | Update only control node |

**Trade-off**: Ansible is slightly slower per run (SSH overhead) but operationally simpler.

### But SSH isn't the only connection method

**Metaphor**: SSH is Ansible's default "phone line," but it has other ways to reach things that don't pick up phone calls — walkie-talkies for Windows, intercoms for containers, and a direct line to itself.

Ansible uses **connection plugins** to talk to different types of targets:

| Connection Plugin | Target | How it works |
|-------------------|--------|--------------|
| `ssh` (default) | Linux/Unix servers | Standard SSH — the default for everything |
| `winrm` / `psrp` | Windows servers | Uses Windows Remote Management (WinRM) or PowerShell Remoting Protocol — because Windows doesn't natively run SSH |
| `local` | The control node itself | Skips network entirely — runs modules on the machine running Ansible |
| `docker` | Docker containers | Connects directly via Docker CLI (`docker exec`) — no SSH needed inside containers |
| `network_cli` | Network devices (Cisco, Juniper) | SSH-based but with special handling for CLI prompts, enable modes, and non-standard shells |
| `httpapi` | Network/cloud APIs | REST API calls — for devices managed through HTTP interfaces (firewalls, SDN controllers) |
| `kubectl` | Kubernetes pods | Executes inside pods via `kubectl exec` — no SSH inside pods |
| `podman` | Podman containers | Like Docker connection but for Podman |

**Example — managing Windows alongside Linux:**

```yaml
# inventory.ini
[linux_servers]
web1.example.com

[windows_servers]
win1.example.com

[windows_servers:vars]
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_user=Administrator
ansible_password={{ vault_win_password }}
```

**Example — running tasks locally (useful for API calls):**

```yaml
- name: Create AWS resources from control node
  hosts: localhost
  connection: local
  tasks:
    - name: Create S3 bucket
      amazon.aws.s3_bucket:
        name: my-app-bucket
        state: present
```

**Example — configuring a Docker container directly:**

```yaml
# inventory.ini
[containers]
my_nginx_container ansible_connection=docker
```

!!! info "Key Insight"
    "Agentless" doesn't mean "SSH only." It means **no persistent agent installed on targets**. Ansible adapts its connection method to whatever the target understands — SSH, WinRM, API calls, container runtimes — but never requires you to install and maintain Ansible software on the managed node.

---

## Q4: What is Inventory — and why separate "what to do" from "where to do it"?

**Metaphor**: A recipe (playbook) says "make pasta." The guest list (inventory) says who gets served. You write the recipe once and serve it to any table.

**Answer**: Inventory is the list of servers Ansible manages, organized into groups.

```ini
# inventory.ini
[webservers]
web1.example.com
web2.example.com
web3.example.com

[databases]
db1.example.com
db2.example.com

[production:children]
webservers
databases
```

Now your playbook targets groups, not specific IPs:

```yaml
- hosts: webservers     # Only web servers get nginx
  roles:
    - nginx

- hosts: databases      # Only DB servers get postgres
  roles:
    - postgresql
```

**Why separate?** The same playbook works for dev (2 servers), staging (10 servers), and production (100 servers) — you just swap the inventory file:

```bash
ansible-playbook site.yml -i inventory/production.ini
ansible-playbook site.yml -i inventory/staging.ini
```

---

## Q5: What is a Module, and how is it different from running a shell command?

**Metaphor**: A module is like a **specialist contractor**. You don't tell an electrician "strip the wire, twist the copper, wrap with tape." You say "install an outlet here." The electrician knows HOW, checks if one already exists, and reports back whether they made a change.

**Answer**: A module is a self-contained unit of work that:

1. **Checks current state** — Is nginx already installed?
2. **Acts only if needed** — Installs only if missing
3. **Reports back** — `changed: true` or `changed: false`

Compare:

```yaml
# BAD: Raw command — not idempotent, no state check
- name: Install nginx
  command: apt-get install -y nginx
  # Runs EVERY time. No way to know if anything changed.

# GOOD: Module — idempotent, state-aware
- name: Install nginx
  apt:
    name: nginx
    state: present
  # Checks if already installed. Reports "ok" if so. Reports "changed" if it installed.
```

**Key modules to know**:

| Module | Purpose | Example |
|--------|---------|---------|
| `apt`/`yum` | Install packages | `apt: name=nginx state=present` |
| `copy` | Put a file on server | `copy: src=app.conf dest=/etc/app.conf` |
| `template` | Put a file with variables filled in | `template: src=app.conf.j2 dest=/etc/app.conf` |
| `service` | Start/stop/restart daemons | `service: name=nginx state=started enabled=yes` |
| `user` | Manage user accounts | `user: name=deploy state=present` |
| `file` | Set permissions, create dirs | `file: path=/opt/app state=directory mode=0755` |

---

## Q6: What is the difference between a Task, Play, and Playbook?

**Metaphor**: Think of a **concert**:

- **Task** = A single musician playing one note
- **Play** = One song performed by a specific group of musicians
- **Playbook** = The entire concert setlist

**Answer**:

```yaml
# This YAML file is a PLAYBOOK (the whole concert)

- name: Configure web tier        # This is a PLAY (one song)
  hosts: webservers               # Who performs
  become: yes                     # With elevated privileges
  tasks:                          # The notes in the song
    - name: Install nginx         # TASK 1
      apt:
        name: nginx
        state: present

    - name: Start nginx           # TASK 2
      service:
        name: nginx
        state: started

- name: Configure database tier   # Another PLAY (next song)
  hosts: databases
  become: yes
  tasks:
    - name: Install PostgreSQL    # TASK 1 (of this play)
      apt:
        name: postgresql
        state: present
```

**Why this structure?** Because deploying a full application involves different tasks on different groups of servers, often in a specific order (databases before web servers).

---

## Q7: What is a Role, and why not just write one giant playbook?

**Metaphor**: A role is a **Lego brick**. You build "nginx" as a self-contained brick, "postgresql" as another, "monitoring" as another. Then you assemble them in any combination for any project. A monolithic playbook is like sculpting from a single block of marble — beautiful but not reusable.

**Answer**: A role is a reusable, self-contained package of tasks, files, templates, and variables.

Structure:

```
roles/
└── nginx/
    ├── tasks/main.yml       # What to do
    ├── handlers/main.yml    # Conditional restarts
    ├── templates/nginx.conf.j2  # Config with variables
    ├── files/index.html     # Static files to copy
    ├── defaults/main.yml    # Default variables (overridable)
    └── vars/main.yml        # Fixed variables
```

Using roles in a playbook:

```yaml
- hosts: webservers
  roles:
    - nginx          # Just reference the brick
    - monitoring     # Snap another one on
    - security_hardening
```

**Benefits**:

- **Reuse**: Same nginx role for all projects
- **Test independently**: Validate the role in isolation
- **Share**: Ansible Galaxy has thousands of community roles
- **Separation of concerns**: Each role does one thing well

---

## Q8: What is a Template, and why can't you just copy static files?

**Metaphor**: A template is a **form letter** with blanks. "Dear `___`, your appointment is at `___`." Each recipient gets a personalized letter from the same template. A static file is a photocopy — everyone gets the exact same thing.

**Answer**: Servers differ. A web server's config needs its own IP, hostname, core count, environment-specific settings. Templates use **Jinja2** to fill in values dynamically.

Template file (`nginx.conf.j2`):

```nginx
worker_processes {{ ansible_processor_vcpus }};

server {
    listen 80;
    server_name {{ inventory_hostname }};
    root {{ app_root | default('/var/www/html') }};

    {% if enable_ssl %}
    listen 443 ssl;
    ssl_certificate /etc/ssl/{{ domain }}.crt;
    {% endif %}
}
```

Playbook usage:

```yaml
- name: Deploy nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx
```

**Result**: Each server gets a config tailored to its specs, generated from one source of truth.

---

## Q9: What are Handlers, and why not just restart services immediately?

**Metaphor**: Imagine you're redecorating a room. You move furniture (task 1), paint the walls (task 2), install new light fixtures (task 3). You only need to **flip the breaker once** at the end — not after every single change. A handler is the "flip the breaker" that waits until all changes are done.

**Answer**: A handler runs **only when notified** and **only once** at the end of all tasks, no matter how many tasks notify it.

```yaml
tasks:
  - name: Update nginx.conf
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: restart nginx          # Hey, something changed!

  - name: Update SSL cert
    copy:
      src: ssl.crt
      dest: /etc/ssl/app.crt
    notify: restart nginx          # Something changed again!

  - name: Update mime types
    copy:
      src: mime.types
      dest: /etc/nginx/mime.types
    notify: restart nginx          # And again!

handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted
    # Runs ONCE at the end. Not 3 times.
    # If nothing changed? Doesn't run at all.
```

**Why?** Restarting a service causes brief downtime. Minimizing restarts = maximizing availability.

---

## Q10: How does Ansible fit with other tools (Terraform, Docker, Kubernetes)?

**Metaphor**: Building a house:

- **Terraform** = The construction company that **builds the house** (provisions infrastructure — VMs, networks, load balancers)
- **Ansible** = The interior designer who **furnishes and configures** it (installs software, deploys configs, manages services)
- **Docker** = Delivering rooms as **pre-built shipping containers** (immutable application packaging)
- **Kubernetes** = The **building management system** that ensures the right containers are running in the right places

**Answer**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Typical Flow                               │
│                                                              │
│  Terraform         Ansible              Docker/K8s           │
│  ─────────         ───────              ────────             │
│  "Create 3 VMs" → "Install Docker,  → "Run containers       │
│  "Create VPC"      configure OS,       with app images"      │
│  "Create LB"       set up users,                             │
│                    deploy certs"                              │
└─────────────────────────────────────────────────────────────┘
```

| Question | Answer |
|----------|--------|
| **Do I need Ansible if I use containers?** | Less, but still useful for configuring the hosts that RUN containers, managing secrets, bootstrapping clusters |
| **Do I need Terraform if I use Ansible?** | Ansible CAN provision cloud resources, but Terraform tracks state better for infrastructure lifecycle |
| **When does Ansible become unnecessary?** | Fully immutable infrastructure — you never configure a running server, you replace it with a new image |

---

## Q11: Is Ansible still relevant in 2026, or should I focus on alternatives?

**Metaphor**: Ansible is like a **Swiss Army knife** — it can do many things and remains useful even after you buy specialized power tools. You won't use it to build an entire house anymore (Terraform does that), but you still reach for it daily for tasks the power tools can't handle.

**Answer**: Ansible is still relevant, but its scope has narrowed. It's no longer the "do everything" tool — it now occupies a specific, important niche.

### Where Ansible remains the right choice

| Use Case | Why Ansible wins |
|----------|-----------------|
| Day 1/Day 2 server configuration | Install packages, manage users, deploy configs, harden OS |
| Hybrid/legacy environments | Bare metal, VMs, on-prem gear that can't be containerized |
| Network device automation | Routers, switches, firewalls (Cisco, Juniper, Palo Alto) |
| Bootstrapping Kubernetes clusters | Configure nodes *before* K8s takes over |
| Compliance/security hardening | CIS benchmarks, patching, audit enforcement across fleets |
| Multi-cloud orchestration glue | Stitch together workflows across providers |

### Where Ansible is losing ground

| Scenario | Better alternative | Why |
|----------|-------------------|-----|
| Provisioning cloud infra (VMs, VPCs, LBs) | **Terraform / OpenTofu** | State tracking, plan/apply workflow, drift detection |
| Application deployment on Kubernetes | **Helm / Kustomize / ArgoCD** | K8s-native, declarative, GitOps-integrated |
| Immutable infrastructure (bake-and-deploy) | **Packer + Terraform** | Never configure running servers, just replace them |
| Container workloads | **Docker Compose / Kubernetes** | Ansible configures servers; containers eliminate servers |
| Complex programming logic in IaC | **Pulumi / CDK** | Real programming languages vs YAML gymnastics |

### The 2026 consensus pattern

```
Terraform/OpenTofu  →  Provision infrastructure (Day 0)
Ansible             →  Configure infrastructure (Day 1 & 2)
Kubernetes/ArgoCD   →  Manage application workloads (Day 2+)
```

These tools are **complementary, not competing**. The "Ansible is dead" narrative is wrong — but so is "use Ansible for everything."

### When to NOT learn Ansible

- Your entire stack is containerized and runs on Kubernetes
- You practice fully immutable infrastructure (never SSH into anything)
- You're a pure application developer who never touches servers

### When to absolutely learn it

- You manage VMs, bare metal, or hybrid environments
- Your org has networking gear to automate
- You need to bootstrap/configure hosts before other tools take over
- Job market: Ansible remains a top-3 skill in DevOps/SRE job postings in 2026

### The modern skill set (learn together, not in isolation)

```
┌────────────────────────────────────────────────────────────┐
│  1. Terraform/OpenTofu  — Provision infrastructure          │
│  2. Ansible             — Configure infrastructure          │
│  3. Docker + Kubernetes — Application workloads             │
│  4. ArgoCD/Flux         — GitOps continuous delivery        │
└────────────────────────────────────────────────────────────┘
```

!!! tip "Bottom Line"
    Ansible fills a gap that containers and Kubernetes don't cover — the OS layer, the network layer, and the glue between systems. That gap is smaller than 2020, but it's not gone. Learn Ansible, but know where it ends and other tools begin.

---

## Q12: Do I still need Ansible if I have GitHub Actions?

**Metaphor**: GitHub Actions is a **delivery truck** — it moves packages from point A to point B on a schedule or trigger. Ansible is a **mechanic** — it makes sure the engine, brakes, and tires on every truck in your fleet are configured correctly. The truck doesn't replace the mechanic; they do different jobs.

**Answer**: They solve different problems and often work **together**, not as replacements.

### What each tool actually does

| | GitHub Actions | Ansible |
|---|---|---|
| **Core job** | Run workflows triggered by events (push, PR, schedule) | Ensure servers/devices reach a desired state |
| **Runs where** | GitHub-hosted runners (ephemeral VMs) or self-hosted runners | From a control node into your actual infrastructure |
| **Knows about** | Your code repository, CI/CD pipeline | Your servers, network devices, cloud resources |
| **State management** | Stateless — fresh VM each run | Stateful awareness — checks current state, acts only if needed |
| **Targets** | Build artifacts, test results, deployments | Servers, VMs, containers, network gear, cloud APIs |
| **Idempotent?** | No — re-running a workflow re-does everything | Yes — re-running a playbook only fixes drift |

### The key difference explained

**GitHub Actions** answers: *"When code changes, what pipeline should run?"*

```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
      - run: npm run build
      - run: aws s3 sync ./dist s3://my-bucket   # Deploy artifact
```

**Ansible** answers: *"What should this server look like right now?"*

```yaml
# playbook.yml
- hosts: production_servers
  tasks:
    - name: Ensure nginx is installed and running
      apt: name=nginx state=present
    - name: Deploy latest config
      template: src=nginx.conf.j2 dest=/etc/nginx/nginx.conf
    - name: Ensure firewall rules
      ufw: rule=allow port=443
```

### When GitHub Actions is enough (no Ansible needed)

- **Serverless apps** — Lambda, Cloudflare Workers, Vercel → no servers to configure
- **Fully containerized** — Build image in CI → push to registry → K8s pulls it → done
- **Static sites** — Build → deploy to S3/Netlify/Pages → no server state to manage
- **Simple cloud deployments** — `aws ecs update-service` or `kubectl apply` from a workflow

### When you still need Ansible (GitHub Actions can't replace it)

- **Server configuration** — "Ensure all 50 servers have the right SSH keys, users, and firewall rules"
- **Drift detection and correction** — Someone manually changed a server; Ansible puts it back
- **Network automation** — Configure Cisco switches; GitHub Actions has no way to talk to them
- **On-premises infrastructure** — No internet access, no GitHub runners can reach them
- **Ongoing state enforcement** — Run Ansible on a schedule to *maintain* state, not just deploy once
- **Multi-step server orchestration** — "Update DB servers first, then app servers, then run health checks"

### The common pattern: Use them TOGETHER

```
┌──────────────────────────────────────────────────────────────┐
│  Developer pushes code                                        │
│       ↓                                                       │
│  GitHub Actions:                                              │
│    1. Run tests                                               │
│    2. Build artifact                                          │
│    3. Run: ansible-playbook deploy.yml -e "version=2.1.0"    │
│       ↓                                                       │
│  Ansible (called BY GitHub Actions):                          │
│    1. Connect to production servers via SSH                   │
│    2. Deploy new app version                                  │
│    3. Update configs if needed                                │
│    4. Restart services only if changed                        │
│    5. Run smoke tests                                         │
└──────────────────────────────────────────────────────────────┘
```

```yaml
# GitHub Actions workflow that CALLS Ansible
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Ansible
        run: pip install ansible
      - name: Run deployment playbook
        run: ansible-playbook -i inventory/production deploy.yml
        env:
          ANSIBLE_HOST_KEY_CHECKING: "false"
```

### Decision table

| Your situation | Use |
|----------------|-----|
| Build/test code on every push | GitHub Actions alone |
| Deploy static site or container image | GitHub Actions alone |
| Configure 20 servers identically | Ansible (triggered manually or by GitHub Actions) |
| Deploy app AND configure server state | GitHub Actions triggers Ansible |
| Manage network devices | Ansible alone (GitHub Actions can't reach them) |
| Enforce compliance across fleet continuously | Ansible on a cron (no GitHub Actions needed) |

!!! info "Bottom Line"
    GitHub Actions is a **CI/CD pipeline orchestrator**. Ansible is a **server/infrastructure state manager**. If you have servers to configure and maintain, GitHub Actions doesn't replace Ansible — it's the trigger that kicks Ansible off. If you're fully serverless/containerized, you may genuinely never need Ansible.

---

## Q13: How do I test Ansible locally before touching real servers?

**Metaphor**: A pilot doesn't learn to fly on a passenger jet full of people. They use a **flight simulator** first — same controls, same physics, zero risk. Testing Ansible locally is your flight simulator before you touch production.

**Answer**: There's a **testing pyramid** — start fast and cheap at the bottom, get more realistic (but slower) as you go up.

### The Ansible Testing Pyramid

```
            ┌─────────────────────┐
            │   Production Run    │  ← Real servers (last step)
           ─┼─────────────────────┼─
          / │  Molecule + Docker  │ \  ← Full role test in containers
         /  ├─────────────────────┤  \
        /   │  Check Mode (--check)│   \ ← Dry run on real servers
       /    ├─────────────────────┤    \
      /     │  Vagrant / Local VMs │     \ ← Full OS simulation
     /      ├─────────────────────┤      \
    /       │  ansible-lint        │       \ ← Static analysis (instant)
   /        ├─────────────────────┤        \
  /         │  Syntax Check        │         \ ← Does it even parse?
 /──────────┴─────────────────────┴──────────\
```

### Level 1: Syntax Check (instant, catches typos)

Does your YAML even parse? Zero risk — never touches a server.

```bash
# Check syntax only
ansible-playbook site.yml --syntax-check
```

```
# Output if broken:
ERROR! Syntax Error while loading YAML.
  mapping values are not allowed in this context
  line 12, column 8
```

### Level 2: Linting with ansible-lint (seconds, catches bad practices)

Like a spell-checker for Ansible — catches common mistakes, deprecated features, and style issues.

```bash
# Install
pip install ansible-lint

# Run
ansible-lint site.yml
```

```
# Example output:
WARNING  role-name: Role name 'myRole' does not match pattern
WARNING  yaml[truthy]: Truthy value should be one of [true, false]
WARNING  no-changed-when: Commands should have a "changed_when" attribute
```

What it catches:

- Using `command` instead of a proper module
- Missing `changed_when` on shell tasks
- Deprecated syntax
- YAML formatting issues
- Security concerns (e.g., no_log missing on password tasks)

### Level 3: Check Mode / Dry Run (safe on real servers)

Ansible connects to real servers but **makes no changes** — it just reports what *would* change.

```bash
# Dry run — shows what would happen
ansible-playbook site.yml --check

# Dry run + show file diffs
ansible-playbook site.yml --check --diff
```

```
# Output example:
TASK [Deploy nginx config] ****
--- /etc/nginx/nginx.conf (current)
+++ /etc/nginx/nginx.conf (proposed)
@@ -1,3 +1,4 @@
 worker_processes auto;
+worker_rlimit_nofile 65535;
 events {

changed: [web1.example.com]   ← Would change, but didn't
```

!!! warning "Limitation"
    Check mode is a simulation. Tasks that depend on results of previous tasks (e.g., register a variable then use it) may not work correctly in check mode because the previous task didn't actually run.

### Level 4: Local VMs with Vagrant (full OS, realistic)

Spin up real VMs on your laptop. Closest to production without touching production.

```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.define "web" do |web|
    web.vm.box = "ubuntu/jammy64"
    web.vm.network "private_network", ip: "192.168.56.10"
  end

  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/jammy64"
    db.vm.network "private_network", ip: "192.168.56.11"
  end
end
```

```ini
# inventory/vagrant.ini
[webservers]
192.168.56.10 ansible_user=vagrant ansible_ssh_private_key_file=.vagrant/machines/web/virtualbox/private_key

[databases]
192.168.56.11 ansible_user=vagrant ansible_ssh_private_key_file=.vagrant/machines/db/virtualbox/private_key
```

```bash
# Workflow
vagrant up                                          # Create VMs
ansible-playbook -i inventory/vagrant.ini site.yml  # Test playbook
vagrant destroy -f                                  # Clean up
```

**Pros**: Full OS, systemd, networking, services — everything works like real servers
**Cons**: Slow to boot (minutes), uses more RAM/CPU

### Level 5: Molecule + Docker (the standard, fast, automated)

**Molecule** is the official Ansible testing framework. It automates: create container → run role → verify results → destroy.

```bash
# Install
pip install molecule molecule-docker

# Initialize a new role with Molecule
molecule init role my_nginx_role

# Or add Molecule to existing role
cd roles/nginx
molecule init scenario --driver-name docker
```

Molecule structure inside a role:

```
roles/nginx/
├── tasks/main.yml
├── molecule/
│   └── default/
│       ├── molecule.yml       # Test configuration
│       ├── converge.yml       # Playbook to test
│       └── verify.yml         # Assertions (did it work?)
```

**molecule.yml** — defines test environment:

```yaml
---
driver:
  name: docker

platforms:
  - name: ubuntu-test
    image: ubuntu:22.04
    pre_build_image: true
    command: /sbin/init
    privileged: true
  - name: rocky-test
    image: rockylinux:9
    pre_build_image: true
    command: /sbin/init
    privileged: true

provisioner:
  name: ansible
```

**converge.yml** — the playbook that exercises your role:

```yaml
---
- name: Converge
  hosts: all
  become: true
  roles:
    - nginx
```

**verify.yml** — assert the role did its job:

```yaml
---
- name: Verify
  hosts: all
  tasks:
    - name: Check nginx is installed
      command: nginx -v
      changed_when: false

    - name: Check nginx is running
      service_facts:
    - name: Assert nginx service is running
      assert:
        that:
          - "'nginx' in services"
          - "services['nginx'].state == 'running'"
```

```bash
# Run the full test lifecycle
molecule test

# Output:
# --> Creating instances...
# --> Running prepare...
# --> Running converge...       (applies your role)
# --> Running idempotence...    (runs again — should report 0 changes!)
# --> Running verify...         (checks assertions)
# --> Destroying instances...
```

!!! tip "The idempotence check is gold"
    Molecule runs your role TWICE. The second run must show `changed=0`. If anything changes on the second run, your role is NOT idempotent — and that's a bug.

### Level 6: Run Molecule in CI (GitHub Actions)

Automate tests on every pull request:

```yaml
# .github/workflows/test-ansible.yml
name: Test Ansible Roles
on: [push, pull_request]

jobs:
  molecule:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install ansible molecule molecule-docker
      - run: molecule test
        working-directory: roles/nginx
```

### Quick Reference: Which method when?

| Method | Speed | Realism | Use When |
|--------|-------|---------|----------|
| `--syntax-check` | Instant | None | Every save — catches YAML errors |
| `ansible-lint` | Seconds | None | Before every commit — catches bad practices |
| `--check --diff` | Seconds | Medium | Before production runs — see what WOULD change |
| Vagrant | Minutes | High | Testing full OS interactions, networking, systemd |
| Molecule + Docker | 30-60s | Medium-High | Automated role testing, CI/CD integration |
| Molecule + Vagrant | Minutes | Highest | When Docker can't simulate (kernel modules, full init) |

### My recommended workflow

```
┌──────────────────────────────────────────────────────────┐
│  1. Write/edit role                                       │
│  2. ansible-lint roles/nginx/             (instant)      │
│  3. molecule converge                     (30 sec)       │
│  4. molecule verify                       (10 sec)       │
│  5. molecule test (full cycle w/ idempotence) (60 sec)   │
│  6. Push → GitHub Actions runs molecule   (automated)    │
│  7. ansible-playbook --check --diff       (on staging)   │
│  8. ansible-playbook                      (production)   │
└──────────────────────────────────────────────────────────┘
```

!!! success "Key Principle"
    **Never run untested playbooks on production.** The cost of testing (seconds to minutes locally) is infinitely cheaper than breaking 50 production servers at 2 AM.

---

## Q14: Can Docker simulate real servers like LocalStack simulates AWS?

**Metaphor**: LocalStack is a **perfect stunt double** — it looks and acts exactly like AWS from the outside. Docker containers as Ansible test targets are more like a **mannequin in a crash test** — they're shaped like a person and good enough to test most things, but they don't have a heartbeat (real kernel, real systemd, real networking).

**Answer**: Yes, Docker can simulate servers — and it's the standard approach — but with important limitations you must understand.

### The comparison

| | LocalStack (for AWS) | Docker containers (for Ansible) |
|---|---|---|
| **What it simulates** | AWS API endpoints (S3, EC2, Lambda, etc.) | Linux servers (Ubuntu, Rocky, Debian) |
| **Fidelity** | High — same API, same responses | Medium — same packages, but shared kernel |
| **What works** | Most AWS API calls behave identically | Package installs, file management, user creation, service management |
| **What doesn't work** | Some advanced AWS features | Kernel modules, full networking, iptables, real reboots, hardware |
| **Speed** | Fast | Very fast (seconds to spin up) |
| **Cost** | Free | Free |

### What Docker CAN simulate well (covers ~80% of Ansible tasks)

```yaml
# All of these work perfectly in Docker containers:
- apt/yum: name=nginx state=present          ✅ Package management
- copy: src=app.conf dest=/etc/app/           ✅ File operations
- template: src=config.j2 dest=/etc/config    ✅ Template rendering
- user: name=deploy state=present             ✅ User management
- file: path=/opt/app mode=0755               ✅ Permissions
- lineinfile: path=/etc/hosts line="..."      ✅ File editing
- cron: name="backup" job="/usr/bin/backup"   ✅ Cron jobs
- service: name=nginx state=started           ✅ (with systemd container)
```

### What Docker CANNOT simulate (the ~20% gap)

| Can't test in Docker | Why | Alternative |
|---------------------|-----|-------------|
| Kernel modules (iptables, nf_tables) | Containers share host kernel | Vagrant / real VM |
| Real network interfaces (bonding, VLANs) | Docker uses virtual networking | Vagrant |
| Disk mounting (LVM, fstab) | No real block devices | Vagrant |
| Reboot handling | Containers don't reboot like servers | Vagrant |
| SELinux / AppArmor policies | Requires real kernel enforcement | Vagrant |
| Hardware-specific (RAID, GPU) | No hardware in containers | Real hardware / cloud |
| Full firewalld/ufw | Requires real netfilter | Vagrant |

### How to set up Docker containers as "fake servers"

The trick: Use special Docker images that run **systemd** (init system) and **SSH** — making them behave like real servers.

**Dockerfile for a test server:**

```dockerfile
# Dockerfile.test-server
FROM ubuntu:22.04

# Install SSH and systemd (to behave like a real server)
RUN apt-get update && apt-get install -y \
    openssh-server \
    systemd \
    python3 \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create test user with sudo
RUN useradd -m -s /bin/bash ansible && \
    echo "ansible ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Setup SSH
RUN mkdir -p /home/ansible/.ssh && \
    ssh-keygen -A

EXPOSE 22
CMD ["/sbin/init"]
```

**docker-compose.yml — multi-server lab:**

```yaml
services:
  web1:
    build: .
    container_name: web1
    privileged: true    # Required for systemd
    networks:
      ansible_lab:
        ipv4_address: 172.20.0.10

  web2:
    build: .
    container_name: web2
    privileged: true
    networks:
      ansible_lab:
        ipv4_address: 172.20.0.11

  db1:
    build: .
    container_name: db1
    privileged: true
    networks:
      ansible_lab:
        ipv4_address: 172.20.0.20

networks:
  ansible_lab:
    ipam:
      config:
        - subnet: 172.20.0.0/24
```

**inventory for the lab:**

```ini
[webservers]
172.20.0.10 ansible_user=ansible
172.20.0.11 ansible_user=ansible

[databases]
172.20.0.20 ansible_user=ansible

[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

**Workflow:**

```bash
# Spin up fake servers
docker compose up -d

# Test your playbook
ansible-playbook -i inventory/docker-lab.ini site.yml

# Tear down
docker compose down
```

### But what about Ansible tasks that call AWS APIs?

If your Ansible playbook creates AWS resources (S3 buckets, EC2 instances, etc.), you CAN use **LocalStack + Ansible together**:

```yaml
# playbook that creates AWS resources — test against LocalStack
- hosts: localhost
  connection: local
  vars:
    aws_endpoint: "http://localhost:4566"  # LocalStack endpoint
  tasks:
    - name: Create S3 bucket
      amazon.aws.s3_bucket:
        name: my-app-bucket
        state: present
        endpoint_url: "{{ aws_endpoint }}"  # Point to LocalStack

    - name: Create DynamoDB table
      community.aws.dynamodb_table:
        name: app-config
        hash_key_name: id
        endpoint_url: "{{ aws_endpoint }}"
```

```bash
# Start LocalStack
docker run -d -p 4566:4566 localstack/localstack

# Test AWS-related playbook
ansible-playbook aws-resources.yml
```

### The complete local testing stack

```
┌───────────────────────────────────────────────────────────────┐
│                 LOCAL ANSIBLE TESTING STACK                     │
│                                                                │
│  ┌─────────────────┐     ┌─────────────────────────────────┐  │
│  │   LocalStack     │     │   Docker "Server" Containers    │  │
│  │                  │     │                                  │  │
│  │  Simulates:      │     │  Simulates:                      │  │
│  │  • S3, EC2, RDS  │     │  • Ubuntu servers (web1, web2)   │  │
│  │  • Lambda, SQS   │     │  • Rocky servers (db1)           │  │
│  │  • DynamoDB      │     │  • Running SSH + systemd         │  │
│  │                  │     │  • Real packages & services      │  │
│  └────────┬─────────┘     └──────────────┬──────────────────┘  │
│           │                               │                     │
│           └───────────┐   ┌───────────────┘                     │
│                       ▼   ▼                                     │
│              ┌─────────────────────┐                            │
│              │   Ansible Playbook   │                            │
│              │                      │                            │
│              │  - AWS tasks → LocalStack                        │
│              │  - Server tasks → Docker containers              │
│              └─────────────────────┘                            │
│                                                                │
│  Cost: $0    Time to spin up: ~30 seconds                      │
└───────────────────────────────────────────────────────────────┘
```

### Molecule does all this automatically

You don't need to manage Docker Compose manually — **Molecule** handles the lifecycle:

```yaml
# molecule/default/molecule.yml
driver:
  name: docker
platforms:
  - name: web-ubuntu
    image: geerlingguy/docker-ubuntu2204-ansible  # Pre-built with systemd
    pre_build_image: true
    privileged: true
    command: /sbin/init
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:rw
  - name: db-rocky
    image: geerlingguy/docker-rockylinux9-ansible
    pre_build_image: true
    privileged: true
    command: /sbin/init
```

!!! tip "Community images by Jeff Geerling"
    You don't need to build your own Dockerfiles. The `geerlingguy/docker-*-ansible` images are pre-configured with systemd + Python + SSH for every major distro. They're the standard for Molecule testing.

### Summary: Is Docker "good enough"?

| If your playbook does... | Docker is... |
|--------------------------|-------------|
| Package management, file ops, users, services | ✅ Perfect |
| AWS API calls (S3, EC2, etc.) | ✅ Use LocalStack alongside |
| Systemd service management | ✅ Works with privileged containers |
| Network device config (Cisco, etc.) | ❌ No — need real devices or vendor simulators |
| Kernel/networking (iptables, bonding) | ❌ No — need Vagrant VM |
| Full end-to-end with real reboots | ❌ No — need Vagrant VM |

!!! success "Bottom Line"
    Docker covers ~80% of what you'd test with Ansible. Add LocalStack for AWS API tasks. Only fall back to Vagrant/VMs for the remaining ~20% that requires a real kernel. This is not a single "LocalStack for Ansible" product — it's a combination of Docker + Molecule + LocalStack that achieves the same goal: **test everything locally for free before touching real infrastructure.**

---

## Q15: What exactly is Molecule, and why not just use Docker or Vagrant directly?

**Metaphor**: Docker and Vagrant are **raw building materials** (bricks and lumber). Molecule is a **construction foreman** — it doesn't replace bricks, it uses them while managing the entire building process: laying foundation, checking quality at each step, tearing down scaffolding, and signing off that the building meets code.

You *could* manage Docker containers yourself, manually run playbooks against them, manually check if things worked, and manually clean up. Molecule automates that entire workflow into a single command.

**Answer**: Molecule is NOT an alternative to Docker or Vagrant — it **uses** them. It's a test framework that orchestrates the full test lifecycle.

### The core misunderstanding

```
❌  "Molecule vs Docker vs Vagrant"     (wrong — they're different layers)
✅  "Molecule USES Docker or Vagrant"   (correct — Molecule is the orchestrator)
```

```
┌─────────────────────────────────────────────────────────┐
│                    Molecule                               │
│              (test orchestrator)                          │
│                                                          │
│    "What to create, what to run, what to verify,         │
│     and in what order"                                   │
│                                                          │
│         ┌──────────┐      ┌──────────┐                   │
│         │  Docker  │  OR  │  Vagrant │  ← "Drivers"     │
│         │ (fast)   │      │ (full VM)│                   │
│         └──────────┘      └──────────┘                   │
│              ↑                   ↑                        │
│     Creates containers    Creates VMs                    │
│     to test against       to test against                │
└─────────────────────────────────────────────────────────┘
```

### What Molecule actually does: The 6-phase lifecycle

When you run `molecule test`, it executes these phases in order:

```bash
molecule test
```

```
Phase 1: DEPENDENCY    → Install required Ansible collections/roles
              ↓
Phase 2: CREATE        → Spin up Docker containers (or Vagrant VMs)
              ↓
Phase 3: PREPARE       → Pre-configure test instances (install prereqs)
              ↓
Phase 4: CONVERGE      → Run your Ansible role against the instances
              ↓
Phase 5: IDEMPOTENCE   → Run the role AGAIN — assert 0 changes
              ↓
Phase 6: VERIFY        → Run assertions (did the role actually work?)
              ↓
Phase 7: DESTROY       → Tear everything down, leave no trace
```

### Why each phase matters

| Phase | What it does | Why it's important |
|-------|-------------|-------------------|
| **Create** | Spins up test targets | Consistent, fresh environment every time |
| **Prepare** | Pre-installs basics | Simulates a real server's baseline state |
| **Converge** | Applies your role | Tests that the role runs without errors |
| **Idempotence** | Runs role a 2nd time | **Proves re-running is safe** (the killer feature) |
| **Verify** | Checks end state | Confirms the role *actually achieved its goal* |
| **Destroy** | Cleans up | No leftover containers/VMs polluting your machine |

### Without Molecule (manual approach — what you'd do with plain Docker)

```bash
# YOU have to remember and do each step manually:

# 1. Create container
docker run -d --name test-server --privileged ubuntu:22.04 /sbin/init

# 2. Run your playbook
ansible-playbook -i "172.17.0.2," -u root roles/nginx/tests/test.yml

# 3. Did it work? Check manually...
docker exec test-server nginx -v
docker exec test-server systemctl status nginx

# 4. Is it idempotent? Run again and eyeball the output...
ansible-playbook -i "172.17.0.2," -u root roles/nginx/tests/test.yml
# ...count the "changed" lines manually

# 5. Clean up (if you remember)
docker rm -f test-server

# 6. What about testing on Rocky Linux too? Do it all again...
# 7. What about CI? Write all this in a script yourself...
```

**Problems**: Manual, error-prone, nobody remembers all steps, no standard, hard to add to CI, no assertion framework.

### With Molecule (one command does everything)

```bash
molecule test
```

```
--> Dependency: Installing collections...
--> Creating instances...
    Creating container web-ubuntu...    ✓
    Creating container db-rocky...      ✓
--> Preparing instances...              ✓
--> Converging (applying role)...
    TASK [nginx : Install nginx] changed
    TASK [nginx : Deploy config] changed
    TASK [nginx : Start nginx]   changed
--> Idempotence check...
    TASK [nginx : Install nginx] ok        ← no change (good!)
    TASK [nginx : Deploy config] ok        ← no change (good!)
    TASK [nginx : Start nginx]   ok        ← no change (good!)
    Idempotence check: PASSED ✓
--> Verifying...
    TASK [Check nginx installed]   ok  ✓
    TASK [Check nginx running]     ok  ✓
    TASK [Check port 80 listening] ok  ✓
    Verification: PASSED ✓
--> Destroying instances...
    Removing container web-ubuntu...    ✓
    Removing container db-rocky...      ✓

ALL TESTS PASSED
```

### The idempotence check — Molecule's killer feature

This is the thing you **cannot easily do manually** and the main reason Molecule exists:

```
First run (converge):
  Install nginx    → changed ✓  (expected — it wasn't there)
  Deploy config    → changed ✓  (expected — new file)
  Start service    → changed ✓  (expected — wasn't running)

Second run (idempotence):
  Install nginx    → ok ✓       (already installed, no action)
  Deploy config    → ok ✓       (file already correct, no action)
  Start service    → ok ✓       (already running, no action)
```

If the second run shows ANY `changed` → **your role has a bug**. Common causes:

- Using `command`/`shell` without `changed_when: false`
- Template that regenerates slightly different content each run
- A task that always restarts a service instead of using handlers

### Multi-platform testing in one config

Test the same role on 3 different OS versions simultaneously:

```yaml
# molecule/default/molecule.yml
driver:
  name: docker

platforms:
  - name: ubuntu-22
    image: geerlingguy/docker-ubuntu2204-ansible
    pre_build_image: true
    privileged: true
    command: /sbin/init

  - name: ubuntu-24
    image: geerlingguy/docker-ubuntu2404-ansible
    pre_build_image: true
    privileged: true
    command: /sbin/init

  - name: rocky-9
    image: geerlingguy/docker-rockylinux9-ansible
    pre_build_image: true
    privileged: true
    command: /sbin/init

provisioner:
  name: ansible

verifier:
  name: ansible  # Use Ansible tasks for verification
```

One `molecule test` → runs your role on all 3 platforms → verifies all 3 → destroys all 3.

### Molecule with Vagrant (when Docker isn't enough)

```yaml
# molecule/vagrant/molecule.yml
driver:
  name: vagrant

platforms:
  - name: firewall-test
    box: ubuntu/jammy64
    memory: 1024
    cpus: 2
    interfaces:
      - network_name: private_network
        ip: 192.168.56.10

provisioner:
  name: ansible

# Use this scenario for roles that need real kernel (iptables, etc.)
```

```bash
# Run the vagrant scenario specifically
molecule test -s vagrant
```

### Development workflow with Molecule

During development, you don't run the full `test` cycle every time — you iterate:

```bash
# First time: create containers and apply role
molecule converge

# Edit your role, then re-apply (fast — containers still running)
molecule converge

# Happy with it? Run verification
molecule verify

# Final check: full lifecycle including idempotence
molecule test

# Just want to destroy and start fresh?
molecule destroy
```

### Quick comparison: Why Molecule wins

| Concern | Plain Docker | Plain Vagrant | Molecule |
|---------|-------------|--------------|----------|
| Setup effort | Write Dockerfile, compose, scripts | Write Vagrantfile | `molecule init` (30 seconds) |
| Idempotence testing | Manual (run twice, count changes) | Manual | **Automatic** — fails if not idempotent |
| Multi-OS testing | Manage multiple containers yourself | Multiple VMs (slow, heavy) | One config, all platforms |
| Verification/assertions | `docker exec` + eyeballing | SSH in + check | Declarative verify.yml |
| CI integration | Write custom scripts | Slow, often can't run in CI | `molecule test` in any CI |
| Cleanup | Hope you remember `docker rm` | `vagrant destroy` | **Automatic** — always cleans up |
| Standardization | Every team does it differently | Every team does it differently | **Industry standard** — same workflow everywhere |
| Speed | Fast (but you do everything) | Slow (minutes per VM) | Fast (uses Docker by default) |

!!! success "Bottom Line"
    Molecule isn't a replacement for Docker or Vagrant — it's the **automation layer on top** that turns manual testing into a repeatable, one-command process. Its idempotence check alone justifies its existence: it catches bugs that manual testing almost always misses. Think of it as `pytest` for Ansible — you could test Python code manually too, but why would you?

---

## Q16: Is Molecule only for local testing? What do I actually run on production servers?

**Yes — Molecule is purely a testing tool. It never touches production.**

**Metaphor**: Molecule is a **crash test facility** — you smash cars into walls to prove they're safe. Once the car passes all crash tests, you ship the exact same car design to customers. The crash test facility doesn't deliver cars to customers; it just proves they're safe to deliver.

Similarly: you test your role with Molecule locally → once it passes → you run the same role with plain `ansible-playbook` against real servers.

### What runs where

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   YOUR LAPTOP / CI SERVER              REAL SERVERS              │
│   ─────────────────────────            ────────────              │
│                                                                  │
│   molecule test                        ansible-playbook          │
│     ↓                                    ↓                       │
│   Creates Docker containers            Connects via SSH          │
│   Applies role                         Applies the SAME role     │
│   Checks idempotence                   On real servers           │
│   Verifies results                     In production             │
│   Destroys containers                                            │
│                                                                  │
│   PURPOSE: Prove it works              PURPOSE: Actually do it   │
│   RISK: Zero                           RISK: Real                │
│   COST: Free                           COST: Real                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Full real-world example: nginx role from development to production

#### Step 1: Write the role

```
roles/nginx/
├── tasks/main.yml
├── handlers/main.yml
├── templates/nginx.conf.j2
├── defaults/main.yml
└── molecule/
    └── default/
        ├── molecule.yml
        ├── converge.yml
        └── verify.yml
```

**roles/nginx/tasks/main.yml:**

```yaml
---
- name: Install nginx
  apt:
    name: nginx
    state: present
    update_cache: yes

- name: Deploy nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    mode: '0644'
  notify: restart nginx

- name: Ensure nginx is running and enabled
  service:
    name: nginx
    state: started
    enabled: yes
```

**roles/nginx/handlers/main.yml:**

```yaml
---
- name: restart nginx
  service:
    name: nginx
    state: restarted
```

#### Step 2: Test with Molecule (local — never touches real servers)

**molecule/default/molecule.yml:**

```yaml
driver:
  name: docker
platforms:
  - name: nginx-test
    image: geerlingguy/docker-ubuntu2204-ansible
    pre_build_image: true
    privileged: true
    command: /sbin/init
provisioner:
  name: ansible
verifier:
  name: ansible
```

**molecule/default/converge.yml:**

```yaml
---
- name: Converge
  hosts: all
  become: true
  roles:
    - nginx
```

**molecule/default/verify.yml:**

```yaml
---
- name: Verify
  hosts: all
  become: true
  tasks:
    - name: Check nginx is installed
      command: nginx -v
      changed_when: false

    - name: Check nginx is running
      service_facts:

    - name: Assert nginx is active
      assert:
        that:
          - "'nginx.service' in services"
          - "services['nginx.service'].state == 'running'"

    - name: Check port 80 is listening
      wait_for:
        port: 80
        timeout: 5
```

**Run it:**

```bash
molecule test
```

```
✓ Dependency installed
✓ Container created
✓ Role applied (converge)
✓ Idempotence PASSED (0 changes on second run)
✓ Verification PASSED (nginx installed, running, port 80 open)
✓ Container destroyed

RESULT: Role is safe to use on real servers.
```

#### Step 3: Dry run on real staging servers (optional safety check)

```bash
# See what WOULD change on real servers — without changing anything
ansible-playbook -i inventory/staging.ini site.yml --check --diff
```

```
TASK [nginx : Install nginx] --- ok (already installed)
TASK [nginx : Deploy config] --- changed (diff shown below)
  - worker_processes 2;
  + worker_processes 4;
TASK [nginx : Ensure running] --- ok (already running)
```

#### Step 4: Apply to real production servers (no Molecule involved)

```bash
# This is plain ansible-playbook — the standard Ansible command
ansible-playbook -i inventory/production.ini site.yml
```

```ini
# inventory/production.ini
[webservers]
prod-web-01.example.com
prod-web-02.example.com
prod-web-03.example.com

[webservers:vars]
ansible_user=deploy
ansible_ssh_private_key_file=~/.ssh/prod_key
```

```
TASK [nginx : Install nginx] ---- ok
TASK [nginx : Deploy config] ---- changed
TASK [nginx : Ensure running] --- ok
HANDLER [nginx : restart nginx] - changed

PLAY RECAP:
prod-web-01  : ok=3  changed=2
prod-web-02  : ok=3  changed=2
prod-web-03  : ok=3  changed=2
```

**Done. Real servers configured. Same role that Molecule already proved works.**

### The complete flow visualized

```
┌────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT → PRODUCTION                      │
│                                                                  │
│  ① Write/edit role                                               │
│       ↓                                                          │
│  ② molecule test              ← Docker containers (disposable)  │
│       ↓                         Tests: syntax, converge,         │
│       │                         idempotence, verification        │
│       ↓                                                          │
│  ③ git push → CI runs          ← GitHub Actions runs            │
│    molecule test again           molecule test automatically     │
│       ↓                                                          │
│  ④ ansible-playbook --check    ← Real staging servers           │
│    (dry run on staging)          Shows what would change         │
│       ↓                                                          │
│  ⑤ ansible-playbook            ← Real production servers        │
│    (apply for real)              Actually makes changes          │
│                                                                  │
│  Molecule's job ends at step ③. Steps ④ and ⑤ are plain        │
│  ansible-playbook — the same command you'd use without          │
│  Molecule. Molecule just GUARANTEES your role works before       │
│  you point it at real servers.                                   │
└────────────────────────────────────────────────────────────────┘
```

### Common confusion cleared up

| Question | Answer |
|----------|--------|
| Does Molecule run on production? | **No** — never. It's only for testing. |
| What command configures real servers? | `ansible-playbook` — same as always |
| Does the role change between testing and production? | **No** — exact same role, exact same code |
| Then what's the point of Molecule? | It **proves** the role works before you risk real servers |
| Can I skip Molecule and just run on production? | Yes, technically — like you can skip unit tests and deploy. You'll regret it at 3 AM. |
| Is Molecule mandatory? | No. It's a best practice, not a requirement. Small teams skip it. Mature teams never do. |

!!! tip "Think of it like this"
    ```
    Software development:    pytest (local)     →  deploy to production
    Ansible development:     molecule (local)   →  ansible-playbook on production
    ```
    The testing tool and the production tool are DIFFERENT commands that exercise the SAME code.

---

## Summary: The Mental Model

```
┌─────────────────────────────────────────────────────────────┐
│                    ANSIBLE MENTAL MODEL                       │
│                                                              │
│  INVENTORY          →  "WHO"   (which servers)               │
│  PLAYBOOK           →  "WHAT"  (desired end state)           │
│  MODULES            →  "HOW"   (idempotent units of work)    │
│  TEMPLATES          →  "PERSONALIZE" (per-server configs)    │
│  ROLES              →  "PACKAGE" (reusable building blocks)  │
│  HANDLERS           →  "REACT" (only when things change)     │
│  VAULT              →  "PROTECT" (encrypted secrets)         │
│                                                              │
│  Runs over SSH. No agents. Declarative. Idempotent.          │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Topics

- [Terraform](../terraform/index.md) — Infrastructure provisioning
- [Docker](../docker/index.md) — Containerization
- [Kubernetes](../kubernetes/index.md) — Container orchestration

---

**Tags**: #ansible #configuration-management #automation #infrastructure-as-code #devops #first-principles

**Difficulty**: <span class="difficulty-beginner">Beginner</span> → <span class="difficulty-intermediate">Intermediate</span>
