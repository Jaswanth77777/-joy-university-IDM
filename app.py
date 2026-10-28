import os
import csv
import io
import sqlite3
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template_string, session

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024
app.secret_key = os.getenv("SECRET_KEY", "joy-university-change-this-secret")
ADMIN_USER = os.getenv("JOY_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("JOY_ADMIN_PASSWORD", "joy123")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.getenv("VERCEL"):
    DB_PATH = "/tmp/joy_university.db"
else:
    DB_PATH = os.path.join(BASE_DIR, "joy_university.db")

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            prn TEXT NOT NULL UNIQUE,
            department TEXT DEFAULT '',
            course TEXT DEFAULT '',
            year TEXT DEFAULT '',
            batch TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            blood_group TEXT DEFAULT '',
            dob TEXT DEFAULT '',
            hostel TEXT DEFAULT '',
            address TEXT DEFAULT '',
            photo TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            employee_id TEXT NOT NULL UNIQUE,
            department TEXT DEFAULT '',
            designation TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            blood_group TEXT DEFAULT '',
            dob TEXT DEFAULT '',
            address TEXT DEFAULT '',
            photo TEXT DEFAULT '',
            joined_at TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

CSS = """
*{box-sizing:border-box}html,body{min-height:100%}body{margin:0;font-family:Arial,Helvetica,sans-serif;color:#10213f;background:#071d3f;position:relative}body:before{content:"";position:fixed;inset:0;z-index:-2;background-image:url("https://joyuniversity.edu.in/images/JU_Header-Images-About-us.jpeg");background-size:cover;background-position:center;background-repeat:no-repeat}body:after{content:"";position:fixed;inset:0;z-index:-1;background:linear-gradient(135deg,rgba(2,24,58,.72),rgba(8,72,145,.54),rgba(255,255,255,.18))}a{text-decoration:none}.top{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.94);backdrop-filter:blur(12px);border-bottom:1px solid #dce6f5}
a{text-decoration:none}.top{position:sticky;top:0;z-index:10;background:#fff;border-bottom:1px solid #dce6f5}.palette{display:flex;align-items:center;gap:6px;flex-wrap:wrap}.swatch{width:28px;height:28px;border:2px solid #fff;border-radius:50%;box-shadow:0 0 0 1px #b8c7d8;cursor:pointer}.swatch[aria-pressed="true"]{box-shadow:0 0 0 2px #0c4f9e,0 0 0 4px #fff}.importbox{padding:20px;display:grid;gap:12px}.notice{padding:12px 14px;border-radius:10px;background:#eaf8ef;color:#176b40;font-weight:700;font-size:13px}.topin{max-width:1200px;margin:auto;min-height:70px;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;gap:12px}.brand{display:flex;align-items:center;gap:10px;color:#082a65}.logo{width:45px;height:45px;border-radius:12px;background:linear-gradient(135deg,#073b87,#1480df);color:#fff;display:grid;place-items:center;font-weight:900}.brand b{display:block}.brand small{color:#788aa0;letter-spacing:1px}.nav{display:flex;gap:7px;flex-wrap:wrap}.btn{display:inline-flex;align-items:center;justify-content:center;border:0;border-radius:9px;padding:10px 14px;font-weight:700;cursor:pointer;background:#edf4fc;color:#21466e}.primary{background:linear-gradient(135deg,#0754bd,#1580df);color:#fff}.danger{background:#d92e45;color:#fff}.green{background:#16844c;color:#fff}.page{max-width:1200px;margin:auto;padding:25px 15px 50px}.hero{border-radius:22px;padding:28px;color:#fff;background:linear-gradient(135deg,#062b68,#0b59b6,#1580df);box-shadow:0 18px 45px #123b7026}.hero h1{margin:0;font-size:clamp(28px,5vw,46px)}.hero p{opacity:.85}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:20px}.stat{padding:15px;border:1px solid #ffffff25;border-radius:13px;background:#ffffff12}.stat b{font-size:24px;display:block}.panel{margin-top:20px;background:#fff;border:1px solid #dce6f3;border-radius:18px;overflow:hidden;box-shadow:0 10px 30px #1c396010}.panelhead{padding:17px;border-bottom:1px solid #e6edf7;display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap}.search{display:flex;gap:7px;max-width:520px;width:100%}input,select,textarea{width:100%;padding:11px 12px;border:1px solid #cfdbea;border-radius:9px;outline:0;background:#fff}input:focus,select:focus,textarea:focus{border-color:#1680df;box-shadow:0 0 0 3px #1680df18}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:12px 14px;border-bottom:1px solid #edf1f7;font-size:13px;white-space:nowrap}th{font-size:11px;background:#f6f9fd;color:#53677f;text-transform:uppercase}.tablewrap{overflow:auto}.student{display:flex;align-items:center;gap:9px}.mini{width:40px;height:40px;border-radius:9px;overflow:hidden;background:#eaf3ff;display:grid;place-items:center;font-weight:900;color:#1355a0}.mini img{width:100%;height:100%;object-fit:cover}.actions{display:flex;gap:5px;flex-wrap:wrap}.empty{text-align:center;padding:50px;color:#71829a}.form{max-width:1000px;margin:auto}.formhead{padding:24px;color:#fff;background:linear-gradient(135deg,#082c68,#0c63c7)}.formhead h1{margin:0}.formbody{padding:24px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}.full{grid-column:1/-1}label{display:block;margin-bottom:6px;font-size:12px;font-weight:800;color:#53677f}.upload{display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:center;padding:16px;margin-bottom:20px;background:#f5f9fe;border:1px solid #dfe9f5;border-radius:14px}.preview{width:150px;height:150px;border-radius:14px;overflow:hidden;background:#eaf3ff;display:grid;place-items:center;color:#6b819e}.preview img{width:100%;height:100%;object-fit:cover}.formactions{display:flex;justify-content:flex-end;gap:8px;margin-top:20px;flex-wrap:wrap}.cardpage{min-height:calc(100vh - 70px);padding:25px 12px 50px;display:flex;align-items:center;flex-direction:column}.toolbar{width:min(760px,100%);display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:18px}.scene{width:min(440px,92vw);height:min(440px,92vw);aspect-ratio:1/1;perspective:1400px}.idcard{width:100%;height:100%;aspect-ratio:1/1;position:relative;transform-style:preserve-3d;transition:transform .8s}.idcard.back{transform:perspective(1200px) rotateY(0deg);animation:cardSideReveal .42s ease both}.idcard.back .front{display:none}.idcard.back .backface{display:flex;transform:none;animation:backFaceReveal .42s ease both}.face{position:absolute;inset:0;backface-visibility:hidden;border-radius:24px;overflow:hidden;background:#fff;box-shadow:0 30px 70px #001f4e55,0 8px 18px #001f4e22;border:1px solid #ffffffb8}.front:after,.backface:after{content:"";position:absolute;inset:0;pointer-events:none;border-radius:inherit;background:linear-gradient(125deg,#ffffff55 0%,transparent 24%,transparent 65%,#ffffff20 100%);mix-blend-mode:screen}.idcard{filter:drop-shadow(0 22px 22px #001a4030)}.cardtop{position:relative;overflow:hidden}.cardtop:after{content:"";position:absolute;width:190px;height:190px;right:-60px;top:-115px;border:1px solid #ffffff4a;border-radius:50%;box-shadow:0 0 0 18px #ffffff0d,0 0 0 38px #ffffff0a}.theme-black .cardtop{background:linear-gradient(135deg,#0a0a0a,#292929,#050505)}.theme-black .prn{background:#f0f0f0;color:#0a0a0a}.theme-blue .cardtop{background:linear-gradient(135deg,#004e6a,#007ba7,#20a9d5)}.theme-blue .prn{background:#e1f7ff;color:#006384}.theme-rose .cardtop{background:linear-gradient(135deg,#a90051,#ff2d95,#ff6eb6)}.theme-rose .prn{background:#ffe5f1;color:#a90051}.theme-emerald .cardtop{background:linear-gradient(135deg,#075c48,#0d9b78,#39c6a2)}.theme-emerald .prn{background:#e0fff4;color:#07654e}.theme-violet .cardtop{background:linear-gradient(135deg,#45208a,#7952d9,#b08aff)}.theme-violet .prn{background:#f0eaff;color:#5126a0}.theme-mocha .cardtop{background:linear-gradient(135deg,#35271d,#5B4632,#80664f)}.theme-mocha .prn{background:#eee4da;color:#5B4632}.theme-champagne .cardtop{background:linear-gradient(135deg,#c5a45f,#F4D9A0,#fff0c9);color:#382a14}.theme-champagne .cardtop .mark{color:#382a14;border-color:#382a1450;background:#ffffff40}.theme-champagne .prn{background:#fff3d4;color:#77551b}.theme-amber .cardtop{background:linear-gradient(135deg,#874311,#C8792C,#e89b4e)}.theme-amber .prn{background:#fff0e0;color:#93480f}.theme-mocha .faculty-accent{color:#5B4632}.theme-champagne .faculty-accent{color:#8b6828}.theme-amber .faculty-accent{color:#C8792C}.theme-black .faculty-accent{color:#0a0a0a}.theme-blue .faculty-accent{color:#007ba7}.theme-rose .faculty-accent{color:#ff2d95}.theme-emerald .faculty-accent{color:#0d9b78}.theme-violet .faculty-accent{color:#7952d9}.faculty-tag{display:inline-block;margin-top:7px;padding:5px 9px;border-radius:7px;background:#eef4fa;color:#294563;font-size:10px;font-weight:900;letter-spacing:.5px}.faculty-mark{font-size:9px;letter-spacing:1.4px;color:#6b7f96;text-transform:uppercase}.faculty-detail{border-left:3px solid #007ba7;padding-left:9px}.backface{transform:none;display:none;flex-direction:column}.cardtop{height:100px;padding:17px;color:#fff;display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,#06265e,#0860c9)}.mark{width:58px;height:58px;border-radius:15px;background:#ffffff18;border:1px solid #ffffff40;display:grid;place-items:center;font-weight:900;font-size:20px}.unititle b{display:block;font-size:20px}.unititle small{opacity:.8;letter-spacing:1px}.cardcontent{padding:20px}.photoarea{display:flex;align-items:center;gap:15px}.photo{width:112px;height:130px;border-radius:15px;overflow:hidden;background:#eaf3ff;display:grid;place-items:center;font-size:35px;font-weight:900;color:#1355a0;flex:none}.photo img{width:100%;height:100%;object-fit:cover}.studentmain h2{margin:0;color:#092d63;font-size:23px;line-height:1.1}.course{font-size:11px;color:#71839b;margin-top:6px}.prn{display:inline-block;margin-top:8px;padding:6px 9px;border-radius:7px;background:#eaf3ff;color:#0956af;font-size:10px;font-weight:900}.details{margin-top:18px;display:grid;grid-template-columns:1fr 1fr;gap:8px}.detail{padding:9px;background:#f5f8fc;border-radius:8px}.detail label{font-size:8px;margin:0}.detail b{display:block;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.cardbottom{position:absolute;left:20px;right:20px;bottom:15px;display:flex;justify-content:space-between;font-size:8px;color:#7c8da3}.valid{padding:5px 8px;background:#eaf8ef;color:#187b46;border-radius:7px;font-weight:900}.backcontent{padding:22px;height:100%;display:flex;flex-direction:column}.backhead{display:flex;gap:12px;align-items:center;padding-bottom:14px;border-bottom:1px solid #e2e9f3}.backhead .mark{background:linear-gradient(135deg,#073b87,#0d72d6);color:#fff}.backhead b{display:block;color:#092f68;font-size:18px}.backsection{margin-top:15px}.backsection h3{font-size:11px;color:#0a4e9e;margin:0 0 7px;text-transform:uppercase}.backsection p{font-size:10px;line-height:1.55;color:#596d86;margin:3px 0}.address{padding:10px;background:#f5f8fc;border-radius:9px;font-size:10px;color:#536983}.signatures{margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:20px}.sig{text-align:center;border-top:1px solid #9caabc;padding-top:5px;font-size:8px;color:#687b94}.footer{text-align:center;padding:25px;color:#7d8da1;font-size:11px}@media(max-width:800px){.stats{grid-template-columns:1fr 1fr}.grid{grid-template-columns:1fr}.full{grid-column:auto}.upload{grid-template-columns:1fr}.preview{margin:auto}.topin{align-items:flex-start;flex-direction:column}.nav{width:100%}}@media(max-width:520px){.stats{gap:7px}.stat{padding:11px}.stat b{font-size:19px}.photo{width:95px;height:115px}.studentmain h2{font-size:19px}}@media print{@page{size:440px 440px;margin:0}html,body{width:440px;height:440px;margin:0;background:#fff}.no-print{display:none!important}.cardpage{width:440px;height:440px;min-height:440px;padding:0;display:block}.scene{width:440px;height:440px;perspective:none}.idcard{width:440px;height:440px;transform:none!important}.face{border-radius:0;box-shadow:none}body:not(.print-back) .backface{display:none}.print-back .front{display:none}.print-back .backface{display:block;transform:none}}
"""

LOADER = """
<div id="loader" style="position:fixed;inset:0;z-index:99999;background:linear-gradient(135deg,rgba(3,24,61,.78),rgba(7,84,189,.62),rgba(21,145,238,.45)),url("https://joyuniversity.edu.in/images/JU_Header-Images-About-us.jpeg");background-size:cover;background-position:center;display:grid;place-items:center;color:#fff;transition:opacity .45s">
  <div class="loading-watermark">JU</div>
  <div style="position:relative;text-align:center;width:min(390px,88vw);padding:35px 25px">
    <div style="width:82px;height:82px;margin:0 auto 18px;border-radius:24px;background:#ffffff16;border:1px solid #ffffff35;display:grid;place-items:center;font-size:28px;font-weight:900;box-shadow:0 15px 40px #00183d55">JU</div>
    <div style="font-size:28px;font-weight:900;letter-spacing:2px">JOY UNIVERSITY</div>
    <div style="opacity:.82;margin-top:8px;font-size:11px;letter-spacing:1.5px">STUDENT ID CARD MANAGEMENT SYSTEM</div>
    <div class="loading-ring"></div>
    <div style="font-size:12px;font-weight:700;opacity:.9">Loading system...</div>
    <div class="loading-track"><div id="loadingBar"></div></div>
    <div id="loadingPercent" style="font-size:10px;opacity:.7;margin-top:7px">0%</div>
  </div>
</div>
<style>
.loading-watermark{position:absolute;inset:0;display:grid;place-items:center;font-size:55vw;font-weight:900;color:#fff;opacity:.025;pointer-events:none}
.loading-ring{width:52px;height:52px;border:5px solid #ffffff35;border-top-color:#fff;border-right-color:#fff;border-radius:50%;margin:24px auto 12px;animation:spin 1s linear infinite}
.loading-track{height:5px;background:#ffffff25;border-radius:20px;overflow:hidden;margin:13px auto 0;max-width:270px}
#loadingBar{height:100%;width:0;background:#fff;border-radius:20px;transition:width .12s linear}
@keyframes spin{to{transform:rotate(360deg)}}@keyframes cardSideReveal{0%{transform:perspective(1200px) rotateY(0deg) scale(.98)}45%{transform:perspective(1200px) rotateY(12deg) scale(.985)}100%{transform:perspective(1200px) rotateY(0deg) scale(1)}}@keyframes backFaceReveal{0%{opacity:.25;transform:translateX(7px)}100%{opacity:1;transform:translateX(0)}}
</style>
<script>
(function(){
  var bar=document.getElementById("loadingBar"), pct=document.getElementById("loadingPercent"), n=0;
  var timer=setInterval(function(){n=Math.min(n+4,96);if(bar)bar.style.width=n+"%";if(pct)pct.textContent=n+"%"},60);
  window.finishLoading=function(){
    clearInterval(timer);n=100;
    if(bar)bar.style.width="100%";if(pct)pct.textContent="100%";
    setTimeout(function(){var x=document.getElementById("loader");if(x){x.style.opacity="0";setTimeout(function(){x.remove()},450)}},180);
  };
  window.addEventListener("load",function(){setTimeout(window.finishLoading,260)});
})();
</script>
<script>
function goBack(){if(document.referrer && document.referrer.indexOf(location.host)!==-1){history.back()}else{location.href="/"}}
document.addEventListener("click",function(e){
  var a=e.target.closest("a");
  if(a && a.href && a.target!="_blank" && !a.href.startsWith("javascript:") && a.getAttribute("href") && !a.getAttribute("href").startsWith("#")){
    var loader=document.getElementById("loader");
    if(loader){loader.style.opacity="1";loader.style.display="grid";}
  }
});
document.addEventListener("submit",function(){
  var loader=document.getElementById("loader");
  if(loader){loader.style.opacity="1";loader.style.display="grid";if(window.finishLoading)window.finishLoading();}
});
</script>
"""

LOGIN = """
<main style="min-height:100vh;display:grid;place-items:center;padding:30px 15px">
  <section style="width:min(460px,100%);background:rgba(255,255,255,.94);backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.7);border-radius:24px;padding:30px;box-shadow:0 30px 90px rgba(0,20,60,.45)">
    <div style="text-align:center">
      <div style="width:76px;height:76px;margin:0 auto 14px;border-radius:22px;background:linear-gradient(135deg,#073b87,#1480df);color:#fff;display:grid;place-items:center;font-size:25px;font-weight:900;box-shadow:0 12px 30px #073b8740">JU</div>
      <h1 style="margin:0;color:#082a65;font-size:30px">JOY UNIVERSITY</h1>
      <p style="margin:7px 0 24px;color:#64758b;font-size:12px;letter-spacing:1px">STUDENT ID CARD MANAGEMENT SYSTEM</p>
    </div>
    {% if error %}<div style="padding:11px 13px;border-radius:10px;background:#fff0f2;color:#b42338;font-size:13px;font-weight:700;margin-bottom:14px">{{error}}</div>{% endif %}
    <form method="post">
      <label>USERNAME</label><input name="username" required autocomplete="username" placeholder="Enter username">
      <label style="margin-top:14px">PASSWORD</label><input name="password" type="password" required autocomplete="current-password" placeholder="Enter password">
      <button class="btn primary" style="width:100%;margin-top:20px;padding:13px">Login to Dashboard</button>
    </form>
    <div style="margin-top:18px;text-align:center;color:#7a8aa0;font-size:11px">Secure university administration access</div>
  </section>
</main>
"""

def page(body, title="JOY UNIVERSITY"):
    return render_template_string(
        "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{{title}}</title><style>"
        + CSS +
        "</style></head><body>" + LOADER + body + "</body></html>",
        title=title
    )

NAV = """
<header class="top"><div class="topin">
<a class="brand" href="{{url_for('home')}}"><div class="logo">JU</div><div><b>JOY UNIVERSITY</b><small> STUDENT ID MANAGEMENT</small></div></a>
<nav class="nav"><button type="button" class="btn" onclick="goBack()">← Back</button><a class="btn" href="{{url_for('home')}}">Dashboard</a><a class="btn" href="{{url_for('teachers')}}">Teachers</a><a class="btn" href="{{url_for('bulk_import')}}">Bulk Import</a><a class="btn primary" href="{{url_for('add_student')}}">+ Add Student</a><a class="btn danger" href="{{url_for('logout')}}">Logout</a></nav>
</div></header>
"""

DASH = NAV + """
<main class="page">
<section class="hero"><h1>Student &amp; Faculty ID Studio</h1><p>Manage separate student and teacher profiles, then create polished square 3D ID cards with quick colour themes.</p>
<div class="stats"><div class="stat"><b>{{total}}</b>Total Students</div><div class="stat"><b>{{teachers_total}}</b>Faculty Members</div><div class="stat"><b>{{departments}}</b>Departments</div><div class="stat"><b>{{photos}}</b>Photos Added</div></div><div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn" style="background:#fff;color:#0754bd" href="{{url_for('teachers')}}">Manage Faculty</a><a class="btn" style="background:#fff;color:#0754bd" href="{{url_for('add_teacher')}}">+ Add Faculty ID</a></div></section>
<section class="panel"><div class="panelhead"><div><h2 style="margin:0">Student Profiles</h2><div style="font-size:12px;color:#71839a;margin-top:4px">Logged in as {{session_user}}</div></div><div class="actions"><a class="btn" href="{{url_for('download_csv_template')}}">CSV Template</a><a class="btn primary" href="{{url_for('bulk_import')}}">Bulk Import CSV</a></div><form class="search"><input name="q" value="{{q}}" placeholder="Search name, PRN, department, course..."><button class="btn primary">Search</button>{% if q %}<a class="btn" href="{{url_for('home')}}">Clear</a>{% endif %}</form></div>
<div class="tablewrap">{% if students %}<table><thead><tr><th>Student</th><th>PRN</th><th>Department</th><th>Course</th><th>Year</th><th>Actions</th></tr></thead><tbody>
{% for s in students %}<tr><td><div class="student"><div class="mini">{% if s.photo %}<img src="{{s.photo}}">{% else %}{{s.name[:1].upper()}}{% endif %}</div><b>{{s.name}}</b></div></td><td>{{s.prn}}</td><td>{{s.department or "-"}}</td><td>{{s.course or "-"}}</td><td>{{s.year or "-"}}</td><td><div class="actions"><a class="btn primary" href="{{url_for('card',sid=s.id)}}">ID Card</a><a class="btn" href="{{url_for('edit_student',sid=s.id)}}">Edit</a><a class="btn danger" href="{{url_for('delete_student',sid=s.id)}}" onclick="return confirm('Delete this student?')">Delete</a></div></td></tr>{% endfor %}
</tbody></table>{% else %}<div class="empty"><h3>No students found</h3><p>Add a student to generate an ID card.</p><a class="btn primary" href="{{url_for('add_student')}}">+ Add Student</a></div>{% endif %}</div></section>
</main><div class="footer">JOY UNIVERSITY • Student ID Card Management System</div>
"""

FORM = NAV + """
<main class="page"><section class="panel form"><div class="formhead"><h1>{% if student %}Edit Student Profile{% else %}Add New Student{% endif %}</h1><p>Enter the details used on the university ID card.</p>{% if error %}<p style="color:#ffd7dc;font-weight:bold">{{error}}</p>{% endif %}</div>
<form class="formbody" method="post">
<div class="upload"><div class="preview">{% if student and student.photo %}<img id="preview" src="{{student.photo}}">{% else %}<img id="preview" style="display:none">{% endif %}</div><div><h3>Student Photo</h3><input id="photoFile" type="file" accept="image/*"><input id="photoData" type="hidden" name="photo" value="{{student.photo if student else ''}}"><p style="font-size:12px;color:#71839a">Use a JPG/PNG/WEBP image. It is stored with the student profile.</p></div></div>
<div class="grid">
<div><label>FULL NAME *</label><input name="name" required value="{{student.name if student else ''}}"></div>
<div><label>PRN / STUDENT ID *</label><input name="prn" required value="{{student.prn if student else ''}}"></div>
<div><label>DEPARTMENT</label><input name="department" value="{{student.department if student else ''}}"></div>
<div><label>COURSE</label><input name="course" value="{{student.course if student else ''}}"></div>
<div><label>YEAR</label><select name="year"><option value="">Select</option>{% for y in ['1st Year','2nd Year','3rd Year','4th Year','5th Year'] %}<option {% if student and student.year==y %}selected{% endif %}>{{y}}</option>{% endfor %}</select></div>
<div><label>BATCH</label><input name="batch" value="{{student.batch if student else ''}}"></div>
<div><label>PHONE</label><input name="phone" value="{{student.phone if student else ''}}"></div>
<div><label>EMAIL</label><input name="email" type="email" value="{{student.email if student else ''}}"></div>
<div><label>BLOOD GROUP</label><select name="blood_group"><option value="">Select</option>{% for b in ['A+','A-','B+','B-','AB+','AB-','O+','O-'] %}<option {% if student and student.blood_group==b %}selected{% endif %}>{{b}}</option>{% endfor %}</select></div>
<div><label>DATE OF BIRTH</label><input name="dob" type="date" value="{{student.dob if student else ''}}"></div>
<div><label>HOSTEL / RESIDENCE</label><input name="hostel" value="{{student.hostel if student else ''}}"></div>
<div class="full"><label>ADDRESS</label><textarea name="address">{{student.address if student else ''}}</textarea></div>
</div><div class="formactions"><a class="btn" href="{{url_for('home')}}">Cancel</a><button class="btn primary">Save Student</button></div></form></section></main>
<div class="footer">JOY UNIVERSITY • Student ID Card Management System</div>
<script>
document.getElementById("photoFile").addEventListener("change",function(){
 var f=this.files[0]; if(!f)return;
 if(f.size>4*1024*1024){alert("Please use an image smaller than 4 MB.");this.value="";return;}
 var r=new FileReader(); r.onload=function(e){document.getElementById("photoData").value=e.target.result;var p=document.getElementById("preview");p.src=e.target.result;p.style.display="block"};r.readAsDataURL(f);
});
</script>
"""

CARD = NAV + """
<main class="cardpage"><div class="toolbar no-print"><h2>3D Student ID Card • Square 1:1</h2><div class="nav"><button class="btn" onclick="frontSide()">Front</button><button class="btn" onclick="backSide()">Back</button><button class="btn green" onclick="printCard()">Print Card</button></div><div class="palette" aria-label="Card color theme"><span style="font-size:11px;font-weight:800;color:#fff">CARD COLORS</span><button type="button" class="swatch" title="Jet Black #0A0A0A" style="background:#0A0A0A" aria-label="Jet Black" data-theme="black" onclick="setTheme('black')"></button><button type="button" class="swatch" title="Cerulean Blue #007BA7" style="background:#007BA7" aria-label="Cerulean Blue" data-theme="blue" onclick="setTheme('blue')"></button><button type="button" class="swatch" title="Neon Rose #FF2D95" style="background:#FF2D95" aria-label="Neon Rose" data-theme="rose" onclick="setTheme('rose')"></button><button type="button" class="swatch" title="Emerald" style="background:#0D9B78" aria-label="Emerald" data-theme="emerald" onclick="setTheme('emerald')"></button><button type="button" class="swatch" title="Violet" style="background:#7952D9" aria-label="Violet" data-theme="violet" onclick="setTheme('violet')"></button><button type="button" class="swatch" title="Mocha Brown #5B4632" style="background:#5B4632" aria-label="Mocha Brown" data-theme="mocha" onclick="setTheme('mocha')"></button><button type="button" class="swatch" title="Champagne Gold #F4D9A0" style="background:#F4D9A0" aria-label="Champagne Gold" data-theme="champagne" onclick="setTheme('champagne')"></button><button type="button" class="swatch" title="Burnt Amber #C8792C" style="background:#C8792C" aria-label="Burnt Amber" data-theme="amber" onclick="setTheme('amber')"></button></div></div>
<div class="scene"><div id="idCard" class="idcard theme-blue">
<div class="face front"><div class="cardtop"><div class="mark">JU</div><div class="unititle"><b>JOY UNIVERSITY</b><small>STUDENT IDENTITY CARD</small></div></div>
<div class="cardcontent"><div class="photoarea"><div class="photo">{% if student.photo %}<img src="{{student.photo}}">{% else %}{{student.name[:1].upper()}}{% endif %}</div><div class="studentmain"><h2>{{student.name}}</h2><div class="course">{{student.course or 'Student'}}</div><div class="prn">PRN: {{student.prn}}</div></div></div>
<div class="details"><div class="detail"><label>Department</label><b>{{student.department or '-'}}</b></div><div class="detail"><label>Year</label><b>{{student.year or '-'}}</b></div><div class="detail"><label>Batch</label><b>{{student.batch or '-'}}</b></div><div class="detail"><label>Blood Group</label><b>{{student.blood_group or '-'}}</b></div><div class="detail"><label>Phone</label><b>{{student.phone or '-'}}</b></div><div class="detail"><label>DOB</label><b>{{student.dob or '-'}}</b></div></div></div>
<div class="cardbottom"><span>Property of JOY UNIVERSITY</span><span class="valid">VALID ID</span></div></div>
<div class="face backface"><div class="backcontent"><div class="backhead"><div class="mark">JU</div><div><b>JOY UNIVERSITY</b><small>STUDENT IDENTITY CARD</small></div></div>
<div class="backsection"><h3>Student Information</h3><p>Name: <b>{{student.name}}</b></p><p>PRN: <b>{{student.prn}}</b></p><p>Department: <b>{{student.department or '-'}}</b></p><p>Course: <b>{{student.course or '-'}}</b></p><p>Hostel: <b>{{student.hostel or '-'}}</b></p></div>
<div class="backsection"><h3>Address</h3><div class="address">{{student.address or 'University Address'}}</div></div>
<div class="backsection"><h3>Important Notice</h3><p>This card is the property of JOY UNIVERSITY. If found, please return it to the university administration office. Students should carry this ID while on campus.</p></div>
<div class="backsection"><h3>Contact</h3><p>Student Administration Office<br>administration@joyuniversity.edu<br>{{student.phone or 'University Office'}}</p></div>
<div class="signatures"><div class="sig">Student Signature</div><div class="sig">Authorized Signature</div></div></div></div>
</div></div></main><div class="footer no-print">JOY UNIVERSITY • Student ID Card Management System</div>
<script>
function setTheme(name){var card=document.getElementById("idCard");card.classList.remove("theme-black","theme-blue","theme-rose","theme-emerald","theme-violet","theme-mocha","theme-champagne","theme-amber");card.classList.add("theme-"+name);document.querySelectorAll(".swatch").forEach(function(b){b.setAttribute("aria-pressed",b.getAttribute("data-theme")===name?"true":"false")});try{localStorage.setItem("joyCardTheme",name)}catch(e){}}
(function(){try{setTheme(localStorage.getItem("joyCardTheme")||"blue")}catch(e){setTheme("blue")}})();
function frontSide(){document.getElementById("idCard").classList.remove("back");document.body.classList.remove("print-back")}
function backSide(){document.getElementById("idCard").classList.add("back");document.body.classList.add("print-back")}
function printCard(){window.print()}
</script>
"""


BULK_IMPORT = NAV + """
<main class="page"><section class="panel form"><div class="formhead"><h1>Bulk Import Students</h1><p>Upload a CSV file to add many student profiles at once.</p></div>
<div class="importbox">
<div class="notice">Use the CSV template so column names match. Existing PRNs are skipped to avoid duplicates.</div>
<p style="margin:0;color:#53677f;font-size:13px">Required columns: <b>name, prn</b>. Optional columns: department, course, year, batch, phone, email, blood_group, dob, hostel, address, photo.</p>
<a class="btn" style="width:max-content" href="{{url_for('download_csv_template')}}">Download CSV Template</a>
<form method="post" enctype="multipart/form-data">
<label>CSV FILE</label><input type="file" name="file" accept=".csv,text/csv" required>
<div class="formactions"><a class="btn" href="{{url_for('home')}}">Cancel</a><button class="btn primary">Import Students</button></div>
</form>
{% if result %}<div class="notice">Import finished: {{result.added}} added, {{result.skipped}} skipped.</div>{% endif %}
{% if error %}<div style="padding:12px;background:#fff0f2;color:#b42338;border-radius:10px;font-weight:700">{{error}}</div>{% endif %}
</div></section></main><div class="footer">JOY UNIVERSITY • Bulk Student Import</div>
"""


TEACHERS_DASH = NAV + """
<main class="page"><section class="hero"><h1>Faculty ID Management</h1><p>Faculty records are separate from student records. Create individual staff cards with quick colour themes.</p><div class="stats"><div class="stat"><b>{{total}}</b>Faculty Members</div><div class="stat"><b>{{departments}}</b>Departments</div><div class="stat"><b>{{photos}}</b>Photos Added</div><div class="stat"><b>JU</b>Faculty ID Studio</div></div><div style="display:flex;gap:9px;flex-wrap:wrap;margin-top:16px"><a class="btn" style="background:#fff;color:#0754bd" href="{{url_for('home')}}">Student Management</a><a class="btn" style="background:#fff;color:#0754bd" href="{{url_for('add_teacher')}}">+ Add Faculty</a></div></section>
<section class="panel"><div class="panelhead"><div><h2 style="margin:0">Faculty Profiles</h2><div style="font-size:12px;color:#71839a;margin-top:4px">Teachers and staff only</div></div><form class="search"><input name="q" value="{{q}}" placeholder="Search name, employee ID, department..."><button class="btn primary">Search</button>{% if q %}<a class="btn" href="{{url_for('teachers')}}">Clear</a>{% endif %}</form></div><div class="tablewrap">{% if records %}<table><thead><tr><th>Faculty Member</th><th>Employee ID</th><th>Designation</th><th>Department</th><th>Actions</th></tr></thead><tbody>{% for t in records %}<tr><td><div class="student"><div class="mini">{% if t.photo %}<img src="{{t.photo}}">{% else %}{{t.name[:1].upper()}}{% endif %}</div><b>{{t.name}}</b></div></td><td>{{t.employee_id}}</td><td>{{t.designation or '-'}}</td><td>{{t.department or '-'}}</td><td><div class="actions"><a class="btn primary" href="{{url_for('teacher_card',tid=t.id)}}">Faculty ID</a><a class="btn" href="{{url_for('edit_teacher',tid=t.id)}}">Edit</a><a class="btn danger" href="{{url_for('delete_teacher',tid=t.id)}}" onclick="return confirm('Delete this faculty profile?')">Delete</a></div></td></tr>{% endfor %}</tbody></table>{% else %}<div class="empty"><h3>No faculty profiles yet</h3><p>Add a teacher or staff member to create a faculty ID card.</p><a class="btn primary" href="{{url_for('add_teacher')}}">+ Add Faculty</a></div>{% endif %}</div></section></main><div class="footer">JOY UNIVERSITY • Faculty ID Management</div>
"""

TEACHER_FORM = NAV + """
<main class="page"><section class="panel form"><div class="formhead"><h1>{% if teacher %}Edit Faculty Profile{% else %}Create Faculty ID{% endif %}</h1><p>Teacher records are stored separately from student records.</p>{% if error %}<p style="color:#ffd7dc;font-weight:bold">{{error}}</p>{% endif %}</div><form class="formbody" method="post"><div class="upload"><div class="preview">{% if teacher and teacher.photo %}<img id="preview" src="{{teacher.photo}}">{% else %}<img id="preview" style="display:none">{% endif %}</div><div><h3>Faculty Photo</h3><input id="photoFile" type="file" accept="image/*"><input id="photoData" type="hidden" name="photo" value="{{teacher.photo if teacher else ''}}"><p style="font-size:12px;color:#71839a">Use a clear staff photo (JPG, PNG or WEBP, max 4 MB).</p></div></div><div class="grid"><div><label>FULL NAME *</label><input name="name" required value="{{teacher.name if teacher else ''}}"></div><div><label>EMPLOYEE ID *</label><input name="employee_id" required value="{{teacher.employee_id if teacher else ''}}"></div><div><label>DESIGNATION / ROLE</label><input name="designation" placeholder="Professor, Lecturer, HOD..." value="{{teacher.designation if teacher else ''}}"></div><div><label>DEPARTMENT</label><input name="department" value="{{teacher.department if teacher else ''}}"></div><div><label>PHONE</label><input name="phone" value="{{teacher.phone if teacher else ''}}"></div><div><label>EMAIL</label><input name="email" type="email" value="{{teacher.email if teacher else ''}}"></div><div><label>BLOOD GROUP</label><select name="blood_group"><option value="">Select</option>{% for b in ['A+','A-','B+','B-','AB+','AB-','O+','O-'] %}<option {% if teacher and teacher.blood_group==b %}selected{% endif %}>{{b}}</option>{% endfor %}</select></div><div><label>DATE OF BIRTH</label><input name="dob" type="date" value="{{teacher.dob if teacher else ''}}"></div><div class="full"><label>ADDRESS</label><textarea name="address">{{teacher.address if teacher else ''}}</textarea></div></div><div class="formactions"><a class="btn" href="{{url_for('teachers')}}">Cancel</a><button class="btn primary">Save Faculty Profile</button></div></form></section></main><div class="footer">JOY UNIVERSITY • Faculty ID Management</div><script>document.getElementById("photoFile").addEventListener("change",function(){var f=this.files[0];if(!f)return;if(f.size>4*1024*1024){alert("Please use an image smaller than 4 MB.");this.value="";return;}var r=new FileReader();r.onload=function(e){document.getElementById("photoData").value=e.target.result;var p=document.getElementById("preview");p.src=e.target.result;p.style.display="block"};r.readAsDataURL(f);});</script>
"""

TEACHER_CARD = NAV + """
<main class="cardpage"><div class="toolbar no-print"><h2>Faculty ID Card • Square 1:1</h2><div class="nav"><button class="btn" onclick="frontSide()">Front</button><button class="btn" onclick="backSide()">Back</button><button class="btn green" onclick="printCard()">Print Card</button></div><div class="palette" aria-label="Faculty card colours"><span style="font-size:11px;font-weight:800;color:#fff">QUICK COLOURS</span><button type="button" class="swatch" title="Jet Black #0A0A0A" style="background:#0A0A0A" data-theme="black" onclick="setTheme('black')"></button><button type="button" class="swatch" title="Cerulean Blue #007BA7" style="background:#007BA7" data-theme="blue" onclick="setTheme('blue')"></button><button type="button" class="swatch" title="Neon Rose #FF2D95" style="background:#FF2D95" data-theme="rose" onclick="setTheme('rose')"></button><button type="button" class="swatch" title="Emerald" style="background:#0D9B78" data-theme="emerald" onclick="setTheme('emerald')"></button><button type="button" class="swatch" title="Violet" style="background:#7952D9" data-theme="violet" onclick="setTheme('violet')"></button><button type="button" class="swatch" title="Mocha Brown #5B4632" style="background:#5B4632" data-theme="mocha" onclick="setTheme('mocha')"></button><button type="button" class="swatch" title="Champagne Gold #F4D9A0" style="background:#F4D9A0" data-theme="champagne" onclick="setTheme('champagne')"></button><button type="button" class="swatch" title="Burnt Amber #C8792C" style="background:#C8792C" data-theme="amber" onclick="setTheme('amber')"></button></div></div><div class="scene"><div id="idCard" class="idcard theme-blue"><div class="face front"><div class="cardtop"><div class="mark">JU</div><div class="unititle"><b>JOY UNIVERSITY</b><small>FACULTY IDENTITY CARD</small></div></div><div class="cardcontent"><div class="faculty-mark">UNIVERSITY FACULTY • OFFICIAL ID</div><div class="photoarea" style="margin-top:12px"><div class="photo">{% if teacher.photo %}<img src="{{teacher.photo}}">{% else %}{{teacher.name[:1].upper()}}{% endif %}</div><div class="studentmain"><h2>{{teacher.name}}</h2><div class="course">{{teacher.department or 'University Faculty'}}</div><div class="prn faculty-accent">EMP ID: {{teacher.employee_id}}</div><div class="faculty-tag">{{teacher.designation or 'FACULTY MEMBER'}}</div></div></div><div class="details"><div class="detail faculty-detail"><label>Department</label><b>{{teacher.department or '-'}}</b></div><div class="detail faculty-detail"><label>Designation</label><b>{{teacher.designation or '-'}}</b></div><div class="detail faculty-detail"><label>Phone</label><b>{{teacher.phone or '-'}}</b></div><div class="detail faculty-detail"><label>Blood Group</label><b>{{teacher.blood_group or '-'}}</b></div></div></div><div class="cardbottom"><span>JOY UNIVERSITY • FACULTY</span><span class="valid">AUTHORIZED</span></div></div><div class="face backface"><div class="backcontent"><div class="backhead"><div class="mark">JU</div><div><b>JOY UNIVERSITY</b><small>FACULTY IDENTITY CARD</small></div></div><div class="backsection"><h3>Faculty Details</h3><p>Name: <b>{{teacher.name}}</b></p><p>Employee ID: <b>{{teacher.employee_id}}</b></p><p>Designation: <b>{{teacher.designation or '-'}}</b></p><p>Department: <b>{{teacher.department or '-'}}</b></p><p>Email: <b>{{teacher.email or '-'}}</b></p><p>Date of Birth: <b>{{teacher.dob or '-'}}</b></p></div><div class="backsection"><h3>Address</h3><div class="address">{{teacher.address or 'University Address'}}</div></div><div class="backsection"><h3>Institution Property</h3><p>This faculty card remains the property of JOY UNIVERSITY. Display it on campus and return it to administration when employment ends.</p></div><div class="signatures"><div class="sig">Faculty Signature</div><div class="sig">Authorized Signature</div></div></div></div></div></div></main><div class="footer no-print">JOY UNIVERSITY • Faculty ID Card</div><script>function setTheme(name){var card=document.getElementById("idCard");card.classList.remove("theme-black","theme-blue","theme-rose","theme-emerald","theme-violet");card.classList.add("theme-"+name);document.querySelectorAll(".swatch").forEach(function(b){b.setAttribute("aria-pressed",b.getAttribute("data-theme")===name?"true":"false")});try{localStorage.setItem("joyFacultyCardTheme",name)}catch(e){}}(function(){try{setTheme(localStorage.getItem("joyFacultyCardTheme")||"blue")}catch(e){setTheme("blue")}})();function frontSide(){document.getElementById("idCard").classList.remove("back");document.body.classList.remove("print-back")}function backSide(){document.getElementById("idCard").classList.add("back");document.body.classList.add("print-back")}function printCard(){window.print()}</script>
"""

def login_required(view):
    from functools import wraps
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("home"))
    error = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session["user"] = username
            return redirect(url_for("home"))
        error = "Invalid username or password."
    return page(render_template_string(LOGIN, error=error), "Login - JOY UNIVERSITY")

@app.route("/bulk-import", methods=["GET", "POST"])
@login_required
def bulk_import():
    result = None
    error = ""
    if request.method == "POST":
        upload = request.files.get("file")
        if not upload or not upload.filename:
            error = "Choose a CSV file first."
        elif not upload.filename.lower().endswith(".csv"):
            error = "Please upload a .csv file."
        else:
            try:
                stream = io.StringIO(upload.stream.read().decode("utf-8-sig"), newline=None)
                reader = csv.DictReader(stream)
                if not reader.fieldnames or not {"name", "prn"}.issubset({h.strip().lower() for h in reader.fieldnames if h}):
                    raise ValueError("CSV must include name and prn column headers.")
                fields = ["name", "prn", "department", "course", "year", "batch", "phone", "email", "blood_group", "dob", "hostel", "address", "photo"]
                con = db()
                added = 0
                skipped = 0
                for row in reader:
                    normalized = {(key or "").strip().lower(): (value or "").strip() for key, value in row.items()}
                    name = normalized.get("name", "")
                    prn = normalized.get("prn", "")
                    if not name or not prn:
                        skipped += 1
                        continue
                    values = [name, prn] + [normalized.get(k, "") for k in fields[2:]]
                    try:
                        con.execute("INSERT INTO students(name,prn,department,course,year,batch,phone,email,blood_group,dob,hostel,address,photo,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (*values, datetime.now().isoformat()))
                        added += 1
                    except sqlite3.IntegrityError:
                        skipped += 1
                con.commit()
                con.close()
                result = {"added": added, "skipped": skipped}
            except (UnicodeDecodeError, csv.Error, ValueError) as exc:
                error = "Could not import CSV: " + str(exc)
    return page(render_template_string(BULK_IMPORT, result=result, error=error), "Bulk Import - JOY UNIVERSITY")

@app.route("/bulk-import/template.csv")
@login_required
def download_csv_template():
    from flask import Response
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["name", "prn", "department", "course", "year", "batch", "phone", "email", "blood_group", "dob", "hostel", "address", "photo"])
    writer.writerow(["Aarav Kumar", "JU2026001", "Computer Science", "B.Sc Computer Science", "1st Year", "2026-2030", "9876543210", "aarav@example.com", "O+", "2007-05-12", "Hostel A", "Campus address", ""])
    from flask import Response
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=joy_university_students_template.csv"})


@app.route("/teachers")
@login_required
def teachers():
    q = request.args.get("q", "").strip()
    con = db()
    if q:
        like = "%" + q + "%"
        records = con.execute("SELECT * FROM teachers WHERE name LIKE ? OR employee_id LIKE ? OR department LIKE ? OR designation LIKE ? ORDER BY id DESC", (like, like, like, like)).fetchall()
    else:
        records = con.execute("SELECT * FROM teachers ORDER BY id DESC").fetchall()
    total = con.execute("SELECT COUNT(*) c FROM teachers").fetchone()["c"]
    departments = con.execute("SELECT COUNT(DISTINCT department) c FROM teachers WHERE department!=''").fetchone()["c"]
    photos = con.execute("SELECT COUNT(*) c FROM teachers WHERE photo!=''").fetchone()["c"]
    con.close()
    return page(render_template_string(TEACHERS_DASH, records=records, total=total, departments=departments, photos=photos, q=q), "Faculty Management - JOY UNIVERSITY")

def teacher_form_data():
    return {k: request.form.get(k, "").strip() for k in ["name", "employee_id", "department", "designation", "phone", "email", "blood_group", "dob", "address", "photo"]}

@app.route("/teacher/add", methods=["GET", "POST"])
@login_required
def add_teacher():
    if request.method == "POST":
        d = teacher_form_data()
        if not d["name"] or not d["employee_id"]:
            return page(render_template_string(TEACHER_FORM, teacher=d, error="Name and employee ID are required."), "Add Faculty")
        con = db()
        try:
            con.execute("INSERT INTO teachers(name,employee_id,department,designation,phone,email,blood_group,dob,address,photo,joined_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (*[d[k] for k in ["name", "employee_id", "department", "designation", "phone", "email", "blood_group", "dob", "address", "photo"]], datetime.now().isoformat()))
            con.commit()
        except sqlite3.IntegrityError:
            con.close()
            return page(render_template_string(TEACHER_FORM, teacher=d, error="Employee ID already exists."), "Add Faculty")
        con.close()
        return redirect(url_for("teachers"))
    return page(render_template_string(TEACHER_FORM, teacher=None, error=""), "Add Faculty")

@app.route("/teacher/edit/<int:tid>", methods=["GET", "POST"])
@login_required
def edit_teacher(tid):
    con = db()
    old = con.execute("SELECT * FROM teachers WHERE id=?", (tid,)).fetchone()
    con.close()
    if not old:
        return redirect(url_for("teachers"))
    if request.method == "POST":
        d = teacher_form_data()
        if not d["name"] or not d["employee_id"]:
            return page(render_template_string(TEACHER_FORM, teacher=d, error="Name and employee ID are required."), "Edit Faculty")
        con = db()
        try:
            con.execute("UPDATE teachers SET name=?,employee_id=?,department=?,designation=?,phone=?,email=?,blood_group=?,dob=?,address=?,photo=? WHERE id=?", (*[d[k] for k in ["name", "employee_id", "department", "designation", "phone", "email", "blood_group", "dob", "address", "photo"]], tid))
            con.commit()
        except sqlite3.IntegrityError:
            con.close()
            return page(render_template_string(TEACHER_FORM, teacher=d, error="Employee ID already belongs to another faculty member."), "Edit Faculty")
        con.close()
        return redirect(url_for("teacher_card", tid=tid))
    return page(render_template_string(TEACHER_FORM, teacher=old, error=""), "Edit Faculty")

@app.route("/teacher/delete/<int:tid>")
@login_required
def delete_teacher(tid):
    con = db()
    con.execute("DELETE FROM teachers WHERE id=?", (tid,))
    con.commit()
    con.close()
    return redirect(url_for("teachers"))

@app.route("/teacher/card/<int:tid>")
@login_required
def teacher_card(tid):
    con = db()
    teacher = con.execute("SELECT * FROM teachers WHERE id=?", (tid,)).fetchone()
    con.close()
    if not teacher:
        return redirect(url_for("teachers"))
    return page(render_template_string(TEACHER_CARD, teacher=teacher), "Faculty ID Card - JOY UNIVERSITY")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def home():
    q = request.args.get("q","").strip()
    con = db()
    if q:
        s = "%" + q + "%"
        students = con.execute("SELECT * FROM students WHERE name LIKE ? OR prn LIKE ? OR department LIKE ? OR course LIKE ? OR batch LIKE ? ORDER BY id DESC",(s,s,s,s,s)).fetchall()
    else:
        students = con.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    total = con.execute("SELECT COUNT(*) c FROM students").fetchone()["c"]
    departments = con.execute("SELECT COUNT(DISTINCT department) c FROM students WHERE department!=''").fetchone()["c"]
    photos = con.execute("SELECT COUNT(*) c FROM students WHERE photo!=''").fetchone()["c"]
    teachers_total = con.execute("SELECT COUNT(*) c FROM teachers").fetchone()["c"]
    con.close()
    return page(render_template_string(DASH,students=students,total=total,teachers_total=teachers_total,departments=departments,photos=photos,q=q,session_user=session.get("user", "")),"Dashboard - JOY UNIVERSITY")

def form_data():
    return {k:request.form.get(k,"").strip() for k in ["name","prn","department","course","year","batch","phone","email","blood_group","dob","hostel","address","photo"]}

@app.route("/add",methods=["GET","POST"])
@login_required
def add_student():
    if request.method=="POST":
        d=form_data()
        if not d["name"] or not d["prn"]:
            return page(render_template_string(FORM,student=d,error="Name and PRN are required."),"Add Student")
        con=db()
        try:
            con.execute("""INSERT INTO students(name,prn,department,course,year,batch,phone,email,blood_group,dob,hostel,address,photo,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(*[d[k] for k in ["name","prn","department","course","year","batch","phone","email","blood_group","dob","hostel","address","photo"]],datetime.now().isoformat()))
            con.commit()
        except sqlite3.IntegrityError:
            con.close()
            return page(render_template_string(FORM,student=d,error="PRN already exists."),"Add Student")
        con.close()
        return redirect(url_for("home"))
    return page(render_template_string(FORM,student=None,error=""),"Add Student")

@app.route("/edit/<int:sid>",methods=["GET","POST"])
@login_required
def edit_student(sid):
    con=db(); old=con.execute("SELECT * FROM students WHERE id=?",(sid,)).fetchone(); con.close()
    if not old:return redirect(url_for("home"))
    if request.method=="POST":
        d=form_data()
        if not d["name"] or not d["prn"]:
            return page(render_template_string(FORM,student=d,error="Name and PRN are required."),"Edit Student")
        con=db()
        try:
            con.execute("""UPDATE students SET name=?,prn=?,department=?,course=?,year=?,batch=?,phone=?,email=?,blood_group=?,dob=?,hostel=?,address=?,photo=? WHERE id=?""",(*[d[k] for k in ["name","prn","department","course","year","batch","phone","email","blood_group","dob","hostel","address","photo"]],sid))
            con.commit()
        except sqlite3.IntegrityError:
            con.close()
            return page(render_template_string(FORM,student=d,error="PRN already belongs to another student."),"Edit Student")
        con.close()
        return redirect(url_for("card",sid=sid))
    return page(render_template_string(FORM,student=old,error=""),"Edit Student")

@app.route("/delete/<int:sid>")
@login_required
def delete_student(sid):
    con=db();con.execute("DELETE FROM students WHERE id=?",(sid,));con.commit();con.close()
    return redirect(url_for("home"))

@app.route("/card/<int:sid>")
@login_required
def card(sid):
    con=db(); student=con.execute("SELECT * FROM students WHERE id=?",(sid,)).fetchone();con.close()
    if not student:return redirect(url_for("home"))
    return page(render_template_string(CARD,student=student),"Student ID Card")

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")))
