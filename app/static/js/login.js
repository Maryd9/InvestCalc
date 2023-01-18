formAuthUser.onsubmit = async (url) => {
    url.preventDefault();

    let response = await fetch('/signin', {
        method: 'POST',
        headers: {},
        body: new FormData(formAuthUser)
    });
    let result = await response.json();
    alert(result.message);
};