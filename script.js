(function(){
  var burger=document.getElementById('burger'),menu=document.getElementById('menu'),scrim=document.getElementById('scrim');
  function setMenu(open){
    menu.classList.toggle('open',open);scrim.classList.toggle('on',open);
    burger.setAttribute('aria-expanded',open);burger.setAttribute('aria-label',open?'Close menu':'Open menu');
    if(open){menu.removeAttribute('inert')}else{menu.setAttribute('inert','')}
  }
  burger.addEventListener('click',function(){setMenu(burger.getAttribute('aria-expanded')!=='true')});
  scrim.addEventListener('click',function(){setMenu(false)});
  menu.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&menu.classList.contains('open')){setMenu(false);burger.focus()}});
  window.matchMedia('(min-width:900px)').addEventListener('change',function(m){if(m.matches)setMenu(false)});

  var els=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
    els.forEach(function(el){io.observe(el)});
  }else{els.forEach(function(el){el.classList.add('in')})}

  /* Paste the Square payment link between the quotes below */
  var SQUARE_LINK="";
  var pb=document.getElementById('payBtn');
  if(pb){ if(SQUARE_LINK){pb.href=SQUARE_LINK}else{pb.removeAttribute('target')} }
  var eb=document.getElementById('etBtn');
  if(eb){
    var box=document.getElementById('etBox'),em=document.getElementById('etEmail'),pm=document.getElementById('payMsg');
    /* e-Transfer address, kept in pieces so simple scrapers do not find it */
    var user='payments',host='toiletcalls.example';
    eb.addEventListener('click',function(){
      var open=eb.getAttribute('aria-expanded')==='true';
      if(!open){em.textContent=user+'@'+host}
      box.hidden=open;eb.setAttribute('aria-expanded',!open);
    });
    document.getElementById('etCopy').addEventListener('click',function(){
      var addr=user+'@'+host;
      try{navigator.clipboard.writeText(addr).then(function(){pm.textContent='Email copied.'},function(){pm.textContent='Please copy the email above.'})}
      catch(e){pm.textContent='Please copy the email above.'}
    });
  }
  var yr=document.getElementById('yr');if(yr)yr.textContent=new Date().getFullYear();
  var qf=document.getElementById('quote');if(qf)qf.addEventListener('submit',function(e){
    e.preventDefault();
    var f=e.target,m=document.getElementById('formMsg');
    if(!f.name.value.trim()||!f.phone.value.trim()){m.textContent='Please add your name and phone number.';return}
    m.textContent='Thanks. This demo form is not connected yet, so nothing was sent.';
  });
})();