formAuthUser.onsubmit = async (url) => {

    let response = await fetch('/signin', {
        method: 'POST',
        headers: {},
        body: new FormData(formAuthUser)
    });


};