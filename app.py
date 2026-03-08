from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Dict, List, Optional
import json

app = FastAPI(title="Couple Games")

HTML = r"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Couple Games 💕</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Color+Emoji&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root{--emoji-font:'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji','Noto Emoji',sans-serif;--rose:#e8637a;--rose-deep:#c04469;--blush:#f2a4b5;--cream:#fdf6f0;--dark:#2c1a22;--muted:#7a5060;--gold:#c9956b;--glass:rgba(255,248,245,.82);--border:rgba(232,99,122,.16);--shadow:0 20px 60px rgba(44,26,34,.14);--ok:#2bb673}
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:"Be Vietnam Pro",'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji','Noto Emoji',sans-serif;background:var(--cream);color:var(--dark);min-height:100vh;overflow-x:hidden}
    body::before{content:"";position:fixed;inset:0;background:radial-gradient(ellipse 80% 60% at 10% 0%,rgba(242,164,181,.30) 0%,transparent 55%),radial-gradient(ellipse 60% 50% at 90% 100%,rgba(201,149,107,.18) 0%,transparent 50%),radial-gradient(ellipse 50% 70% at 50% 50%,rgba(253,246,240,1) 0%,rgba(248,234,230,1) 100%);z-index:0;pointer-events:none}
    .petals-wrap,.sparkle-layer,.toast-layer{position:fixed;inset:0;pointer-events:none;z-index:2;overflow:hidden}
    .petal{position:absolute;top:-40px;border-radius:50% 0 50% 0;background:rgba(232,99,122,.18);animation:fall linear infinite}
    @keyframes fall{0%{transform:translateY(0) rotate(0deg);opacity:.85}100%{transform:translateY(110vh) rotate(540deg);opacity:0}}
    .stone-fly{position:fixed;font-size:20px;font-family:'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji',sans-serif;pointer-events:none;z-index:9999;animation:flyArc .55s cubic-bezier(.25,.46,.45,.94) forwards}
    @keyframes flyArc{0%{transform:translate(0,0) scale(.7);opacity:1}50%{transform:translate(calc(var(--tx)*.5),calc(var(--ty)*.5 - 30px)) scale(1.1);opacity:1}100%{transform:translate(var(--tx),var(--ty)) scale(.8);opacity:0}}
    .stone-suck{position:fixed;font-size:20px;font-family:'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji',sans-serif;pointer-events:none;z-index:9999;animation:suckIn .6s ease-in forwards}
    @keyframes suckIn{0%{transform:translate(0,0) scale(1);opacity:1}100%{transform:translate(var(--tx),var(--ty)) scale(.2);opacity:0}}
    .pit.flash{animation:pitFlash .5s ease}
    @keyframes pitFlash{0%,100%{}40%{box-shadow:0 0 0 8px rgba(232,99,122,.3)}}
    .pit.capture-glow{animation:captureGlow .7s ease}
    @keyframes captureGlow{0%,100%{}40%{box-shadow:0 0 0 10px rgba(255,183,71,.35);background:rgba(255,247,220,.98)}}
    .win-heart{position:fixed;bottom:-20px;font-size:26px;font-family:'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji','Noto Emoji',sans-serif;pointer-events:none;z-index:9999;animation:heartRise 3s linear forwards}
    @keyframes heartRise{0%{transform:translateY(0) translateX(0) scale(.8) rotate(0deg);opacity:0}10%{opacity:1}100%{transform:translateY(-110vh) translateX(var(--hx)) scale(1.2) rotate(20deg);opacity:0}}
    .toast{position:absolute;left:50%;bottom:24px;transform:translateX(-50%);padding:12px 18px;border-radius:14px;background:rgba(44,26,34,.9);color:white;font-size:14px;font-weight:600;box-shadow:0 10px 28px rgba(0,0,0,.18);animation:toastInOut 2.5s ease forwards;white-space:nowrap;max-width:calc(100vw - 24px);overflow:hidden;text-overflow:ellipsis}
    .toast.warn{background:linear-gradient(135deg,#c05a1a,#e8913a);animation:toastInOut 3.2s ease forwards}
    @keyframes toastInOut{0%{opacity:0;transform:translateX(-50%) translateY(16px)}12%,80%{opacity:1;transform:translateX(-50%) translateY(0)}100%{opacity:0;transform:translateX(-50%) translateY(10px)}}
    .warn-banner{display:none;position:absolute;top:16px;left:50%;transform:translateX(-50%);z-index:30;background:linear-gradient(135deg,#c05a1a,#e8913a);color:white;border-radius:18px;padding:14px 20px;text-align:center;box-shadow:0 12px 32px rgba(200,80,20,.28);min-width:240px;max-width:calc(100% - 32px)}
    .warn-banner.show{display:block}
    .warn-banner h4{font-family:"Playfair Display",serif;font-size:17px;margin-bottom:4px}
    .warn-banner p{font-size:13px;opacity:.92}
    .snitch-banner{display:none;position:fixed;bottom:32px;right:24px;z-index:9998;min-width:220px;max-width:300px;background:linear-gradient(135deg,#7b3fa0,#c060e0);color:white;border-radius:20px;padding:14px 18px 14px 16px;box-shadow:0 14px 36px rgba(120,40,180,.32);animation:snitchIn .4s cubic-bezier(.34,1.56,.64,1) forwards}
    .snitch-banner.show{display:flex;align-items:flex-start;gap:11px}
    @keyframes snitchIn{from{opacity:0;transform:translateX(40px) scale(.9)}to{opacity:1;transform:translateX(0) scale(1)}}
    .snitch-icon{font-size:28px;line-height:1;flex-shrink:0}
    .snitch-body{flex:1}
    .snitch-title{font-family:"Playfair Display",serif;font-size:14px;font-weight:700;margin-bottom:3px}
    .snitch-msg{font-size:12.5px;opacity:.92;line-height:1.45}
    .snitch-close{position:absolute;top:9px;right:12px;font-size:16px;cursor:pointer;opacity:.7;background:none;border:none;color:white}
    .spark{position:absolute;width:10px;height:10px;border-radius:999px;background:rgba(232,99,122,.3);animation:sparkUp .9s ease-out forwards}
    @keyframes sparkUp{0%{transform:translate(0,0) scale(.6);opacity:0}20%{opacity:1}100%{transform:translate(var(--tx),var(--ty)) scale(1.3);opacity:0}}
    .app{position:relative;z-index:1;max-width:1320px;margin:0 auto;padding:24px 20px 40px;display:grid;grid-template-columns:330px 1fr;gap:20px}
    .header{grid-column:1/-1;text-align:center;padding:30px 20px 18px}
    .header-eyebrow{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--rose);margin-bottom:8px}
    .header h1{font-family:"Playfair Display",serif;font-size:clamp(28px,4vw,48px);line-height:1.1;font-weight:700}
    .header h1 span{color:var(--rose);font-style:italic}
    .header-divider{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:14px}
    .header-divider::before,.header-divider::after{content:"";width:80px;height:1px;background:linear-gradient(90deg,transparent,var(--blush))}
    .header-divider::after{transform:scaleX(-1)}
    .panel,.board-wrap{background:var(--glass);border:1px solid var(--border);border-radius:28px;backdrop-filter:blur(24px);box-shadow:var(--shadow)}
    .panel{padding:22px;display:flex;flex-direction:column;gap:14px;height:fit-content;position:sticky;top:18px}
    .panel-section-title{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--rose);font-weight:700}
    .field{display:flex;flex-direction:column;gap:5px}
    .field label{font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
    .field input{background:rgba(255,255,255,.88);border:1.5px solid rgba(232,99,122,.22);border-radius:14px;padding:12px 16px;font-size:15px;font-family:inherit;color:var(--dark);outline:none;transition:.2s}
    .field input:focus{border-color:var(--rose);box-shadow:0 0 0 4px rgba(232,99,122,.10)}
    .btn{width:100%;padding:13px 18px;border:none;border-radius:16px;font-family:inherit;font-size:14px;font-weight:700;cursor:pointer;transition:transform .15s,box-shadow .15s;letter-spacing:.03em}
    .btn:hover{transform:translateY(-2px)}
    .btn-primary{background:linear-gradient(135deg,var(--rose),var(--rose-deep));color:white;box-shadow:0 4px 16px rgba(232,99,122,.32)}
    .btn-ghost{background:rgba(255,255,255,.72);color:var(--rose);border:1.5px solid rgba(232,99,122,.28)}
    .divider{height:1px;background:linear-gradient(90deg,transparent,rgba(232,99,122,.2),transparent)}
    .chat-wrap{background:rgba(255,255,255,.56);border:1px solid var(--border);border-radius:18px;overflow:hidden;display:flex;flex-direction:column}
    .chat-header{padding:10px 14px;border-bottom:1px solid rgba(232,99,122,.1);font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--rose)}
    .chat-log{max-height:200px;overflow-y:auto;padding:12px 12px 6px;display:flex;flex-direction:column;gap:10px}
    .chat-log::-webkit-scrollbar{width:4px}
    .chat-log::-webkit-scrollbar-thumb{background:var(--blush);border-radius:4px}
    .msg-row{display:flex;flex-direction:column;gap:2px;animation:msgIn .25s ease}
    .msg-row.mine{align-items:flex-end}.msg-row.theirs{align-items:flex-start}.msg-row.center{align-items:center}
    @keyframes msgIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
    .msg-sender{font-size:10.5px;font-weight:700;color:var(--muted);padding:0 4px}
    .msg-row.mine .msg-sender{color:var(--rose-deep)}
    .msg{padding:9px 13px;border-radius:18px;font-size:13.5px;line-height:1.5;max-width:88%;word-break:break-word}
    .msg-row.mine .msg{background:white;color:var(--dark);border:1.5px solid rgba(232,99,122,.22);border-bottom-right-radius:5px;box-shadow:0 2px 8px rgba(44,26,34,.06)}
    .msg-row.theirs .msg{background:linear-gradient(135deg,var(--rose),var(--rose-deep));color:white;border-bottom-left-radius:5px;box-shadow:0 3px 10px rgba(232,99,122,.22)}
    .msg-row.center .msg{background:rgba(232,99,122,.08);color:var(--rose);font-style:italic;border-radius:10px;text-align:center;font-size:12px;padding:6px 12px;max-width:100%}
    .chat-input-row{display:flex;align-items:flex-end;gap:8px;padding:10px 12px;border-top:1px solid rgba(232,99,122,.1);background:rgba(255,255,255,.6)}
    .chat-input-wrap{flex:1;background:rgba(255,255,255,.95);border:1.5px solid rgba(232,99,122,.22);border-radius:20px;padding:9px 14px;display:flex;align-items:center;transition:.2s}
    .chat-input-wrap:focus-within{border-color:var(--rose);box-shadow:0 0 0 3px rgba(232,99,122,.10)}
    .chat-input-wrap input{flex:1;background:none;border:none;outline:none;font-size:13.5px;font-family:inherit;color:var(--dark)}
    .btn-send{background:linear-gradient(135deg,var(--rose),var(--rose-deep));color:white;border:none;border-radius:50%;width:38px;height:38px;font-size:16px;cursor:pointer;transition:.15s;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(232,99,122,.3)}
    .btn-send:hover{transform:scale(1.08)}
    /* LOBBY */
    .lobby-inner{display:flex;flex-direction:column;gap:20px;padding:28px}
    .lobby-title{font-family:"Playfair Display",serif;font-size:24px;font-style:italic;text-align:center}
    .lobby-sub{font-size:13px;color:var(--muted);text-align:center;line-height:1.6;margin-top:4px}
    .game-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
    .game-card{background:rgba(255,255,255,.82);border:2px solid rgba(232,99,122,.18);border-radius:22px;padding:22px 14px 18px;display:flex;flex-direction:column;align-items:center;gap:10px;cursor:pointer;transition:transform .18s,border-color .18s,box-shadow .18s;position:relative;text-align:center;user-select:none}
    .game-card:hover{transform:translateY(-5px);border-color:var(--rose);box-shadow:0 14px 36px rgba(232,99,122,.20)}
    .game-card.selected{border-color:var(--rose);background:rgba(232,99,122,.07);box-shadow:0 0 0 4px rgba(232,99,122,.14)}
    .game-card.disabled-card{opacity:.4;cursor:not-allowed;pointer-events:none}
    .game-card-icon{font-size:40px;line-height:1;font-family:'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji',sans-serif}
    .game-card-name{font-family:"Playfair Display",serif;font-size:16px;font-weight:700}
    .game-card-desc{font-size:12px;color:var(--muted);line-height:1.5}
    .game-card-badge{position:absolute;top:10px;right:10px;background:linear-gradient(135deg,var(--rose),var(--rose-deep));color:white;border-radius:999px;padding:3px 9px;font-size:10px;font-weight:700}
    .waiting-block{background:rgba(232,99,122,.06);border:1.5px dashed rgba(232,99,122,.3);border-radius:18px;padding:20px;text-align:center}
    .waiting-emoji{font-size:32px;display:block;margin-bottom:8px;font-family:'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji',sans-serif;animation:bob 1.4s ease-in-out infinite}
    @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
    .waiting-text{font-size:14px;color:var(--muted);line-height:1.6}
    .waiting-text strong{color:var(--rose)}
    .lobby-cta{width:100%;padding:14px;border:none;border-radius:16px;font-family:inherit;font-size:15px;font-weight:700;cursor:pointer;background:linear-gradient(135deg,var(--rose),var(--rose-deep));color:white;box-shadow:0 4px 16px rgba(232,99,122,.32);transition:transform .15s,opacity .15s}
    .lobby-cta:hover{transform:translateY(-2px)}
    .lobby-cta:disabled{opacity:.45;cursor:not-allowed;transform:none}
    .ready-row{display:flex;gap:10px;align-items:center;justify-content:center}
    .ready-pill{display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.75);border:1.5px solid rgba(232,99,122,.2);border-radius:999px;padding:7px 14px;font-size:13px;font-weight:700;color:var(--muted)}
    .ready-pill.ok{border-color:var(--ok);color:var(--ok);background:rgba(43,182,115,.08)}
    .ready-pill .dot{width:8px;height:8px;border-radius:50%;background:rgba(232,99,122,.3)}
    .ready-pill.ok .dot{background:var(--ok)}
    /* OAQ */
    .board-wrap { padding: 24px; display: flex; flex-direction: column; gap: 16px; position: relative; overflow: hidden; }
    .score-area { display: flex; align-items: flex-start; gap: 10px; }
    .score-card-float {
      background: rgba(255,255,255,.92); border: 1px solid rgba(232,99,122,.16);
      border-radius: 20px; padding: 12px 16px; box-shadow: 0 4px 18px rgba(232,99,122,.10);
      display: flex; flex-direction: column; gap: 8px; min-width: 220px;
      backdrop-filter: blur(12px); align-self: flex-start;
    }
    .score-love-note {
      background: linear-gradient(160deg, rgba(232,99,122,.08), rgba(242,164,181,.14));
      border: 1px solid rgba(232,99,122,.18); border-radius: 20px;
      padding: 14px 18px; display: flex; flex-direction: column;
      align-items: flex-start; justify-content: space-between; gap: 10px;
      flex: 1; cursor: pointer; align-self: stretch;
      transition: transform .15s, box-shadow .15s;
      box-shadow: 0 4px 14px rgba(232,99,122,.08);
    }
    .score-love-note:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(232,99,122,.16); }
    .score-love-note:active { transform: scale(.96); }
    .score-love-note-header { display: flex; align-items: center; justify-content: space-between; width: 100%; }
    .score-love-note-emoji { font-size: 26px; line-height: 1; transition: transform .2s; }
    .score-love-note:hover .score-love-note-emoji { transform: scale(1.2) rotate(10deg); }
    .score-love-note-text {
      font-size: 13px; line-height: 1.6; color: var(--rose-deep);
      font-style: italic; font-weight: 500; display: block;
      word-break: normal; overflow-wrap: break-word;
      white-space: pre-line; width: 100%; text-align: left;
    }
    .score-love-note.refreshing .score-love-note-emoji,
    .score-love-note.refreshing .score-love-note-text { animation: loveRefresh .3s ease; }
    .score-love-btn {
      background: rgba(255,255,255,.8); border: 1.5px solid rgba(232,99,122,.22);
      border-radius: 50%; width: 38px; height: 38px; flex-shrink: 0;
      font-size: 18px; cursor: pointer; transition: transform .2s, box-shadow .15s;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 2px 6px rgba(232,99,122,.10); align-self: center;
    }
    .score-love-btn:hover { transform: rotate(20deg) scale(1.18); box-shadow: 0 4px 12px rgba(232,99,122,.2); }
    .score-love-btn:active { transform: scale(.88); }
    .score-love-btn.spin { animation: btnSpin .35s cubic-bezier(.34,1.5,.64,1); }
    @keyframes btnSpin { 0%{transform:rotate(0) scale(1)} 50%{transform:rotate(180deg) scale(1.2)} 100%{transform:rotate(360deg) scale(1)} }
    .score-players { display: flex; align-items: center; gap: 0; }
    .score-side { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 3px; transition: transform .2s; }
    .score-side.winning { transform: translateY(-2px); }
    .score-avatar { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: white; margin-bottom: 2px; }
    .score-avatar.p1 { background: linear-gradient(135deg, var(--rose), var(--rose-deep)); }
    .score-avatar.p2 { background: linear-gradient(135deg, var(--gold), #a06030); }
    .score-pname { font-size: 10px; font-weight: 700; color: var(--muted); letter-spacing: .05em; max-width: 72px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-align: center; }
    .score-num-big { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; color: var(--dark); line-height: 1; transition: color .25s, transform .25s; }
    .score-side.winning .score-num-big { color: var(--rose); transform: scale(1.08); }
    .score-divider-vs { display: flex; flex-direction: column; align-items: center; gap: 2px; padding: 0 10px; }
    .score-vs-text { font-family: 'Playfair Display', serif; font-style: italic; font-size: 17px; color: var(--blush); }
    .score-bar-wrap { height: 5px; border-radius: 999px; background: rgba(232,99,122,.12); overflow: hidden; }
    .score-bar-inner { height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--rose), var(--gold)); transition: width .4s ease; }
    .turn-chip { display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,.75); border: 1px solid rgba(232,99,122,.16); border-radius: 999px; padding: 10px 16px; font-size: 13px; color: var(--muted); font-weight: 600; }
    .pulse-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--rose); animation: pulseDot 1.6s infinite; }
    @keyframes pulseDot { 0%{box-shadow:0 0 0 0 rgba(232,99,122,.45)} 70%{box-shadow:0 0 0 10px rgba(232,99,122,0)} 100%{box-shadow:0 0 0 0 rgba(232,99,122,0)} }
    .board-label { display: flex; justify-content: space-between; align-items: center; padding: 0 6px; }
    .player-tag { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 700; color: var(--muted); }
    .player-tag .dot { width: 10px; height: 10px; border-radius: 50%; background: var(--rose); }
    .player-tag.p2 .dot { background: var(--gold); }
    .board-shell { position: relative; background: linear-gradient(180deg,rgba(255,255,255,.32),rgba(255,255,255,.16)); border-radius: 26px; padding: 16px; border: 1px solid rgba(232,99,122,.08); }
    .board-hint { display: none; }
    .board { display: grid; grid-template-columns: 150px repeat(5, 1fr) 150px; grid-template-rows: 1fr 1fr; gap: 12px; }
    .pit {
      border-radius: 22px; background: rgba(255,255,255,.78); border: 1.5px solid rgba(232,99,122,.18);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 6px; padding: 12px 8px; user-select: none;
      transition: background .2s, border-color .2s, transform .15s, box-shadow .2s, opacity .2s;
      min-height: 110px; position: relative; overflow: hidden;
    }
    .pit.small { cursor: pointer; }
    .pit.small:hover { background: rgba(255,255,255,.95); transform: translateY(-3px); box-shadow: 0 10px 28px rgba(232,99,122,.14); }
    #pit-0 { grid-column: 1; grid-row: 1 / 3; min-height: 232px; background: linear-gradient(160deg,rgba(255,255,255,.92),rgba(255,235,240,.82)); border-color: rgba(232,99,122,.28); }
    #pit-6 { grid-column: 7; grid-row: 1 / 3; min-height: 232px; background: linear-gradient(160deg,rgba(255,255,255,.92),rgba(255,235,240,.82)); border-color: rgba(232,99,122,.28); }
    #pit-1 { grid-column: 2; grid-row: 1; }
    #pit-2 { grid-column: 3; grid-row: 1; }
    #pit-3 { grid-column: 4; grid-row: 1; }
    #pit-4 { grid-column: 5; grid-row: 1; }
    #pit-5 { grid-column: 6; grid-row: 1; }
    #pit-11 { grid-column: 2; grid-row: 2; }
    #pit-10 { grid-column: 3; grid-row: 2; }
    #pit-9  { grid-column: 4; grid-row: 2; }
    #pit-8  { grid-column: 5; grid-row: 2; }
    #pit-7  { grid-column: 6; grid-row: 2; }
    .pit::before { content:''; position:absolute; inset:0; background:radial-gradient(circle at 50% 30%,rgba(232,99,122,.05),transparent 70%); pointer-events:none; }
    .pit-label { font-size: 10.5px; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); font-weight:700; opacity:.78; }
    .pit-count { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 700; color: var(--dark); line-height: 1; }
    #pit-0 .pit-count, #pit-6 .pit-count { font-size: 44px; color: var(--rose); }
    .pit-stones { font-size: 16px; line-height: 1.4; text-align: center; letter-spacing: 1px; min-height: 22px; }
    .pit-star { font-size: 14px; opacity:.6; }
    .pit.disabled { opacity: .38; cursor: not-allowed; pointer-events: none; }
    .pit.can { border-color: rgba(232,99,122,.7); background: rgba(255,240,244,.95); box-shadow: 0 0 0 3px rgba(232,99,122,.12); }
    .pit.can .pit-label { color: var(--rose); opacity: 1; }
    .pit.selected { transform: translateY(-4px) scale(1.02); border-color: var(--rose); box-shadow: 0 0 0 4px rgba(232,99,122,.2), 0 14px 28px rgba(232,99,122,.18); }
    .pit.active-cursor { border-color: #f7a800; box-shadow: 0 0 0 4px rgba(247,168,0,.25); background: rgba(255,252,230,.95); }
    .pit.shake { animation: shakePit .4s ease; }
    @keyframes shakePit { 0%,100%{transform:translateX(0)} 20%{transform:translateX(-6px)} 40%{transform:translateX(6px)} 60%{transform:translateX(-4px)} 80%{transform:translateX(4px)} }
    .board-wrap.your-turn .pit.can { animation: glowPulse 1.8s ease-in-out infinite; }
    @keyframes glowPulse { 0%,100%{box-shadow:0 0 0 3px rgba(232,99,122,.12)} 50%{box-shadow:0 0 0 8px rgba(232,99,122,.22),0 10px 24px rgba(232,99,122,.14)} }
    .board.flipped { transform: scale(-1, -1); }
    .board.flipped .pit { transform: scale(-1, -1); }
    .board.flipped .pit.small:hover { transform: scale(-1, -1) translateY(-3px); }
    .board.flipped .pit.selected { transform: scale(-1, -1) translateY(-4px) scale(1.02); }
    .board.flipped .pit.active-cursor { transform: scale(-1, -1); }
    .move-picker { position:absolute; display:none; z-index:20; min-width:160px; background:rgba(255,255,255,.97); border:1.5px solid rgba(232,99,122,.28); border-radius:18px; padding:14px; box-shadow:0 18px 40px rgba(44,26,34,.18); backdrop-filter:blur(12px); }
    .move-picker.show { display:block; animation:pickerIn .18s ease; }
    @keyframes pickerIn { from{opacity:0;transform:translateY(8px) scale(.98)} to{opacity:1;transform:translateY(0) scale(1)} }
    .move-picker-title { font-size:12px; font-weight:700; color:var(--rose); text-align:center; margin-bottom:10px; text-transform:uppercase; letter-spacing:.08em; }
    .move-picker-actions { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
    .move-pick-btn { border:none; border-radius:12px; padding:11px 12px; cursor:pointer; font-family:inherit; font-size:13px; font-weight:700; transition:.15s; background:linear-gradient(135deg,var(--rose),var(--rose-deep)); color:white; }
    .move-pick-btn:hover { transform:translateY(-1px); opacity:.92; }
    .turn-overlay { display:none; position:absolute; inset:0; background:linear-gradient(180deg,rgba(255,255,255,.36),rgba(255,255,255,.18)); backdrop-filter:blur(2px); z-index:3; align-items:center; justify-content:center; border-radius:28px; pointer-events:none; }
    .turn-overlay.show { display:flex; animation:fadeIn .25s ease; }
    @keyframes fadeIn { from{opacity:0} to{opacity:1} }
    .turn-overlay-card { background:rgba(44,26,34,.88); color:white; padding:18px 24px; border-radius:18px; text-align:center; box-shadow:0 16px 40px rgba(0,0,0,.16); }
    .turn-overlay-card h3 { font-family:'Playfair Display',serif; font-size:26px; margin-bottom:4px; font-style:italic; }
    .turn-overlay-card p { font-size:14px; opacity:.88; }
    .timers-row { display: flex; align-items: center; justify-content: space-between; padding: 0 6px; gap: 8px; }
    .timer-block { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,.72); border: 1px solid rgba(232,99,122,.16); border-radius: 999px; padding: 7px 14px; flex: 1; transition: background .3s, border-color .3s, box-shadow .3s; }
    .timer-block.active { background: rgba(232,99,122,.10); border-color: rgba(232,99,122,.45); box-shadow: 0 0 0 3px rgba(232,99,122,.10); }
    .timer-name { font-size: 12px; font-weight: 700; color: var(--muted); flex: 1; }
    .timer-val  { font-family: 'Playfair Display', serif; font-size: 18px; font-weight: 700; color: var(--dark); min-width: 38px; text-align: center; }
    .timer-block.active .timer-val { color: var(--rose); }
    .timer-sep  { font-size: 16px; opacity: .35; flex-shrink: 0; }
    .ready-btn { border: none; border-radius: 999px; padding: 10px 22px; font-family: inherit; font-size: 14px; font-weight: 700; cursor: pointer; background: linear-gradient(135deg, var(--rose), var(--rose-deep)); color: white; box-shadow: 0 4px 14px rgba(232,99,122,.32); transition: transform .15s, box-shadow .15s, opacity .15s; }
    .ready-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(232,99,122,.36); }
    .ready-btn:active { transform: scale(.96); }
    .ready-btn:disabled { opacity: .5; cursor: not-allowed; transform: none; }
    .win-banner { display:none; background:linear-gradient(135deg,var(--rose),var(--rose-deep)); color:white; border-radius:18px; padding:18px; text-align:center; font-family:'Playfair Display',serif; }
    .win-banner.show { display:block; animation:winIn .35s ease; }
    @keyframes winIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
    .win-banner h2 { font-size:26px; font-style:italic; margin-bottom:4px; }
    .win-banner p { font-size:14px; opacity:.9; font-family:'Be Vietnam Pro',sans-serif; }
    .board-topbar { display: flex; align-items: stretch; justify-content: space-between; gap: 14px; }
    .score-love-note { align-self: stretch; }
    .back-btn { border: none; border-radius: 16px; padding: 11px 20px; font-family: inherit; font-size: 13px; font-weight: 700; cursor: pointer; background: rgba(255,255,255,.8); color: var(--rose); border: 1.5px solid rgba(232,99,122,.28); transition: transform .15s; }
    .back-btn:hover { transform: translateY(-2px); }
    @media (max-width:640px) {
      .board-topbar { flex-direction: column; align-items: stretch; gap: 10px; }
      .score-love-note { flex: unset; align-self: auto; width: 100%; padding: 14px 16px; justify-content: center; }
      .score-love-note-text { font-size: 12.5px; }
      .score-card-float { width: 100%; min-width: unset; }
    }
    /* CARO */
    .caro-wrap{padding:24px;display:flex;flex-direction:column;gap:16px}
    .caro-info-row{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
    .caro-scores{display:flex;align-items:center;gap:12px}
    .caro-chip{background:rgba(255,255,255,.8);border:1.5px solid rgba(232,99,122,.2);border-radius:16px;padding:10px 16px;display:flex;flex-direction:column;align-items:center;gap:2px;min-width:80px;transition:border-color .2s,background .2s}
    .caro-chip.active{border-color:var(--rose);background:rgba(232,99,122,.08);box-shadow:0 0 0 3px rgba(232,99,122,.12)}
    .caro-chip-name{font-size:11px;font-weight:700;color:var(--muted)}
    .caro-chip-score{font-family:"Playfair Display",serif;font-size:26px;font-weight:700;color:var(--dark)}
    .caro-chip.active .caro-chip-score{color:var(--rose)}
    .caro-vs{font-family:"Playfair Display",serif;font-style:italic;font-size:18px;color:var(--blush)}
    .caro-turn-chip{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.75);border:1px solid rgba(232,99,122,.16);border-radius:999px;padding:9px 16px;font-size:13px;color:var(--muted);font-weight:600}
    .caro-size-tag{background:linear-gradient(135deg,rgba(232,99,122,.15),rgba(242,164,181,.2));border:1px solid rgba(232,99,122,.22);border-radius:999px;padding:6px 14px;font-size:12px;font-weight:700;color:var(--rose)}
    .caro-board-outer{display:flex;justify-content:center;overflow-x:auto;padding:4px}
    .caro-grid{display:inline-grid;border-radius:18px;overflow:hidden;box-shadow:0 8px 28px rgba(44,26,34,.12);background:rgba(255,255,255,.75);border:1.5px solid rgba(232,99,122,.18)}
    .caro-cell{width:clamp(34px,4.5vw,52px);height:clamp(34px,4.5vw,52px);display:flex;align-items:center;justify-content:center;font-size:clamp(16px,2.5vw,28px);font-family:"Playfair Display",serif;font-weight:700;cursor:pointer;transition:background .15s;border:1px solid rgba(232,99,122,.10);position:relative;user-select:none}
    .caro-cell:hover{background:rgba(232,99,122,.07)}
    .caro-cell.placed{cursor:default}
    .caro-cell.xmark{color:var(--rose)}
    .caro-cell.omark{color:var(--gold);font-size:1.22em;line-height:1}
    .caro-cell.win-cell{background:rgba(232,99,122,.18);animation:caroW .4s ease}
    @keyframes caroW{0%,100%{}50%{background:rgba(232,99,122,.32)}}
    .caro-cell.can-play:hover::after{content:"";position:absolute;inset:4px;border-radius:8px;border:2px dashed rgba(232,99,122,.3)}
    .caro-cell.last-move{box-shadow:inset 0 0 0 2.5px rgba(201,149,107,.9);background:rgba(201,149,107,.10);animation:lastMoveIn .35s cubic-bezier(.34,1.4,.64,1)}
    .caro-cell.last-move.xmark{box-shadow:inset 0 0 0 2.5px rgba(232,99,122,.85);background:rgba(232,99,122,.10)}
    .caro-cell.last-move.omark{box-shadow:inset 0 0 0 2.5px rgba(201,149,107,.85);background:rgba(201,149,107,.12)}
    @keyframes lastMoveIn{0%{transform:scale(1.18);opacity:.5}100%{transform:scale(1);opacity:1}}
    .hidden{display:none!important}
    @media(max-width:1060px){
      .app{grid-template-columns:1fr}.panel{position:relative;top:0}
      .board{grid-template-columns:110px repeat(5,1fr) 110px;gap:8px}
      #pit-0,#pit-6{min-height:190px}.pit{min-height:82px}.pit-count{font-size:26px}
      #pit-0 .pit-count,#pit-6 .pit-count{font-size:32px}.pit-stones{font-size:13px}
      .game-grid{grid-template-columns:1fr 1fr 1fr}
    }
    @media(max-width:640px){
      .app{padding:14px 10px 24px}.board-wrap,.caro-wrap{padding:12px}.board-shell{padding:8px}
      .board{grid-template-columns:62px repeat(5,1fr) 62px;gap:5px}
      #pit-0,#pit-6{min-height:154px}.pit{min-height:66px;padding:5px 3px;border-radius:14px}
      .pit-count{font-size:19px}#pit-0 .pit-count,#pit-6 .pit-count{font-size:23px}
      .pit-stones{font-size:10px}.pit-label{font-size:8.5px}
      .score-area{flex-direction:column}.score-card-float{min-width:unset}
      .game-grid{grid-template-columns:1fr 1fr}
      .caro-cell{width:clamp(26px,8vw,42px);height:clamp(26px,8vw,42px);font-size:clamp(13px,3.5vw,22px)}
    }
  </style>
</head>
<body>
<div class="petals-wrap" id="petals"></div>
<div class="sparkle-layer" id="sparkleLayer"></div>
<div class="toast-layer" id="toastLayer"></div>

<!-- Snitch banner (đối thủ dùng mẹo) -->
<div class="snitch-banner" id="snitchBanner">
  <div class="snitch-icon">😳</div>
  <div class="snitch-body">
    <div class="snitch-title" id="snitchTitle">Ối! Mẹo bị lộ rồi~</div>
    <div class="snitch-msg"  id="snitchMsg">Đối thủ vừa thử dùng mẹo nhưng không được đâu nha 😆</div>
  </div>
  <button class="snitch-close" onclick="hideSnitchBanner()">🌸</button>
</div>

<div class="app">
  <div class="header">
    <div class="header-eyebrow">Trò chơi dành cho hai trái tim</div>
    <h1>Couple <span>Games</span> 💕</h1>
    <div class="header-divider"><div style="font-size:18px;letter-spacing:6px">🌸 💕 🌸</div></div>
  </div>

  <!-- LEFT PANEL -->
  <div class="panel">
    <div class="panel-section-title">Kết nối phòng chơi</div>
    <div class="field"><label>Tên của bạn</label><input id="name" placeholder="Ví dụ: Chéng ✧ T"/></div>
    <div class="field"><label>Mã phòng</label><input id="room" placeholder="Ví dụ: couple"/></div>
    <button class="btn btn-primary" onclick="connectWS()">✦ Vào phòng</button>
    <button class="btn btn-ghost" onclick="randomRoom()">🎲 Tạo mã phòng ngẫu nhiên</button>
    <div class="divider"></div>
    <div class="chat-wrap">
      <div class="chat-header">💌 Nhắn tin yêu thương</div>
      <div class="chat-log" id="chatLog"></div>
      <div class="chat-input-row">
        <div class="chat-input-wrap"><input id="chatInput" placeholder="Nhắn gì đó dễ thương nhé…" onkeydown="if(event.key==='Enter')sendChat()"/></div>
        <button class="btn-send" onclick="sendChat()">➤</button>
      </div>
    </div>
  </div>

  <!-- RIGHT AREA -->
  <div id="rightArea">

    <!-- LOBBY -->
    <div class="board-wrap" id="lobbyWrap">
      <div class="lobby-inner">
        <div>
          <div class="lobby-title">Chọn trò chơi 🎮</div>
          <div class="lobby-sub" id="lobbySub">Kết nối phòng để bắt đầu chọn trò chơi</div>
        </div>
        <div class="game-grid">
          <div class="game-card disabled-card" id="card-oanquan" onclick="selectGame('oanquan')">
            <div class="game-card-badge">Dân gian</div>
            <div class="game-card-icon">🎲</div>
            <div class="game-card-name">Ô Ăn Quan</div>
            <div class="game-card-desc">Rải quân khéo léo<br>Ăn quan là thắng!</div>
          </div>
          <div class="game-card disabled-card" id="card-caro3" onclick="selectGame('caro3')">
            <div class="game-card-badge">Caro</div>
            <div class="game-card-icon">✕</div>
            <div class="game-card-name">Caro ×3</div>
            <div class="game-card-desc">Bàn 3×3<br>3 liên tiếp là thắng</div>
          </div>
          <div class="game-card disabled-card" id="card-caro5" onclick="selectGame('caro5')">
            <div class="game-card-badge">Caro</div>
            <div class="game-card-icon">◯</div>
            <div class="game-card-name">Caro ×5</div>
            <div class="game-card-desc">Bàn 15×15<br>5 liên tiếp là thắng</div>
          </div>
        </div>
        <div id="lobbyAction"></div>
        <div class="ready-row" id="readyRow" style="display:none">
          <div class="ready-pill" id="rp1"><div class="dot"></div><span id="rn1">P1</span></div>
          <div style="font-size:18px;color:var(--blush)">💕</div>
          <div class="ready-pill" id="rp2"><div class="dot"></div><span id="rn2">P2</span></div>
        </div>
      </div>
    </div>

    <!-- O AN QUAN -->
    <div class="board-wrap hidden" id="oaqWrap">
      <div class="turn-overlay" id="turnOverlay">
        <div class="turn-overlay-card">
          <h3>Tới lượt bạn 🌸</h3>
          <p>Chạm vào một ô sáng để đi</p>
        </div>
      </div>
      <div class="warn-banner" id="warnBanner">
        <h4>⚠️ Nước đi không hợp lệ</h4>
        <p id="warnBannerText">Không được ăn quan! Hãy chọn ô khác hoặc đổi hướng rải.</p>
      </div>
      <div class="board-topbar">
        <div class="score-love-note" id="scoreLoveNote">
          <div class="score-love-note-header">
            <span class="score-love-note-emoji" id="scoreLoveEmoji">💕</span>
            <button class="score-love-btn" id="scoreLoveBtn" onclick="refreshScoreLove()">✨</button>
          </div>
          <span class="score-love-note-text" id="scoreLoveText">Chơi vui nha!</span>
        </div>
        <div class="score-card-float">
          <div class="score-players">
            <div class="score-side" id="scoreCard1">
              <div class="score-avatar p1" id="savatar1">P1</div>
              <div class="score-pname" id="sname1">Người chơi 1</div>
              <div class="score-num-big" id="s1">0</div>
            </div>
            <div class="score-divider-vs"><span class="score-vs-text">vs</span></div>
            <div class="score-side" id="scoreCard2">
              <div class="score-avatar p2" id="savatar2">P2</div>
              <div class="score-pname" id="sname2">Người chơi 2</div>
              <div class="score-num-big" id="s2">0</div>
            </div>
          </div>
          <div class="score-bar-wrap">
            <div class="score-bar-inner" id="scoreBar" style="width:50%"></div>
          </div>
        </div>
      </div>
      <div class="board-label">
        <div class="player-tag"><div class="dot"></div><span id="labelP1">Người chơi 1 • hàng dưới</span></div>
        <div style="font-size:13px;color:var(--muted);opacity:.75;font-weight:600;" id="boardLabelCenter">0:00 💕 0:00</div>
        <div class="player-tag p2"><div class="dot"></div><span id="labelP2">Người chơi 2 • hàng trên</span></div>
      </div>
      <div class="timers-row" id="timersRow" style="display:none;">
        <div class="timer-block" id="timerBlock1">
          <span class="timer-name" id="timerName1">Người chơi 1</span>
          <span class="timer-val" id="timerVal1">0:00</span>
        </div>
        <div class="timer-sep">💕</div>
        <div class="timer-block" id="timerBlock2">
          <span class="timer-val" id="timerVal2">0:00</span>
          <span class="timer-name" id="timerName2">Người chơi 2</span>
        </div>
      </div>
      <div class="board-shell">
        <div class="board-hint" id="boardHint">Kết nối phòng để bắt đầu chơi.</div>
        <div class="move-picker" id="movePicker">
          <div class="move-picker-title">Chọn hướng rải</div>
          <div class="move-picker-actions">
            <button class="move-pick-btn" onclick="confirmMove('left')">👈 Trái</button>
            <button class="move-pick-btn" onclick="confirmMove('right')">Phải 👉</button>
          </div>
        </div>
        <div class="board" id="board">
          <div class="pit" id="pit-0"></div>
          <div class="pit small" id="pit-1"  onclick="play(1)"></div>
          <div class="pit small" id="pit-2"  onclick="play(2)"></div>
          <div class="pit small" id="pit-3"  onclick="play(3)"></div>
          <div class="pit small" id="pit-4"  onclick="play(4)"></div>
          <div class="pit small" id="pit-5"  onclick="play(5)"></div>
          <div class="pit" id="pit-6"></div>
          <div class="pit small" id="pit-11" onclick="play(11)"></div>
          <div class="pit small" id="pit-10" onclick="play(10)"></div>
          <div class="pit small" id="pit-9"  onclick="play(9)"></div>
          <div class="pit small" id="pit-8"  onclick="play(8)"></div>
          <div class="pit small" id="pit-7"  onclick="play(7)"></div>
        </div>
      </div>
      <div style="display:flex;justify-content:flex-start;padding:0 6px;gap:10px;align-items:center;flex-wrap:wrap;">
        <div class="turn-chip">
          <span class="pulse-dot"></span>
          <span id="turnChipText">Đang chờ người chơi...</span>
        </div>
        <button class="ready-btn" id="readyBtn" onclick="sendReady()" style="display:none"></button>
        <button class="back-btn" onclick="requestBackLobby()">🏠 Đổi game</button>
      </div>
      <div class="win-banner" id="winBanner">
        <h2 id="winText">😍 Chiến thắng!</h2>
        <p id="winSub">Ván đấu kết thúc rồi 💕</p>
      </div>
    </div>

    <!-- CARO -->
    <div class="board-wrap hidden" id="caroWrap">
      <div class="caro-wrap">
        <div class="caro-info-row">
          <div class="caro-scores">
            <div class="caro-chip" id="cch1"><div class="caro-chip-name" id="ccn1">P1</div><div class="caro-chip-score" id="ccs1">0</div></div>
            <div class="caro-vs">vs</div>
            <div class="caro-chip" id="cch2"><div class="caro-chip-name" id="ccn2">P2</div><div class="caro-chip-score" id="ccs2">0</div></div>
          </div>
          <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
            <div class="caro-size-tag" id="caroSizeTag">Caro ×3</div>
            <div class="caro-turn-chip"><span class="pulse-dot"></span><span id="caroTurnText">Đang chờ...</span></div>
          </div>
        </div>
        <div class="caro-board-outer"><div class="caro-grid" id="caroGrid"></div></div>
        <div class="win-banner hidden" id="caroWinBanner"><h2 id="caroWinTxt">😍 Chiến thắng!</h2><p id="caroWinSub">💕</p></div>
        <div style="display:flex;gap:10px;flex-wrap:wrap">
          <button class="new-game-btn hidden" id="caroNewBtn" onclick="requestNewCaro()">🎮 Ván mới</button>
          <button class="back-btn" onclick="requestBackLobby()">🏠 Đổi game</button>
        </div>
      </div>
    </div>

  </div><!-- /rightArea -->
</div><!-- /app -->

<script>
// ── UTILS ──
function sleep(ms){return new Promise(r=>setTimeout(r,ms))}
function getPitEl(i){return document.getElementById('pit-'+i)}

function showToast(t,w){
  var l=document.getElementById('toastLayer'),d=document.createElement('div');
  d.className='toast'+(w?' warn':'');d.innerText=t;l.appendChild(d);
  setTimeout(()=>d.remove(),w?3300:2600)
}
var _wt=null;
function showWarnBanner(m){
  var b=document.getElementById('warnBanner');
  document.getElementById('warnBannerText').innerHTML=m;
  b.classList.add('show');clearTimeout(_wt);
  _wt=setTimeout(()=>b.classList.remove('show'),3200)
}
function flyStone(a,b,e){
  if(!a||!b)return;e=e||'🌸';
  var r1=a.getBoundingClientRect(),r2=b.getBoundingClientRect();
  var s=document.createElement('div');s.className='stone-fly';s.innerText=e;
  s.style.left=(r1.left+r1.width/2)+'px';s.style.top=(r1.top+r1.height/2)+'px';
  s.style.setProperty('--tx',(r2.left-r1.left)+'px');
  s.style.setProperty('--ty',(r2.top-r1.top)+'px');
  document.body.appendChild(s);
  b.classList.add('flash');
  setTimeout(()=>{s.remove();b.classList.remove('flash')},600)
}
function suckStone(a,b,e){
  if(!a||!b)return;e=e||'💮';
  var r1=a.getBoundingClientRect(),r2=b.getBoundingClientRect();
  var s=document.createElement('div');s.className='stone-suck';s.innerText=e;
  s.style.left=(r1.left+r1.width/2)+'px';s.style.top=(r1.top+r1.height/2)+'px';
  s.style.setProperty('--tx',(r2.left-r1.left)+'px');
  s.style.setProperty('--ty',(r2.top-r1.top)+'px');
  document.body.appendChild(s);
  a.classList.add('capture-glow');
  setTimeout(()=>{s.remove();a.classList.remove('capture-glow')},650)
}
function burst(el,n){
  if(!el)return;n=n||8;
  var rect=el.getBoundingClientRect(),lyr=document.getElementById('sparkleLayer');
  for(var i=0;i<n;i++){
    var s=document.createElement('div');s.className='spark';
    s.style.left=(rect.left+rect.width/2)+'px';
    s.style.top=(rect.top+rect.height/2)+'px';
    s.style.setProperty('--tx',((Math.random()-.5)*100)+'px');
    s.style.setProperty('--ty',(-20-Math.random()*80)+'px');
    lyr.appendChild(s);setTimeout(()=>s.remove(),950)
  }
}
function winHearts(n){
  var hs=['💕','💖','🌸','💝','🌷','💘','😍','💞','💗','🍒','🌺','💌'];
  for(var i=0;i<(n||24);i++){
    var h=document.createElement('div');h.className='win-heart';
    h.innerText=hs[i%hs.length];
    h.style.left=(Math.random()*100)+'vw';
    h.style.animationDelay=(Math.random()*.8)+'s';
    h.style.setProperty('--hx',((Math.random()-.5)*120)+'px');
    document.body.appendChild(h);setTimeout(()=>h.remove(),3200)
  }
}
function randomRoom(){
  document.getElementById('room').value='couple-'+Math.random().toString(36).slice(2,8);
  showToast('Đã tạo mã phòng 🎲')
}
function show(id){document.getElementById(id).classList.remove('hidden')}
function hide(id){document.getElementById(id).classList.add('hidden')}

// ── SNITCH (từ code 1) ──
var SNITCH_MSGS=[
  ['😳 Ối, mẹo bị lộ!',   '{{name}} vừa thử ăn quan ngay lần đầu nhưng không qua được đâu nha 😏'],
  ['🌷 Mẹo hay đó~',       '{{name}} định dùng chiêu bí mật nhưng trọng tài thổi còi rồi 💕'],
  ['😘 Bắt được rồi nè!',  '{{name}} vừa thử mẹo ăn quan nhưng bị phát hiện ngay tắp lự 💝'],
  ['🙈 Thấy hết rồi nhé~', '{{name}} muốn dùng mẹo nhưng luật không cho phép đó 💗'],
  ['🍒 Dấu vết còn in!',   '{{name}} vừa bị từ chối một nước đi "đặc biệt" hihi 🌷'],
  ['😍 Trời ơi ngộ quá!',  '{{name}} nghĩ qua được sao? Luật chơi ngăn lại rồi 😍'],
  ['💌 Chơi đẹp nào bé~',  '{{name}} vừa thử dùng mẹo ăn quan nhưng không được đâu nha 💞'],
];
function showSnitchBanner(name){
  var pair=SNITCH_MSGS[Math.floor(Math.random()*SNITCH_MSGS.length)];
  var title=pair[0],msg=pair[1].replace('{{name}}',name||'Đối thủ');
  document.getElementById('snitchTitle').innerText=title;
  document.getElementById('snitchMsg').innerText=msg;
  var b=document.getElementById('snitchBanner');
  b.classList.remove('show');void b.offsetWidth;b.classList.add('show');
  return {title:title,msg:msg}
}
function hideSnitchBanner(){document.getElementById('snitchBanner').classList.remove('show')}

// ── STATE ──
var ws=null, myRole=null, latestOAQ=null, latestCaro=null;
var latestState=null;
var lastMyTurn=false, isAnimating=false;
var isAnim=false;
var selectedPit=null, selectedPitEl=null;
var selPit=null, selPitEl=null;
var currentGame=null;

// ── WS ──
function connectWS(){
  var room=document.getElementById('room').value.trim();
  var name=document.getElementById('name').value.trim()||'Người chơi';
  localStorage.setItem('cg_name',name);localStorage.setItem('cg_room',room);
  if(!room){showToast('Chưa nhập mã phòng.');return}
  if(ws)ws.close();
  var proto=location.protocol==='https:'?'wss':'ws';
  ws=new WebSocket(proto+'://'+location.host+'/ws/'+encodeURIComponent(room)+'?name='+encodeURIComponent(name));
  ws.onopen=()=>showToast('Đã vào phòng '+room+' 💕');
  ws.onmessage=e=>{
    var d=JSON.parse(e.data);
    if(d.type==='welcome'){
      myRole=d.role;
      showToast(d.role==='p1'?'Bạn là chủ phòng 🌸':'Bạn là P2 🌺')
    }
    if(d.type==='lobby')      handleLobby(d);
    if(d.type==='state')      handleOAQ(d.state, d.steps||[], d.mover||null);
    if(d.type==='caro_state') handleCaro(d);
    if(d.type==='chat')       addChat(d.text,'msg',d.name);
    if(d.type==='system')     addChat(d.text,'sys');
    // FIX: xử lý opponent_cheat giống code 1
    if(d.type==='opponent_cheat'){
      var snitch=showSnitchBanner(d.name||'Đối thủ');
      if(ws&&ws.readyState===1)
        ws.send(JSON.stringify({action:'chat',text:snitch.title+' — '+snitch.msg}))
    }
    if(d.type==='invalid_move'){
      var msg=d.text||'Nước đi không hợp lệ.';
      showWarnBanner('⚠️ '+msg+'<br><small>Chọn ô khác hoặc đổi hướng nhé 🌸</small>');
      showToast('⚠️ '+msg,true);
      if(d.pit!=null){
        var pe=getPitEl(d.pit);
        if(pe){pe.classList.remove('shake');void pe.offsetWidth;pe.classList.add('shake');setTimeout(()=>pe.classList.remove('shake'),450)}
      }
      if(latestOAQ)applyOAQStateUI(latestOAQ,latestOAQ.turn===myRole&&!latestOAQ.winner)
    }
  };
  ws.onclose=()=>{showToast('Đã ngắt kết nối');myRole=null;currentGame=null}
}

// ── LOBBY ──
function gameLabel(g){return g==='oanquan'?'Ô Ăn Quan':g==='caro3'?'Caro ×3':'Caro ×5'}

function handleLobby(d){
  currentGame=null;
  show('lobbyWrap');hide('oaqWrap');hide('caroWrap');
  latestOAQ=null;latestCaro=null;
  var ls=d.lobby_state||{};
  var p1n=(ls.players&&ls.players.p1)||'Người chơi 1';
  var p2n=(ls.players&&ls.players.p2)||'Người chơi 2';
  var isHost=(myRole==='p1');
  ['oanquan','caro3','caro5'].forEach(g=>{
    var c=document.getElementById('card-'+g);
    c.classList.toggle('disabled-card',!isHost);
    c.classList.toggle('selected',d.selected_game===g)
  });
  var sub=document.getElementById('lobbySub');
  if(!myRole)           sub.innerText='Kết nối phòng để bắt đầu';
  else if(isHost)       sub.innerText='Bạn là chủ phòng — chọn trò chơi bên dưới 💕';
  else                  sub.innerText='Đang chờ chủ phòng chọn trò chơi...';
  var aa=document.getElementById('lobbyAction');
  if(isHost&&d.selected_game){
    aa.innerHTML='<button class="lobby-cta" onclick="sendConfirm()">✦ Bắt đầu '+gameLabel(d.selected_game)+'!</button>';
  } else if(!isHost&&d.selected_game){
    aa.innerHTML='<div class="waiting-block"><span class="waiting-emoji">🎮</span><div class="waiting-text"><strong>'+p1n+'</strong> đã chọn <strong>'+gameLabel(d.selected_game)+'</strong><br>Đang chờ bắt đầu...</div></div>';
  } else if(!isHost&&myRole){
    aa.innerHTML='<div class="waiting-block"><span class="waiting-emoji">⌛</span><div class="waiting-text">Đang chờ <strong>'+p1n+'</strong> chọn trò chơi...</div></div>';
  } else {aa.innerHTML=''}
  if(myRole){
    document.getElementById('readyRow').style.display='flex';
    document.getElementById('rn1').innerText=p1n;
    document.getElementById('rn2').innerText=p2n;
    document.getElementById('rp1').className='ready-pill'+(ls.p1_online?' ok':'');
    document.getElementById('rp2').className='ready-pill'+(ls.p2_online?' ok':'');
  }
}
function selectGame(g){
  if(myRole!=='p1'){showToast('Chỉ chủ phòng mới chọn.');return}
  if(!ws||ws.readyState!==1){showToast('Chưa kết nối.');return}
  ws.send(JSON.stringify({action:'select_game',game:g}))
}
function sendConfirm(){if(ws&&ws.readyState===1)ws.send(JSON.stringify({action:'confirm_game'}))}
function requestBackLobby(){if(ws&&ws.readyState===1)ws.send(JSON.stringify({action:'back_lobby'}))}

// ── Ô ĂN QUAN ──
function getPitEl(idx){return document.getElementById('pit-'+idx);}

function flyStone(fromEl,toEl,emoji){
  if(!fromEl||!toEl)return; emoji=emoji||'🌸';
  var r1=fromEl.getBoundingClientRect(),r2=toEl.getBoundingClientRect();
  var s=document.createElement('div');
  s.className='stone-fly';s.innerText=emoji;
  s.style.left=(r1.left+r1.width/2)+'px';s.style.top=(r1.top+r1.height/2)+'px';
  s.style.setProperty('--tx',(r2.left-r1.left)+'px');
  s.style.setProperty('--ty',(r2.top-r1.top)+'px');
  document.body.appendChild(s);
  toEl.classList.add('flash');
  setTimeout(function(){s.remove();toEl.classList.remove('flash');},600);
}
function suckStone(fromEl,toEl,emoji){
  if(!fromEl||!toEl)return; emoji=emoji||'💮';
  var r1=fromEl.getBoundingClientRect(),r2=toEl.getBoundingClientRect();
  var s=document.createElement('div');
  s.className='stone-suck';s.innerText=emoji;
  s.style.left=(r1.left+r1.width/2)+'px';s.style.top=(r1.top+r1.height/2)+'px';
  s.style.setProperty('--tx',(r2.left-r1.left)+'px');
  s.style.setProperty('--ty',(r2.top-r1.top)+'px');
  document.body.appendChild(s);
  fromEl.classList.add('capture-glow');
  setTimeout(function(){s.remove();fromEl.classList.remove('capture-glow');},650);
}

function stoneText(n){
  if(n<=0)return'·';
  var arr=['🌸','🍒','💗','🌷'],s='',max=Math.min(n,12);
  for(var i=0;i<max;i++)s+=arr[i%arr.length];
  if(n>12)s+=' +'+(n-12);return s;
}
function renderPit(id,value,label,isQuan){
  var el=getPitEl(id);if(!el)return;
  if(isQuan){
    el.innerHTML='<div class="pit-label">'+label+'</div>'+
                 '<div class="pit-count">'+value+'</div>'+
                 '<div class="pit-stones">'+stoneText(value)+'</div>'+
                 '<div class="pit-star">👑 Quan</div>';
  }else{
    el.innerHTML='<div class="pit-label">'+label+'</div>'+
                 '<div class="pit-count">'+value+'</div>'+
                 '<div class="pit-stones">'+stoneText(value)+'</div>';
  }
}
function renderBoard(board){
  var isP2View=myRole==='p2';
  var lq0=isP2View?'Ô 12 • Quan phải':'Ô 12 • Quan trái';
  var lq6=isP2View?'Ô 6 • Quan trái' :'Ô 6 • Quan phải';
  renderPit(0, board[0], lq0,true);
  renderPit(1, board[1], 'Ô 11');
  renderPit(2, board[2], 'Ô 10');
  renderPit(3, board[3], 'Ô 9');
  renderPit(4, board[4], 'Ô 8');
  renderPit(5, board[5], 'Ô 7');
  renderPit(6, board[6], lq6,true);
  renderPit(7, board[7], 'Ô 5');
  renderPit(8, board[8], 'Ô 4');
  renderPit(9, board[9], 'Ô 3');
  renderPit(10,board[10],'Ô 2');
  renderPit(11,board[11],'Ô 1');
}

function hideMovePicker(){
  document.getElementById('movePicker').classList.remove('show');
  selectedPit=null;
  if(selectedPitEl){selectedPitEl.classList.remove('selected');selectedPitEl=null;}
}
function showMovePicker(pit,el){
  var picker=document.getElementById('movePicker');
  var shell=document.querySelector('.board-shell');
  var sr=shell.getBoundingClientRect(),er=el.getBoundingClientRect();
  selectedPit=pit;selectedPitEl=el;
  document.querySelectorAll('.pit').forEach(function(x){x.classList.remove('selected');});
  el.classList.add('selected');
  var left=er.left-sr.left+er.width/2-80;
  var top=er.top-sr.top-78;
  if(left<8)left=8;
  if(left>sr.width-168)left=sr.width-168;
  if(top<8)top=er.bottom-sr.top+8;
  picker.style.left=left+'px';picker.style.top=top+'px';
  picker.classList.add('show');
}
function confirmMove(direction){
  if(!ws||ws.readyState!==1){showToast('Chưa kết nối phòng.');hideMovePicker();return;}
  if(selectedPit==null){hideMovePicker();return;}
  var serverDir=direction;
  if(selectedPit!==0&&selectedPit!==6)
    serverDir=(direction==='left')?'right':'left';
  ws.send(JSON.stringify({action:'move',pit:selectedPit,direction:serverDir}));
  pauseTimer();
  hideMovePicker();
}

var isAnimating=false;
async function animateSteps(steps,finalBoard,mover){
  isAnimating=true;
  var scoreTarget=mover==='p1'?document.getElementById('scoreCard1'):document.getElementById('scoreCard2');
  var emojis=['🌸','🌷','💮','💕'],eidx=0;
  for(var i=0;i<steps.length;i++){
    var step=steps[i];
    if(step.type==='place'){
      flyStone(getPitEl(step.from),getPitEl(step.to),emojis[eidx++%emojis.length]);
      renderBoard(step.board);await sleep(320);
    }else if(step.type==='capture'){
      suckStone(getPitEl(step.pit),scoreTarget,'💮');
      renderBoard(step.board);await sleep(380);
    }else if(step.type==='highlight'){
      document.querySelectorAll('.pit').forEach(function(x){x.classList.remove('active-cursor');});
      var hl=getPitEl(step.pit);if(hl)hl.classList.add('active-cursor');
      await sleep(180);
    }
  }
  document.querySelectorAll('.pit').forEach(function(x){x.classList.remove('active-cursor');});
  renderBoard(finalBoard);isAnimating=false;
}

// ── timers ──
var timerSecs={p1:0,p2:0};
var timerInterval=null;
var timerActive=null;
function fmtTime(s){var m=Math.floor(s/60),ss=s%60;return m+':'+(ss<10?'0':'')+ss;}
function updateCenterTimerLabel(){
  var el=document.getElementById('boardLabelCenter');if(!el)return;
  el.innerText=fmtTime(timerSecs.p1)+' 💕 '+fmtTime(timerSecs.p2);
}
function updateTimerDisplay(){
  document.getElementById('timerVal1').innerText=fmtTime(timerSecs.p1);
  document.getElementById('timerVal2').innerText=fmtTime(timerSecs.p2);
  document.getElementById('timerBlock1').classList.toggle('active',timerActive==='p1');
  document.getElementById('timerBlock2').classList.toggle('active',timerActive==='p2');
  updateCenterTimerLabel();
}
function startTimer(role){
  timerActive=role;
  if(timerInterval)clearInterval(timerInterval);
  timerInterval=setInterval(function(){if(timerActive){timerSecs[timerActive]++;updateTimerDisplay();}},1000);
  updateTimerDisplay();
}
function pauseTimer(){
  timerActive=null;
  if(timerInterval){clearInterval(timerInterval);timerInterval=null;}
  updateTimerDisplay();
}
function stopTimers(){
  pauseTimer();
  document.getElementById('timersRow').style.display='none';
}
function initTimers(p1name,p2name){
  timerSecs={p1:0,p2:0};
  document.getElementById('timerName1').innerText=p1name||'Người chơi 1';
  document.getElementById('timerName2').innerText=p2name||'Người chơi 2';
  document.getElementById('timersRow').style.display='none';
  updateTimerDisplay();
}

function myAllowedIndices(){
  if(myRole==='p1')return[7,8,9,10,11];
  if(myRole==='p2')return[1,2,3,4,5];
  return[];
}

function handleOAQ(state, steps, mover){
  currentGame='oanquan';
  show('oaqWrap');hide('lobbyWrap');hide('caroWrap');
  latestState=state; latestOAQ=state;
  var isMyTurn=state.started&&state.turn===myRole&&!state.winner;
  if(steps&&steps.length>0){
    animateSteps(steps,state.board,mover).then(function(){applyOAQStateUI(state,isMyTurn);});
  }else{
    renderBoard(state.board);applyOAQStateUI(state,isMyTurn);
  }
}

function applyOAQStateUI(state,isMyTurn){
  latestState=state;
  var boardEl=document.getElementById('board');
  if(boardEl)boardEl.classList.toggle('flipped',myRole==='p2');
  document.querySelectorAll('.pit.small').forEach(function(el){
    el.classList.remove('can','disabled');
    if(!state.started){el.classList.add('disabled');return;}
    var idx=parseInt(el.id.replace('pit-',''));
    var allowed=myRole==='p1'?[7,8,9,10,11]:myRole==='p2'?[1,2,3,4,5]:[];
    var canPlay=isMyTurn&&allowed.indexOf(idx)!==-1&&state.board[idx]>0;
    el.classList.add(canPlay?'can':'disabled');
  });
  document.getElementById('oaqWrap').classList.toggle('your-turn',isMyTurn&&!!state.started);

  var readyBtn=document.getElementById('readyBtn');
  if(!state.started&&myRole){
    var alreadyReady=state.ready&&state.ready[myRole];
    readyBtn.style.display='inline-flex';
    readyBtn.disabled=alreadyReady;
    if(!alreadyReady){
      readyBtn.innerText=myRole==='p1'?'💝 Bắt đầu':'🌸 Sẵn sàng';
    }else{
      readyBtn.innerText=myRole==='p1'?'😍 Đang chờ sẵn sàng...':'💕 Đang chờ bắt đầu...';
    }
  }else{readyBtn.style.display='none';}

  var tp=(state.players&&state.players[state.turn])||state.turn||'—';
  var chipText;
  if(state.winner){
    chipText='Ván đấu đã kết thúc';
  }else if(!state.started){
    var p1n_=(state.players&&state.players.p1)||'Người chơi 1';
    var p2n_=(state.players&&state.players.p2)||'';
    var p2Display=p2n_||'Người chơi 2';
    var r1=!!(state.ready&&state.ready.p1);
    var r2=!!(state.ready&&state.ready.p2);
    if(!r1&&!r2) chipText=p2n_?'Đợi '+p2n_+' sẵn sàng':'Đang chờ người chơi...';
    else if(r1&&!r2) chipText='Chờ '+p2Display+' sẵn sàng';
    else if(!r1&&r2) chipText='Chờ '+p1n_+' bắt đầu';
    else chipText='Đang bắt đầu...';
  }else{
    chipText=isMyTurn?'Tới lượt bạn • chọn một ô sáng':('Đang chờ '+tp+' đi');
  }
  document.getElementById('turnChipText').innerText=chipText;

  var p1n=(state.players&&state.players.p1)||'Người chơi 1';
  var p2n=(state.players&&state.players.p2)||'Người chơi 2';
  if(myRole==='p2'){
    document.getElementById('labelP1').innerText=p1n+' • hàng trên';
    document.getElementById('labelP2').innerText=p2n+' • hàng dưới (bạn)';
  }else{
    document.getElementById('labelP1').innerText=p1n+' • hàng dưới'+(myRole==='p1'?' (bạn)':'');
    document.getElementById('labelP2').innerText=p2n+' • hàng trên';
  }

  var sc1=state.scores.p1,sc2=state.scores.p2;
  document.getElementById('s1').innerText=sc1;
  document.getElementById('s2').innerText=sc2;
  document.getElementById('scoreCard1').classList.toggle('winning',sc1>sc2);
  document.getElementById('scoreCard2').classList.toggle('winning',sc2>sc1);
  var pn1=(state.players&&state.players.p1)||'P1';
  var pn2=(state.players&&state.players.p2)||'P2';
  document.getElementById('sname1').innerText=pn1;
  document.getElementById('sname2').innerText=pn2;
  document.getElementById('savatar1').innerText=pn1.charAt(0).toUpperCase()||'P';
  document.getElementById('savatar2').innerText=pn2.charAt(0).toUpperCase()||'P';
  var total=sc1+sc2;
  document.getElementById('scoreBar').style.width=(total>0?Math.round(sc1/total*100):50)+'%';

  var overlay=document.getElementById('turnOverlay');
  if(isMyTurn&&!lastMyTurn){
    overlay.classList.add('show');showToast('Tới lượt bạn 🌸');
    setTimeout(function(){overlay.classList.remove('show');},1200);
  }else if(!isMyTurn)overlay.classList.remove('show');
  lastMyTurn=isMyTurn;

  if(state.started&&!state.winner){
    var p1n__=(state.players&&state.players.p1)||'Người chơi 1';
    var p2n__=(state.players&&state.players.p2)||'Người chơi 2';
    if(!window.__timersInited){initTimers(p1n__,p2n__);window.__timersInited=true;}
    startTimer(state.turn);
  }else if(state.winner){stopTimers();}

  var banner=document.getElementById('winBanner');
  if(state.winner){
    banner.classList.add('show');
    if(!window.__winShown){winHearts(28);window.__winShown=true;}
    if(state.winner==='draw'){
      document.getElementById('winText').innerText='💞 Hòa rồi!';
      document.getElementById('winSub').innerText='Hai người xứng đôi thật sự 🌸';
    }else{
      var wname=(state.players&&state.players[state.winner])||state.winner;
      document.getElementById('winText').innerText='😍 '+wname+' chiến thắng!';
      document.getElementById('winSub').innerText='Ván đấu đã kết thúc 💕';
    }
    burst(document.getElementById('winBanner'),22);
  }else{
    banner.classList.remove('show');window.__winShown=false;
    window.__timersInited=window.__timersInited||false;
  }
}

function play(index){
  if(!ws||ws.readyState!==1){showToast('Chưa kết nối phòng.');return;}
  if(!latestState)return;
  if(!latestState.started){showToast('Ván đấu chưa bắt đầu.');return;}
  if(latestState.winner){showToast('Ván này đã kết thúc.');return;}
  if(latestState.turn!==myRole){showToast('Chưa tới lượt của bạn.');return;}
  if(myAllowedIndices().indexOf(index)===-1){showToast('Bạn chỉ bấm ô phía mình.');return;}
  if((latestState.board[index]||0)<=0){showToast('Ô này đang trống.');return;}
  if(isAnimating){showToast('Đang hiển thị nước đi trước...');return;}
  burst(getPitEl(index),6);
  showMovePicker(index,getPitEl(index));
}
function sendReady(){
  if(!ws||ws.readyState!==1)return;
  ws.send(JSON.stringify({action:'ready'}));
  var btn=document.getElementById('readyBtn');
  btn.disabled=true;
  btn.innerText=myRole==='p1'?'😍 Đang chờ sẵn sàng...':'💕 Đang chờ bắt đầu...';
}
document.addEventListener('click',function(e){
  if(!e.target.closest('.pit.small')&&!e.target.closest('#movePicker'))hideMovePicker();
});

// ── CARO ──
function handleCaro(d){
  currentGame=d.state.size===3?'caro3':'caro5';
  show('caroWrap');hide('lobbyWrap');hide('oaqWrap');
  latestCaro=d.state;renderCaroBoard(d.state);applyCaroUI(d.state)
}
function renderCaroBoard(state){
  var grid=document.getElementById('caroGrid'),n=state.size;
  grid.style.gridTemplateColumns='repeat('+n+',1fr)';grid.innerHTML='';
  var isMyTurn=state.started&&state.turn===myRole&&!state.winner;
  var lm=state.last_move;
  for(var r=0;r<n;r++){
    for(var c=0;c<n;c++){
      var cell=document.createElement('div');cell.className='caro-cell';
      var v=state.board[r*n+c];
      if(v==='X'){cell.classList.add('xmark','placed');cell.innerText='✕'}
      else if(v==='O'){cell.classList.add('omark','placed');cell.innerText='◯'}
      else if(isMyTurn){
        cell.classList.add('can-play');
        (function(rr,cc){cell.onclick=()=>playCaroCell(rr,cc)})(r,c)
      }
      if(lm&&lm[0]===r&&lm[1]===c)cell.classList.add('last-move');
      if(state.winning_cells&&state.winning_cells.find(wc=>wc[0]===r&&wc[1]===c))cell.classList.add('win-cell');
      grid.appendChild(cell)
    }
  }
}
function applyCaroUI(state){
  var p1n=(state.players&&state.players.p1)||'P1';
  var p2n=(state.players&&state.players.p2)||'P2';
  document.getElementById('ccn1').innerText=p1n;
  document.getElementById('ccn2').innerText=p2n;
  document.getElementById('ccs1').innerText=(state.scores&&state.scores.p1)||0;
  document.getElementById('ccs2').innerText=(state.scores&&state.scores.p2)||0;
  document.getElementById('cch1').classList.toggle('active',state.turn==='p1'&&!state.winner&&state.started);
  document.getElementById('cch2').classList.toggle('active',state.turn==='p2'&&!state.winner&&state.started);
  document.getElementById('caroSizeTag').innerText='Caro ×'+state.size;
  var isMyTurn=state.started&&state.turn===myRole&&!state.winner;
  var tp=(state.players&&state.players[state.turn])||state.turn||'—';
  var myMark=myRole==='p1'?'✕':'○';
  document.getElementById('caroTurnText').innerText=
    state.winner    ?'Ván kết thúc':
    !state.started  ?'Đang chờ...':
    isMyTurn        ?'Tới lượt bạn ('+myMark+')':
    'Đang chờ '+tp;
  var wb=document.getElementById('caroWinBanner');
  var nb=document.getElementById('caroNewBtn');
  if(state.winner){
    wb.classList.remove('hidden');wb.classList.add('show');nb.classList.remove('hidden');
    if(!window._caroWin){winHearts(24);window._caroWin=true}
    if(state.winner==='draw'){
      document.getElementById('caroWinTxt').innerText='💞 Hòa rồi!';
      document.getElementById('caroWinSub').innerText='Hai người xứng đôi 🌸'
    } else {
      var wn=(state.players&&state.players[state.winner])||state.winner;
      document.getElementById('caroWinTxt').innerText='😍 '+wn+' thắng!';
      document.getElementById('caroWinSub').innerText='Ván kết thúc 💕'
    }
    burst(wb,16)
  } else {wb.classList.add('hidden');wb.classList.remove('show');nb.classList.add('hidden');window._caroWin=false}
  if(isMyTurn&&!lastMyTurn)showToast('Tới lượt bạn 🌸 ('+myMark+')');
  lastMyTurn=isMyTurn
}
function playCaroCell(r,c){
  if(!ws||ws.readyState!==1){showToast('Chưa kết nối.');return}
  if(!latestCaro||latestCaro.winner){showToast('Ván đã kết thúc.');return}
  if(latestCaro.turn!==myRole){showToast('Chưa tới lượt.');return}
  ws.send(JSON.stringify({action:'caro_move',row:r,col:c}))
}
function requestNewCaro(){if(ws&&ws.readyState===1)ws.send(JSON.stringify({action:'caro_new_game'}))}

// ── CHAT ──
function sendChat(){
  var inp=document.getElementById('chatInput'),txt=inp.value.trim();
  if(!txt||!ws||ws.readyState!==1)return;
  ws.send(JSON.stringify({action:'chat',text:txt}));inp.value=''
}
function addChat(text,cls,sender){
  var log=document.getElementById('chatLog');
  var row=document.createElement('div'),bubble=document.createElement('div');
  bubble.className='msg';
  if(cls==='sys'){row.className='msg-row center';bubble.innerText=text}
  else{
    var myName=document.getElementById('name').value.trim()||'Người chơi';
    var isMine=!sender||sender===myName;
    row.className='msg-row '+(isMine?'mine':'theirs');
    if(sender){var ne=document.createElement('div');ne.className='msg-sender';ne.innerText=sender;row.appendChild(ne)}
    bubble.innerText=text
  }
  row.appendChild(bubble);log.appendChild(row);log.scrollTop=log.scrollHeight
}

// ── LOVE NOTES ──
var LOVES=[
  ['💕','Thua hay thắng gì cũng không quan trọng\nbằng được ngồi chơi cùng nhau nha~ 💕'],
  ['🔥','Dù đối thủ có là người yêu\nthì vẫn phải chơi hết mình đó nha hihi 🔥'],
  ['🙈','Nếu bị thua thì cứ nhớ:\nngười thua được quyền đòi một cái ôm nhé! 🤗'],
  ['💌','Bí quyết thắng:\nrải thật khéo, cười thật tươi, và yêu thật nhiều 💖'],
  ['💞','Chơi game với người mình thích\nlà một trong những điều hạnh phúc nhất đời 🥰'],
  ['😈','Đừng có dùng mẹo nha!\nTrừ mẹo là... làm người kia cười để mất tập trung 😏💕'],
  ['🌙','Dù ai thắng ai thua,\ncuối ngày vẫn là của nhau mà~ 💞'],
  ['🎀','Mỗi nước đi là một khoảnh khắc bên nhau.\nRải chậm thôi, đừng vội! 🌸'],
  ['😘','Ván đấu kết thúc thế nào cũng phải\nkết thúc bằng nụ hôn nhé! 😘'],
  ['☀️','Dự báo hôm nay:\n100% có mưa cưng chiều và nắng ngọt ngào ☀️💖'],
  ['💝','Hai người + một bàn cờ + nhiều tiếng cười\n= công thức hoàn hảo cho buổi tối! ✨'],
  ['🏆','Quan trọng không phải ai thắng\nmà là ai được nghe "em/anh chơi hay ghê" trước 😄'],
];
var lastSL=-1,BTN_EM=['💕','💝','🌷','💌','🌸','💖','😍','🍒'],lastBI=-1;
function refreshScoreLove(){
  var i;do{i=Math.floor(Math.random()*LOVES.length)}while(i===lastSL);lastSL=i;
  var bi;do{bi=Math.floor(Math.random()*BTN_EM.length)}while(bi===lastBI);lastBI=bi;
  var n=LOVES[i];
  document.getElementById('scoreLoveEmoji').innerText=n[0];
  document.getElementById('scoreLoveText').innerText=n[1];
  var btn=document.getElementById('scoreLoveBtn');
  btn.innerText=BTN_EM[bi];
  btn.classList.remove('spin');void btn.offsetWidth;btn.classList.add('spin');
  setTimeout(()=>btn.classList.remove('spin'),370)
}
refreshScoreLove();

// ── INIT ──
window.addEventListener('DOMContentLoaded',()=>{
  var n=localStorage.getItem('cg_name'),r=localStorage.getItem('cg_room');
  if(n)document.getElementById('name').value=n;
  if(r)document.getElementById('room').value=r
});
(function(){
  var w=document.getElementById('petals');
  for(var i=0;i<16;i++){
    var el=document.createElement('div');el.className='petal';var sz=10+Math.random()*14;
    el.style.cssText='left:'+Math.random()*100+'%;width:'+sz+'px;height:'+sz+'px;animation-duration:'+(7+Math.random()*10)+'s;animation-delay:'+(-Math.random()*14)+'s;opacity:'+(0.12+Math.random()*.25)+';';
    w.appendChild(el)
  }
})();
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# GAME LOGIC — Ô Ăn Quan
# ─────────────────────────────────────────────────────────────────────────────

CIRCLE = [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]
CIRCLE_POS = [None] * 12
for _pos, _idx in enumerate(CIRCLE):
    CIRCLE_POS[_idx] = _pos


def next_idx(idx: int, direction: str) -> int:
    pos = CIRCLE_POS[idx]
    if direction == "right":
        pos = (pos + 1) % 12
    else:
        pos = (pos - 1) % 12
    return CIRCLE[pos]


def side_indices(player: str) -> List[int]:
    return [7, 8, 9, 10, 11] if player == "p1" else [1, 2, 3, 4, 5]


def create_state() -> dict:
    return {
        "board":           [10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5],
        "turn":            "p1",
        "scores":          {"p1": 0, "p2": 0},
        "winner":          None,
        "message":         "Người chơi 1 đi trước.",
        "players":         {"p1": "", "p2": ""},
        "first_move_done": {"p1": False, "p2": False},
        "ready":           {"p1": False, "p2": False},
        "started":         False,
    }


def can_play(state: dict, player: str, pit: int) -> Optional[str]:
    if state["winner"]:          return "Ván này đã kết thúc."
    if state["turn"] != player:  return "Chưa tới lượt của bạn."
    if pit not in side_indices(player): return "Bạn chỉ được chọn ô ở bên mình."
    if state["board"][pit] <= 0: return "Ô này đang trống."
    return None


def collect_remaining(state: dict):
    b = state["board"]
    state["scores"]["p1"] += sum(b[i] for i in [7, 8, 9, 10, 11]) + b[6]
    state["scores"]["p2"] += sum(b[i] for i in [1, 2, 3, 4, 5])   + b[0]
    for i in range(12): b[i] = 0


def both_quan_eaten(board):  return board[0] == 0 and board[6] == 0
def no_moves_left(board):    return all(board[i] == 0 for i in [1,2,3,4,5,7,8,9,10,11])


def check_end(state: dict) -> bool:
    b = state["board"]
    if both_quan_eaten(b) or no_moves_left(b):
        collect_remaining(state)
        s1, s2 = state["scores"]["p1"], state["scores"]["p2"]
        state["winner"] = "p1" if s1 > s2 else ("p2" if s2 > s1 else "draw")
        return True
    return False


def try_refill(state: dict, player: str) -> bool:
    side, b = side_indices(player), state["board"]
    if any(b[i] > 0 for i in side): return True
    if state["scores"][player] < len(side): return False
    for i in side:
        b[i] = 1
        state["scores"][player] -= 1
    return True


def would_eat_quan(board: List[int], pit: int, direction: str) -> bool:
    b = list(board); stones = b[pit]; b[pit] = 0; cursor = pit
    while True:
        while stones > 0:
            nxt = next_idx(cursor, direction); b[nxt] += 1; stones -= 1; cursor = nxt
        nxt = next_idx(cursor, direction)
        if b[nxt] > 0 and nxt not in (0, 6):
            cursor = nxt; stones = b[cursor]; b[cursor] = 0; continue
        skip = nxt; eat = next_idx(skip, direction)
        while b[skip] == 0 and b[eat] > 0:
            if eat in (0, 6): return True
            b[eat] = 0; cursor = eat
            skip = next_idx(cursor, direction); eat = next_idx(skip, direction)
        break
    return False


def apply_move(state: dict, player: str, pit: int, direction: str):
    err = can_play(state, player, pit)
    if err:
        state["message"] = err
        return [], None

    first_move_done = state.get("first_move_done")
    if not isinstance(first_move_done, dict):
        done = bool(first_move_done)
        first_move_done = {"p1": done, "p2": done}
        state["first_move_done"] = first_move_done

    player_first_done = bool(first_move_done.get(player, False))
    if (not player_first_done) and would_eat_quan(state["board"], pit, direction):
        state["message"] = "Lượt đầu của mỗi người chơi không được ăn quan!"
        return [], pit

    board = state["board"]
    steps: List[dict] = []

    def snap():
        return board[:]

    stones = board[pit]
    board[pit] = 0
    cursor = pit
    captured = 0
    while True:
        while stones > 0:
            nxt = next_idx(cursor, direction)
            board[nxt] += 1
            stones -= 1
            steps.append({"type": "place", "from": cursor, "to": nxt, "board": snap()})
            cursor = nxt

        nxt = next_idx(cursor, direction)
        if board[nxt] > 0 and nxt not in (0, 6):
            cursor = nxt
            stones = board[cursor]
            board[cursor] = 0
            steps.append({"type": "highlight", "pit": cursor, "board": snap()})
            continue

        skip = nxt
        eat = next_idx(skip, direction)
        while board[skip] == 0 and board[eat] > 0:
            captured += board[eat]
            steps.append({"type": "capture", "pit": eat, "board": snap()})
            board[eat] = 0
            steps.append({"type": "capture", "pit": eat, "board": snap()})
            cursor = eat
            skip = next_idx(cursor, direction)
            eat = next_idx(skip, direction)

        if captured:
            state["scores"][player] += captured
        break

    first_move_done[player] = True
    player_name = state["players"].get(player) or player
    dir_text = "trái" if direction == "left" else "phải"
    state["message"] = (
        f"{player_name} rải {dir_text} và ăn {captured} quân."
        if captured
        else f"{player_name} rải {dir_text}."
    )

    if not check_end(state):
        next_player = "p2" if player == "p1" else "p1"
        if not try_refill(state, next_player):
            collect_remaining(state)
            s1, s2 = state["scores"]["p1"], state["scores"]["p2"]
            state["winner"] = "p1" if s1 > s2 else ("p2" if s2 > s1 else "draw")
            np_name = state["players"].get(next_player) or next_player
            state["message"] += f" {np_name} không đủ quân rải lại — ván kết thúc!"
        else:
            if any(board[i] > 0 for i in side_indices(next_player)):
                state["turn"] = next_player
            else:
                if any(board[i] > 0 for i in side_indices(player)):
                    state["message"] += f" {player_name} đi tiếp vì đối phương hết đá."
                else:
                    check_end(state)

    return steps, None

# GAME LOGIC — Caro
# ─────────────────────────────────────────────────────────────────────────────

def create_caro_state(size: int, players: dict, scores: dict = None) -> dict:
    return {
        "size":          size,
        "board":         [""] * size * size,
        "turn":          "p1",
        "players":       players,
        "scores":        scores or {"p1": 0, "p2": 0},
        "winner":        None,
        "winning_cells": [],
        "last_move":     None,
        "started":       True,
    }


def check_caro_win(board, size: int, mark: str):
    win_len = 3 if size == 3 else 5
    dirs    = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(size):
        for c in range(size):
            if board[r * size + c] != mark: continue
            for dr, dc in dirs:
                cells = [(r + i * dr, c + i * dc) for i in range(win_len)]
                if all(0 <= rr < size and 0 <= cc < size and board[rr * size + cc] == mark
                       for rr, cc in cells):
                    return cells
    return []


def apply_caro_move(state: dict, player: str, row: int, col: int):
    if state["winner"]:             return "Ván đã kết thúc."
    if state["turn"] != player:     return "Chưa tới lượt."
    n = state["size"]
    if not (0 <= row < n and 0 <= col < n): return "Ô không hợp lệ."
    if state["board"][row * n + col] != "": return "Ô đã có quân."
    mark = "X" if player == "p1" else "O"
    state["board"][row * n + col] = mark
    state["last_move"] = [row, col]
    win = check_caro_win(state["board"], n, mark)
    if win:
        state["winner"] = player
        state["winning_cells"] = win
        state["scores"][player] = state["scores"].get(player, 0) + 1
    elif all(c != "" for c in state["board"]):
        state["winner"] = "draw"
    else:
        state["turn"] = "p2" if player == "p1" else "p1"
    return None


# ─────────────────────────────────────────────────────────────────────────────
# SERVER
# ─────────────────────────────────────────────────────────────────────────────

class Room:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
        self.names:       Dict[str, str]       = {}
        self.game:         str  = None
        self.selected_game: str = None
        self.oaq_state:   dict  = None
        self.caro_state:  dict  = None

    def lobby_payload(self) -> dict:
        return {
            "type":          "lobby",
            "game":          self.game,
            "selected_game": self.selected_game,
            "lobby_state": {
                "players":   {"p1": self.names.get("p1", ""), "p2": self.names.get("p2", "")},
                "p1_online": "p1" in self.connections,
                "p2_online": "p2" in self.connections,
            },
        }

    async def broadcast(self, payload: dict):
        dead = []
        for role, sock in list(self.connections.items()):
            try:   await sock.send_text(json.dumps(payload))
            except: dead.append(role)
        for r in dead:
            self.connections.pop(r, None); self.names.pop(r, None)

    async def sync_lobby(self):
        for role, sock in list(self.connections.items()):
            payload = self.lobby_payload()
            payload["is_host"] = (role == "p1")
            try:   await sock.send_text(json.dumps(payload))
            except: pass

    async def sync_oaq(self, steps=None, mover: str = None):
        if not self.oaq_state: return
        self.oaq_state["players"]["p1"] = self.names.get("p1", "")
        self.oaq_state["players"]["p2"] = self.names.get("p2", "")
        await self.broadcast({"type": "state", "state": self.oaq_state,
                              "steps": steps or [], "mover": mover})

    async def sync_caro(self):
        if not self.caro_state: return
        self.caro_state["players"]["p1"] = self.names.get("p1", "")
        self.caro_state["players"]["p2"] = self.names.get("p2", "")
        await self.broadcast({"type": "caro_state", "state": self.caro_state})

    def start_game(self):
        if self.selected_game == "oanquan":
            self.game = "oanquan"
            self.oaq_state = create_state()
            self.oaq_state["players"]["p1"] = self.names.get("p1", "")
            self.oaq_state["players"]["p2"] = self.names.get("p2", "")
        elif self.selected_game in ("caro3", "caro5"):
            self.game = self.selected_game
            size    = 3 if self.selected_game == "caro3" else 15
            players = {"p1": self.names.get("p1", ""), "p2": self.names.get("p2", "")}
            self.caro_state = create_caro_state(size, players)

    def reset_to_lobby(self):
        self.game = None; self.selected_game = None
        self.oaq_state = None; self.caro_state = None


rooms: Dict[str, Room] = {}


@app.get("/")
async def home():
    return HTMLResponse(HTML)


@app.websocket("/ws/{room_id}")
async def ws_endpoint(websocket: WebSocket, room_id: str, name: str = "Người chơi"):
    await websocket.accept()
    room = rooms.setdefault(room_id, Room())

    if   "p1" not in room.connections: role = "p1"
    elif "p2" not in room.connections: role = "p2"
    else:
        await websocket.send_text(json.dumps({"type": "system", "text": "Phòng đã đủ 2 người."}))
        await websocket.close(); return

    room.connections[role] = websocket
    room.names[role]       = name

    await websocket.send_text(json.dumps({
        "type":    "welcome",
        "role":    role,
        "message": f"Bạn là {'Người chơi 1' if role == 'p1' else 'Người chơi 2'}.",
    }))
    await room.broadcast({"type": "system", "text": f"{name} đã vào phòng."})

    if   room.game == "oanquan"                        and room.oaq_state:  await room.sync_oaq()
    elif room.game in ("caro3", "caro5")               and room.caro_state: await room.sync_caro()
    else:                                                                    await room.sync_lobby()

    try:
        while True:
            raw    = await websocket.receive_text()
            data   = json.loads(raw)
            action = data.get("action")

            if action == "chat":
                txt = (data.get("text") or "").strip()[:300]
                if txt:
                    await room.broadcast({"type": "chat", "name": room.names.get(role, role), "text": txt})

            elif action == "select_game":
                if role != "p1":
                    await websocket.send_text(json.dumps({"type": "system", "text": "Chỉ chủ phòng mới chọn."}))
                    continue
                g = data.get("game")
                if g in ("oanquan", "caro3", "caro5"):
                    room.selected_game = g; await room.sync_lobby()

            elif action == "confirm_game":
                if role != "p1":
                    await websocket.send_text(json.dumps({"type": "system", "text": "Chỉ chủ phòng."}))
                    continue
                if not room.selected_game:
                    await websocket.send_text(json.dumps({"type": "system", "text": "Chưa chọn game."}))
                    continue
                room.start_game()
                if   room.game == "oanquan": await room.sync_oaq()
                else:                        await room.sync_caro()

            elif action == "back_lobby":
                room.reset_to_lobby(); await room.sync_lobby()
                await room.broadcast({"type": "system", "text": f"{room.names.get(role, role)} quay về sảnh chờ."})

            elif action == "ready":
                if room.game != "oanquan" or not room.oaq_state: continue
                if not room.oaq_state["started"]:
                    room.oaq_state["ready"][role] = True
                    if room.oaq_state["ready"]["p1"] and room.oaq_state["ready"]["p2"]:
                        room.oaq_state["started"] = True
                        room.oaq_state["message"] = "Ván bắt đầu! P1 đi trước."
                    await room.sync_oaq()

            elif action == "move":
                if room.game != "oanquan" or not room.oaq_state: continue
                if not room.oaq_state["started"]:
                    await websocket.send_text(json.dumps({"type": "system", "text": "Chưa bắt đầu!"}))
                    continue
                pit       = int(data.get("pit", -1))
                direction = data.get("direction", "right")
                steps, inv = apply_move(room.oaq_state, role, pit, direction)
                if inv is not None:
                    cheater_name = room.names.get(role, role)
                    await websocket.send_text(json.dumps({
                        "type": "invalid_move",
                        "text": room.oaq_state["message"],
                        "pit":  inv,
                    }))
                    opp = room.connections.get("p2" if role == "p1" else "p1")
                    if opp:
                        try: await opp.send_text(json.dumps({"type": "opponent_cheat", "name": cheater_name}))
                        except: pass
                else:
                    await room.sync_oaq(steps=steps, mover=role)

            elif action == "caro_move":
                if room.game not in ("caro3", "caro5") or not room.caro_state: continue
                row = int(data.get("row", 0)); col = int(data.get("col", 0))
                err = apply_caro_move(room.caro_state, role, row, col)
                if err: await websocket.send_text(json.dumps({"type": "system", "text": err}))
                else:   await room.sync_caro()

            elif action == "caro_new_game":
                if room.game not in ("caro3", "caro5") or not room.caro_state: continue
                size    = room.caro_state["size"]
                scores  = room.caro_state.get("scores", {"p1": 0, "p2": 0})
                players = {"p1": room.names.get("p1", ""), "p2": room.names.get("p2", "")}
                room.caro_state = create_caro_state(size, players, scores)
                await room.sync_caro()
                await room.broadcast({"type": "system", "text": f"{room.names.get(role, role)} bắt đầu ván mới 🎮"})

    except WebSocketDisconnect:
        room.connections.pop(role, None)
        left = room.names.pop(role, role)
        await room.broadcast({"type": "system", "text": f"{left} đã rời phòng."})
        if   room.game == "oanquan"          and room.oaq_state:  await room.sync_oaq()
        elif room.game in ("caro3", "caro5") and room.caro_state: await room.sync_caro()
        else:                                                      await room.sync_lobby()
        if not room.connections: rooms.pop(room_id, None)