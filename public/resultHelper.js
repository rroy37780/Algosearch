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


searchForm.addEventListener('submit',async(e)=>{
    e.preventDefault();
    console.log("Keyword Searched: ",question_results.value);
    loader.style.display='flex';
    results.style.display='none';
    const queryString=encodeURIComponent(question_results.value);
    
    const response = await fetch(`/search?query=${queryString}`, {
        method: 'GET',
    });

    console.log('Response Status:', response.status);
    if (!response.ok) {
        throw new Error('Failed to fetch results.');
    }

    const data = await response.json(); // Assuming the backend sends JSON data
    console.log("Fetched Data:", data);
    
    // Assuming 'data' is an array of result objects
    for (let i = 0; i < 5; i++) {
        const result = data[i];
        // Dynamically update the search result heading and body
        document.querySelector(`#result_${i + 1}`).innerHTML=`<a href=${result.link} target='_blank'>${result.title}</a>`
        // document.querySelector(`#result_${i + 1}`).innerText = ;
        const idx=result.body.indexOf("Example 1:");
        document.querySelector(`#content_${i + 1}`).innerText = result.body ? result.body.slice(0, idx).slice(0,200)+"..." : 'No content available'; // Slice body to 100 characters
    }

    // Hide loader and display results
    setTimeout(() => {
        results.style.display = 'block';
        loader.style.display = 'none';
    }, 500);


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

// infinite_scrolling();
window.addEventListener('scroll',()=>{
    if(window.scrollY+window.innerHeight >= document.documentElement.scrollHeight)
    {
        infinite_scrolling();
    }
})

const params=new URLSearchParams(window.location.search);
const searchQuery= params.get('query');

if(searchQuery){
    const searchBox=document.querySelector('#question_results');
    searchBox.value=decodeURIComponent(searchQuery);
    const searchButton=document.querySelector('#btn_results');
    searchButton.click();
    window.history.pushState(null, null, `/results`);
}
