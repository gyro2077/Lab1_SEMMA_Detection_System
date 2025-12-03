#!/usr/bin/env python3
"""
GENERADOR MASIVO DE DATASET
Crea 500+ ejemplos sintéticos de vulnerabilidades realistas
"""

import os
import random

EXAMPLES_DIR = "/home/gyro/Documents/OCT25-MAR26/SOFT_SEGURO/PARCIAL_DOS/4Diciembre/SEMMA/examples/generated"
os.makedirs(EXAMPLES_DIR, exist_ok=True)

generated_count = 0

# ============= SQLI TEMPLATES (100+ variaciones) =============

# Variables comunes para SQLi
sqli_tables = ['users', 'products', 'accounts', 'orders', 'customers', 'employees', 'posts', 'comments']
sqli_columns = ['id', 'username', 'email', 'password', 'name', 'userid', 'account_id', 'product_id']
sqli_operators = ['=', '>', '<', 'LIKE', 'IN']

# Python SQLi - 30 variaciones
for i in range(30):
    table = random.choice(sqli_tables)
    col = random.choice(sqli_columns)
    
    template = random.choice([
        # String formatting
        f'''import sqlite3

def get_{table}(search_term):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM {table} WHERE {col} = {{}}".format(search_term)
    cursor.execute(query)
    return cursor.fetchall()
''',
        # f-string
        f'''import mysql.connector

def search_{table}(keyword):
    conn = mysql.connector.connect(host='localhost', database='app')
    cursor = conn.cursor()
    sql = f"SELECT * FROM {table} WHERE {col} LIKE '%{{keyword}}%'"
    cursor.execute(sql)
    return cursor.fetchall()
''',
        # % formatting
        f'''import psycopg2

def find_{table}(value):
    conn = psycopg2.connect("dbname=main")
    cur = conn.cursor()
    query = "SELECT * FROM {table} WHERE {col} = '%s'" % value
    cur.execute(query)
    return cur.fetchone()
''',
        # String concatenation
        f'''import sqlite3

def lookup_{table}(user_input):
    db = sqlite3.connect('app.db')
    cursor = db.cursor()
    sql = "SELECT * FROM {table} WHERE {col} = '" + user_input + "'"
    cursor.execute(sql)
    return cursor.fetchall()
'''
    ])
    
    filename = f"sqli_python_{i+1:03d}.py"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

# PHP SQLi - 30 variaciones
for i in range(30):
    table = random.choice(sqli_tables)
    col = random.choice(sqli_columns)
    
    template = random.choice([
        # mysqli_query
        f'''<?php
$search = $_GET['search'];
$conn = mysqli_connect("localhost", "user", "pass", "db");
$query = "SELECT * FROM {table} WHERE {col} = '" . $search . "'";
$result = mysqli_query($conn, $query);
while($row = mysqli_fetch_assoc($result)) {{
    echo $row['{col}'];
}}
?>''',
        # PDO without prepared statements
        f'''<?php
$id = $_POST['id'];
$db = new PDO('mysql:host=localhost;dbname=app', 'user', 'pass');
$sql = "SELECT * FROM {table} WHERE {col} = " . $id;
$stmt = $db->query($sql);
$data = $stmt->fetchAll();
?>''',
        # mysql_query (deprecated but still seen)
        f'''<?php
$keyword = $_REQUEST['keyword'];
$link = mysql_connect('localhost', 'user', 'password');
mysql_select_db('database');
$query = "SELECT * FROM {table} WHERE {col} LIKE '%$keyword%'";
$result = mysql_query($query);
?>'''
    ])
    
    filename = f"sqli_php_{i+1:03d}.php"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

# Node.js SQLi - 20 variaciones
for i in range(20):
    table = random.choice(sqli_tables)
    col = random.choice(sqli_columns)
    
    template = random.choice([
        # mysql module
        f'''const mysql = require('mysql');

function get{table.capitalize()}(userId) {{
    const connection = mysql.createConnection({{
        host: 'localhost',
        user: 'root',
        database: 'app'
    }});
    
    const query = `SELECT * FROM {table} WHERE {col} = ${{userId}}`;
    connection.query(query, (error, results) => {{
        console.log(results);
    }});
}}
''',
        # pg module
        f'''const {{ Pool }} = require('pg');
const pool = new Pool();

async function search{table.capitalize()}(term) {{
    const sql = "SELECT * FROM {table} WHERE {col} LIKE '%" + term + "%'";
    const result = await pool.query(sql);
    return result.rows;
}}
'''
    ])
    
    filename = f"sqli_node_{i+1:03d}.js"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

print(f"[+] Generated {generated_count} SQLi examples")

# ============= XSS TEMPLATES (100+ variaciones) =============

xss_sinks = ['innerHTML', 'outerHTML', 'document.write', 'insertAdjacentHTML']
xss_sources = ['location.search', 'location.hash', 'document.referrer', 'window.name']

# JavaScript XSS - 30 variaciones
for i in range(30):
    sink = random.choice(xss_sinks)
    source = random.choice(xss_sources)
    
    template = random.choice([
        # innerHTML
        f'''// XSS via {sink}
function displayUserData() {{
    const params = new URLSearchParams({source});
    const data = params.get('data');
    document.getElementById('content').{sink} = data;
}}
''',
        # document.write
        f'''// XSS via document.write
const userInput = new URLSearchParams({source}).get('input');
document.write('<div>' + userInput + '</div>');
''',
        # jQuery
        f'''// jQuery XSS
$(document).ready(function() {{
    const msg = new URLSearchParams({source}).get('msg');
    $('#message').html(msg);
}});
''',
        # Template literals
        f'''// Template literal XSS
function showGreeting() {{
    const name = new URLSearchParams({source}).get('name');
    document.body.{sink} = `<h1>Hello ${{name}}</h1>`;
}}
'''
    ])
    
    filename = f"xss_js_{i+1:03d}.js"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

# PHP XSS - 30 variaciones
for i in range(30):
    template = random.choice([
        # echo
        '''<?php
$name = $_GET['name'];
echo "<h1>Welcome " . $name . "</h1>";
?>''',
        # printf
        '''<?php
$comment = $_POST['comment'];
printf("<div class='comment'>%s</div>", $comment);
?>''',
        # Heredoc
        '''<?php
$bio = $_REQUEST['bio'];
$html = <<<HTML
<div class="bio">
    <p>$bio</p>
</div>
HTML;
echo $html;
?>'''
    ])
    
    filename = f"xss_php_{i+1:03d}.php"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

# React/Vue/Angular XSS - 20 variaciones
frameworks = [
    ('jsx', 'dangerouslySetInnerHTML', 'React'),
    ('vue', 'v-html', 'Vue'),
    ('ts', 'bypassSecurityTrustHtml', 'Angular')
]

for i in range(20):
    ext, method, fw = random.choice(frameworks)
    
    if fw == 'React':
        template = f'''// React XSS
import React from 'react';

function UserPost({{ content }}) {{
    return <div dangerouslySetInnerHTML={{{{__html: content}}}} />;
}}
'''
    elif fw == 'Vue':
        template = f'''<!-- Vue XSS -->
<template>
    <div v-html="userContent"></div>
</template>

<script>
export default {{
    data() {{
        return {{ userContent: this.$route.query.content }}
    }}
}}
</script>
'''
    else:  # Angular
        template = f'''// Angular XSS
import {{ DomSanitizer }} from '@angular/platform-browser';

export class Component {{
    constructor(private sanitizer: DomSanitizer) {{}}
    
    displayHTML(html: string) {{
        return this.sanitizer.bypassSecurityTrustHtml(html);
    }}
}}
'''
    
    filename = f"xss_{fw.lower()}_{i+1:03d}.{ext}"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

print(f"[+] Generated {generated_count - 80} XSS examples")

# ============= RCE TEMPLATES (80+ variaciones) =============

rce_commands = ['ls', 'cat', 'ping', 'nslookup', 'wget', 'curl', 'whoami', 'id']

# Python RCE - 25 variaciones
for i in range(25):
    cmd = random.choice(rce_commands)
    
    template = random.choice([
        # os.system
        f'''import os

def execute_command(user_input):
    # VULNERABLE: Command injection
    os.system("{cmd} " + user_input)
''',
        # subprocess with shell=True
        f'''import subprocess

def run_process(filename):
    # VULNERABLE
    subprocess.call("{cmd} " + filename, shell=True)
''',
        # eval
        f'''def calculate(expression):
    # EXTREMELY VULNERABLE
    result = eval(expression)
    return result
''',
        # exec
        f'''def execute_code(code):
    # DANGEROUS
    exec(code)
'''
    ])
    
    filename = f"rce_python_{i+1:03d}.py"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

# PHP RCE - 25 variaciones
for i in range(25):
    cmd = random.choice(rce_commands)
    
    template = random.choice([
        # exec
        f'''<?php
$file = $_GET['file'];
exec("{cmd} " . $file, $output);
echo implode("\\n", $output);
?>''',
        # shell_exec
        f'''<?php
$domain = $_POST['domain'];
$result = shell_exec("{cmd} " . $domain);
echo $result;
?>''',
        # system
        f'''<?php
$ip = $_REQUEST['ip'];
system("{cmd} " . $ip);
?>''',
        # backticks
        f'''<?php
$host = $_GET['host'];
$output = `{cmd} $host`;
echo $output;
?>'''
    ])
    
    filename = f"rce_php_{i+1:03d}.php"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

# Node.js RCE - 15 variaciones
for i in range(15):
    cmd = random.choice(rce_commands)
    
    template = random.choice([
        # child_process.exec
        f'''const {{ exec }} = require('child_process');

function processFile(filename) {{
    exec(`{cmd} ${{filename}}`, (error, stdout) => {{
        console.log(stdout);
    }});
}}
''',
        # child_process.spawn with shell
        f'''const {{ spawn }} = require('child_process');

function runCommand(arg) {{
    const proc = spawn('{cmd}', [arg], {{ shell: true }});
    proc.stdout.on('data', (data) => console.log(data));
}}
'''
    ])
    
    filename = f"rce_node_{i+1:03d}.js"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

# Java RCE - 15 variaciones
for i in range(15):
    template = f'''import java.io.*;

public class CommandExecutor {{
    public void execute(String input) throws IOException {{
        // VULNERABLE: Command injection
        Runtime.getRuntime().exec("ls " + input);
    }}
}}
'''
    
    filename = f"rce_java_{i+1:03d}.java"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

print(f"[+] Generated {generated_count - 160} RCE examples")

# ============= PATH TRAVERSAL (30 variaciones) =============

for i in range(30):
    template = random.choice([
        # Python
        '''import os

def read_file(filename):
    # VULNERABLE: Path traversal
    with open("/var/www/uploads/" + filename, 'r') as f:
        return f.read()
''',
        # PHP include
        '''<?php
$page = $_GET['page'];
// VULNERABLE
include("/var/www/pages/" . $page);
?>''',
        # Node.js
        '''const fs = require('fs');

function getFile(name) {
    // VULNERABLE
    const content = fs.readFileSync('/uploads/' + name);
    return content;
}
''',
        # Java
        '''import java.io.*;

public class FileReader {
    public String readFile(String name) throws IOException {
        File file = new File("/data/" + name);
        // VULNERABLE: Path traversal
        return new String(Files.readAllBytes(file.toPath()));
    }
}
'''
    ])
    
    ext = 'py' if 'import os' in template or 'import' in template[:20] else ('php' if '<?php' in template else ('js' if 'const' in template else 'java'))
    filename = f"path_traversal_{i+1:03d}.{ext}"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

print(f"[+] Generated 30 Path Traversal examples")

# ============= DESERIALIZATION (30 variaciones) =============

for i in range(30):
    template = random.choice([
        # Python pickle
        '''import pickle

def load_user(data):
    # VULNERABLE: Unsafe deserialization
    user = pickle.loads(data)
    return user
''',
        # Python YAML
        '''import yaml

def parse_config(config_str):
    # VULNERABLE
    config = yaml.load(config_str)
    return config
''',
        # Java
        '''import java.io.*;

public class DataLoader {
    public Object deserialize(byte[] data) throws Exception {
        ObjectInputStream ois = new ObjectInputStream(
            new ByteArrayInputStream(data)
        );
        return ois.readObject();
    }
}
''',
        # PHP
        '''<?php
$data = $_POST['data'];
// VULNERABLE
$object = unserialize($data);
?>''',
        # Node.js
        '''const serialize = require('node-serialize');

function loadData(input) {
    // VULNERABLE
    const obj = serialize.unserialize(input);
    return obj;
}
'''
    ])
    
    ext = 'py' if 'import' in template[:20] else ('java' if 'public class' in template else ('php' if '<?php' in template else 'js'))
    filename = f"deserialization_{i+1:03d}.{ext}"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

print(f"[+] Generated 30 Deserialization examples")

# ============= WEAK CRYPTO (30 variaciones) =============

for i in range(30):
    template = random.choice([
        # MD5
        '''import hashlib

def hash_password(password):
    # VULNERABLE: Weak hash
    return hashlib.md5(password.encode()).hexdigest()
''',
        # DES
        '''from Crypto.Cipher import DES

def encrypt(data, key):
    # VULNERABLE: Weak cipher
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(data)
''',
        # SHA1
        '''import hashlib

def generate_token(data):
    # VULNERABLE
    return hashlib.sha1(data.encode()).hexdigest()
''',
        # PHP MD5
        '''<?php
$password = $_POST['password'];
// VULNERABLE
$hash = md5($password);
?>''',
        # Node.js MD5
        '''const crypto = require('crypto');

function hashData(data) {
    // VULNERABLE
    return crypto.createHash('md5').update(data).digest('hex');
}
'''
    ])
    
    ext = 'py' if 'import' in template[:20] else ('php' if '<?php' in template else 'js')
    filename = f"weak_crypto_{i+1:03d}.{ext}"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

print(f"[+] Generated 30 Weak Crypto examples")

# ============= SAFE CODE (100 variaciones) =============

for i in range(100):
    template = random.choice([
        # Python safe SQL
        '''import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    # SAFE: Prepared statement
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()
''',
        # Python safe command
        '''import subprocess

def ping_host(hostname):
    # SAFE: No shell, args list
    result = subprocess.run(['ping', '-c', '4', hostname], 
                          capture_output=True, shell=False)
    return result.stdout
''',
        # PHP prepared statement
        '''<?php
$id = $_GET['id'];
$conn = new PDO('mysql:host=localhost;dbname=app', 'user', 'pass');
// SAFE
$stmt = $conn->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$id]);
?>''',
        # Node.js parameterized query
        '''const { Pool } = require('pg');

async function getUser(userId) {
    // SAFE: Parameterized query
    const result = await pool.query(
        'SELECT * FROM users WHERE id = $1',
        [userId]
    );
    return result.rows[0];
}
''',
        # Input validation
        '''def process_file(filename):
    # SAFE: Input validation
    if not filename.isalnum():
        raise ValueError("Invalid filename")
    
    with open(f"/uploads/{filename}", 'r') as f:
        return f.read()
'''
    ])
    
    ext = 'py' if 'import' in template or 'def ' in template else ('php' if '<?php' in template else 'js')
    filename = f"safe_code_{i+1:03d}.{ext}"
    with open(os.path.join(EXAMPLES_DIR, filename), 'w') as f:
        f.write(template)
    generated_count += 1

print(f"[+] Generated 100 Safe Code examples")

print(f"\n✅ TOTAL GENERATED: {generated_count} examples")
print(f"📁 Location: {EXAMPLES_DIR}")
print(f"\n[+] Next: Run python3 scripts/5_make_features.py")
