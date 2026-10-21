// ---------- A · +40 kg (cogieron → pelo) ----------
const A0=T.cogieron-.12, A1=T.camcut1+.16;
defocus(A0,A1); scene('#sA',A0,A1);
IN('#sAcard',A0+.05,{y:80,s:.94,d:.5});
const kg={v:0};
tl.fromTo(kg,{v:0},{v:40,duration:.9,ease:'power2.out',...IR,onUpdate:()=>{document.getElementById('kgNum').textContent='+'+Math.round(kg.v);}},T.n40-.05);
tl.fromTo('#kgFill',{scaleX:0},{scaleX:1,duration:.9,ease:'power2.out',...IR},T.n40-.05);
tl.fromTo('#needle',{rotation:-60,svgOrigin:'60 58'},{rotation:55,svgOrigin:'60 58',duration:.9,ease:'back.out(2)',...IR},T.n40-.05);

// ---------- chips: sin deporte / sin cuidarte ----------
IN('#cDep',T.deporte-.05,{y:24}); tl.fromTo('#sDep',{'--strike':0},{'--strike':1,duration:.35,ease:'power2.out',...IR},T.deporte+.35);
IN('#cCui',T.cuidarte-.05,{y:24}); tl.fromTo('#sCui',{'--strike':0},{'--strike':1,duration:.35,ease:'power2.out',...IR},T.cuidarte+.35);
OUT(['#cDep','#cCui'],T.ylo-.05);

// ---------- B · ni para ti / la empresa / nada ----------
// split B: speaker on top, the listener's nod below; the two lines dock as chips on the speaker panel
IN('#cTi',T.nitu-.05,{y:24}); IN('#cEm',T.niemp-.05,{y:24});
OUT(['#cTi','#cEm'],T.ninada-.2);
const B0=T.ninada-.12, B1=T.camcut2+.2;
defocus(B0,B1,.36,.45); scene('#sB',B0,B1);
IN('#r1',B0,{y:40,d:.34}); IN('#r2',B0+.06,{y:40,d:.34}); IN('#r3',T.ninada,{y:50,s:.9});
tl.to('#r3',{scale:1.04,duration:.18,yoyo:true,repeat:1,ease:'sine.inOut'},T.ninada+.45);

// ---------- C · deporte de riesgo ----------
const C0=T.deporte2-.1, C1=T.situ;
defocus(C0,C1); scene('#sC',C0,C1);
tl.fromTo('#warnTri',{strokeDashoffset:1300},{strokeDashoffset:0,duration:.6,ease:'power2.out',...IR},C0+.05);
tl.fromTo('#warnMark',{opacity:0,scale:.5,svgOrigin:'250 250'},{opacity:1,scale:1,svgOrigin:'250 250',duration:.35,ease:'back.out(2.5)',...IR},C0+.45);
IN('#cL1',C0+.1,{y:40}); IN('#cL2',T.riesgo-.05,{y:30,s:.85,d:.36});
tl.to('#warn',{scale:1.05,duration:.22,yoyo:true,repeat:1,ease:'sine.inOut',transformOrigin:'50% 60%'},T.riesgo+.1);

// ---------- D · maratón: split-screen panel slides up (reference split reveal) ----------
const D0=T.maraton-.12, D1=T.lomas;
tl.fromTo('#panel',{yPercent:100},{yPercent:0,duration:.5,ease:'power3.out',...IR},D0);
tl.to('#panel',{yPercent:100,duration:.42,ease:'power3.in'},D1-.3);
tl.set('#panel',{yPercent:100},0);
const rp=document.getElementById('routeP'),RL=rp.getTotalLength(),runner=document.getElementById('runner'),run={p:0};
rp.style.strokeDasharray=RL;rp.style.strokeDashoffset=RL;
const place=()=>{const pt=rp.getPointAtLength(run.p*RL);runner.setAttribute('cx',pt.x);runner.setAttribute('cy',pt.y);rp.style.strokeDashoffset=RL*(1-run.p);document.getElementById('kmN').textContent=(run.p*42.195).toFixed(1).replace('.',',');};
place();
tl.fromTo(run,{p:0},{p:.34,duration:T.lomas-D0-.5,ease:'power1.out',...IR,onUpdate:place},D0+.3);
tl.to('#runner',{y:5,duration:.12,yoyo:true,repeat:1},T.entrenado+.1);
IN('#noTrain',T.entrenado-.05,{y:20,d:.34});

// ---------- lesión ----------
IN('#cLes',T.lesiones-.05,{y:20});
[[-10,.05],[9,.1],[-6,.15],[0,.2]].forEach(k=>tl.to('#cLes',{x:k[0],duration:.05},T.lesiones+.25+k[1]));
OUT('#cLes',T.esigual-.32);

// ---------- E · maratón sin entrenar = emprender ----------
const E0=T.esigual-.08, E1=T.noteP;
defocus(E0,E1,.34,.4); scene('#sE',E0,E1);
tl.fromTo('#sE',{scale:1.18},{scale:1,duration:.5,ease:'power3.out',...IR},E0);  // zoom-through entry
IN('#eq1',E0+.04,{y:30});
tl.fromTo('#eqS',{opacity:0,scale:.4},{opacity:1,scale:1,duration:.35,ease:'back.out(2.4)',...IR},T.esigual+.9);
tl.fromTo('#eq2',{opacity:0,y:60,scale:.9,filter:'blur(10px)'},{opacity:1,y:0,scale:1,filter:'blur(0px)',duration:.42,ease:'power4.out',...IR},T.emprender2-.06);

// ---------- battery: tirar y tirar y tirar ----------
IN('#bat',T.puedes-.1,{y:24});
const bat={v:100};
const setBat=()=>{document.getElementById('batPct').textContent=Math.round(bat.v)+'%';document.getElementById('batFill').style.transform='scaleX('+(bat.v/100)+')';document.getElementById('batFill').style.background=bat.v>45?'#5CD41C':bat.v>20?'#D54B4D':'#D31C1F';};
setBat();
[[T.tirar1,70],[T.tirar2,40],[T.tirar3,15],[T.consec+.2,4]].forEach((k,i,arr)=>{
  const from=i?arr[i-1][1]:100;
  tl.fromTo(bat,{v:from},{v:k[1],duration:.3,ease:'power2.out',...IR,onUpdate:setBat},k[0]);
});
tl.to('#batFill',{opacity:.25,duration:.12,yoyo:true,repeat:5,ease:'none'},T.consec+.55);

// ---------- climax: ¡petarás! ----------
const P=T.petaras;
flash(P);
tl.to('#bat',{scale:1.25,opacity:0,filter:'blur(12px)',duration:.25,ease:'power2.out'},P);
tl.fromTo('#pet',{opacity:0,scale:1.7},{opacity:1,scale:1,duration:.26,ease:'power4.out',...IR},P);
shake(P);

// no end card: the climax slab holds to the last frame (CFG.vidEnd)
