const btn=document.querySelector('#btn');
const question=document.querySelector('#question');
btn.addEventListener('click',(e)=>{
    e.preventDefault();
    const queryString=encodeURIComponent(question.value);
    window.location.href=`/results?query=${queryString}`;
});