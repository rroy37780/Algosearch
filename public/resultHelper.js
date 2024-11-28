const content=document.querySelectorAll('.src');
const modalDialog=document.querySelector('#modal-dialog');
const modalOverlay=document.querySelector('#modal-overlay');
content.forEach(function (item){
    item.addEventListener('click',function(e){
        console.log(e.target);
        modalDialog.style.display='flex';
        modalOverlay.style.display='none';
    })
})

const closeBtn=document.querySelector('#close-modal-btn');
closeBtn.addEventListener('click',()=>{
    modalDialog.style.display='none';
    modalOverlay.style.display='block'
});

const searchForm=document.querySelector('#form');
const results=document.querySelector('#search_results');

const loader=document.querySelector('#loading');

searchForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    console.log("Keyword Searched: ",question_results.value);
    loader.style.display='flex';
    setTimeout(()=>{
        results.style.display='block';
        loader.style.display='none';
    },5000);
});

const searchdiv=document.querySelector('#search_results');

infinite_scrolling =()=>{
    const cnt=20;
    for (let i=0;i<cnt;i++)
    {
        const test_line=document.createElement('p');
        test_line.innerText='This is a test line for infinite scrolling';
        searchdiv.appendChild(test_line);
    }
};

infinite_scrolling();
window.addEventListener('scroll',()=>{
    if(window.scrollY+window.innerHeight >= document.documentElement.scrollHeight)
    {
        infinite_scrolling();
    }
})
