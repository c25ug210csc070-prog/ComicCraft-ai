function showLoading(){
  const button=document.getElementById('submitBtn');
  const loading=document.getElementById('loading');
  if(button){button.disabled=true;button.textContent='Generating...';}
  if(loading){loading.hidden=false;}
}
