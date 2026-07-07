/* Fieldstop — offline multi-system camera field guide */
(function(){
"use strict";
var SYS = window.FIELDSTOP_SYSTEMS || [];
var $  = function(s,r){return (r||document).querySelector(s);};
var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};

var D, featById, scenById, featByName, curGroup;

function norm(s){return (s||"").toLowerCase().replace(/[^a-z0-9\s/+]/g," ").replace(/\s+/g," ").trim();}
function tokens(s){return norm(s).split(" ").filter(Boolean);}
function keyName(n){return norm(n).replace(/\s*\/.*$/,"").replace(/setting$/,"").trim();}
function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}

/* Fuji GFX menu-item -> feature id aliases (per-system maps can be added later) */
var MENU_FEATURE_ALIAS = {
  "image size":"image_size","image quality":"image_size","raw recording":"image_size",
  "select jpeg heif":"image_size","film simulation":"film_simulation","monochromatic color":"monochromatic_color",
  "grain effect":"grain_effect","color chrome effect":"color_chrome","color chrome fx blue":"color_chrome",
  "smooth skin effect":"smooth_skin","dynamic range":"dynamic_range","d range priority":"drange_priority",
  "white balance":"white_balance","tone curve":"tone_curve","clarity":"clarity","high iso nr":"high_iso_nr",
  "long exposure nr":"long_exposure_nr","edit save custom":"edit_custom","face eye detection":"face_eye",
  "subject detection":"subject_detection","af c custom settings":"afc_custom","pre af":"pre_af",
  "af illuminator":"af_illuminator","mf assist":"mf_assist","focus check":"focus_check",
  "release focus priority":"release_focus_priority","touch screen mode":"touch_screen",
  "self timer":"self_timer","interval timer shooting":"interval_timer","ae bkt":"ae_bkt",
  "focus bkt":"focus_bkt","photometry":"photometry","shutter type":"shutter_type",
  "flicker reduction":"flicker_reduction","flickerless s s":"flicker_reduction","is mode":"is_mode",
  "35mm format mode":"format35","flash function":"flash_function","commander":"commander_setting",
  "ch":"commander_setting","red eye removal":"red_eye","electronic level":"electronic_level",
  "framing guideline":"framing_guideline","natural live view":"natural_live_view",
  "preview exp wb in manual mode":"preview_exp_wb","evf brightness":"disp_brightness","lcd brightness":"disp_brightness",
  "function fn":"fn_setting","edit save quick menu":"quick_menu","performance":"power_management",
  "auto power off":"power_management"
};
function featForMenuItem(name){
  var k=keyName(name);
  if(MENU_FEATURE_ALIAS[k]) return MENU_FEATURE_ALIAS[k];
  if(featByName[k]) return featByName[k];
  return null;
}

function indexSystem(){
  featById={}; D.features.forEach(function(f){featById[f.id]=f;});
  scenById={}; D.scenarios.forEach(function(s){scenById[s.id]=s;});
  featByName={}; D.features.forEach(function(f){featByName[keyName(f.name)]=f.id;});
  curGroup=D.menu[0].key;
}

/* ---------------- Advisor matching ---------------- */
function expand(qtokens){
  var set={}; qtokens.forEach(function(t){set[t]=1;});
  Object.keys(D.synonyms).forEach(function(key){
    var kt=tokens(key), syns=D.synonyms[key];
    var hitKey = kt.every(function(w){return set[w];}) || qtokens.indexOf(key)>-1;
    var hitSyn = syns.some(function(s){ return tokens(s).every(function(w){return set[w];}); });
    if(hitKey){ syns.forEach(function(s){ tokens(s).forEach(function(w){set[w]=1;}); }); }
    if(hitSyn){ kt.forEach(function(w){set[w]=1;}); }
  });
  return Object.keys(set);
}
function scoreScenario(sc, qset){
  var score=0, tset={};
  sc.tags.forEach(function(t){ tokens(t).forEach(function(w){tset[w]=(tset[w]||0)+1;}); tset[norm(t)]=(tset[norm(t)]||0)+1; });
  sc.tags.forEach(function(t){ if(qset.indexOf(norm(t))>-1 && norm(t).indexOf(" ")>-1) score+=4; });
  qset.forEach(function(w){ if(tset[w]) score+=2; });
  tokens(sc.title).forEach(function(w){ if(qset.indexOf(w)>-1 && w.length>3) score+=1.5; });
  tokens(sc.summary).forEach(function(w){ if(qset.indexOf(w)>-1 && w.length>4) score+=0.5; });
  return score;
}
function advise(query){
  var q=tokens(query); if(!q.length) return [];
  var qset=expand(q);
  return D.scenarios.map(function(s){return {s:s,score:scoreScenario(s,qset)};})
    .filter(function(x){return x.score>0;})
    .sort(function(a,b){return b.score-a.score;});
}

/* ---------------- Renderers ---------------- */
function scenarioCard(sc){
  var h='<div class="card"><div class="card-head"><h2>'+esc(sc.title)+'</h2><p>'+esc(sc.summary)+'</p></div><div class="readout">';
  sc.settings.forEach(function(r){
    h+='<div class="rrow"><div class="c">'+esc(r.c)+'</div><div class="vwrap"><div class="v">'+esc(r.v)+'</div><div class="why">'+esc(r.why)+'</div></div></div>';
  });
  h+='</div>';
  if(sc.steps&&sc.steps.length){
    h+='<div class="block-label">On the camera</div><ol class="steps">';
    sc.steps.forEach(function(st){h+='<li>'+esc(st)+'</li>';});
    h+='</ol>';
  }
  if(sc.caution){h+='<div class="caution"><b>Watch</b><div>'+esc(sc.caution)+'</div></div>';}
  if(sc.related&&sc.related.length){
    h+='<div class="block-label">Learn these features</div><div class="related">';
    sc.related.forEach(function(fid){ if(featById[fid]) h+='<button class="rtag" data-feat="'+fid+'">'+esc(featById[fid].name)+'</button>'; });
    h+='</div>';
  }
  return h+'</div>';
}
function renderAsk(query, ranked){
  var box=$('#askResult');
  if(!query){ box.innerHTML=''; return; }
  if(!ranked.length){
    box.innerHTML='<div class="empty"><b>No match yet</b>Try naming the subject or the problem \u2014 e.g. "milky way over mountains", "silky waterfall", "focus stack a foreground", "star trails", or "aurora".</div>';
    return;
  }
  var best=ranked[0].s;
  var h='<div class="match-note">Best setup for your shot</div>'+scenarioCard(best);
  if(ranked.length>1){
    h+='<div class="more-matches"><div class="lbl">Also relevant</div><div class="chips">';
    ranked.slice(1,5).forEach(function(x){ h+='<button class="chip amber" data-scen="'+x.s.id+'">'+esc(x.s.title)+'</button>'; });
    h+='</div></div>';
  }
  box.innerHTML=h;
  box.scrollIntoView({behavior:'smooth',block:'nearest'});
}
function openScenario(id){
  var sc=scenById[id]; if(!sc) return;
  setView('ask');
  $('#askInput').value=sc.title;
  renderAsk(sc.title,[{s:sc,score:99}].concat(advise(sc.tags.slice(0,4).join(" ")).filter(function(x){return x.s.id!==id;}).slice(0,4)));
}
function openFeature(id){
  var f=featById[id]; if(!f) return;
  var h='<div class="grab"></div><div class="fm">'+esc(f.path)+'</div><h2>'+esc(f.name)+'</h2>';
  h+='<div class="sect">What it does</div><div class="body">'+esc(f.what)+'</div>';
  h+='<div class="sect">How to set it</div><div class="body">'+esc(f.how)+'</div>';
  if(f.page){ h+='<div class="pageref">Owner\u2019s Manual \u2014 <b>p.'+f.page+'</b></div>'; }
  showSheet(h);
}
function openMenuItem(d){
  var loc = d.group + ' \u203a ' + d.cat;
  var h='<div class="grab"></div><div class="fm">'+esc(loc)+'</div><h2>'+esc(d.name)+'</h2>';
  h+='<div class="sect">On the camera</div><div class="body">Find it under <b>'+esc(d.cat)+'</b> \u2192 '+esc(d.name)+'.</div>';
  h+='<div class="sect">Plain-language explanation</div><div class="body" style="color:var(--muted)">Not written up for this item yet \u2014 the manual page below has the full description. (Items with a green dot in the list have an in-app explanation.)</div>';
  if(d.page && d.page!=='0'){ h+='<div class="pageref">Owner\u2019s Manual \u2014 <b>p.'+esc(d.page)+'</b></div>'; }
  showSheet(h);
}
function renderRecipes(){
  var h=''; D.recipes.forEach(function(r){
    h+='<button class="recipe" data-scen="'+r.scenario+'"><div class="g">'+esc(r.genre)+'</div><div class="l">'+esc(r.line)+'</div><div class="arw">Open setup \u203a</div></button>';
  });
  $('#recipeGrid').innerHTML=h;
}
function renderSeg(){
  var h=''; D.menu.forEach(function(g){ h+='<button class="seg'+(g.key===curGroup?' on':'')+'" data-group="'+g.key+'">'+esc(g.key)+'</button>'; });
  $('#menuSeg').innerHTML=h;
}
function renderMenu(filter){
  filter=norm(filter||''); var host=$('#menuList'); var h='';
  var groups = filter ? D.menu : D.menu.filter(function(g){return g.key===curGroup;});
  var any=false;
  groups.forEach(function(g){
    g.categories.forEach(function(cat){
      var items=cat.items.filter(function(it){ return !filter || norm(it.name).indexOf(filter)>-1 || norm(cat.name).indexOf(filter)>-1; });
      if(!items.length) return; any=true;
      h+='<div class="cat'+(filter?' open':'')+'"><button class="cat-h"><span class="nm">'+esc(cat.name)+(filter?' \u00b7 '+esc(g.key):'')+'</span><span class="ct">'+items.length+'</span><svg class="cv" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l6 6-6 6"/></svg></button><div class="cat-body">';
      items.forEach(function(it){
        var fid=featForMenuItem(it.name);
        h+='<button class="mi'+(fid?' has':'')+'" '+(fid?('data-feat="'+fid+'" '):'')+'data-name="'+esc(it.name)+'" data-cat="'+esc(cat.name)+'" data-group="'+esc(g.key)+'" data-page="'+it.page+'">'+(fid?'<span class="exp"></span>':'<span class="gap"></span>')+'<span class="nm">'+esc(it.name)+'</span><span class="pg">p.'+it.page+'</span></button>';
      });
      h+='</div></div>';
    });
  });
  host.innerHTML = any ? h : '<div class="empty"><b>Nothing found</b>No menu item matches \u201c'+esc(filter)+'\u201d.</div>';
}
var learnTab='features';
function renderLearn(filter){
  filter=norm(filter||''); var host=$('#learnList'); var h='';
  if(learnTab==='features'){
    var list=D.features.filter(function(f){ return !filter || norm(f.name).indexOf(filter)>-1 || norm(f.what).indexOf(filter)>-1; })
      .sort(function(a,b){return a.name<b.name?-1:1;});
    if(!list.length){ host.innerHTML='<div class="empty"><b>No feature found</b>Try another word.</div>'; return; }
    list.forEach(function(f){
      h+='<button class="frow" data-feat="'+f.id+'"><div class="fn">'+esc(f.name)+'</div><div class="fm">'+esc(f.path)+(f.page?' \u00b7 p.'+f.page:'')+'</div><div class="fw">'+esc(f.what)+'</div></button>';
    });
  } else if(learnTab==='film'){
    D.filmSims.filter(function(s){ return !filter || norm(s.name+' '+s.best+' '+s.desc).indexOf(filter)>-1; }).forEach(function(s){
      h+='<div class="sim"><div class="sn">'+esc(s.name)+' <span class="sb">'+esc(s.best)+'</span></div><div class="sd">'+esc(s.desc)+'</div></div>';
    });
  } else {
    var fw=D.firmware;
    h+='<div class="fw-card"><h3>Firmware '+esc(fw.current)+' <span class="tagpill note">current</span></h3><p>'+esc(fw.verified)+' Released '+esc(fw.released)+'. '+esc(fw.note)+'</p>';
    h+='<div class="sect" style="font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);margin:16px 0 6px">Check your version</div><ol class="fw-steps">';
    fw.how_to_check.forEach(function(s){h+='<li>'+esc(s)+'</li>';}); h+='</ol></div>';
    fw.changes.forEach(function(c){ h+='<div class="fw-card"><h3>'+esc(c.title)+' <span class="tagpill '+c.kind+'">'+c.kind+'</span></h3><p>'+esc(c.body)+'</p></div>'; });
  }
  host.innerHTML=h;
}

/* ---------------- Sheet ---------------- */
function showSheet(html){ $('#sheet').innerHTML=html; $('#sheet').classList.add('show'); $('#scrim').classList.add('show'); }
function closeSheet(){ $('#sheet').classList.remove('show'); $('#scrim').classList.remove('show'); }

/* ---------------- System switching ---------------- */
function persist(id){ try{ localStorage.setItem('fieldstop.system', id); }catch(e){} }
function restore(){ try{ return localStorage.getItem('fieldstop.system'); }catch(e){ return null; } }
function updateHeader(){
  $('#sysModel').textContent = D.model;
  $('#sysChev').style.display = SYS.length>1 ? '' : 'none';
  $('#fwChip').innerHTML = '<span class="dot"></span>FW '+esc(D.firmware.current);
}
function renderAll(){ renderRecipes(); renderSeg(); renderMenu(''); renderLearn(''); }
function setSystem(id){
  D = SYS.filter(function(s){return s.id===id;})[0] || SYS[0];
  indexSystem(); persist(D.id); updateHeader(); renderAll();
  $('#askInput').value=''; $('#askResult').innerHTML=''; $('#menuSearch').value=''; $('#learnSearch').value='';
  setView('ask');
}
function openSystemPicker(){
  if(SYS.length<2) return;
  var h='<div class="grab"></div><div class="sect" style="margin-top:2px">Camera system</div>';
  SYS.forEach(function(s){
    var on = s.id===D.id;
    h+='<button class="sysrow'+(on?' on':'')+'" data-sys="'+s.id+'"><div><div class="sm">'+esc(s.brand)+'</div><div class="sl">'+esc(s.model)+'</div></div>'+(on?'<span class="tick">\u2713</span>':'<span class="tick" style="color:var(--green)">\u203a</span>')+'</button>';
  });
  h+='<div class="body" style="margin-top:14px;color:var(--faint);font-size:12.5px">More systems can be dropped in as data modules \u2014 one install covers them all.</div>';
  showSheet(h);
}

/* ---------------- View routing ---------------- */
function setView(name){
  $$('.view').forEach(function(v){v.classList.toggle('active',v.id==='view-'+name);});
  $$('.tab').forEach(function(t){t.classList.toggle('on',t.dataset.view===name);});
  window.scrollTo({top:0,behavior:'auto'});
}

/* ---------------- Init ---------------- */
function init(){
  if(!SYS.length){ document.body.innerHTML='<p style="color:#ccc;font-family:monospace;padding:40px">No camera data module loaded.</p>'; return; }
  var vm=document.querySelector('meta[name="fieldstop-version"]');
  var av=$('#appVer'); if(av && vm){ av.innerHTML='ƒieldstop <b>v'+vm.content+'</b>'; }
  var start = restore();
  D = SYS.filter(function(s){return s.id===start;})[0] || SYS[0];
  indexSystem(); updateHeader(); renderAll();

  $$('.tab').forEach(function(t){ t.addEventListener('click',function(){setView(t.dataset.view);}); });

  function runAsk(){ renderAsk($('#askInput').value, advise($('#askInput').value)); }
  $('#askGo').addEventListener('click',runAsk);
  $('#askInput').addEventListener('keydown',function(e){ if(e.key==='Enter'){e.preventDefault();runAsk();this.blur();} });
  $$('.chip[data-q]').forEach(function(c){ c.addEventListener('click',function(){ $('#askInput').value=c.dataset.q; runAsk(); }); });

  $('#sysSwitch').addEventListener('click',openSystemPicker);
  $('#fwChip').addEventListener('click',function(){ setView('learn'); learnTab='firmware'; syncSubtabs(); renderLearn($('#learnSearch').value); });

  $('#menuSeg').addEventListener('click',function(e){ var b=e.target.closest('.seg'); if(!b)return; curGroup=b.dataset.group; renderSeg(); $('#menuSearch').value=''; renderMenu(''); });
  $('#menuSearch').addEventListener('input',function(){ renderMenu(this.value); });
  $('#menuList').addEventListener('click',function(e){
    var mi=e.target.closest('.mi'); if(mi){ if(mi.dataset.feat){ openFeature(mi.dataset.feat); } else { openMenuItem(mi.dataset); } return; }
    var ch=e.target.closest('.cat-h'); if(ch){ ch.parentNode.classList.toggle('open'); }
  });

  function syncSubtabs(){ $$('.subtab').forEach(function(t){t.classList.toggle('on',t.dataset.learn===learnTab);}); }
  $$('.subtab').forEach(function(t){ t.addEventListener('click',function(){ learnTab=t.dataset.learn; syncSubtabs(); renderLearn($('#learnSearch').value); }); });
  $('#learnSearch').addEventListener('input',function(){ renderLearn(this.value); });

  document.addEventListener('click',function(e){
    var sysb=e.target.closest('[data-sys]'); if(sysb){ setSystem(sysb.dataset.sys); closeSheet(); return; }
    var s=e.target.closest('[data-scen]'); if(s){ openScenario(s.dataset.scen); return; }
    var fr=e.target.closest('.frow[data-feat]'); if(fr){ openFeature(fr.dataset.feat); return; }
    var f=e.target.closest('[data-feat]'); if(f && !e.target.closest('.mi')){ openFeature(f.dataset.feat); return; }
  });
  $('#scrim').addEventListener('click',closeSheet);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape')closeSheet(); });

  setView('ask');
}
document.addEventListener('DOMContentLoaded',init);

if('serviceWorker' in navigator){
  window.addEventListener('load',function(){ navigator.serviceWorker.register('./fieldstop-sw.js').catch(function(){}); });
}
})();
