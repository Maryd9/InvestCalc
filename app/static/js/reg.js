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

    if (result.ok) {
        console.log(result);
        alert("Регистрация прошла успешно");
        const data = {id: id, token: emailVal, password: passwordVal};

    } else {
        console.log(result);

        alert("Неверный email или пароль");
    }
};