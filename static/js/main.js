
//GET SEARCH FORM AND PAGE LINKS
let search_form = document.getElementById('search_form')
let page_links = document.getElementsByClassName('page-link')

//ENSURE SEARCH FORM EXISTS
if (search_form) {
    for (let i = 0; page_links.length > i; i++) {
        page_links[i].addEventListener('click', function (e) {
            e.preventDefault()

            //GET THE DATA ATTRIBUTE
            let page = this.dataset.page

            //ADD HIDDEN SEARCH INPUT TO FORM
            search_form.innerHTML += `<input value=${page} name="page" hidden/>`


            //SUBMIT FORM
            search_form.submit()
        })
    }
}



let tags = document.getElementsByClassName('post-tag')

for (let i = 0; tags.length > i; i++) {
    tags[i].addEventListener('click', (e) => {
        let tag_id = e.target.dataset.tag
        let post_id = e.target.dataset.post

        // console.log('TAG ID:', tagId)
        // console.log('PROJECT ID:', projectId)

        fetch('https://devbloq.herokuapp.com/api/remove-tag/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'post': post_id, 'tag': tag_id })
        })
            .then(response => response.json())
            .then(data => {
                e.target.remove()
            })

    })
}
