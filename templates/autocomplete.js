const search = document.getElementById('search');
const search_results = document.getElementById('results');

const searchAnime = async searchName => {
    const url = `/search/?name=${searchName}` 

    if(searchName.length < 3) {
        result = []
        search_results.innerHTML = ''
        search_results.style.display = 'none'
    } else {
        result = new Promise(resolve => {
            fetch(url)
            .then(response => response.json())
            .then(data => {
                resolve(data.data)
            })
        })
    }
    
    matches = await result;

    // console.log(matches)

    outputHtml(matches);
}

const outputHtml = matches => {
    if(matches.length > 0) {
        search_results.style.display = ''
        const html = matches.map(match => `
        <div class='autocomplete_result' onclick="window.location='/animes/${match.MAL_ID}';">
            <img src=${match.picture} width="65px" 
            height="90px" alt='anime picture'>
            <h6 style="font-size: 18px">${match.name}</h6>
            <p style="font-size: 15px">(${match.releaseyear})</p>
        </div>
        `).join('')

        search_results.innerHTML = html
    } else {
        search_results.innerHTML = ''
        search_results.style.display = 'none'
    }

 }


search.addEventListener('input', () => searchAnime(search.value));