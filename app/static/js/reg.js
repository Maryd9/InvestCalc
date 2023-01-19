formSignUpUser.onsubmit = async (e) => {

    e.preventDefault();

    var usernameVal = document.getElementById('usernameReg').value;
    var emailVal = document.getElementById('emailReg').value;
    var passwordVal = document.getElementById('passwordReg').value;

    const data = {username: usernameVal, email: emailVal, password: passwordVal};

    let response = await fetch('/signup', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    let result = await response.json();

    if (result.message === "OK") {
        alert("Регистрация прошла успешно");

        fetch('/home/user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'userid': result.user_id
            })
        });


    } else {
        console.log(result);
        alert("Пользователь с таким еmail уже зарегистрирован");
    }
};